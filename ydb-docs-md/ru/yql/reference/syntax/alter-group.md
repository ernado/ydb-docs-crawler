---
title: "ALTER GROUP"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-group?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-group"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-group.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-group.md"
description: "Добавляет или удаляет группу указанному пользователю. Для одного оператора вы можете указать несколько пользователей. Синтаксис."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER GROUP

Добавляет или удаляет группу указанному пользователю. Для одного оператора вы можете указать несколько пользователей.

## Синтаксис {#sintaksis}

```yql
ALTER GROUP role_name ADD USER user_name [, ... ]
ALTER GROUP role_name DROP USER user_name [, ... ]
```

- `role_name` — имя группы.
- `user_name` — имя пользователя.

## Встроенные группы {#vstroennye-gruppy}

YDB может иметь набор групп и пользователей уже с момента начального развёртывания.

Подробнее см. [Первичные настройки безопасности](../../../reference/configuration/security_config.md#security-bootstrap) и [Начальная настройка безопасности кластера](../../../security/builtin-security.md).

Такие пользователи и группы ничем не отличаются от пользователей и групп, созданных позже.
