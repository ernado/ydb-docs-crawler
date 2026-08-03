---
title: "CREATE OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-object-type-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-object-type-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-object-type-secret.md"
description: "Внимание. Данная команда устарела и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе Секреты."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE OBJECT (TYPE SECRET)

> [!CAUTION]
> **Данная команда устарела** и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе [Секреты](../../../concepts/datamodel/secrets.md).

Для создания [секрета](../../../concepts/datamodel/secrets.md) используется следующий SQL-запрос:

```yql
CREATE OBJECT <secret_name> (TYPE SECRET) WITH value = "<secret_value>";
```

Где:

- `secret_name` - имя секрета.
- `secret_value` - содержимое секрета.

## Пример {#primer}

Следующий запрос создает секрет с именем `MySecretName` и значением `MySecretData`.

```yql
CREATE OBJECT MySecretName (TYPE SECRET) WITH value = "MySecretData";
```
