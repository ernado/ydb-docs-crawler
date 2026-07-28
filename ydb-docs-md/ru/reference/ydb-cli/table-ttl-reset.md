---
title: "Сброс параметров TTL"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/table-ttl-reset?version=v26.1"
doc_path: "ru/reference/ydb-cli/table-ttl-reset"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/table-ttl-reset.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/table-ttl-reset.md"
description: "С помощью подкоманды table ttl reset вы можете выключить TTL для указанной таблицы. Общий вид команды: ydb [global options...] table ttl reset <table path>."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Сброс параметров TTL

С помощью подкоманды `table ttl reset` вы можете выключить [TTL](../../concepts/ttl.md) для указанной таблицы.

Общий вид команды:

```bash
ydb [global options...] table ttl reset <table path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `table path` — путь таблицы.

Посмотрите описание команды выключения TTL:

```bash
ydb table ttl reset --help
```

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Выключите TTL для таблицы `series`:

```bash
ydb -p quickstart table ttl reset \
  series
```
