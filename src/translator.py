"""Вычисление констант и формирование XML-документа."""

import operator
from decimal import Decimal, DecimalException
from xml.etree import ElementTree as et

from .parser import parse

OPERATIONS = {"+": operator.add, "-": operator.sub, "pow": operator.pow}


def evaluate(node, constants):
    """Вычислить число, массив, ссылку или бинарное выражение."""
    if node.data == "number":
        return Decimal(node.children[0])
    if node.data == "array":
        return [evaluate(item, constants) for item in node.children[1:]]
    if node.data == "reference":
        name = node.children[0]
        if name not in constants:
            raise ValueError(f"неизвестная константа {name}")
        return constants[name]
    symbol, left, right = node.children
    args = [evaluate(item, constants) for item in (left, right)]
    if not all(isinstance(arg, Decimal) for arg in args):
        raise ValueError(f"операция {symbol} требует два числа")
    try:
        result = OPERATIONS[symbol](*args)
        if not result.is_finite():
            raise ValueError("результат вне диапазона")
        return result
    except DecimalException as error:
        raise ValueError(f"недопустимый результат операции {symbol}") from error


def append_value(parent, value):
    """Добавить типизированный XML-элемент, сохраняя вложенность."""
    if isinstance(value, Decimal):
        et.SubElement(parent, "number").text = str(value)
    else:
        array = et.SubElement(parent, "list")
        for item in value:
            append_value(array, item)


def translate(source):
    """Преобразовать программу в XML, разрешая имена по порядку."""
    root = et.Element("config")
    constants = {}
    for node in parse(source).children:
        if node.data == "declaration":
            _, name, body = node.children
            if name in constants:
                raise ValueError(f"повторное объявление {name}")
            constants[name] = evaluate(body, constants)
            element = et.SubElement(root, "var", name=str(name))
            append_value(element, constants[name])
        else:
            append_value(root, evaluate(node, constants))
    et.indent(root)
    return et.tostring(root, encoding="unicode")
