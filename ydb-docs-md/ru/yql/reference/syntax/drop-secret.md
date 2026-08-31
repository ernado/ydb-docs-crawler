---
title: "DROP SECRET"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-secret.md"
description: "Команда DROP SECRET удаляет существующий секрет. Синтаксис: DROP SECRET secret_name. secret_name — имя удаляемого секрета. Разрешения."
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# DROP SECRET

Команда `DROP SECRET` удаляет существующий [секрет](../../../concepts/datamodel/secrets.md).

Синтаксис:

```sql
DROP SECRET secret_name
```

- `secret_name` — имя удаляемого секрета.

## Разрешения {#razresheniya}

Для удаления секрета требуются [права](grant.md#permissions-list) `REMOVE SCHEMA` и `ALTER SCHEMA`.

## Примеры {#primery}

Удалить секрет с именем `secret_name`:

```sql
DROP SECRET secret_name;
```

## См. также {#sm-takzhe}

- [CREATE SECRET](create-secret.md)
- [ALTER SECRET](alter-secret.md)
