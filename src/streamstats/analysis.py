from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from streamstats.constants import ERROR_LEVELS
from streamstats.models import Log, Stat


def analysis(event: Iterable[Log | None]) -> Stat:
    total = 0
    skip = 0
    timestamp_st: datetime | None = None
    timestamp_end: datetime | None = None
    cnt_level: dict[str,int] = {}
    cnt_source: dict[str,int] = {}
    top_error: dict[str,int] = {}
    for i in event:
        if i is None:
            skip += 1
            continue
        total +=1
        if timestamp_st is None or i.timestamp< timestamp_st:
            timestamp_st = i.timestamp
        if timestamp_end is None or i.timestamp > timestamp_end:
            timestamp_end = i.timestamp
        cnt_level[i.level] = cnt_level.get(i.level,0) + 1
        cnt_source[i.source] = cnt_source.get(i.source,0) + 1
        if i.level in ERROR_LEVELS:
            top_error[i.source]= top_error.get(i.source,0)+ 1
    sort_errors = sorted(top_error.items(), key = lambda x: (-x[1],x[0]))
    top_5 = sort_errors[:5]
    return Stat(
        total = total,
        skip = skip,
        timestamp_st = timestamp_st,
        timestamp_end = timestamp_end,
        cnt_level = cnt_level,
        cnt_source = cnt_source,
        top_error = top_5
    )