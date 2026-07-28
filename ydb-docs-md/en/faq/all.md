---
title: "All questions on one page"
url: "https://ydb.tech/docs/en/faq/all?version=v26.1"
doc_path: "en/faq/all"
version: "v26.1"
lang: "en"
source_path: "en/core/faq/all.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/faq/all.md"
description: "All questions on one page General questions General questions about YDB What is YDB?"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# All questions on one page

## General questions {#common}

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

## SDK {#SDK}

# SDK

## What should I do if the SDK crashes when shutting down an application? {#what-to-do-if-the-sdk-crashes-urgently-when-the-app-is-shut-down}

Make sure not to wrap SDK components in a singleton, since their lifetime shouldn't exceed the execution time of the `main()` function. When a client is destroyed, session pools are emptied, so network navigation is required. But gRPC contains global static variables that might already be destroyed by this time. This disables gRPC. If you need to declare a driver as a global object, invoke the `Stop(true)` function on the driver before exiting the `main()` function.

## What should I do if, when using a `fork()`system call, a program does not work properly in a child process? {#program-does-not-work-correctly-when-calling-fork}

Using `fork()` in multithreaded applications is an antipattern. Since both the SDK and the gRPC library are multithreaded applications, their stability is not guaranteed.

## What do I do if I get the "Active sessions limit exceeded" error even though the current number of active sessions is within limits? {#active-sessions-does-not-exceed-the-limit}

The limit applies to the number of active sessions. An active session is a session passed to the client to be used in its code. A session is returned to the pool in a destructor. In this case, the session itself is a replicated object. You may have saved a copy of the session in the code.

## Is it possible to make queries to different databases from the same application? {#make-requests-to-different-databases-from-the-same-application}

Yes, the C++ SDK lets you override the DB parameters and token when creating a client. There is no need to create separate drivers.

## What should I do if a VM has failed and it's impossible to make a query? {#vms-failed-and-you-cant-make-a-request}

To detect that a VM is unavailable, set a client timeout. All queries contain the client timeout parameters. The timeout value should be an order of magnitude greater than the expected query execution time.

## Errors

# Errors

## Possible causes for "Status: OVERLOADED Error: Pending previous query completion" in the C++ SDK

Q: When running two queries, I try to get a response from the future method of the second one. It returns: `Status: OVERLOADED Why: <main>: Error: Pending previous query completion`.

A: Sessions in the SDK are single-threaded. To run multiple queries at once, you need to create multiple sessions.

## What do I do if I frequently get the "Transaction locks invalidated" error? {#locks-invalidated}

Typically, if you get this error, repeat a transaction, as YDB uses optimistic locking. If this error occurs frequently, this is the result of a transaction reading a large number of rows or of many transactions competing for the same "hot" rows. It makes sense to view the queries running in the transaction and check if they're reading unnecessary rows.

## What causes the "Exceeded maximum allowed number of active transactions" error? {#exceed-number-transactions}

The logic on the client side should try to keep transactions as short as possible.

No more than 10 active transactions are allowed per session. When starting a transaction, use either the commit flag for autocommit or an explicit commit/rollback.

## What do I do if I get the Datashard: Reply size limit exceeded error in response to a query? {#reply-size-exceeded}

This error means that, as a query was running, one of the participating data shards attempted to return over 50 MB of data, which exceeds the allowed limit.

Recommendations:

- A general recommendation is to reduce the amount of data processed in a transaction.
- If a query involves a `Join`, it's a good idea to make sure that the method used is [Index lookup Join](yql.md#index-lookup-join).
- If a simple selection is performed, make sure that it is done by keys, or add `LIMIT` in the query.

## What do I do is I get the "Datashard program size limit exceeded" in response to a query? {#program-size-exceeded}

This error means that the size of a program (including parameter values) exceeded the 50-MB limit for one of the data shards. In most cases, this indicates an attempt to write over 50 MB of data to database tables in a single transaction. All modifying operations in a transaction such as `UPSERT`, `REPLACE`, `INSERT`, or `UPDATE` count as records.

You need to reduce the total size of records in one transaction. Normally, we don't recommend combining queries that logically don't require transactionality in a single transaction. When adding/updating data in batches, we recommend reducing the size of one batch to values not exceeding a few megabytes.

## YQL

# YQL

## General questions {#common1}

### How do I select table rows by a list of keys? {#explicit-keys}

You can select table rows based on a specified list of table primary key (or key prefix) values using the `IN` operator:

```yql
DECLARE $keys AS List<UInt64>;

SELECT * FROM some_table
WHERE Key1 IN $keys;
```

If a selection is made using a composite key, the query parameter must have the type of a list of tuples:

```yql
DECLARE $keys AS List<Tuple<UInt64, String>>;

SELECT * FROM some_table
WHERE (Key1, Key2) IN $keys;
```

To select rows effectively, make sure that the value types in the parameters match the key column types in the table.

### Is search by index performed for conditions containing the LIKE operator? {#like-index}

You can only use the `LIKE` operator to search a table index if it specifies a row prefix:

```yql
SELECT * FROM string_key_table
WHERE Key LIKE "some_prefix%";
```

### Why does a query return only 1000 rows? {#result-rows-limit}

1000 rows is the response size limit per YQL query. If a response is shortened, it is flagged as `Truncated`. To output more table rows, you can use [paginated output](../dev/paging.md) or the `ReadTable` operation.

### How to escape quotes of JSON strings when adding them to a table? {#escaping-quotes}

Consider an example with two possible options for adding a JSON string to a table:

```yql
UPSERT INTO test_json(id, json_string)
VALUES
    (1, Json(@@[{"name":"Peter \"strong cat\" Kourbatov"}]@@)),
    (2, Json('[{"name":"Peter \\\"strong cat\\\" Kourbatov"}]'))
;
```

