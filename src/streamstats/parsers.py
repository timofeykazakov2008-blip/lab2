from __future__ import annotations

import csv
from collections.abc import Iterator
from datetime import datetime

from streamstats.models import Log


def parcer_csv(file: str) -> Iterator[Log]:
    with open(file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return
        for row in reader:
            if not row or all(not s1.strip() for s1 in row):
                continue
            timestamp = datetime.fromisoformat(row[0].strip())
            level = row[1].strip()
            source = row[2].strip()
            message = row[3].strip()
            yield Log(
                timestamp=timestamp,
                level=level,
                source=source,
                message=message,
            )
