from __future__ import annotations

from datetime import datetime

from streamstats.analysis import analysis
from streamstats.models import Log


def test_empty() -> None:
    stats = analysis([])
    assert stats.total == 0
    assert stats.skip == 0
    assert stats.timestamp_st is None
    assert stats.timestamp_end is None
    assert stats.cnt_level == {}

def test_analysis() -> None:
    t1 = datetime(2008, 8, 18, 10, 0, 11)
    t2 = datetime(2025, 10, 15, 12, 0, 0)
    events = [
        Log(t1, 'INFO', 'auth', 'login'),
        None,
        Log(t2, 'ERROR', 'db', 'fail'),
    ]
    stats = analysis(events)
    assert stats.total == 2
    assert stats.skip == 1
    assert stats.timestamp_st == t1
    assert stats.timestamp_end == t2
    assert stats.cnt_level == {'INFO': 1, 'ERROR': 1}

def test_top_error_1() -> None:
    t = datetime(2016, 9, 15, 0, 11, 0)
    events = [
        Log(t, 'ERROR', 'z', 'err'),
        Log(t, 'ERROR', 'a', 'err'),
        Log(t, 'ERROR', 'b', 'err'),
    ]
    stats = analysis(events)
    assert stats.top_error == [('a', 1), ('b', 1), ('z', 1)]

def test_top_error_2() -> None:
    t = datetime(2016, 9, 15, 0, 11, 0)
    events = [
        Log(t, 'ERROR', 'z', 'err'),
        Log(t, 'ERROR', 'z', 'err'),
        Log(t, 'ERROR', 'a', 'err'),
        Log(t, 'ERROR', 'b', 'err'),
        Log(t, 'ERROR', 'k', 'err'),
    ]
    stats = analysis(events)
    assert stats.top_error == [('z', 2), ('a', 1), ('b', 1), ('k', 1)]
