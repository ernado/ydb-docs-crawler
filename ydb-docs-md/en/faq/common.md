---
title: "General questions about YDB"
url: "https://ydb.tech/docs/en/faq/common?version=v26.1"
doc_path: "en/faq/common"
version: "v26.1"
lang: "en"
source_path: "en/core/faq/common.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/faq/common.md"
description: "General questions about YDB What is YDB?"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# General questions about YDB

## What is YDB?

YDB is a distributed fault-tolerant SQL DBMS. YDB offers high availability and scalability, while ensuring strong consistency and support for ACID transactions. Queries are made using an SQL dialect (YQL).

YDB is a fully managed database. DB instances are created through the YDB database management service.

## What features does YDB provide? {#ydb-features}

YDB provides high availability and data security through synchronous replication in three availability zones. YDB also ensures even load distribution across available hardware resources. This means you don't need to order resources, YDB automatically provisions and releases resources based on the user load.

## What consistency model does YDB use? {#ydb-consistency}

To read data, YDB uses a model of strict data consistency.

## How do I design a primary key? {#create-pk}

To design a primary key properly, follow the rules below.

- Avoid situations where most of the load falls on a single [partition](../concepts/datamodel/table.md#partitioning) of a table. With even load distribution, it's easier to achieve high overall performance.This rule implies that you shouldn't use a monotonically increasing sequence, such as timestamp, as a table's primary key.
- The fewer table partitions a query uses, the faster it runs. For greater performance, follow the one query — one partition rule.
- Avoid situations where a small part of the DB is under much heavier load than the rest of the DB.

For more information, see [choosing a primary key](../dev/primary-key/index.md).

## How do I evenly distribute load across table partitions? {#balance-shard-load}

You can use the following techniques to distribute the load evenly across table partitions and increase overall DB performance.

- To avoid using uniformly increasing primary key values, you can:

  - Change the order of its components.
  - use a hash of the key column values as the primary key.

- Reduce the number of partitions used in a single query.

For more information, see [choosing a primary key](../dev/primary-key/index.md).

## Can I use NULL in a key column? {#null}

In YDB, all columns, including key ones, may contain a `NULL` value, but we don't recommend using `NULL` as values in key columns.

Per the SQL standard (ISO/IEC 9075), you can't compare `NULL` with other values. Therefore, the use of concise SQL statements with simple comparison operators may result in rows containing NULL being skipped during filtering, for example.

## Is there an optimal size of a database row? {#string-size}

To achieve high performance, we don't recommend writing rows larger than 8 MB and key columns larger than 2 KB to the DB.

For more information about limits, see [Database limits](../concepts/limits-ydb.md).

## How are secondary indexes used in YDB? {#secondary_indexes}

Secondary indexes in YDB are global and can be non-unique.

For more information, see [Secondary indexes](../concepts/query_execution/secondary_indexes.md).

## How are paginated results printed? {#paging}

To print paginated results, we recommend selecting data sorted by primary key sequentially, limiting the number of rows with the `LIMIT` keyword. We do not recommend using the `OFFSET` keyword to solve this problem.

For more information, see [Paginated results](../dev/paging.md).

## How do I delete expired data? {#ttl}

To efficiently delete outdated data, we recommend using [TTL](../concepts/ttl.md).

## Syncing two data centers in geographically distributed clusters {#sinc-between-dc}

The lead [tablet](../concepts/glossary.md#tablet) writes data to a [distributed network storage](../concepts/glossary.md#distributed-storage) that saves copies to several data centers. YDB does not commit a user query until after the required number of copies are saved to the required number of data centers.
