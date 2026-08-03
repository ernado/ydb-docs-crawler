---
title: "Интеграции YDB"
url: "https://ydb.tech/docs/ru/integrations/?version=v26.1"
doc_path: "ru/integrations/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/index.md"
description: "В данном разделе приведена основная информация про интеграции YDB со сторонними системами. Примечание."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Интеграции YDB

В данном разделе приведена основная информация про интеграции YDB со сторонними системами.

> [!NOTE]
> В дополнение к своему собственному нативному протоколу, YDB обладает слоем совместимости, что позволяет внешним системам подключаться к базам данных по сетевому протоколу [Apache Kafka](../reference/kafka-api/index.md). Благодаря слою совместимости, множество инструментов, разработанных для работы с Kafka, могут также взаимодействовать с YDB. Уровень совместимости каждого конкретного приложения необходимо уточнять отдельно.

## Графические пользовательские интерфейсы {#gui}

| Среда | Инструкция | Уровень поддержки |
| --- | --- | --- |
| Встроенный UI | [Справка](../reference/embedded-ui/index.md) |  |
| [DBeaver](https://dbeaver.com) | [Инструкция](gui/dbeaver.md) | C помощью [JDBC-драйвера](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| JetBrains Database viewer | — | C помощью [JDBC-драйвера](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| [JetBrains DataGrip](https://www.jetbrains.com/ru-ru/datagrip/) | [Инструкция](gui/datagrip.md) | C помощью [JDBC-драйвера](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| Другие JDBC-совместимые IDE | — | C помощью [JDBC-драйвера](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| [Jupyter Notebook](https://jupyter.org) | [Инструкция](gui/jupyter.md) | С помощью [YDB-SQLAlchemy](https://github.com/ydb-platform/ydb-sqlalchemy/releases) |

## Визуализация данных (Business Intelligence, BI) {#bi}

| Среда | Уровень поддержки | Инструкция |
| --- | --- | --- |
| [Apache Superset](https://superset.apache.org) | [ydb-sqlalchemy](https://github.com/ydb-platform/ydb-sqlalchemy/releases) | [Инструкция](visualization/superset.md) |
| [DataLens](https://datalens.tech) | Полный | [Инструкция](visualization/datalens.md) |
| [Grafana](https://grafana.com) | Полный | [Инструкция](visualization/grafana.md) |

## Оркестрация {#orchestration}

| Среда | Инструкция |
| --- | --- |
| [Apache Airflow™](https://airflow.apache.org) | [Инструкция](orchestration/airflow.md) |

## Поставка данных {#ingestion}

| Система поставки | Инструкция |
| --- | --- |
| [FluentBit](https://fluentbit.io) | [Инструкция](ingestion/fluent-bit.md) |
| [LogStash](https://www.elastic.co/logstash) | [Инструкция](ingestion/logstash.md) |
| [Kafka Connect Sink](https://docs.confluent.io/platform/current/connect/index.html) | [Инструкция](https://github.com/ydb-platform/ydb-kafka-sink-connector) |

### Потоковая поставка данных {#potokovaya-postavka-dannyh}

| Система поставки | Инструкция |
| --- | --- |
| [Apache Kafka API](https://kafka.apache.org) | [Инструкция](../reference/kafka-api/index.md) |
| [Apache Kafka Connect](https://kafka.apache.org/documentation/#connect) | [Инструкция](../reference/kafka-api/connect/index.md) |

## Миграции данных {#data_migration}

| Источник | Инструкция |
| --- | --- |
| Произвольные [JDBC-источники данных](https://ru.wikipedia.org/wiki/Java_Database_Connectivity) | [Инструкция](data-migration/import-jdbc.md) |
| [MySQL](https://www.mysql.com/) | [Инструкция](data-migration/import-mysql.md) |

## Миграции схемы {#schema_migration}

| Среда | Инструкция |
| --- | --- |
| [goose](https://github.com/pressly/goose/) | [Инструкция](migration/goose.md) |
| [Liquibase](https://www.liquibase.com) | [Инструкция](migration/liquibase.md) |
| [Flyway](https://documentation.red-gate.com/fd/) | [Инструкция](migration/flyway.md) |
| [dbt](https://www.getdbt.com/) | [Инструкция](migration/dbt.md) |

## Движки выполнения запросов {#query_engines}

| Движок | Инструкция |
| --- | --- |
| [Apache Spark™](https://spark.apache.org) | [Инструкция](query-engines/spark.md) |

## Объектно-реляционное отображение (ORM) {#orm}

| Система | Инструкция |
| --- | --- |
| [Hibernate](https://hibernate.org/orm/) | [Инструкция](orm/hibernate.md) |
| [Spring Data JDBC](https://spring.io/projects/spring-data-jdbc) | [Инструкция](orm/spring-data-jdbc.md) |
| [JOOQ](https://www.jooq.org/) | [Инструкция](orm/jooq.md) |
| [Dapper](https://www.learndapper.com/) | [Инструкция](orm/dapper.md) |
| [Entity Framework](https://docs.microsoft.com/ef/core/index) | [Инструкция](orm/entity-framework.md) |
| [Linq To DB](https://linq2db.github.io/) | [Инструкция](orm/linq2db.md) |
| [SQLAlchemy](https://www.sqlalchemy.org/) | [Инструкция](orm/sqlalchemy.md) |
| [Django](https://www.djangoproject.com/) | [Инструкция](orm/django.md) |

## Векторный поиск {#vectorsearch}

| Инструмент | Инструкция |
| --- | --- |
| [LangChain](https://python.langchain.com/docs/introduction/) | [Инструкция](vectorsearch/langchain.md) |
| [Mem0](https://mem0.ai/) | [Инструкция](vectorsearch/mem0.md) |

## Конвертация SQL-диалектов {#sql-translation}

| Инструмент | Инструкция |
| --- | --- |
| Плагин [ydb-sqlglot-plugin](https://github.com/ydb-platform/ydb-sqlglot-plugin) для [SQLGlot](https://github.com/tobymao/sqlglot) | [Инструкция](sql-translation/sqlglot.md) |
| Конвертер SQL-диалектов в YQL | [Инструкция](sql-translation/sql-dialect-converter.md) |

## Смотрите также {#smotrite-takzhe}

- [Справка по YDB SDK](../reference/ydb-sdk/index.md)
- [Kafka API](../reference/kafka-api/index.md)
