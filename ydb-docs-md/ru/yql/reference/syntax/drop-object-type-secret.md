---
title: "DROP OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-object-type-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-object-type-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-object-type-secret.md"
description: "Внимание. Данная команда устарела и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе Секреты."
revision: "b61acf8801342bea386583a9946acfb5e803ab09"
---

# DROP OBJECT (TYPE SECRET)

> [!CAUTION]
> **Данная команда устарела** и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе [Секреты](../../../concepts/datamodel/secrets.md).

Удаляет указанный [секрет](../../../concepts/datamodel/secrets.md).

Если секрета с таким именем не существует, возвращается ошибка.

## Пример {#primer}

```yql
DROP OBJECT my_secret (TYPE SECRET);
```
