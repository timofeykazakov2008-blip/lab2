from __init__.py import annotations

class StreamsStatsErrors(Exception):
    """Базовые ошибки streamstats"""

class FileError(StreamsStatsErrors):
    """Неподдерживаемый файл"""
