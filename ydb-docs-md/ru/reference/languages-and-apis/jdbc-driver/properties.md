---
title: "Свойства JDBC-драйвера"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/jdbc-driver/properties?version=v26.1"
doc_path: "ru/reference/languages-and-apis/jdbc-driver/properties"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/jdbc-driver/properties.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/jdbc-driver/properties.md"
description: "JDBC-драйвер для YDB поддерживает следующие конфигурационные свойства, которые можно указать в JDBC URL или передать через дополнительные свойства:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Свойства JDBC-драйвера

JDBC-драйвер для YDB поддерживает следующие конфигурационные свойства, которые можно указать в [JDBC URL](properties.md#jdbc-url) или передать через дополнительные свойства:

- `saFile` — ключ сервисной учётной записи (Service Account Key). Значением свойства может быть содержимое ключа или путь к файлу с ключом.

- `iamEndpoint` — IAM-эндпойнт для аутентификации с помощью ключа сервисной учётной записи (Service Account Key).

- `token` — токен для аутентификации. Значением свойства может быть содержимое токена или путь к файлу с токеном.

- `useMetadata` — использование режима аутентификации **Metadata**. Возможные значения:

  - `true` — использовать режим аутентификации **Metadata**;
  - `false` — не использовать режим аутентификации **Metadata**.

  Значение по умолчанию: `false`.

- `metadataURL` — эндпойнт для получения токена в режиме аутентификации **Metadata**.

- `localDatacenter` — название локального датацентра, в котором выполняется приложение.

- `secureConnection` — использование TLS. Возможные значения:

  - `true` — принудительно использовать TLS;
  - `false` — не использовать TLS.

  Обычно безопасное соединение указывается с помощью протокола `grpcs://` в строке JDBC URL. Небезопасное соединение указывается с помощью протокола `grpc://`.

- `secureConnectionCertificate` — сертификат CA для TLS-соединения. Значением свойства может быть содержимое сертификата или путь к файлу с сертификатом.

> [!NOTE]
> Ссылки на файлы в свойствах `saFile`, `token` или `secureConnectionCertificate` должны содержать префикс `file:`. Примеры:
>
> - `saFile=file:~/mysakey1.json`
> - `token=file:/opt/secret/token-file`
> - `secureConnectionCertificate=file:/etc/ssl/cacert.cer`

## Использование режима QueryService {#ispolzovanie-rezhima-queryservice}

По умолчанию JDBC-драйвер для YDB использует старый API для обработки запросов, обеспечивая совместимость с предыдущими версиями YDB. Однако у этого API есть [дополнительные ограничения](../../../concepts/limits-ydb.md#query). Чтобы отключить это поведение и использовать новый API QueryService, укажите свойство `useQueryService=true` в строке JDBC URL.

## Примеры JDBC URL {#jdbc-url}

- Локальный Docker контейнер с анонимной аутентификацией и без TLS:
  `jdbc:ydb:grpc://localhost:2136/local`

- Удаленный кластер, размещенный на собственном сервере:
  `jdbc:ydb:grpcs://<host>:2135/Root/<testdb>?secureConnectionCertificate=file:~/<myca>.cer`

- Экземпляр облачной базы данных с токеном:
  `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?token=file:~/my_token`

- Экземпляр облачной базы данных с файлом сервисного аккаунта:
  `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?saFile=file:~/sa_key.json`
