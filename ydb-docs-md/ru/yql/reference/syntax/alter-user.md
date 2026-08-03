---
title: "ALTER USER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-user?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-user"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-user.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-user.md"
description: "Изменяет пароль пользователя. Синтаксис: ALTER USER user_name [ WITH ] option [... ]. user_name — имя пользователя. option — опция команды:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER USER

Изменяет пароль пользователя.

Синтаксис:

```yql
ALTER USER user_name [ WITH ] option [ ... ]
```

- `user_name` — имя пользователя.

- `option` — опция команды:

  - `PASSWORD 'password'` — изменяет пароль на `password`.
  - `PASSWORD NULL` — устанавливает пустой пароль.
  - `NOLOGIN` - запрет на логин пользователя (блокировка пользователя).
  - `LOGIN` - разрешение на логин пользователя (разблокировка пользователя).

## Встроенные пользователи {#vstroennye-polzovateli}

YDB может иметь набор групп и пользователей уже с момента начального развёртывания.

Подробнее см. [Первичные настройки безопасности](../../../reference/configuration/security_config.md#security-bootstrap) и [Начальная настройка безопасности кластера](../../../security/builtin-security.md).

Такие пользователи и группы ничем не отличаются от пользователей и групп, созданных позже.
