#!/usr/bin/env python3
"""
Quick Review - Lightweight skill validation script

Validates SKILL.md frontmatter without external dependencies.
Use alongside `uvx skills-ref validate` for comprehensive checking.

Usage:
    python quick_review.py <path/to/skill>
    python quick_review.py ./my-skill
"""

import json
import re
import sys
from pathlib import Path

import yaml


def validate_frontmatter(skill_path: Path) -> dict:
    """Validate SKILL.md frontmatter and return structured report."""
    issues = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {
            "valid": False,
            "issues": [{"severity": "critical", "text": "SKILL.md not found"}]
        }

    content = skill_md.read_text(encoding="utf-8")

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {
            "valid": False,
            "issues": [{"severity": "critical", "text": "No YAML frontmatter found"}]
        }

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return {
            "valid": False,
            "issues": [{"severity": "critical", "text": f"Invalid YAML: {e}"}]
        }

    if not isinstance(frontmatter, dict):
        return {
            "valid": False,
            "issues": [{"severity": "critical", "text": "Frontmatter must be a dictionary"}]
        }

    # Check required fields
    if "name" not in frontmatter:
        issues.append({
            "severity": "critical",
            "file": "SKILL.md",
            "line": 1,
            "text": "Missing required 'name' field in frontmatter",
            "fix": "Add `name: skill-name` to frontmatter (hyphen-case, lowercase)"
        })

    if "description" not in frontmatter:
        issues.append({
            "severity": "critical",
            "file": "SKILL.md",
            "line": 1,
            "text": "Missing required 'description' field in frontmatter",
            "fix": "Add `description: ...` to frontmatter (1-1024 chars)"
        })

    # Validate name format
    name = frontmatter.get("name", "")
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            issues.append({
                "severity": "major",
                "file": "SKILL.md",
                "text": f"Name '{name}' should be hyphen-case (lowercase letters, digits, hyphens only)",
                "fix": "Use lowercase with hyphens: 'my-skill', 'csv-processor'"
            })
        if name.startswith("-") or name.endswith("-") or "--" in name:
            issues.append({
                "severity": "major",
                "file": "SKILL.md",
                "text": f"Name '{name}' cannot start/end with hyphen or have consecutive hyphens",
                "fix": "Remove leading/trailing/consecutive hyphens"
            })
        if len(name) > 64:
            issues.append({
                "severity": "major",
                "file": "SKILL.md",
                "text": f"Name is {len(name)} chars, max is 64",
                "fix": "Shorten the name"
            })

    # Validate description
    description = frontmatter.get("description", "")
    if description:
        if len(description) > 1024:
            issues.append({
                "severity": "major",
                "file": "SKILL.md",
                "text": f"Description is {len(description)} chars, max is 1024",
                "fix": "Shorten the description"
            })
        if "<" in description or ">" in description:
            issues.append({
                "severity": "major",
                "file": "SKILL.md",
                "text": "Description cannot contain angle brackets",
                "fix": "Remove < and > characters"
            })

    # Check for unexpected fields
    allowed = {"name", "description", "license", "metadata", "compatibility", "allowed-tools"}
    unexpected = set(frontmatter.keys()) - allowed
    if unexpected:
        issues.append({
            "severity": "minor",
            "file": "SKILL.md",
            "text": f"Unexpected fields: {', '.join(sorted(unexpected))}",
            "fix": "Remove or document if intentional"
        })

    # Check body length (approximate line count)
    body_start = match.end()
    body = content[body_start:].strip()
    line_count = len(body.split("\n"))

    if line_count > 500:
        issues.append({
            "severity": "major",
            "file": "SKILL.md",
            "text": f"SKILL.md body is {line_count} lines (recommended: <500)",
            "fix": "Move detailed content to references/ directory"
        })

    return {
        "valid": len([i for i in issues if i["severity"] == "critical"]) == 0,
        "skill_path": str(skill_path),
        "issues": issues,
        "summary": {
            "critical": len([i for i in issues if i["severity"] == "critical"]),
            "major": len([i for i in issues if i["severity"] == "major"]),
            "minor": len([i for i in issues if i["severity"] == "minor"])
        }
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_review.py <path/to/skill>")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    if not skill_path.exists():
        print(f"Error: Path not found: {skill_path}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"Error: Not a directory: {skill_path}")
        sys.exit(1)

    result = validate_frontmatter(skill_path)

    # Output as JSON for programmatic consumption
    print(json.dumps(result, indent=2))

    # Also print human-readable summary
    print("\n--- Summary ---")
    print(f"Critical: {result['summary']['critical']}")
    print(f"Major: {result['summary']['major']}")
    print(f"Minor: {result['summary']['minor']}")

    if result["valid"]:
        print("\n✅ Validation passed (no critical issues)")
    else:
        print("\n❌ Validation failed (critical issues found)")
        sys.exit(1)


if __name__ == "__main__":
    main()