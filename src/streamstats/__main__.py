from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Iterable

from streamstats.analysis import analysis
from streamstats.errors import StreamsStatsErrors
from streamstats.models import Log
from streamstats.parsers import parser_csv, parser_json
from streamstats.report import json_report


def logging_fix() -> None:
    """Настраивает базовое логирование уровня WARNING"""
    logging.basicConfig(level = logging.WARNING, format = '%(levelname)s: %(message)s')
def crt_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(prog = 'streamstats', description = 'Потоковый анализатор лог-файлов CSV и JSONL')
    parsers = parser.add_subparsers(dest="command", required=True)
    analyze = parsers.add_parser('analyze', help = 'Анализ логов')
    analyze.add_argument('input', nargs = '+', metavar = 'INPUT', help = 'Пути файлов логов')
    analyze.add_argument('--format', choices = ['csv','jsonl'], required = True, help = 'Формат входа данных')
    analyze.add_argument('--output', required = True, help = 'Путь сохранения итогового JSON файла')
    analyze.add_argument('--skip-invalid', action = 'store_true', help='Пропускать некорректные строки вместо аварийной остановки')
    return parser

def stream(file: list[str], format: str, skip_invalid: bool) -> Iterable[Log | None]:
    """Объединяет чтение нескольких файлов в единый поток событий"""
    for files in file:
        if format == 'csv':
            yield from parser_csv(files,skip_invalid)
        elif format == 'jsonl':
            yield from parser_json(files,skip_invalid)
        else:
            raise StreamsStatsErrors(f'Неподдерживаемый файл: {format}')
def main(argv: list[str] | None = None) -> int:
    """Запускает CLI и возвращает код завершения"""
    logging_fix()
    parser = crt_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if args.command == 'analyze':
        try:
            stream_event = stream(file = args.input, format = args.format, skip_invalid = args.skip_invalid)
            stats = analysis(stream_event)
            json_report(stats, args.output)
            return 0
        except StreamsStatsErrors as error:
            sys.stderr.write(f'Ошибка: {error}\n')
            return 2
        except OSError:
            sys.stderr.write('Ошибочный файл\n')
            return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())



    