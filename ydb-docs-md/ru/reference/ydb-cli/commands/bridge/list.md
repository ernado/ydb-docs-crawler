---
title: "admin cluster bridge list"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/bridge/list?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/bridge/list"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/bridge/list.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/bridge/list.md"
description: "Функциональность Корпоративной СУБД Яндекса. Данная функциональность доступна только в Корпоративной СУБД Яндекса. В open-source версии YDB она отсутствует."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster bridge list

> [!NOTE]
> **Функциональность Корпоративной СУБД Яндекса**
>
> Данная функциональность доступна только в [Корпоративной СУБД Яндекса](../../../../downloads/yandex-enterprise-database.md). В open-source версии YDB она отсутствует.

С помощью команды `admin cluster bridge list` можно вывести состояние каждого pile в [режиме bridge](../../../../concepts/bridge.md).

Общий вид команды:

```bash
ydb [global options...] admin cluster bridge list [options...]
```

- `global options` — [глобальные параметры](../global-options.md) CLI.
- `options` — [параметры подкоманды](list.md#options).

Просмотр справки по команде:

```bash
ydb admin cluster bridge list --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--format <pretty, json, csv>` | Формат вывода. Допустимые значения: `pretty`, `json`, `csv`. Значение по умолчанию: `pretty`. |

## Примеры {#examples}

Вывести список pile в человекочитаемом формате:

```bash
ydb admin cluster bridge list

pile-a: PRIMARY
pile-b: SYNCHRONIZED
```

Вывести состояние в формате JSON:

```bash
ydb admin cluster bridge list --format json

{
  "pile-a": "PRIMARY",
  "pile-b": "SYNCHRONIZED"
}
```

Вывести состояние в формате CSV:

```bash
ydb admin cluster bridge list --format csv

pile,state
pile-a,PRIMARY
pile-b,SYNCHRONIZED
```
