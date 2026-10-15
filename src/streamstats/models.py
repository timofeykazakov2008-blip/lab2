from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

VAL_LEVELS: frozenset[str] = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
ERROR_LEVELS: frozenset[str] = frozenset({"ERROR", "CRITICAL"})

@dataclass(frozen=True)
class Log:
    timestamp: datetime
    level: str
    source: str
    message: str
