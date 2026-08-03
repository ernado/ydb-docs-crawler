---
title: "Удаление таблицы"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/table-drop?version=v26.1"
doc_path: "ru/reference/ydb-cli/table-drop"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/table-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/table-drop.md"
description: "С помощью подкоманды table drop вы можете удалить указанную таблицу. Общий вид команды: ydb [global options...] table drop [options...] <table path>."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Удаление таблицы

С помощью подкоманды `table drop` вы можете удалить указанную таблицу.

Общий вид команды:

```bash
ydb [global options...] table drop [options...] <table path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](table-drop.md#options).
- `table path` — путь таблицы.

Посмотрите описание команды удаления таблицы:

```bash
ydb table drop --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--timeout` | Время, в течение которого должна быть выполнена операция на сервере. |

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Удалите таблицу `series`:

```bash
ydb -p quickstart table drop series
```
