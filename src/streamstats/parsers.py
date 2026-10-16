from __future__ import annotations

import csv
import logging
from collections.abc import Iterator
from datetime import datetime

from streamstats.errors import InvalidEventError, InvalidTimeErrors
from streamstats.models import VAL_LEVELS, Log

logger = logging.getLogger(__name__)

def check_time(time:str, file:str, line:int) -> datetime:
    clean_time = time.strip()
    if not clean_time:
        raise InvalidTimeErrors(
            "Поле времени 'timestamp' не может быть пустым",
            file,
            line,
        )
    try:
        return datetime.fromisoformat(clean_time)
    except ValueError as error:
        raise InvalidTimeErrors(
            f"Неверный формат даты в поле 'timestamp': '{time}'",
            file,
            line,
        ) from error

def validate(row:list[str], file:str, line:int) -> Log:
    if len(row) != 4:
        raise InvalidEventError(
            f"Не 4 поля, получено {len(row)}",
            file,
            line,
        )
    timestamp = check_time(row[0], file, line)
    level = row[1].upper().strip()
    if level not in VAL_LEVELS:
        raise InvalidEventError(
            f"Недопустивмый уровень VAL_LEVELS: '{level}'",
            file,
            line,
        )
    source = row[2].strip()
    if not source:
        raise InvalidEventError(
                    "Поле не 'source' не может пустовать",
                    file,
                    line,
                )
    message = row[3].strip()
    return Log(
    timestamp=timestamp,
    level=level,
    source=source,
    message=message,
    )
def parcer_csv(file: str, skip_invalid: bool = False) -> Iterator[Log | None]:
    with open(file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            head = next(reader)
        except StopIteration:
            return
        clear_head = ["timestamp", "level", "source", "message"]
        if [s.strip().lower() for s in head] != clear_head and not skip_invalid:
            raise InvalidEventError(
                "Некорректный заголовок CSV", 
                file, 
                line=1,
            )
        for line_number, row in enumerate(reader, start = 2):
            if not row or all(not s.strip() for s in row):
                continue
            try:
                yield validate(row, file, line_number)
            except (InvalidEventError, InvalidTimeErrors) as error:
                if skip_invalid:
                    logger.warning("Пропущена некорректная строка: %s", error)
                    yield None
                else:
                    raise
