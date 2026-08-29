#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the agent to trigger (read the
skill) for a set of queries. Outputs results as JSON.

The default behavior assumes the Claude Code agent: it creates a fake command
file in `.claude/commands/`, runs `claude -p` with the query, and watches
`stream-json` events for the agent invoking the `Skill` or `Read` tool on
that command file.

For other agents, override the env vars below. If your agent uses a
different trigger-detection protocol (e.g., a different output format or
tool names), you will need to subclass or fork this script.

Environment variables:
  EVAL_AGENT_CLI    — non-interactive agent command (default: `claude`).
  EVAL_PROJECT_DIR  — subdirectory under the project root where skill
                      commands live (default: `.claude`). Used for both
                      command-file placement and project-root discovery.
  EVAL_EXTRA_FLAGS  — flags passed after the agent CLI and before the
                      query (default: `-p --output-format stream-json
                      --verbose --include-partial-messages`). Strip flags
                      that your agent does not support.
  EVAL_NESTING_GUARD_VAR — env var name removed before spawning the
                      subprocess so the agent allows nested calls
                      (default: `CLAUDECODE`).
  EVAL_TRIGGER_TOOL — name of the agent's skill-invocation tool
                      (default: `Skill`).
  EVAL_TRIGGER_READ — name of the agent's file-read tool
                      (default: `Read`).
"""

import argparse
import json
import os
import select
import shlex
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# Make sibling scripts importable regardless of how this script is invoked
# (uv run, python -m, etc.).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import parse_skill_md  # noqa: E402

# Default configuration. Override via env vars (see module docstring).
DEFAULT_AGENT_CLI = "claude"
DEFAULT_PROJECT_DIR = ".claude"
DEFAULT_EXTRA_FLAGS = "-p --output-format stream-json --verbose --include-partial-messages"
DEFAULT_NESTING_GUARD = "CLAUDECODE"
DEFAULT_TRIGGER_TOOL = "Skill"
DEFAULT_TRIGGER_READ = "Read"


def _get_config() -> dict:
    """Resolve runtime config from env vars, falling back to defaults."""
    return {
        "agent_cli": os.environ.get("EVAL_AGENT_CLI", DEFAULT_AGENT_CLI),
        "project_dir": os.environ.get("EVAL_PROJECT_DIR", DEFAULT_PROJECT_DIR),
        "extra_flags": shlex.split(os.environ.get("EVAL_EXTRA_FLAGS", DEFAULT_EXTRA_FLAGS)),
        "nesting_guard": os.environ.get("EVAL_NESTING_GUARD_VAR", DEFAULT_NESTING_GUARD),
        "trigger_tool": os.environ.get("EVAL_TRIGGER_TOOL", DEFAULT_TRIGGER_TOOL),
        "trigger_read": os.environ.get("EVAL_TRIGGER_READ", DEFAULT_TRIGGER_READ),
    }


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for the agent's
    config directory (default: `.claude/`). Override `EVAL_PROJECT_DIR` to
    match your agent's directory name.
    """
    project_dir = _get_config()["project_dir"]
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / project_dir).is_dir():
            return parent
    return current


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Creates a command file in the agent's commands dir so it appears in the
    agent's available_skills list, then runs the agent CLI with the raw
    query. Watches stream-json events for the agent invoking its
    skill-invocation or read tool on that command file.
    """
    cfg = _get_config()
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    project_commands_dir = Path(project_root) / cfg["project_dir"] / "commands"
    command_file = project_commands_dir / f"{clean_name}.md"

    try:
        project_commands_dir.mkdir(parents=True, exist_ok=True)
        # Use YAML block scalar to avoid breaking on quotes in description
        indented_desc = "\n  ".join(skill_description.split("\n"))
        command_content = (
            f"---\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n"
        )
        command_file.write_text(command_content, encoding="utf-8")

        # Build the command: <agent_cli> <extra_flags...> [<query>] [model]
        cmd = [cfg["agent_cli"], *cfg["extra_flags"]]
        if "-p" in cmd:
            p_idx = cmd.index("-p")
            cmd.insert(p_idx + 1, query)
        else:
            cmd.extend(["-p", query])
        if model:
            cmd.extend(["--model", model])

        # Strip nesting-guard env vars so the subprocess doesn't refuse to run
        # when we're already inside an agent session.
        env = {k: v for k, v in os.environ.items() if k != cfg["nesting_guard"]}

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=env,
        )

        triggered = False
        start_time = time.time()
        buffer = ""
        # Track state for stream event detection
        pending_tool_name = None
        accumulated_json = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Early detection via stream events
                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in (cfg["trigger_tool"], cfg["trigger_read"]):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""
                                else:
                                    return False

                        elif se_type == "content_block_delta" and pending_tool_name:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                if clean_name in accumulated_json:
                                    return True

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                return clean_name in accumulated_json
                            if se_type == "message_stop":
                                return False

                    # Fallback: full assistant message
                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            tool_name = content_item.get("name", "")
                            tool_input = content_item.get("input", {})
                            if tool_name == cfg["trigger_tool"] and clean_name in tool_input.get("skill", ""):
                                triggered = True
                            elif tool_name == cfg["trigger_read"] and clean_name in tool_input.get("file_path", ""):
                                triggered = True
                            return triggered

                    elif event.get("type") == "result":
                        return triggered
        finally:
            # Clean up process on any exit path (return, exception, timeout)
            if process.poll() is None:
                process.kill()
                process.wait()

        return triggered
    finally:
        if command_file.exists():
            command_file.unlink()


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to pass to the agent CLI (default: agent's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
