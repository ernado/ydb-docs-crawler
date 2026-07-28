---
title: "DROP USER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-user?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-user"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-user.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-user.md"
description: "Удаляет указанного пользователя. Для одного оператора вы можете указать несколько пользователей. Синтаксис: DROP USER [ IF EXISTS ] user_name [,...]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP USER

Удаляет указанного пользователя. Для одного оператора вы можете указать несколько пользователей.

Синтаксис:

```yql
DROP USER [ IF EXISTS ] user_name [, ...]
```

- `IF EXISTS` — не выводить ошибку, если пользователь не существует.
- `user_name` — имя удаляемого пользователя. Поддерживается возможность задать список пользователей через запятую, например: `DROP USER user1, user2, user3;`.

## Встроенные пользователи {#vstroennye-polzovateli}

YDB может иметь набор групп и пользователей уже с момента начального развёртывания.

Подробнее см. [Первичные настройки безопасности](../../../reference/configuration/security_config.md#security-bootstrap) и [Начальная настройка безопасности кластера](../../../security/builtin-security.md).

Такие пользователи и группы ничем не отличаются от пользователей и групп, созданных позже.
