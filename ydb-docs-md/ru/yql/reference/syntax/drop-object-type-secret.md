---
title: "DROP OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-object-type-secret?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-object-type-secret"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-object-type-secret.md"
description: "Внимание. Данная команда устарела и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе Секреты."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
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
