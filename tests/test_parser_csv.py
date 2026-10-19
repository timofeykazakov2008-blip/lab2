from __future__ import annotations

from pathlib import Path

import pytest

from streamstats.errors import InvalidTimeErrors
from streamstats.parsers import parser_csv


def test_csv_parser_success(tmp_path: Path) -> None:
    file = tmp_path / 'data.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        '2008-08-18T10:00:00,INFO,auth,Родился\n',
        encoding='utf-8',
    )
    events = list(parser_csv(str(file), skip_invalid = False))
    assert len(events) == 1
    assert events[0] is not None
    assert events[0].level == 'INFO'
    assert events[0].message == 'Родился'

def test_broken_timestamp(tmp_path: Path) -> None:
    file = tmp_path / 'broken.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        'скип,INFO,auth,текст\n',
        encoding='utf-8',
    )
    with pytest.raises(InvalidTimeErrors) as error:
        list(parser_csv(str(file), skip_invalid = False))
    res = str(error.value)
    assert 'timestamp' in res
    assert '2' in res

def test_skip_invalid(tmp_path: Path) -> None:
    file = tmp_path / 'broken.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        'скип,INFO,auth,текст\n'
        '2008-08-18T10:00:00,INFO,auth,Родился\n',
        encoding='utf-8',
    )
    res = list(parser_csv(str(file), skip_invalid = True))
    assert len(res) == 2
    assert res[0] is None
    assert res[1] is not None
    assert res[1].message == 'Родился'

