---
title: "DROP TRANSFER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-transfer?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-transfer"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-transfer.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-transfer.md"
description: "Вызов DROP TRANSFER удаляет экземпляр трансфера. Вместе с экземпляром трансфера удалится и читатель, если он был создан автоматически при создании трансфера. По"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP TRANSFER

Вызов `DROP TRANSFER` удаляет экземпляр [трансфера](../../../concepts/transfer.md). Вместе с экземпляром трансфера удалится и [читатель](../../../concepts/datamodel/topic.md#consumer), если он был создан автоматически при создании трансфера. Попытки удаления читателя будут продолжаться до его успешного удаления.

Вызов `DROP TRANSFER` не удаляет таблицу, в которую записываются данные, и топик, из которого данные читаются.

## Синтаксис {#syntax}

```yql
DROP TRANSFER <name>
```

где:

- `name` — имя экземпляра трансфера.

## Разрешения {#razresheniya}

Для удаления трансфера требуются следующие [права](grant.md#permissions-list):

- `REMOVE SCHEMA` — для удаления экземпляра трансфера;
- `ALTER SCHEMA` — для удаления автоматически созданного читателя топика (если применимо).

## Примеры {#examples}

Следующий запрос удаляет трансфер c именем `my_transfer`:

```yql
DROP TRANSFER my_transfer;
```

## См. также {#sm-takzhe}

- [CREATE TRANSFER](create-transfer.md)
- [ALTER TRANSFER](alter-transfer.md)
- [Трансфер данных](../../../concepts/transfer.md)
