---
title: "Проверка версии конфигурации"
url: "https://ydb.tech/docs/ru/devops/configuration-management/check-config-version?version=v26.1"
doc_path: "ru/devops/configuration-management/check-config-version"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/check-config-version.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/check-config-version.md"
description: "Существует два основных способа проверить, какую версию механизма конфигурации ( V1 или V2 ) используют узлы вашего кластера YDB: Через Embedded UI."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Проверка версии конфигурации

Существует два основных способа проверить, какую версию механизма конфигурации ([V1](configuration-v1/config-overview.md) или [V2](configuration-v2/config-overview.md)) используют узлы вашего кластера YDB:

1. [Через Embedded UI](check-config-version.md#embedded-ui)
2. [Через метрики кластера](check-config-version.md#metrics)

## Через Embedded UI {#embedded-ui}

Данный способ может быть применен, если сбор метрик с кластера YDB в систему мониторинга не настроен. Вы можете проверить версию конфигурации для конкретного узла или переключаться между узлами через встроенный веб-интерфейс [Embedded UI](../../reference/embedded-ui/index.md):

1. Откройте в браузере страницу актора `configs_dispatcher` для любого узла кластера. URL имеет вид:

   ```text
   http://<endpoint>:8765/actors/configs_dispatcher
   ```

   где `<endpoint>` - адрес произвольного узла кластера YDB.

2. В верхней части открывшейся страницы найдите поле `Configuration version`. В нем будет указана версия конфигурации (`v1` или `v2`), используемая данным узлом.

   Так выглядит страница узла, использующего конфигурацию V1:

   ![configs-dispatcher-page-v1](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/configuration-management/_assets/viewer-v1.png)

3. Чтобы проверить другие узлы, используйте поле поиска `Nodes...` в правом верхнем углу страницы для переключения между узлами.

## Через метрики кластера {#metrics}

Данный способ удобен при наличии большого числа узлов в кластере YDB. Если у вас настроен [сбор метрик с кластера YDB в систему мониторинга](../../reference/observability/metrics/index.md), проделайте следующие действия:

1. Найдите дашборд, отображающий метрики кластера.
2. Перейдите к группе сенсоров `config` и подсистеме `configs_dispatcher`.
3. Обратите внимание на сенсоры `ConfigurationV1` и `ConfigurationV2`. Значения этих сенсоров показывают количество узлов кластера, работающих с конфигурацией V1 и V2 соответственно.

Например, если `ConfigurationV1 > 0`, значит в кластере есть узлы, которые используют конфигурацию v1. Если `ConfigurationV2 = 0` и `ConfigurationV2` равен общему числу узлов, значит, все узлы используют конфигурацию V2.
