# Fixture: intentionally non-compliant. Do not "fix" this file.
# It exists so `--check-forbidden` has known matches to find; see
# forbidden-scan-expected.md. The sibling .ruff.toml keeps formatters out.

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from project.models import Model


def parse_value(raw: Optional[str]) -> str | None:
    if TYPE_CHECKING:
        _ = Model
    return raw.strip() if raw else None
