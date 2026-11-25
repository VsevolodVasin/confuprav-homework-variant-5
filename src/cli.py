"""Прочитать конфигурацию из stdin и вывести XML в stdout."""

import sys

from .translator import translate


def main():
    """Направить диагностику в stderr и вернуть статус трансляции."""
    try:
        print(translate(sys.stdin.read()))
    except (ValueError, RecursionError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
