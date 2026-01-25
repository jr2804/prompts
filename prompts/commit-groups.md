---
name: "commit-groups"
description: "Organize related changes into logical commit groups for version control"
---

# commitGroups

There are now multiple uncommitted changes in the repository, which address several topics (linter issues, formatting, refactoring, breaking changes, etc.), partly separated, partly combined. Anaylze the diffs of all files and group changes into logical changesets (at least 1, up to 5), each following the commit message style of the current project. Do not include any other information. Then commit each changeset with the determined message.
