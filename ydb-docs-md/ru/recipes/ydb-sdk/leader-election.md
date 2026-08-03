---
title: "Выбор лидера (leader election)"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/leader-election?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/leader-election"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/leader-election.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/leader-election.md"
description: "Рассмотрим сценарий, где несколько экземпляров приложения хотят выбрать лидера и всегда знать, кто им является."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Выбор лидера (leader election)

Рассмотрим сценарий, где несколько экземпляров приложения хотят выбрать лидера и всегда знать, кто им является.

Этот сценарий можно реализовать с помощью семафоров в [узлах координации YDB](../../reference/ydb-sdk/coordination.md) следующим образом:

1. Создаётся семафор (например, с именем `my-service-leader`) с `Limit=1`.
2. Все экземпляры приложения выполняют `AcquireSemaphore` с `Count=1`, указывая в `Data` свой endpoint.
3. Только у одного экземпляра приложения вызов завершится быстро, остальные встанут в очередь. Тот, у кого вызов завершился успешно, становится текущим лидером.
4. Все экземпляры приложения выполняют `DescribeSemaphore` с `WatchOwners=true` и `IncludeOwners=true`. В результате вызова в `Owners` будет максимум один элемент, из `Data` узнаётся endpoint текущего лидера.
5. При смене лидера вызывается `OnChanged`. В этом случае экземпляры приложения выполняют аналогичный вызов `DescribeSemaphore` и узнают endpoint нового лидера.
