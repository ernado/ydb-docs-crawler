---
title: "table attribute drop"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/table-attribute-drop?version=v26.1"
doc_path: "ru/reference/ydb-cli/table-attribute-drop"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/table-attribute-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/table-attribute-drop.md"
description: "С помощью команды table attribute drop вы можете удалить пользовательский атрибут указанной таблицы. Общий вид команды:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# table attribute drop

С помощью команды `table attribute drop` вы можете удалить [пользовательский атрибут](../../concepts/datamodel/table.md#users-attr) указанной таблицы.

Общий вид команды:

```bash
ydb [global options...] table attribute drop [options...] <table path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](table-attribute-drop.md#options).
- `table path` — путь таблицы.

Посмотрите описание команды добавления пользовательских атрибутов:

```bash
ydb table attribute drop --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--attributes` | Ключ пользовательского атрибута, который нужно удалить. Вы можете указать несколько ключей, используя `,` в качестве разделителя. |

## Примеры {#primery-{examples}}

Удалите пользовательские атрибуты с ключами `attr_key1` и `attr_key2` таблицы `my-table`:

```bash
ydb table attribute drop --attributes attr_key1,attr_key2 my-table
```
