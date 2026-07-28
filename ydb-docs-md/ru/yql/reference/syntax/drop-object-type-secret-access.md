---
title: "DROP OBJECT (TYPE SECRET_ACCESS)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-object-type-secret-access?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-object-type-secret-access"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-object-type-secret-access.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-object-type-secret-access.md"
description: "Внимание. Данная команда устарела и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе Секреты."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP OBJECT (TYPE SECRET_ACCESS)

> [!CAUTION]
> **Данная команда устарела** и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе [Секреты](../../../concepts/datamodel/secrets.md).

Удаляет указанное правило доступа к [секрету](../../../concepts/datamodel/secrets.md#secret_access).

Если правила с таким именем не существует, возвращается ошибка.

## Пример {#primer}

```yql
DROP OBJECT (TYPE SECRET_ACCESS) `MySecretName:another_user`;
```
