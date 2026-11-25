# Домашняя работа · Вариант 5

Транслятор учебного конфигурационного языка в XML. Синтаксический
анализатор Lark строит дерево по грамматике `src/config.lark`.

## Установка и проверка

Требуется Python 3.10 или новее. Из корня репозитория:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make build
make test
```

Переменная `PYTHON` в Makefile задаёт интерпретатор (по умолчанию python3).
