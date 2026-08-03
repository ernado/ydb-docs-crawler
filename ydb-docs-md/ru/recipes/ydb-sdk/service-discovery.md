---
title: "Обнаружение сервисов (service discovery)"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/service-discovery?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/service-discovery"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/service-discovery.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/service-discovery.md"
description: "Рассмотрим сценарий, где экземпляры приложения динамически поднимаются и публикуют свой endpoint, а другие клиенты хотят получать этот список и реагировать на е"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обнаружение сервисов (service discovery)

Рассмотрим сценарий, где экземпляры приложения динамически поднимаются и публикуют свой endpoint, а другие клиенты хотят получать этот список и реагировать на его изменения.

Этот сценарий можно реализовать с помощью семафоров в [узлах координации YDB](../../reference/ydb-sdk/coordination.md) следующим образом:

1. Создаётся семафор (например, с именем `my-service-endpoints`) с `Limit=Max<ui64>()`.
2. Все экземпляры приложения выполняют `AcquireSemaphore` с `Count=1`, указывая в `Data` свой endpoint.
3. Поскольку лимит семафора очень большой, все вызовы `AcquireSemaphore` должны завершиться быстро.
4. На этом этапе публикация завершена, и экземплярам приложения нужно только реагировать на остановку сессии, публикуя себя заново через новую сессию.
5. Клиенты выполняют `DescribeSemaphore` с `IncludeOwners=true` и, при необходимости, с `WatchOwners=true`. В результате вызова в поле `Owners` в `Data` будут содержаться endpoint'ы зарегистрированных экземпляров приложения.
6. При изменении списка endpoint'ов вызывается `OnChanged`. В этом случае клиенты выполняют аналогичный вызов `DescribeSemaphore` и получают обновлённый список.
