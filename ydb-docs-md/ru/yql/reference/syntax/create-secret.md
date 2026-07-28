---
title: "CREATE SECRET"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-secret.md"
description: "Команда CREATE SECRET создаёт секрет. Синтаксис: CREATE SECRET secret_name WITH (option = value [,...]). secret_name — имя создаваемого секрета."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE SECRET

Команда `CREATE SECRET` создаёт [секрет](../../../concepts/datamodel/secrets.md).

Синтаксис:

```sql
CREATE SECRET secret_name
WITH (option = value[, ...])
```

- `secret_name` — имя создаваемого секрета.

- `option` — опция команды:

  - `value` — строка со значением секрета.
  - `inherit_permissions` — опция, при включении которой [права](grant.md) на секрет наследуются от директории, в которой секрет создаётся. При отключении опции от директории наследуется только [право](grant.md#permissions-list) `DESCRIBE SCHEMA`. Владелец секрета получает все возможные права на него в любом случае. По умолчанию — `False`.

## Разрешения {#razresheniya}

Для создания секрета требуется [право](grant.md#permissions-list) `CREATE TABLE`.

## Примеры {#primery}

Создать секрет в корне базы с именем `secret_name` и значением `secret_value`:

```sql
CREATE SECRET secret_name WITH (value = "secret_value");
```

Создать секрет в директории `dir` в корне базы с именем `secret_name` и значением `secret_value`. Если директория `dir` не существует, она будет создана:

```sql
CREATE SECRET `dir/secret_name` WITH (value = "secret_value");
```

Создать секрет в корне базы с именем `secret_name` и значением `secret_value` с правами такими же, как у родительской директории секрета:

```sql
CREATE SECRET secret_name WITH (value = "secret_value", inherit_permissions = True);
```

## См. также {#sm-takzhe}

- [ALTER SECRET](alter-secret.md)
- [DROP SECRET](drop-secret.md)
