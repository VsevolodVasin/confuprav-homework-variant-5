"""Синтаксический анализ учебного языка по грамматике Lark."""

from pathlib import Path

from lark import Lark, UnexpectedInput

GRAMMAR = Path(__file__).with_name("config.lark")
PARSER = Lark.open(str(GRAMMAR), parser="lalr", propagate_positions=True)


def parse(source):
    """Построить дерево или сообщить позицию синтаксической ошибки."""
    try:
        return PARSER.parse(source)
    except UnexpectedInput as error:
        position = f"строка {error.line}, столбец {error.column}"
        raise ValueError(f"{position}: синтаксическая ошибка") from error
