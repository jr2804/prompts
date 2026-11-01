from __future__ import annotations

from collections.abc import Iterable


def parse_values(values: Iterable[str]) -> None:
    pass


def parse_value(raw: str | None) -> str | None:
    return raw.strip() if raw else None
