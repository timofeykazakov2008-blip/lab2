from __future__ import annotations

import json
from typing import Any

from streamstats.models import Stat


def to_dict(stat: Stat) -> dict[str,Any]:
    return{
        'TOTAL_EVENT': stat.total,
        'SKIPPED_ROWS': stat.skip,
        'TIMESTAMP_FIRST': stat.timestamp_st,
        'TIMESTAMP_LAST': stat.timestamp_end,
        'LEVEL_CNT': stat.cnt_level,
        'SOURCE_CNT': stat.cnt_source,
        'TOP_ERRORS': [{'source':source, 'count': count} for source,count in stat.top_error]
    }

def json_report(stat: Stat, path:str) ->None:
    data = to_dict(stat)
    with open(path, mode = 'w', encoding = 'untf-8') as f:
        json.dump(data, f, ensure_ascii = False, indent = 2)