To insert a value in the first line, use `raw string` and the escape method using `\"`. To insert the second line, escaping through `\\\"` is used.

We recommend using `raw string` and the escape method using `\"`, as it is more visual.

### How do I update only those values whose keys are not in the table? {#update-non-existent}

You can use the `LEFT JOIN` operator to identify the keys a table is missing and update their values:

```yql
DECLARE $values AS List<Struct<Key: UInt64, Value: String>>;

UPSERT INTO kv_table
SELECT v.Key AS Key, v.Value AS Value
FROM AS_TABLE($values) AS v
LEFT JOIN kv_table AS t
ON v.Key = t.Key
WHERE t.Key IS NULL;
```

## Join operations {#joins}

### Are there any specific features of Join operations? {#join-operations}

A `Join` in YDB is performed using one of the two methods below:

- Common Join.
- Index Lookup Join.

### Common Join

The contents of both tables (to the left and to the right of `Join`) are sent to the requesting node which applies the operation to the totality of the data. This is the most generic way of performing a `Join` that is used whenever other optimizations are unavailable. For large tables, this method is either slow or doesn't work in general due to exceeding the data transfer limits.

### Index Lookup Join

For rows on the left of `Join`, relevant values are looked up to the right. You use this method whenever the right part is a table and the `Join` key is its primary or secondary index key prefix. In this method, limited selections are made from the right table instead of full reads. This lets you use it when working with large tables.

> [!NOTE]
> For most OLTP queries, we recommend using Index Lookup Join with a small size of the left part. These operations read little data and can be performed efficiently.

### How do I Join data from query parameters? {#constant-table-join}

You can use query parameter data as a constant table. To do this, use the `AS_TABLE` modifier with a parameter whose type is a list of structures:

```yql
DECLARE $data AS List<Struct<Key1: UInt64, Key2: String>>;

SELECT * FROM AS_TABLE($data) AS d
INNER JOIN some_table AS t
ON t.Key1 = d.Key1 AND t.Key2 = d.Key2;
```

There is no explicit limit on the number of entries in the constant table, but mind the standard limit on the total size of query parameters (50 MB).

### What's the best way to implement a query like (key1, key2) IN ((v1, v2), (v3, v4), ...)? {#key-pairs-in}

It's better to write it using a JOIN with a constant table:

```yql
$keys = AsList(
    AsStruct(1 AS Key1, "One" AS Key2),
    AsStruct(2 AS Key1, "Three" AS Key2),
    AsStruct(4 AS Key1, "One" AS Key2)
);

SELECT t.* FROM AS_TABLE($keys) AS k
INNER JOIN table1 AS t
ON t.Key1 = k.Key1 AND t.Key2 = k.Key2;
```

## Transactions

### How efficient is it to run multiple queries in a transaction? {#transaction-queries}

When multiple queries are run sequentially, the total transaction latency may be greater than when the same operations are executed within a single query. This is primarily due to additional network latency for each query. Therefore, if a transaction doesn't need to be interactive, we recommend formulating all operations in a single YQL query.

### Is a separate query atomic? {#atomic-query}

In general, YQL queries can be executed in multiple consecutive phases. For example, a Join query can be executed in two phases: reading data from the left and right table, respectively. This aspect is important when you run a query in a transaction with a low isolation level (`online_read_only`), as in this case, data between execution phases can be updated by other transactions.

## Analytics

## Can YDB be used for analytical workloads (OLAP)?

Yes, it can. If this is the primary type of workload for a given table, make sure it is [column-oriented](../concepts/datamodel/table.md#column-oriented-tables).

## How to choose between row-oriented and column-oriented tables?

Similarly to choosing between transactional (OLTP) and analytical (OLAP) database management systems, this question comes to a number of trade-offs that need to be considered:

- **What's the main use case for the table?** For mostly transactional (OLTP) workloads, use [row-oriented tables](../concepts/datamodel/table.md#row-oriented-tables). For analytical workloads (OLAP), use [column-oriented tables](../concepts/datamodel/table.md#column-oriented-tables). Transactional workloads are characterized by a high rate of queries affecting a small number of rows each. Analytical workloads are characterized by processing large volumes of data to produce relatively small query results.
- **How is the table modified?** As a rule of thumb, row-oriented tables work better when data is frequently modified in place, while column-oriented tables work better when data is mostly appended by adding new rows. Thus, row-oriented tables usually reflect the current state of a dataset, while column-oriented tables often store a history of some sort of immutable events.
- **Which features are needed?** Even though YDB strives for feature parity between row-oriented and column-oriented tables, there might be current limitations to consider. Check the documentation for details on specific features intended to be used with a given table.

Unlike most other database management systems, YDB supports both row-oriented and column-oriented tables in the same [database](../concepts/glossary.md#database). However, keep in mind that transactional and analytical workloads have different resource consumption patterns and might affect each other when the cluster is overloaded.

## Known issues

# Known issues

## Table partitions are not merging when autopartitioning is enabled {#table-partitions-are-not-merging}

For tables created in earlier versions of YDB, the autopartitioning mechanism does not merge partitions even when merge conditions based on load or size are met. This can result in an excessive number of partitions in the table.

This issue is specific to tables that meet the following two criteria:

- The table was created on a YDB cluster prior to version 22.2.
- The table had no minimum partition count value set, either at creation time or afterwards.

To resolve the issue, explicitly set a minimum partition count value for the table. For example, use the [AUTO_PARTITIONING_MIN_PARTITIONS_COUNT](../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) parameter:

```yql
ALTER TABLE `my_table` SET (AUTO_PARTITIONING_MIN_PARTITIONS_COUNT = 1);
```
