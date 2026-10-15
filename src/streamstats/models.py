from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

VAL_LEVELS: tuple[str] = tuple({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
ERROR_LEVELS: tuple[str] = tuple[{"ERROR", "CRITICAL"}]

@dataclass(frozen=True, slots=True)
class Log:
    timestamp: datetime
    level: str
    source: str
    message: str
