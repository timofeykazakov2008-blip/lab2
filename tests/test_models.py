from __future__ import annotations

from datetime import datetime

from streamstats.models import Log


def test_log_creation_valid() -> None:
    """Проверяет создание объекта Log"""
    ts = datetime(2008, 8, 18, 10, 0, 0)
    event = Log(
        timestamp=ts,
        level='INFO',
        source='auth',
        message='Вход выполнен',
    )
    assert event.timestamp == ts
    assert event.level == 'INFO'
    assert event.source == 'auth'
    assert event.message == 'Вход выполнен'


def test_log_equality() -> None:
    """Проверяет равенство двух одинаковых объектов Log"""
    ts = datetime(2008, 8, 18, 10, 0, 0)
    event1 = Log(ts, 'ERROR', 'db', 'Ошибка')
    event2 = Log(ts, 'ERROR', 'db', 'Ошибка')
    assert event1 == event2

