---
title: "Аутентификация Kafka API"
url: "https://ydb.tech/docs/ru/reference/kafka-api/auth?version=v26.1"
doc_path: "ru/reference/kafka-api/auth"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/kafka-api/auth.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/kafka-api/auth.md"
description: "Включение аутентификации. При самостоятельном развертывании YDB по умолчанию используется анонимная аутентификация. , не требующая логина-пароля."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Аутентификация Kafka API

## Включение аутентификации {#vklyuchenie-autentifikacii}

При [самостоятельном развертывании YDB](../../quickstart.md) по умолчанию используется [анонимная аутентификация](../../security/authentication.md#anonymous)  
 , не требующая логина-пароля.

Чтобы включить обязательную аутентификацию, следуйте инструкции в статье [Аутентификация](../../security/authentication.md#static-credentials).

Аутентификация всегда включена при использовании [Kafka API в Yandex Cloud](https://yandex.cloud/ru/docs/data-streams/kafkaapi/auth)

## Механизм аутентификации {#mehanizm-autentifikacii}

В Kafka API поддержано два механизма SASL аутентификации: `PLAIN` и `SCRAM-SHA-256`.  
 Оба механизма могут осуществляться как внутри протокола `TLS`, так и вне, порождая соответственно комбинации:

- `SASL_PLAINTEXT/PLAIN`;
- `SASL_SSL/PLAIN`;
- `SASL_PLAINTEXT/SCRAM-SHA-256`;
- `SASL_SSL/SCRAM-SHA-256`.

> [!WARNING]
> Для использования механизма `SCRAM-SHA-256` при аутентификации существующих пользователей может потребоваться смена пароля.

Для аутентификации необходимы:

- `<user-name>` — имя пользователя. Об управлении пользователями читайте в разделе [Аутентификация](../../security/authentication.md).
- `<password>` — пароль пользователя. Об управлении пользователями читайте в разделе [Аутентификация](../../security/authentication.md).
- `<database>` — путь к [базе данных](../../concepts/connect.md#database), с которой предполагается дальнейшее взаимодействие. (Необходим только для механизма `PLAIN`).

Для механизма `SCRAM-SHA-256` база данных определяется на основе настроек подключения [Kafka Connect](connect/connect-step-by-step.md).  
 Целевой базой данных считается та база, к которой относится [узел базы данных](../../concepts/glossary.md#database-node), имеющий указанный `<ydb-endpoint>`.

Из этих параметров формируются следующие переменные, которые вы можете использовать в  
 `sasl.jaas.config` параметре конфигурации клиента Kafka:

- `<sasl.username>` = `<user-name>[@<database>]`
- `<sasl.password>` = `<password>`

> [!WARNING]
> Обратите внимание, логика формирования `<sasl.username>` и `<sasl.password>` в облачных инсталляциях YDB может отличаться от приведенной здесь.

Примеры аутентификации смотрите в [Чтение и запись](examples.md).
