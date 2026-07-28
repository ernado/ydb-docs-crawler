---
title: "YDB CLI commands"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands?version=v26.1"
doc_path: "en/reference/ydb-cli/commands"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands.md"
description: "YDB CLI commands. General syntax for calling YDB CLI commands: ydb [global options] < command > [<subcommand>...] [ command options]. where:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# YDB CLI commands

General syntax for calling YDB CLI commands:

```bash
ydb [global options] <command> [<subcommand> ...] [command options]
```

where:

- `ydb` is the command to run the YDB CLI from the OS command line.
- `[global options]` are [global options](commands/global-options.md) that are common for all YDB CLI commands.
- `<command>` is the command.
- `[<subcomand> ...]` are subcommands specified if the selected command contains subcommands.
- `[command options]` are command options specific to each command and subcommands.

## Commands {#list}

You can learn about the necessary commands by selecting the subject section in the menu on the left or using the alphabetical list below.

Any command can be run from the command line with the `--help` option to get help on it. You can get a list of all commands supported by the YDB CLI by running the YDB CLI with the `--help` option, but [without any command](commands/service.md).

| Command / subcommand | Brief description |
| --- | --- |
| [admin cluster bridge failover](commands/bridge/failover.md) | Emergency switchover when [pile](../../concepts/glossary.md#pile) is unavailable |
| [admin cluster bridge list](commands/bridge/list.md) | List state of each [pile](../../concepts/glossary.md#pile) in [bridge mode](../../concepts/bridge.md) |
| [admin cluster bridge rejoin](commands/bridge/rejoin.md) | Returning [pile](../../concepts/glossary.md#pile) to the [cluster](../../concepts/glossary.md#cluster) after maintenance or recovery |
| [admin cluster bridge switchover](commands/bridge/switchover.md) | Planned `PRIMARY` [pile](../../concepts/glossary.md#pile) change |
| [admin cluster bridge takedown](commands/bridge/takedown.md) | Taking [pile](../../concepts/glossary.md#pile) out of the [cluster](../../concepts/glossary.md#cluster) for maintenance |
| [admin cluster config fetch](commands/configuration/cluster/fetch.md) | Getting the current dynamic configuration of the [cluster](../../concepts/glossary.md#cluster) |
| [admin cluster config generate](commands/configuration/cluster/generate.md) | Generating a dynamic configuration from a static startup configuration |
| [admin cluster config replace](commands/configuration/cluster/replace.md) | Replacing the [cluster](../../concepts/glossary.md#cluster) dynamic configuration |
| admin cluster config resolve | Computing the final [cluster](../../concepts/glossary.md#cluster) dynamic configuration based on the base configuration and override selectors |
| admin cluster config version | Displaying the [cluster](../../concepts/glossary.md#cluster) configuration version on nodes |
| [admin cluster dump](export-import/tools-dump.md#cluster) | Dumping cluster' metadata to the file system |
| [admin cluster restore](export-import/tools-restore.md#cluster) | Restoring cluster' metadata from the file system |
| admin database config fetch | Getting the current dynamic configuration of the [database](../../concepts/glossary.md#database) |
| admin database config generate | Generating a [database](../../concepts/glossary.md#database) dynamic configuration from a static startup configuration |
| admin database config replace | Replacing the [database](../../concepts/glossary.md#database) dynamic configuration |
| admin database config resolve | Computing the final [database](../../concepts/glossary.md#database) dynamic configuration based on the base configuration and override selectors |
| admin database config version | Displaying the [database](../../concepts/glossary.md#database) configuration version |
| [admin database dump](export-import/tools-dump.md#db) | Dumping database' data and metadata to the file system |
| [admin database restore](export-import/tools-restore.md#db) | Restoring database' data and metadata from the file system |
| [admin node config init](commands/configuration/node/init.md) | Initializing [node](../../concepts/glossary.md#node) configuration |
| auth get-token | Getting an [authentication token](../../concepts/glossary.md#auth-token) from authentication parameters |
| [config info](commands/config-info.md) | Viewing [connection parameters](connect.md) |
|  | [config profile activate](profile/activate.md) |
|  | [config profile create](profile/create.md) |
|  | [config profile delete](profile/create.md) |
|  | [config profile deactivate](profile/activate.md) |
|  | [config profile get](profile/list-and-get.md) |
|  | [config profile list](profile/list-and-get.md) |
|  | [config profile replace](profile/create.md) |
|  | [config profile set](profile/activate.md) |
|  | [config profile update](profile/create.md) |
|  | debug latency |
|  | debug ping |
|  | [discovery list](commands/discovery-list.md) |
|  | [discovery whoami](commands/discovery-whoami.md) |
|  | [export s3](export-import/export-s3.md) |
|  | [import file csv](export-import/import-file.md) |
|  | [import file json](export-import/import-file.md) |
|  | [import file parquet](export-import/import-file.md) |
|  | [import file tsv](export-import/import-file.md) |
|  | [import s3](export-import/import-s3.md) |
|  | [init](profile/create.md) |
|  | [monitoring healthcheck](commands/monitoring-healthcheck.md) |
|  | [operation cancel](operation-cancel.md) |
|  | [operation forget](operation-forget.md) |
|  | [operation get](operation-get.md) |
|  | [operation list](operation-list.md) |
|  | [scheme describe](commands/scheme-describe.md) |
|  | [scheme ls](commands/scheme-ls.md) |
|  | [scheme mkdir](commands/dir.md#mkdir) |
|  | [scheme permissions chown](commands/scheme-permissions.md#chown) |
|  | [scheme permissions clear](commands/scheme-permissions.md#clear) |
|  | [scheme permissions grant](commands/scheme-permissions.md#grant-revoke) |
|  | [scheme permissions revoke](commands/scheme-permissions.md#grant-revoke) |
|  | [scheme permissions set](commands/scheme-permissions.md#set) |
|  | [scheme permissions list](commands/scheme-permissions.md#list) |
|  | [scheme permissions clear-inheritance](commands/scheme-permissions.md#clear-inheritance) |
|  | [scheme permissions set-inheritance](commands/scheme-permissions.md#set-inheritance) |
|  | [scheme rmdir](commands/dir.md#rmdir) |
|  | [scripting yql](scripting-yql.md) |
|  | [sql](sql.md) |
|  | [table attribute add](table-attribute-add.md) |
|  | [table attribute drop](table-attribute-drop.md) |
|  | [table drop](table-drop.md) |
|  | [table index add global-async](commands/secondary_index.md#add) |
|  | [table index add global-sync](commands/secondary_index.md#add) |
|  | [table index drop](commands/secondary_index.md#drop) |
|  | [table index rename](commands/secondary_index.md#rename) |
|  | [table query execute](table-query-execute.md) |
|  | [table query explain](commands/explain-plan.md) |
|  | [table read](commands/readtable.md) |
|  | [table ttl set](table-ttl-set.md) |
|  | [table ttl reset](table-ttl-reset.md) |
|  | [tools copy](tools-copy.md) |
|  | [tools dump](export-import/tools-dump.md#schema-objects) |
|  | [tools infer csv](tools-infer.md) |
|  | [tools rename](commands/tools/rename.md) |
|  | [tools restore](export-import/tools-restore.md#schema-objects) |
|  | [topic create](topic-create.md) |
|  | [topic alter](topic-alter.md) |
|  | [topic drop](topic-drop.md) |
|  | [topic consumer add](topic-consumer-add.md) |
|  | topic consumer describe |
|  | [topic consumer drop](topic-consumer-drop.md) |
|  | [topic consumer offset commit](topic-consumer-offset-commit.md) |
|  | [topic read](topic-read.md) |
|  | [topic write](topic-write.md) |
|  | [update](commands/service.md) |
|  | [version](commands/service.md) |
|  | [workload clickbench init](workload-click-bench.md#init) |
|  | [workload clickbench import files](workload-click-bench.md#load) |
|  | [workload clickbench run](workload-click-bench.md#run) |
|  | [workload clickbench clean](workload-click-bench.md#cleanup) |
|  | [workload kv init](workload-kv.md#init) |
|  | [workload kv run upsert](workload-kv.md#upsert-kv) |
|  | [workload kv run insert](workload-kv.md#insert-kv) |
|  | [workload kv run mixed](workload-kv.md#mixed-kv) |
|  | [workload kv run read-rows](workload-kv.md#read-rows-kv) |
|  | [workload kv run select](workload-kv.md#select-kv) |
|  | [workload kv clean](workload-kv.md#clean) |
|  | workload log init |
|  | workload log import generator |
|  | workload log run bulk_upsert |
|  | workload log run delete |
|  | workload log run insert |
|  | workload log run upsert |
|  | workload log run select |
|  | workload log clean |
|  | workload mixed init |
|  | workload mixed run bulk_upsert |
|  | workload mixed run insert |
|  | workload mixed run upsert |
|  | workload mixed run select |
|  | workload mixed clean |
|  | [workload query init](workload-query.md#init) |
|  | [workload query import](workload-query.md#load) |
|  | [workload query run](workload-query.md#run) |
|  | [workload query clean](workload-query.md#cleanup) |
|  | [workload stock init](commands/workload/stock.md#init) |
|  | [workload stock run add-rand-order](commands/workload/stock.md#insert-random-order) |
|  | [workload stock run put-rand-order](commands/workload/stock.md#submit-random-order) |
|  | [workload stock run put-same-order](commands/workload/stock.md#submit-same-order) |
|  | [workload stock run rand-user-hist](commands/workload/stock.md#get-random-customer-history) |
|  | [workload stock run user-hist](commands/workload/stock.md#get-customer-history) |
|  | [workload stock clean](commands/workload/stock.md#clean) |
|  | [workload topic init](workload-topic.md#init) |
|  | [workload topic run full](workload-topic.md#run-full) |
|  | [workload topic run read](workload-topic.md#run-read) |
|  | [workload topic run write](workload-topic.md#run-write) |
|  | [workload topic clean](workload-topic.md#clean) |
|  | [workload tpcc init](workload-tpcc.md#init) |
|  | [workload tpcc import](workload-tpcc.md#load) |
|  | [workload tpcc check](workload-tpcc.md#consistency_check) |
|  | [workload tpcc run](workload-tpcc.md#run) |
|  | [workload tpcc clean](workload-tpcc.md#cleanup) |
|  | [workload tpcds init](workload-tpcds.md#init) |
|  | [workload tpcds import generator](workload-tpcds.md#load) |
|  | [workload tpcds run](workload-tpcds.md#run) |
|  | [workload tpcds clean](workload-tpcds.md#cleanup) |
|  | [workload tpch init](workload-tpch.md#init) |
|  | [workload tpch import generator](workload-tpch.md#load) |
|  | [workload tpch run](workload-tpch.md#run) |
|  | [workload tpch clean](workload-tpch.md#cleanup) |
|  | [workload transfer topic-to-table init](workload-transfer.md#init) |
|  | [workload transfer topic-to-table run](workload-transfer.md#run) |
|  | [workload transfer topic-to-table clean](workload-transfer.md#clean) |
|  | workload vector init |
|  | workload vector run select |
|  | workload vector run upsert |
|  | workload vector clean |
|  | [yql](yql.md) |
