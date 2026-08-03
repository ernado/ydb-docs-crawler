---
title: "ALTER SECRET"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-secret.md"
description: "Команда ALTER SECRET изменяет существующий секрет. Синтаксис: ALTER SECRET secret_name WITH (option = value [,...]). secret_name — имя изменяемого секрета."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER SECRET

Команда `ALTER SECRET` изменяет существующий [секрет](../../../concepts/datamodel/secrets.md).

Синтаксис:

```sql
ALTER SECRET secret_name
WITH (option = value[, ...])
```

- `secret_name` — имя изменяемого секрета.

- `option` — опция команды:

  - `value` — строка со значением секрета.

## Разрешения {#razresheniya}

Для изменения секрета требуется [право](grant.md#permissions-list) `ALTER SCHEMA`.

## Примеры {#primery}

Изменить значение секрета `secret_name` на `secret_value_new`:

```sql
ALTER SECRET secret_name WITH (value = "secret_value_new");
```

## См. также {#sm-takzhe}

- [CREATE SECRET](create-secret.md)
- [DROP SECRET](drop-secret.md)
