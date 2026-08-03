---
title: "Load testing"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/workload/?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/workload/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/workload/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/workload/index.md"
description: "Load testing. You can use the workload command to run different types of workload against your DB. General format of the command:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Load testing

You can use the `workload` command to run different types of workload against your DB.

General format of the command:

```bash
ydb [global options...] workload [subcommands...]
```

- `global options`: [Global options](../global-options.md).
- `subcommands`: The [subcommands](index.md#subcommands).

See the description of the command to run the data load:

```bash
ydb workload --help
```

## Available subcommands {#subcommands}

The following types of load tests are supported at the moment:

- [Stock](stock.md): An online store warehouse simulator.
- [Key-value](../../workload-kv.md): Key-Value load.
- [ClickBench](../../workload-click-bench.md): [ClickBench analytical benchmark](https://github.com/ClickHouse/ClickBench).
- [TPC-C](../../workload-tpcc.md): [TPC-C benchmark](https://www.tpc.org/tpcc/).
- [TPC-H](../../workload-tpch.md): [TPC-H benchmark](https://www.tpc.org/tpch/).
- [TPC-DS](../../workload-tpcds.md): [TPC-DS benchmark](https://www.tpc.org/tpcds/).
- [Topic](../../workload-topic.md): Topic load.
- [Transfer](../../workload-transfer.md): Transfer load.
- [Query](../../workload-query.md): Query load.
