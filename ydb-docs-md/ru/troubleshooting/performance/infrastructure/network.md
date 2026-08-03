---
title: "Сетевые проблемы"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/infrastructure/network?version=v26.1"
doc_path: "ru/troubleshooting/performance/infrastructure/network"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/infrastructure/network.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/infrastructure/network.md"
description: "Сетевые проблемы, такие как ограниченная пропускная способность, потеря пакетов и нестабильное соединение, могут сильно повлиять на производительность базы данн"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Сетевые проблемы

Сетевые проблемы, такие как ограниченная пропускная способность, потеря пакетов и нестабильное соединение, могут сильно повлиять на производительность базы данных, замедлив скорость обработки запросов или приводя к временным сбоям, например ошибкам превышения срока ожидания (timeout).

## Диагностика {#diagnostika}

Для диагностики сетевых проблем используйте опцию healthcheck во [Встроенном UI](../../../reference/embedded-ui/index.md):

1. Откройте [Встроенный UI](../../../reference/embedded-ui/index.md):

   1. Перейдите во вкладку **Databases** и выберите необходимую базу данных.

   2. На вкладке **Navigation** убедитесь, что выбрана нужная база данных.

   3. Откройте вкладку **Diagnostics**.

   4. На вкладке **Network** включите фильтр **With problems**.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/infrastructure/_assets/diagnostics-network.png)

2. Используйте другие доступные инструменты для мониторинга таких метрик сети как задержки, джиттер, потеря пакетов, пропускная способность и др.

## Рекомендации {#rekomendacii}

Обратитесь к ответственным за сетевую инфраструктуру кластера YDB. В больших организациях это может быть своя команда. В других случаях обратитесь в поддержку облачного сервиса или хостинга.
