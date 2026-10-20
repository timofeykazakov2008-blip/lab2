from __future__ import annotations

import json
from pathlib import Path

from streamstats.__main__ import main


def test_cli(tmp_path: Path) -> None:
    """Проверяет успешный запуск CLI и создание отчет"""
    file = tmp_path / 'go.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        '2008-08-18T00:00:00,INFO,auth,текст\n',
        encoding='utf-8'
    )
    report = tmp_path / "report.json"
    exit_code = main(['analyze',str(file),'--format','csv','--output',str(report)])
    assert exit_code == 0
    assert report.exists()
    data = json.loads(report.read_text(encoding='utf-8'))
    assert data['total_event'] == 1

def test_cli_broke(tmp_path: Path) -> None:
    """Проверяет возврат кода 2 при ошибке без --skip-invalid"""
    file = tmp_path / 'go.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        'скип,INFO,auth,текст\n',
        encoding='utf-8'
    )
    report = tmp_path / "report.json"
    exit_code = main(['analyze',str(file),'--format','csv','--output',str(report)])
    assert exit_code == 2

def test_cli_skip_invalid(tmp_path: Path) -> None:
    """Проверяет успешный запуск CLI с флагом --skip-invalid"""
    file = tmp_path / 'go.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        'скип,INFO,auth,текст\n'
        '2008-08-18T00:00:00,INFO,auth,текст\n',
        encoding='utf-8'
    )
    report = tmp_path / "report.json"
    exit_code = main(['analyze',str(file),'--format','csv','--output',str(report),'--skip-invalid'])
    assert exit_code == 0
    assert report.exists()
    data = json.loads(report.read_text(encoding='utf-8'))
    assert data['total_event'] == 1
    assert data['SKIPPED_ROWS'] == 1