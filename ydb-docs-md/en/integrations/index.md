---
title: "Integrations YDB"
url: "https://ydb.tech/docs/en/integrations/?version=v26.1"
doc_path: "en/integrations/"
version: "v26.1"
lang: "en"
source_path: "en/core/integrations/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/integrations/index.md"
description: "This section provides the main information about YDB integrations with third-party systems. Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Integrations YDB

This section provides the main information about YDB integrations with third-party systems.

> [!NOTE]
> In addition to its own native protocol, YDB has a compatibility layer that allows external systems to connect to databases via [PostgreSQL](../postgresql/intro.md) or [Apache Kafka](../reference/kafka-api/index.md) network protocols. Thanks to the compatibility layer, many tools designed to work with these systems can also interact with YDB. The compatibility level of each specific application must be clarified separately.

## Graphical user interfaces {#gui}

| Environment | Instruction | Compatibility level |
| --- | --- | --- |
| Embedded UI | [Instruction](../reference/embedded-ui/index.md) |  |
| [DBeaver](https://dbeaver.com) | [Instruction](gui/dbeaver.md) | By [JDBC-driver](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| JetBrains Database viewer | — | By [JDBC-driver](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| [JetBrains DataGrip](https://www.jetbrains.com/datagrip/) | [Instruction](gui/datagrip.md) | By [JDBC-driver](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| Other JDBC-compatible IDEs | — | By [JDBC-driver](https://github.com/ydb-platform/ydb-jdbc-driver/releases) |
| [Jupyter Notebook](https://jupyter.org) | [Instruction](gui/jupyter.md) | By [YDB-SQLAlchemy](https://github.com/ydb-platform/ydb-sqlalchemy/releases) |

## Data visualization (Business intelligence, BI) {#bi}

| Environment | Compatibility Level | Instruction |
| --- | --- | --- |
| [Apache Superset](https://superset.apache.org) | [ydb-sqlalchemy](https://github.com/ydb-platform/ydb-sqlalchemy/releases) | [Instruction](visualization/superset.md) |
| [DataLens](https://datalens.tech) | Full | [Instruction](visualization/datalens.md) |
| [Grafana](https://grafana.com) | Full | [Instruction](visualization/grafana.md) |

## Orchestration

| System | Instruction |
| --- | --- |
| [Apache Airflow™](https://airflow.apache.org) | [Instruction](orchestration/airflow.md) |

## Data ingestion {#ingestion}

| Delivery system | Guide |
| --- | --- |
| [FluentBit](https://fluentbit.io) | [Guide](ingestion/fluent-bit.md) |
| [LogStash](https://www.elastic.co/logstash) | [Guide](ingestion/logstash.md) |
| [Kafka Connect Sink](https://docs.confluent.io/platform/current/connect/index.html) | [Guide](https://github.com/ydb-platform/ydb-kafka-sink-connector) |

### Streaming data ingestion {#streaming-ingestion}

| Delivery System | Instruction |
| --- | --- |
| [Apache Kafka API](https://kafka.apache.org) | [Instruction](../reference/kafka-api/index.md) |

## Data migrations {#data_migration}

| Source | Guide |
| --- | --- |
| Arbitrary [JDBC data sources](https://en.wikipedia.org/wiki/Java_Database_Connectivity) | [Guide](data-migration/import-jdbc.md) |
| [MySQL](https://www.mysql.com/) | [Guide](data-migration/import-mysql.md) |

## Schema migrations {#schema_migration}

| Environment | Instruction |
| --- | --- |
| [goose](https://github.com/pressly/goose/) | [Instruction](migration/goose.md) |
| [Liquibase](https://www.liquibase.com) | [Instruction](migration/liquibase.md) |
| [Flyway](https://documentation.red-gate.com/fd/) | [Instruction](migration/flyway.md) |
| [dbt](https://www.getdbt.com/) | [Instruction](migration/dbt.md) |

## Query engines {#query_engines}

| Engine | Guide |
| --- | --- |
| [Apache Spark™](https://spark.apache.org) | [Guide](query-engines/spark.md) |

## Object–relational mapping (ORM) {#orm}

| Delivery System | Instruction |
| --- | --- |
| [Hibernate](https://hibernate.org/orm/) | [Instruction](orm/hibernate.md) |
| [Spring Data JDBC](https://spring.io/projects/spring-data-jdbc) | [Instruction](orm/spring-data-jdbc.md) |
| [JOOQ](https://www.jooq.org/) | [Instruction](orm/jooq.md) |
| [Dapper](https://www.learndapper.com/) | [Instruction](orm/dapper.md) |
| [Entity Framework](https://docs.microsoft.com/ef/core/index) | [Instruction](orm/entity-framework.md) |
| [Linq To DB](https://linq2db.github.io/) | [Instruction](orm/linq2db.md) |
| [SQLAlchemy](https://www.sqlalchemy.org/) | [Instruction](orm/sqlalchemy.md) |
| [Django](https://www.djangoproject.com/) | [Instruction](orm/django.md) |

## Vector search {#vectorsearch}

| Tool | Guide |
| --- | --- |
| [LangChain](https://python.langchain.com/docs/introduction/) | [Guide](vectorsearch/langchain.md) |
| [Mem0](https://mem0.ai/) | [Guide](vectorsearch/mem0.md) |

## See also

- [Reference for YDB SDK](../reference/ydb-sdk/index.md)
- [Kafka API](../reference/kafka-api/index.md)
