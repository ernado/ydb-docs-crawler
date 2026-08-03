---
title: "Публикация конфигурации"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/config-publication?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/config-publication"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/config-publication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/config-publication.md"
description: "Рассмотрим сценарий, где необходимо публиковать небольшую конфигурацию для экземпляров приложения, которые должны оперативно реагировать на её изменения."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Публикация конфигурации

Рассмотрим сценарий, где необходимо публиковать небольшую конфигурацию для экземпляров приложения, которые должны оперативно реагировать на её изменения.

Этот сценарий можно реализовать с помощью семафоров в [узлах координации YDB](../../reference/ydb-sdk/coordination.md) следующим образом:

1. Создаётся семафор (например, с именем `my-service-config`).
2. Через `UpdateSemaphore` публикуется обновлённая конфигурация.
3. Экземпляры приложения делают `DescribeSemaphore` с `WatchData=true`, в результате вызова в `Data` будет текущая версия конфигурации.
4. В случае изменения конфигурации вызывается `OnChanged`. В этом случае экземпляры приложения делают аналогичный вызов `DescribeSemaphore` и получают обновлённую конфигурацию.
