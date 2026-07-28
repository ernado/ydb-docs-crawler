---
title: "CREATE GROUP"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-group?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-group"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-group.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-group.md"
description: "Создает группу с указанным именем. Есть возможность указать список пользователей, входящих в эту группу. Синтаксис."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE GROUP

Создает [группу](../../../concepts/glossary.md#access-group) с указанным именем. Есть возможность указать список [пользователей](../../../concepts/glossary.md#access-user), входящих в эту группу.

## Синтаксис {#sintaksis}

```yql
CREATE GROUP group_name [ WITH USER user_name [ , user_name [ ... ]] [ , ] ]
```

### Параметры {#parametry}

- `group_name` — имя группы. Может содержать строчные буквы латинского алфавита и цифры.
- `user_name` — имя пользователя, который станет участником группы после её создания. Может содержать строчные буквы латинского алфавита и цифры.

## Примеры {#primery}

```yql
CREATE GROUP group1;
```

```yql
CREATE GROUP group2 WITH USER user1;
```

```yql
CREATE GROUP group3 WITH USER user1, user2,;
```

```yql
CREATE GROUP group4 WITH USER user1, user3, user2;
```

## Встроенные группы {#vstroennye-gruppy}

YDB может иметь набор групп и пользователей уже с момента начального развёртывания.

Подробнее см. [Первичные настройки безопасности](../../../reference/configuration/security_config.md#security-bootstrap) и [Начальная настройка безопасности кластера](../../../security/builtin-security.md).

Такие пользователи и группы ничем не отличаются от пользователей и групп, созданных позже.
