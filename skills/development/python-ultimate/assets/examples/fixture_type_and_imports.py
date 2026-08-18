from __future__ import annotations


def parse_value(raw: str | None) -> str | None:
    return raw.strip() if raw else None
