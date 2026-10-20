# Лабораторная работа 2: Потоковый анализатор логов

## Описание проекта
Пакет `streamstats` предназначен для эффективного потокового чтения, фильтрации и анализа структурированных лог-файлов больших объёмов в форматах CSV и JSONL.

Анализатор вычисляет сводные метрики по логам без полной загрузки данных в оперативную память, формируя итоговый аналитический JSON-отчёт.

## Структура проекта

```text
lab2/
├── pyproject.toml              # Конфигурация сборщика пакета и инструментов (ruff, mypy, pytest)
├── README.md                   # README проекта
├── src/
│   └── streamstats/
│       ├── __init__.py         # Инициализация пакета
│       ├── __main__.py         # Точка входа
│       ├── constants.py        # Константы
│       ├── errors.py           # Иерархия пользовательских исключений
│       ├── models.py           # Модели данных
│       ├── parsers.py          # Потоковые построчные генераторы парсеров CSV и JSONL
│       ├── analysis.py         # Однопроходный анализ потока событий и расчёт статистики
│       └── report.py           # Сохранение итогового отчёта
└── tests/
    ├── __init__.py
    ├── test_models.py          # Тестирование валидации
    ├── test_csv_parser.py      # Тесты CSV-парсера
    ├── test_json_parser.py     # Тесты JSON-парсера
    ├── test_analysis.py        # Тестирование агрегации метрик
    ├── test_report.py          # Тестирование выгрузки в JSON
    └── test_cli.py             # Интеграционные тесты CLI с использованием tmp_path
```
## Установка и запуск
1. Настройка виртуального окружения
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
pip install pytest pytest-cov ruff mypy

## Использование консольного интерфейса
python -m streamstats --help
python -m streamstats analyze --help

Примеры запуска
Анализ CSV-файла (режим по умолчанию):
python -m streamstats analyze data.csv --format csv --output report.json

Анализ нескольких JSONL-файлов с пропуском битых строк (--skip-invalid):
python -m streamstats analyze log1.jsonl log2.jsonl --format jsonl --output report.json --skip-invalid

## ruff/mypy/pytest
ruff check .
mypy src/
pytest -v
pytest --cov=streamstats --cov-report=term-missing

