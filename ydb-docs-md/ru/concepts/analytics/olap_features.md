---
title: "Ключевые возможности для аналитики: быстрый справочник"
url: "https://ydb.tech/docs/ru/concepts/analytics/olap_features?version=v26.1"
doc_path: "ru/concepts/analytics/olap_features"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/analytics/olap_features.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/analytics/olap_features.md"
description: "Эта страница — карта документации по аналитическим возможностям YDB. Текст сгруппирован по этапам жизненного цикла данных, чтобы помочь быстро найти необходимую"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Ключевые возможности для аналитики: быстрый справочник

Эта страница — карта документации по аналитическим возможностям YDB. Текст сгруппирован по этапам жизненного цикла данных, чтобы помочь быстро найти необходимую информацию для проектирования, разработки и эксплуатации аналитических решений.

## Проектирование хранилища данных (Concepts & Design) {#proektirovanie-hranilisha-dannyh-concepts-and-design}

Основы организации данных, масштабирования и управления.

### Основные концепции и типы данных {#osnovnye-koncepcii-i-tipy-dannyh}

- [Колоночные таблицы](../datamodel/table.md#column-oriented-tables): архитектура хранения, оптимизированная для OLAP.
- [Типы данных](../../yql/reference/types/index.md): полный справочник по поддерживаемым типам.

### Масштабирование и производительность {#masshtabirovanie-i-proizvoditelnost}

- [Проектирование ключей для максимальной производительности](../../dev/primary-key/column-oriented.md): как выбирать `PRIMARY KEY` и `PARTITION BY`.
- [Партиционирование таблиц](../datamodel/table.md#olap-tables-partitioning): механизм распределения данных по узлам.

### Управление жизненным циклом данных {#upravlenie-zhiznennym-ciklom-dannyh}

- [TTL (Time-to-Live)](../ttl.md): автоматическое удаление устаревших данных по истечении срока.

## Загрузка и выгрузка данных (Ingestion & Egress) {#zagruzka-i-vygruzka-dannyh-ingestion-and-egress}

Инструменты и API для перемещения данных в YDB и из неё.

### Потоковая загрузка (Streaming Ingestion) {#potokovaya-zagruzka-streaming-ingestion}

- [Topics (Kafka API)](../datamodel/topic.md): нативная работа с потоками данных через протокол Kafka.
- [Transfer](../transfer.md): управляемый сервис для переноса данных между топиками и таблицами.
- [Коннектор Fluent Bit](../../integrations/ingestion/fluent-bit.md): прямая загрузка логов.

### Пакетная загрузка (Batch Ingestion) {#paketnaya-zagruzka-batch-ingestion}

- [Коннектор Apache Spark](../../integrations/query-engines/spark.md): чтение и запись данных для ETL/ELT-задач.
- [BulkUpsert API](../../recipes/ydb-sdk/bulk-upsert.md): высокопроизводительная вставка больших объемов данных через SDK.

### Взаимодействие с внешними системами {#vzaimodejstvie-s-vneshnimi-sistemami}

- [Федеративные запросы](../query_execution/federated_query/index.md): выполнение запросов к данным, находящимся во внешних системах (S3, ClickHouse, Postgres).
- [Работа с S3 через внешние таблицы](../query_execution/federated_query/s3/external_table.md): чтение и запись данных в формате Parquet/CSV в Object Storage.

## Обработка и трансформация данных (ETL/ELT) {#obrabotka-i-transformaciya-dannyh-etl/elt}

Язык запросов и интеграция с инструментами оркестрации.

### Язык запросов YQL {#yazyk-zaprosov-yql}

- [Полный справочник по YQL](../../yql/reference/index.md): синтаксис, функции и операторы.
- [Функции для работы с датой и временем](../../yql/reference/udf/list/datetime.md): полный список и типовые сценарии.
- [Функции для работы с JSON](../../yql/reference/builtins/json.md): извлечение данных из JSON-документов.

### Инструменты для построения пайплайнов {#instrumenty-dlya-postroeniya-pajplajnov}

- [Интеграция с dbt (Data Build Tool)](../../integrations/migration/dbt.md): управление ELT-пайплайнами с помощью SQL.
- [Интеграция с Apache Airflow](../../integrations/orchestration/airflow.md): оркестрация сложных ETL/ELT-процессов.

## Разработка и интеграция с приложениями (Development & SDKs) {#razrabotka-i-integraciya-s-prilozheniyami-development-and-sdks}

Инструменты для разработчиков приложений.

- [Обзор YDB SDK](../../reference/ydb-sdk/index.md): нативные SDK для Go, Python, Java, C++, JavaScript.
- [JDBC драйвер](../../reference/languages-and-apis/jdbc-driver/index.md): стандартный способ подключения из Java-экосистемы.
- [YDB CLI](../../reference/ydb-cli/index.md): инструмент командной строки для администрирования и выполнения запросов.

## Анализ данных и визуализация (Analytics & BI) {#analiz-dannyh-i-vizualizaciya-analytics-and-bi}

Интеграция с инструментами для конечных пользователей.

### BI-системы {#bi-sistemy}

- [Apache Superset](../../integrations/visualization/superset.md)
- [Grafana](../../integrations/visualization/grafana.md)
- [Yandex DataLens](../../integrations/visualization/datalens.md)

### Инструменты Data Science {#instrumenty-data-science}

- [Jupyter Notebooks](../../integrations/gui/jupyter.md): выполнение YQL-запросов и анализ данных в интерактивном режиме.

## Эксплуатация и управление производительностью (Operations & Performance) {#ekspluataciya-i-upravlenie-proizvoditelnostyu-operations-and-performance}

Администрирование, мониторинг, безопасность и оптимизация.

### Управление производительностью {#upravlenie-proizvoditelnostyu}

- [Анализ планов запросов (EXPLAIN)](../../dev/query-execution-optimization/query-plans-optimization.md): как понять план выполнения запроса и найти узкие места.
- [Управление нагрузкой (Resource Pools)](../../dev/resource-consumption-management.md): изоляция ресурсов CPU для разных команд или нагрузок.
- [Стоимостной оптимизатор](../query_execution/optimizer.md): обзор принципов работы планировщика запросов.

### Мониторинг и диагностика {#monitoring-i-diagnostika}

- [Встроенный UI](../../reference/embedded-ui/index.md): веб-интерфейс для мониторинга состояния и диагностики кластера.
- [Справочник по метрикам](../../reference/observability/metrics/index.md): полный список метрик для систем мониторинга.
- [Готовые дашборды для Grafana](../../reference/observability/metrics/grafana-dashboards.md): шаблоны для быстрой настройки мониторинга.

### Безопасность и отказоустойчивость {#bezopasnost-i-otkazoustojchivost}

- [Аутентификация и авторизация](../../security/authentication.md): настройка доступа пользователей, в том числе через LDAP.

### Архитектурные ограничения {#arhitekturnye-ogranicheniya}

- [Известные ограничения системы](../../analyst/limitations.md): важный раздел для понимания особенностей и компромиссов архитектуры.
