from __future__ import annotations

from pathlib import Path

import pytest

from streamstats.errors import InvalidEventError
from streamstats.parsers import parser_json


def test_json_parser(tmp_path: Path) -> None:
    file = tmp_path / 'data.json'
    file.write_text(
        '{"timestamp": "2008-08-18T00:00:00", "level": "WARNING", "source": "auth", "message": "Сбой"}\n',
        encoding='utf-8',
    )
    events = list(parser_json(str(file), skip_invalid = False))
    assert len(events) == 1
    assert events[0] is not None
    assert events[0].level == 'WARNING'
    assert events[0].source == 'auth'

def test_json_parser_error(tmp_path: Path) -> None:
    file = tmp_path / 'data.json'
    good_line = '{"timestamp": "2008-08-18T00:00:00", "level": "INFO", "source": "s", "message": "mem"}\n'
    bad_line = '{"timestamp": "2008-08-18T00:00:00", убийца}\n'
    file.write_text((good_line * 3) + bad_line, encoding='utf-8')
    with pytest.raises(InvalidEventError) as error:
        list(parser_json(str(file), skip_invalid = False))
    assert '7' in str(error.value)

