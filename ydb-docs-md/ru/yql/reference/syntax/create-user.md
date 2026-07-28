---
title: "CREATE USER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-user?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-user"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-user.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-user.md"
description: "Создает пользователя с указанным именем и паролем. Синтаксис: CREATE USER user_name [ option ]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE USER

Создает пользователя с указанным именем и паролем.

Синтаксис:

```yql
CREATE USER user_name [option]
```

- `user_name` — имя пользователя. Может содержать строчные буквы латинского алфавита и цифры.

- `option` — опция команды:

  - `PASSWORD 'password'` — создает пользователя с паролем `password`.
  - `PASSWORD NULL` — создает пользователя с пустым паролем (по умолчанию).
  - `NOLOGIN` - запрет на логин пользователя (блокировка пользователя).
  - `LOGIN` - разрешение на логин пользователя (по умолчанию).

> [!NOTE]
> Область действия команд `CREATE USER`, `ALTER USER`, `DROP USER` не распространяется на внешние каталоги пользователей.
>  Учитывайте это, если к YDB подключаются пользователи со сторонней аутентификацией (например, LDAP).
>  Например, команда `CREATE USER` не создаст пользователя в LDAP-каталоге.
>  Подробнее про [взаимодействие YDB с LDAP-каталогом](../../../security/authentication.md#ldap).

## Встроенные пользователи {#vstroennye-polzovateli}

YDB может иметь набор групп и пользователей уже с момента начального развёртывания.

Подробнее см. [Первичные настройки безопасности](../../../reference/configuration/security_config.md#security-bootstrap) и [Начальная настройка безопасности кластера](../../../security/builtin-security.md).

Такие пользователи и группы ничем не отличаются от пользователей и групп, созданных позже.
