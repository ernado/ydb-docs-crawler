---
title: "PDiskLogLoad"
url: "https://ydb.tech/docs/en/contributor/load-actors-pdisk-log?version=v26.1"
doc_path: "en/contributor/load-actors-pdisk-log"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-pdisk-log.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-pdisk-log.md"
description: "All VDisks hosted on a certain PDisk log data about their own performance to the common PDisk log. VDisks gradually delete their obsolete data at the beginning"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# PDiskLogLoad

All VDisks hosted on a certain PDisk log data about their own performance to the common PDisk log. VDisks gradually delete their obsolete data at the beginning of the log to free up disk space. Sometimes, after one VDisk completes logging data and before another one starts logging it, a section with useless obsolete data may appear. In this case, such data is deleted automatically, and the PDiskLogLoad actor will perform a test to check whether such an operation is running correctly.

> [!NOTE]
> This ad-hoc actor is used for testing specific functionality. This is not a load actor. It is designed to check whether something works properly.

## Actor parameters {#options}

The basic actor parameters are described below. For the full list of parameters, see the [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) file in the YDB Git repository.

| Parameter | Description |
| --- | --- |
| `PDiskId` | ID of the Pdisk being loaded on the node. |
| `PDiskGuid` | Globally unique ID of the PDisk being loaded. |
| `VDiskId` | Parameters of the VDisk used to generate load.<br>- `GroupID`: Group ID.<br>- `GroupGeneration`: Group generation.<br>- `Ring`: Group ring ID.<br>- `Domain`: Ring fail domain ID.<br>- `VDisk`: Index of the VDisk in the fail domain. |
| `MaxInFlight` | Number of simultaneously processed requests. |
| `SizeIntervalMin` | Minimum size of log record in bytes. |
| `SizeIntervalMax` | Maximum size of log record in bytes. |
| `BurstInterval` | Interval between logging sessions in bytes. |
| `BurstSize` | Total amount of data to log per session, in bytes. |
| `StorageDuration` | Virtual time in bytes. Indicates how long the VDisk should store its data in the log. |
| `IsWardenlessTest` | Set it to `False` in case the PDiskReadLoad actor is run on the cluster; otherwise, e.g. when it is run during unit tests, set it to `True`. |

## Examples {#example}

The following actor simulates the performance of two VDisks. The first VDisk logs a message of `65536` bytes every `65536` bytes and deletes data that exceeds `1048576` bytes. The second one writes `1024` bytes as messages of `128` bytes every `2147483647` bytes and deletes data that exceeds `2147483647` bytes.

```proto
PDiskLogLoad: {
    Tag: 1
    PDiskId: 1
    PDiskGuid: 12345
    DurationSeconds: 60
    Workers: {
        VDiskId: {GroupID: 1 GroupGeneration: 5 Ring: 1 Domain: 1 VDisk: 1}
        MaxInFlight: 1
        SizeIntervalMin: 65536
        SizeIntervalMax: 65536
        BurstInterval: 65536
        BurstSize: 65536
        StorageDuration: 1048576
    }
    Workers: {
        VDiskId: {GroupID: 2 GroupGeneration: 5 Ring: 1 Domain: 1 VDisk: 1}
        MaxInFlight: 1
        SizeIntervalMin: 128
        SizeIntervalMax: 128
        BurstInterval: 2147483647
        BurstSize: 1024
        StorageDuration: 2147483647
    }
    IsWardenlessTest: false
}
```

The test passes if none of the cluster nodes got overloaded and the status of the PDisk in question is `Normal`. You can check this using the cluster Embedded UI.
