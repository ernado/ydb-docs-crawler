---
title: "Аутентификация"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/auth?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/auth"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/auth.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/auth.md"
description: "YDB поддерживает несколько способов аутентификации подключения к серверной стороне. Каждый из них, как правило, специфичен для конкретной пары окружений: где на"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Аутентификация

YDB поддерживает несколько способов аутентификации подключения к серверной стороне. Каждый из них, как правило, специфичен для конкретной пары окружений: где находится клиентское приложение (в доверенной зоне YDB или вне ее) и серверная часть YDB (докер-контейнер, Yandex.Cloud, data cloud, установка на отдельном кластере)

В данном разделе содержатся рецепты кода с настройкой аутентификации в разных YDB SDK. Общее описание принципов аутентификации в SDK можно прочитать в статье [Аутентификация в SDK](auth.md).

Содержание:

- [С помощью токена](auth-access-token.md)
- [Анонимная](auth-anonymous.md)
- [Файл сервисного аккаунта](auth-service-account.md)
- [Сервис метаданных](auth-metadata.md)
- [С помощью переменных окружения](auth-env.md)
- [С помощью логина и пароля](auth-static.md)
