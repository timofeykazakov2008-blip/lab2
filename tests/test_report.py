from __future__ import annotations

import json
from pathlib import Path

from streamstats.analysis import analysis
from streamstats.report import json_report


def test_json_report(tmp_path: Path) -> None:
    stats = analysis([])
    output = tmp_path / 'report.json'
    json_report(stats, str(output))
    assert output.exists()
    data = json.loads(output.read_text(encoding='utf-8'))
    assert ("total_event" in data)