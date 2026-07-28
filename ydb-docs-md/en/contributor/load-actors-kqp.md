---
title: "Query Processor Load"
url: "https://ydb.tech/docs/en/contributor/load-actors-kqp?version=v26.1"
doc_path: "en/contributor/load-actors-kqp"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-kqp.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-kqp.md"
description: "Runs general performance testing for the YDB cluster by loading all components via the Query Processor layer. The load is similar to that from the workload YDB"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Query Processor Load

Runs general performance testing for the YDB cluster by loading all components via the Query Processor layer. The load is similar to that from the [workload](../reference/ydb-cli/commands/workload/index.md) YDB CLI subcommand, but it is generated from within the cluster.

You can run two types of load:

- **Stock**: Simulates a warehouse of an online store: creates multi-product orders, gets a list of orders per customer.
- **Key-value**: Uses the DB as a key-value store.

Before this test, the necessary tables are created. After it's completed, they are deleted.

## Actor parameters {#options}

The basic actor parameters are described below. For the full list of parameters, see the [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) file in the YDB Git repository.

| Parameter | Description |
| --- | --- |
| `DurationSeconds` | Load duration in seconds. |
| `WindowDuration` | Statistics aggregation window duration. |
| `WorkingDir` | Path to the directory to create test tables in. |
| `NumOfSessions` | The number of parallel threads creating the load. Each thread writes data to its own session. |
| `DeleteTableOnFinish` | Set it to `False` if you do not want the created tables deleted after the load stops. This might be helpful when a large table is created upon the actor's first run, and then queries are made to that table. |
| `UniformPartitionsCount` | The number of partitions created in test tables. |
| `WorkloadType` | Type of load.  <br>For Stock:<br>- `0`: InsertRandomOrder.<br>- `1`: SubmitRandomOrder.<br>- `2`: SubmitSameOrder.<br>- `3`: GetRandomCustomerHistory.<br>- `4`: GetCustomerHistory.<br>For Key-Value:<br>- `0`: UpsertRandom.<br>- `1`: InsertRandom.<br>- `2`: SelectRandom. |
| `Workload` | Kind of load.  <br>`Stock`:<br>- `ProductCount`: Number of products.<br>- `Quantity`: Quantity of each product in stock.<br>- `OrderCount`: Initial number of orders in the database.<br>- `Limit`: Minimum number of shards for tables.<br>`Kv`:<br>- `InitRowCount`: Before load is generated, the load actor writes the specified number of rows to the table.<br>- `StringLen`: Length of the `value` string.<br>- `ColumnsCnt`: Number of columns to use in the table.<br>- `RowsCnt`: Number of rows to insert or read per SQL query. |

## Examples {#example}

The following actor runs a stock load on the `/slice/db` database by making simple UPSERT queries of `64` threads during `30` seconds.

```proto
KqpLoad: {
    DurationSeconds: 30
    WindowDuration: 1
    WorkingDir: "/slice/db"
    NumOfSessions: 64
    UniformPartitionsCount: 1000
    DeleteTableOnFinish: 1
    WorkloadType: 0
    Stock: {
        ProductCount: 100
        Quantity: 1000
        OrderCount: 100
        Limit: 10
    }
}
```

As a result of the test, the number of successful transactions per second, the number of transaction execution retries, and the number of errors are output.
