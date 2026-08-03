---
title: "CREATE OBJECT (TYPE SECRET_ACCESS)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-object-type-secret-access?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-object-type-secret-access"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-object-type-secret-access.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-object-type-secret-access.md"
description: "Внимание. Данная команда устарела и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе Секреты."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE OBJECT (TYPE SECRET_ACCESS)

> [!CAUTION]
> **Данная команда устарела** и будет удалена в будущих версиях YDB. Рекомендуемый синтаксис работы с секретами описан в разделе [Секреты](../../../concepts/datamodel/secrets.md).

Все права на использование секрета принадлежат создателю секрета. Создатель секрета может предоставить право чтения секрета другому пользователю с помощью управления доступом к секретам.

Для управления доступами к секретам используются специальные объекты `SECRET_ACCESS`. Для выдачи разрешения на использование секрета `secret_name` пользователю `user_name` необходимо создать объект `SECRET_ACCESS` с именем `secret_name:user_name`.

```yql
CREATE OBJECT `secret_name:user_name` (TYPE SECRET_ACCESS);
```

Где:

- `secret_name` - имя [секрета](create-object-type-secret.md).
- `user_name` - имя пользователя, которому выдается доступ.

## Пример {#primer}

Следующий SQL-запрос выдаст права на использование секрета `MySecretName` пользователю `another_user`:

```yql
CREATE OBJECT `MySecretName:another_user` (TYPE SECRET_ACCESS);
```
