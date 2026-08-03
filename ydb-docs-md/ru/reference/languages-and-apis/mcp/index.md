---
title: "YDB Model Context Protocol Server"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/mcp/?version=v26.1"
doc_path: "ru/reference/languages-and-apis/mcp/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/mcp/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/mcp/index.md"
description: "YDB Model Context Protocol (MCP) server позволяет работать с базами данных YDB из любой большой языковой модели (LLM), которая поддерживает MCP, используя любой"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# YDB Model Context Protocol Server

[YDB Model Context Protocol (MCP) server](https://github.com/ydb-platform/ydb-mcp) позволяет работать с базами данных YDB из любой [большой языковой модели (LLM)](https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%D1%8F_%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F_%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C), которая поддерживает [MCP](https://modelcontextprotocol.io/introduction), используя любой из [MCP клиентов](https://modelcontextprotocol.io/clients). Эта интеграция обеспечивает работу с базами данных YDB с помощью ИИ на естественном языке.

## Начало работы {#nachalo-raboty}

### Предварительные требования {#predvaritelnye-trebovaniya}

1. Установите [MCP-клиент](https://modelcontextprotocol.io/clients), поддерживающий MCP tools (большинство поддерживают). Примеры конфигурации ниже используют распространённый формат, поддерживаемый несколькими популярными MCP-клиентами (Claude Desktop, Cursor и др.), но вам может потребоваться адаптировать формат под требования вашего клиента.
2. MCP-сервер YDB — это приложение на Python, которое обычно размещается вместе с MCP-клиентом. Существует несколько вариантов установки и запуска MCP-сервера YDB, которые [описаны ниже](index.md#server-arguments), но все они требуют предварительно установленного окружения Python 3.10+.

### Настройка MCP-клиента {#nastrojka-mcp-klienta}

#### Анонимная аутентификация {#anonimnaya-autentifikaciya}

{% list tabs %}

- uvx

  [uvx](https://docs.astral.sh/uv/guides/tools/) позволяет запускать приложения Python без явной установки.

  Настройте YDB MCP в настройках вашего MCP-клиента:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "uvx",
        "args": [
          "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local"
        ]
      }
    }
  }
  ```

- pipx

  [pipx](https://pipx.pypa.io/stable/installation/) позволяет запускать приложения из PyPI без явной установки (сам pipx должен быть установлен заранее).

  Настройте YDB MCP в настройках вашего MCP-клиента:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "pipx",
        "args": [
          "run", "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local"
        ]
      }
    }
  }
  ```

- pip

  При необходимости создайте и активируйте [виртуальное окружение Python](https://docs.python.org/3/library/venv.html). Установите YDB MCP с помощью [pip](https://pypi.org/project/pip/):

  ```bash
  pip install ydb-mcp
  ```

  В настройках вашего MCP-клиента укажите параметры для соединения с YDB MCP:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "python3",
        "args": [
          "-m", "ydb_mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local"
        ]
      }
    }
  }
  ```

{% endlist %}

#### Аутентификация по логину и паролю {#autentifikaciya-po-loginu-i-parolyu}

{% list tabs %}

- uvx

  Настройте аутентификацию по логину/паролю с `uvx`:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "uvx",
        "args": [
          "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local",
          "--ydb-auth-mode", "login-password",
          "--ydb-login", "<ваше-имя-пользователя>",
          "--ydb-password", "<ваш-пароль>"
        ]
      }
    }
  }
  ```

- pipx

  Настройте аутентификацию по логину/паролю с `pipx`:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "pipx",
        "args": [
          "run", "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local",
          "--ydb-auth-mode", "login-password",
          "--ydb-login", "<ваше-имя-пользователя>",
          "--ydb-password", "<ваш-пароль>"
        ]
      }
    }
  }
  ```

- pip

  Настройте аутентификацию по логину/паролю с установленным через `pip` YDB MCP:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "python3",
        "args": [
          "-m", "ydb_mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local",
          "--ydb-auth-mode", "login-password",
          "--ydb-login", "<ваше-имя-пользователя>",
          "--ydb-password", "<ваш-пароль>"
        ]
      }
    }
  }
  ```

{% endlist %}

### Выполнение запросов {#vypolnenie-zaprosov}

Задавайте вашему LLM вопросы относительно данных, хранящихся в YDB, используя настроенного выше клиента MCP. Языковая модель увидит инструменты, доступные ей через MCP, и будет использовать их для выполнения запросов на [YQL](../../../yql/reference/index.md) и других вызовов к API YDB. Пример того, как это может выглядеть:

![Пример использования MCP-сервера YDB](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/reference/languages-and-apis/mcp/_assets/example-usage.png)

## Доступные инструменты {#dostupnye-instrumenty}

MCP-сервер YDB предоставляет следующие инструменты для взаимодействия с базами данных YDB:

- `ydb_query`: Выполнение SQL-запроса к базе данных YDB

  - Параметры:

    - `sql`: Строка SQL-запроса для выполнения

- `ydb_query_with_params`: Выполнение параметризованного SQL-запроса с JSON-параметрами

  - Параметры:

    - `sql`: Строка SQL-запроса с параметрами
    - `params`: JSON-строка, содержащая значения параметров

- `ydb_list_directory`: Просмотр содержимого директории в YDB

  - Параметры:

    - `path`: Путь к директории YDB для просмотра

- `ydb_describe_path`: Получение подробной информации о [схемном объекте](../../../concepts/glossary.md#scheme-object) (таблица, директория и т.д.) по указанному пути YDB

  - Параметры:

    - `path`: Путь YDB для описания

- `ydb_status`: Получение текущего статуса подключения к YDB

## Аргументы командной строки и переменные окружения {#server-arguments}

Следующая таблица описывает параметры командной строки и переменные окружения MCP-сервера YDB:

| Аргумент | Переменная окружения | Значение по умолчанию | Описание |
| --- | --- | --- | --- |
| `--ydb-endpoint` | `YDB_ENDPOINT` | — | Строка подключения к YDB, включающая протокол, имя хоста, порт и имя базы данных |
| `--ydb-login` | `YDB_LOGIN` | — | Логин YDB |
| `--ydb-password` | `YDB_PASSWORD` | — | Пароль YDB |
| `--ydb-auth-mode` | `YDB_AUTH_MODE` | `anonymous` | Режим аутентификации YDB. Возможные значения: `anonymous`, `login-password` |
| `--log-level` | — | `INFO` | Уровень логирования. Возможные значения: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

> [!NOTE]
> Аргументы командной строки имеют приоритет над соответствующими переменными окружения.

## Узнать больше {#uznat-bolshe}

Для получения дополнительной информации посетите [репозиторий YDB MCP на GitHub](https://github.com/ydb-platform/ydb-mcp).
