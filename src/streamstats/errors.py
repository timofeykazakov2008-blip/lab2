
class StreamsStatsErrors(Exception):
    """Базовые ошибки streamstats"""

class FileError(StreamsStatsErrors):
    """Неподдерживаемый файл"""

class InvalidEventError(StreamsStatsErrors):
    """Возбуждается при некорректной структуре записи лога."""

    def __init__(self, message: str, file: str = '', line: int = 0):
        self.file = file
        self.line = line
        self.message = message
        one_message = message
        if file and line:
            one_message = f'{self.file}:{self.line}: {self.message}'
        StreamsStatsErrors.__init__(self, one_message)

class InvalidTimeErrors(StreamsStatsErrors):
    """Ошибка во времени формата ISO 8601."""