---
title: "DROP SECRET"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-secret.md"
description: "Команда DROP SECRET удаляет существующий секрет. Синтаксис: DROP SECRET secret_name. secret_name — имя удаляемого секрета. Разрешения."
revision: "a6ee1837f90009a183281888dccad12a7b30d774"
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
