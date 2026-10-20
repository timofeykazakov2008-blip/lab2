from __future__ import annotations

import csv
import json
import logging
from collections.abc import Iterator
from datetime import datetime

from streamstats.constants import VAL_LEVELS
from streamstats.errors import InvalidEventError, InvalidTimeErrors
from streamstats.models import Log

logger = logging.getLogger(__name__)

def check_time(time:str, file:str, line:int) -> datetime:
    """Проверяет корректную запись времени/datetime"""
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
    """Валидирует поля одной строки CSV и конструирует объект Log"""
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

def validate_json(data: dict[str, object], file:str,line:int) -> Log:
    """Валидирует словарь, полученный из JSONL-строки и конструирует объект Log"""
    keys = {'timestamp', 'level', 'source', 'message'}
    if not keys.issubset(data.keys()):
        skip = keys - set(data.keys())
        raise InvalidEventError(
            f"В JSON отсустствую все нужные условия: '{skip}'",
            file,
            line
        )
    json_timestamp = data["timestamp"]
    json_level = data["level"]
    json_source = data["source"]
    json_message = data["message"]
    if not isinstance(json_timestamp, str):
        raise InvalidTimeErrors(
            "Неправильный timestamp",
            file,
            line
        )
    if not isinstance(json_level, str) or not isinstance(json_source, str) or not isinstance(json_message, str):
            raise InvalidEventError(
                "level source message должны быть типа str",
                file,
                line
            )
    timestamp = check_time(json_timestamp, file, line)
    level = json_level.strip().upper()
    if level not in VAL_LEVELS:
            raise InvalidEventError(
                f"Недопустивмый уровень VAL_LEVELS: '{level}'",
                file,
                line,
            )
    source = json_source.strip()
    if not source:
            raise InvalidEventError(
                        "Поле не 'source' не может пустовать",
                        file,
                        line,
                    )
    message = json_message.strip()
    return Log(
        timestamp = timestamp,
        level = level,
        source = source,
        message = message
    )
def parser_csv(file: str, skip_invalid: bool = False) -> Iterator[Log | None]:
    """Построчно читает CSV-файл и генерирует объекты Log"""
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

def parser_json(file: str, skip_invalid: bool = False) -> Iterator[Log | None]:
    """Построчно читает JSONL-файл и генерирует объекты Log"""
    with open(file, mode="r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start = 1):
            clean_line = line.strip()
            if not clean_line:
                continue
            try:
                try:
                    data = json.loads(clean_line)
                except json.JSONDecodeError as error:
                    raise InvalidEventError(
                        "Неправильная запись JSON",
                        file,
                        line_number
                    ) from error
                if not isinstance(data, dict):
                    raise InvalidEventError(
                        "JSON должен быть объяектом типа (dict)",
                        file,
                        line_number
                    )
                yield validate_json(data, file, line_number)
            except (InvalidEventError, InvalidTimeErrors) as error:
                if skip_invalid:
                    logger.warning("Пропущена некорректная строка: %s", error)
                    yield None
                else:
                    raise


                