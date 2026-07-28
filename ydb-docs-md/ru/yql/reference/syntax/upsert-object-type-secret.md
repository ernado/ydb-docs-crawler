---
title: "UPSERT OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/upsert-object-type-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/upsert-object-type-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/upsert-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/upsert-object-type-secret.md"
description: "Внимание. Данная команда устарела и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе Секреты."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# UPSERT OBJECT (TYPE SECRET)

> [!CAUTION]
> **Данная команда устарела** и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе [Секреты](../../../concepts/datamodel/secrets.md).

Для изменения содержимого [секрета](../../../concepts/datamodel/secrets.md) используется следующий SQL-запрос:

```yql
UPSERT OBJECT `secret_name` (TYPE SECRET) WITH value = `secret_value`;
```

Где:

- `secret_name` - имя секрета.
- `secret_value` - содержимое секрета.

## Пример {#primer}

Следующий запрос устанавливает новое значение секрета с именем `MySecretName` в значение `MySecretData`.

```yql
UPSERT OBJECT `MySecretName` (TYPE SECRET) WITH value = `MySecretData`;
```
