from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from project.models import Model


def parse_value(raw: Optional[str]) -> str | None:
    return raw.strip() if raw else None
