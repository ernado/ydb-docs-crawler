---
title: "PDiskWriteLoad"
url: "https://ydb.tech/docs/en/contributor/load-actors-pdisk-write?version=v26.1"
doc_path: "en/contributor/load-actors-pdisk-write"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-pdisk-write.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-pdisk-write.md"
description: "Tests the performance of writes to the PDisk. The load is generated on behalf of a VDisk. The actor creates chunks on the specified PDisk and writes random data"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# PDiskWriteLoad

Tests the performance of writes to the PDisk. The load is generated on behalf of a VDisk. The actor creates chunks on the specified PDisk and writes random data to them. After the load stops, the data written by the actor is deleted.

You can generate two types of load:

- **Continuous:** The actor ensures the specified number of requests are run concurrently. To generate a continuous load, set a zero interval between requests, e.g., `IntervalMsMin: 0` and `IntervalMsMax: 0`, while keeping the `InFlightWrites` parameter different from zero.
- **Interval:** The actor runs requests at preset intervals. To generate interval load, set a non-zero interval between requests, e.g., `IntervalMsMin: 10` and `IntervalMsMax: 100`. You can set the maximum number of in-flight requests using the `InFlightWrites` parameter. If its value is `0`, their number is unlimited.

## Actor parameters {#options}

The basic actor parameters are described below. For the full list of parameters, see the [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) file in the YDB Git repository.

| Parameter | Description |
| --- | --- |
| `PDiskId` | ID of the Pdisk being loaded on the node. |
| `PDiskGuid` | Globally unique ID of the PDisk being loaded. |
| `VDiskId` | The load is generated on behalf of a VDisk with the following parameters:<br>- `GroupID`: Group ID.<br>- `GroupGeneration`: Group generation.<br>- `Ring`: Group ring ID.<br>- `Domain`: Ring fail domain ID.<br>- `VDisk`: Index of the VDisk in the fail domain. |
| `Chunks` | Chunk parameters.  <br>`Slots`: Number of slots per chunk, determines the write size.  <br>You can specify multiple `Chunks`, in which case a specific chunk to write data to is selected based on its `Weight`. |
| `DurationSeconds` | Load duration in seconds. |
| `IntervalMsMin`,  <br>`IntervalMsMax` | Minimum and maximum intervals between requests under interval load, in milliseconds. The interval value is selected randomly from the specified range. |
| `InFlightWrites` | Number of simultaneously processed write requests. |
| `LogMode` | Logging mode. In `LOG_SEQUENTIAL` mode, data is first written to a chunk and then, once the write is committed, to a log. |
| `Sequential` | Type of writes.<br>- `True`: Sequential.<br>- `False`: Random. |
| `IsWardenlessTest` | Set it to `False` in case the PDiskReadLoad actor is run on the cluster; otherwise, e.g. when it is run during unit tests, set it to `True`. |

## Examples {#example}

The following actor writes data blocks of `32` MB during `120` seconds with `64` in-flight requests (continuous load):

```proto
PDiskWriteLoad: {
    PDiskId: 1000
    PDiskGuid: 2258451612736857634
    VDiskId: {
        GroupID: 11234
        GroupGeneration: 5
        Ring: 1
        Domain: 1
        VDisk: 3
    }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    DurationSeconds: 120
    IntervalMsMin: 0
    IntervalMsMax: 0
    InFlightWrites: 64
    LogMode: LOG_SEQUENTIAL
    Sequential: false
    IsWardenlessTest: false
}
```

When viewing test results, the following value should be of most interest to you:

- `Average speed since start`: Average write speed since start, in MB/s, e.g., `615.484013`.
