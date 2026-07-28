---
title: "DROP GROUP"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-group?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-group"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-group.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-group.md"
description: "Удаляет указанную группу. Для одного оператора вы можете указать несколько групп. Синтаксис: DROP GROUP [ IF EXISTS ] group_name [,...]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP GROUP

Удаляет указанную группу. Для одного оператора вы можете указать несколько групп.

Синтаксис:

```yql
DROP GROUP [ IF EXISTS ] group_name [, ...]
```

- `IF EXISTS` — не выводить ошибку, если группа не существует.
- `group_name` — имя группы, которого нужно удалить.

## Встроенные группы {#vstroennye-gruppy}

YDB может иметь набор групп и пользователей уже с момента начального развёртывания.

Подробнее см. [Первичные настройки безопасности](../../../reference/configuration/security_config.md#security-bootstrap) и [Начальная настройка безопасности кластера](../../../security/builtin-security.md).

Такие пользователи и группы ничем не отличаются от пользователей и групп, созданных позже.
