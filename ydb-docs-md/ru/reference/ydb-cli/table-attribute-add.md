---
title: "table attribute add"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/table-attribute-add?version=v26.1"
doc_path: "ru/reference/ydb-cli/table-attribute-add"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/table-attribute-add.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/table-attribute-add.md"
description: "С помощью команды table attribute add вы можете добавить пользовательский атрибут указанной таблице. Общий вид команды:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# table attribute add

С помощью команды `table attribute add` вы можете добавить [пользовательский атрибут](../../concepts/datamodel/table.md#users-attr) указанной таблице.

Общий вид команды:

```bash
ydb [global options...] table attribute add [options...] <table path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](table-attribute-add.md#options).
- `table path` — путь таблицы.

Посмотрите описание команды добавления пользовательских атрибутов:

```bash
ydb table attribute add --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--attribute` | Пользовательский атрибут в формате `<ключ>=<значение>`. Вы можете использовать `--attribute` несколько раз, чтобы добавить несколько атрибутов в одной команде. |

## Примеры {#primery-{examples}}

Добавьте пользовательский атрибуты с ключами `attr_key1`, `attr_key2` и значениями `attr_value1`,`attr_value2` соответственно таблице `my-table`:

```bash
ydb table attribute add --attribute attr_key1=attr_value1 --attribute attr_key2=attr_value2 my-table
```
