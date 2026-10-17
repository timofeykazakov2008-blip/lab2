from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Log:
    timestamp: datetime
    level: str
    source: str
    message: str

@dataclass(frozen=True)
class Stat:
    total: int
    skip: int
    timestamp_st: datetime | None
    timestamp_end: datetime | None
    cnt_level: dict[str,int]
    cnt_source: dict[str, int]
    top_error: list[tuple[str, int]]