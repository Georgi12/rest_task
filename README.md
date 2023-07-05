# PRL Pipeline
REST приложения для Kaspersky

## Локальный запуск проекта

1. Установить [pyenv](https://github.com/pyenv/pyenv#installation). Установить [poetry](https://python-poetry.org/docs/).
   Установить python актуальной
   версии:
    ```bash
    pyenv install 3.9.17
    pyenv local 3.9.17
   ```

2. Установить зависимости
    ```bash
    # для linux
    poetry install
    ```
3. Активировать окружение через
    ```bash
    poetry shell
    ```

4. Настроить интерпретатор в PyCharm. Если окружение активировано, то путь до интерпретатора можно найти через
    ```bash
    which python
    ```
   
5. Для запуска тестов выполнить команду
    ```bash
    pytest
    ```