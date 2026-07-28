---
title: "Режимы аутентификации"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/jdbc-driver/authentication?version=v26.1"
doc_path: "ru/reference/languages-and-apis/jdbc-driver/authentication"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/jdbc-driver/authentication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/jdbc-driver/authentication.md"
description: "JDBC-драйвер для YDB поддерживает следующие режимы аутентификации:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Режимы аутентификации

JDBC-драйвер для YDB поддерживает следующие [режимы аутентификации](../../ydb-sdk/auth.md):

- **Anonymous** — без аутентификации. Этот режим используется, если не указаны имя пользователя и пароль и не настроены другие методы аутентификации.
- **Static credentials** — используется, если указаны имя пользователя и пароль.
- **Access token** — используется, если указано свойство [`token`](properties.md#token). Требуется YDB токен, который можно получить, выполнив команду `ydb auth get-token` в YDB CLI.
- **Metadata** — используется, если в свойстве [`useMetadata`](properties.md#metadata) указано значение `true`. В этом режиме данные для аутентификации получаются из метаданных виртуальной машины, контейнера serverless или функции serverless, выполненной в облаке.
- **Service account key** — используется, если указано свойство [`saFile`](properties.md#saFile). В этом режиме для аутентификации применяется ключ сервисной учётной записи.
