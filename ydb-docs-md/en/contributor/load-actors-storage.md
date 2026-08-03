---
title: "StorageLoad"
url: "https://ydb.tech/docs/en/contributor/load-actors-storage?version=v26.1"
doc_path: "en/contributor/load-actors-storage"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-storage.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-storage.md"
description: "Tests the read/write performance to and from Distributed Storage. The load is generated on Distributed Storage directly without using any tablet and Query Proce"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# StorageLoad

Tests the read/write performance to and from Distributed Storage. The load is generated on Distributed Storage directly without using any tablet and Query Processor layers. When testing write performance, the actor writes data to the specified storage group. To test read performance, the actor first writes data to the specified storage group and then reads the data. After the load is removed, all the data written by the actor is deleted.

You can generate three types of load:

- **Continuous:** The actor ensures that the specified number of requests are running concurrently. To generate a continuous load, set a zero interval between requests (e.g., `WriteIntervals: { Weight: 1.0 Uniform: { MinUs: 0 MaxUs: 0 } }`), while keeping the `MaxInFlightWriteRequests` parameter value different from zero and omit the `WriteHardRateDispatcher` parameter.
- **Interval:** The actor runs requests at specific intervals. To generate an interval load, set a non-zero interval between requests, e.g., `WriteIntervals: { Weight: 1.0 Uniform: { MinUs: 50000 MaxUs: 50000 } }` and don't set the `WriteHardRateDispatcher` parameter. The maximum number of in-flight requests is set by the `InFlightWrites` parameter (0 means unlimited).
- **Hard rate:** The actor runs requests at certain intervals, but the interval length is adjusted to maintain a configured request rate per second. If the duration of the load is limited by `LoadDuration` than the request rate may differ between start and finish of the workload and will adjust gradually throughout all the main load cycle. To generate a load of this type, set the [parameters of hard rate load](load-actors-storage.md#hard-rate-dispatcher) (parameter `WriteHardRateDispatcher`). Note that if this parameter is set, the hard rate type of load will be launched, regardless the value of the `WriteIntervals` parameter. The maximum number of in-flight requests is set by the `InFlightWrites` parameter (0 means unlimited).

## Actor parameters {#options}

The basic actor parameters are described below. For the full list of parameters, see the [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) file in the YDB Git repository.

| Parameter | Description |
| --- | --- |
| `DurationSeconds` | Load duration. The timer starts upon completion of the initial data allocation. |
| `Tablets` | The load is generated on behalf of a tablet with the following parameters:<br>- `TabletId`: Tablet ID. It must be unique for each load actor across all the cluster nodes. This parameter and `TabletName` are mutually exclusive.<br>- `TabletName`: Tablet name. If the parameter is set, tablets' IDs will be assigned automatically, tablets launched on the same node with the same name will be given the same ID, tablets launched on different nodes will be given different IDs.<br>- `Channel`: Tablet channel.<br>- `GroupId`: ID of the storage group to get loaded.<br>- `Generation`: Tablet generation. |
| `WriteSizes` | Size of the data to write. It is selected randomly for each request from the `Min`-`Max` range. You can set multiple `WriteSizes` ranges, in which case a value from a specific range will be selected based on its `Weight`. |
| `WriteHardRateDispatcher` | Setting up the [parameters of load with hard rate](load-actors-storage.md#hard-rate-dispatcher) for write requests. If this parameter is set than the value of `WriteIntervals` is ignored. |
| `WriteIntervals` | Setting up the [parameters for probabilistic distribution](load-actors-storage.md#params) of intervals between the records loaded at intervals (in milliseconds). You can set multiple `WriteIntervals` ranges, in which case a value from a specific range will be selected based on its `Weight`. |
| `MaxInFlightWriteRequests` | The maximum number of write requests being processed simultaneously. |
| `ReadSizes` | Size of the data to read. It is selected randomly for each request from the `Min`-`Max` range. You can set multiple `ReadSizes` ranges, in which case a value from a specific range will be selected based on its `Weight`. |
| `WriteHardRateDispatcher` | Setting up the [parameters of load with hard rate](load-actors-storage.md#hard-rate-dispatcher) for read requests. If this parameter is set than the value of `ReadIntervals` is ignored. |
| `ReadIntervals` | Setting up the [parameters for probabilistic distribution](load-actors-storage.md#params) of intervals between the queries loaded by intervals (in milliseconds). You can set multiple `ReadIntervals` ranges, in which case a value from a specific range will be selected based on its `Weight`. |
| `MaxInFlightReadRequests` | The maximum number of read requests being processed simultaneously. |
| `FlushIntervals` | Setting up the [parameters for probabilistic distribution](load-actors-storage.md#params) of intervals (in microseconds) between the queries used to delete data written by the write requests in the main load cycle of the StorageLoad actor. You can set multiple `FlushIntervals` ranges, in which case a value from a specific range will be selected based on its `Weight`. Only one flush request will be processed concurrently. |
| `PutHandleClass` | [Class of data writes](load-actors-storage.md#write-class) to the disk subsystem. If the `TabletLog` value is set, the write operation has the highest priority. |
| `GetHandleClass` | [Class of data reads](load-actors-storage.md#read-class) from the disk subsystem. If the `FastRead` is set, the read operation is performed with the highest speed possible. |
| `Initial allocation` | Setting up the [parameters for initial data allocation](load-actors-storage.md#initial-allocation). It defines the amount of data to be written before the start of the main load cycle. This data can be read by read requests along with the data written in the main load cycle. |

### Write requests class {#write-class}

| Class | Description |
| --- | --- |
| `TabletLog` | The highest priority of write operation. |
| `AsyncBlob` | Used for writing SSTables and their parts. |
| `UserData` | Used for writing user data as separate blobs. |

### Read requests class {#read-class}

| Class | Description |
| --- | --- |
| `AsyncRead` | Used for reading compacted tablets' data. |
| `FastRead` | Used for fast reads initiated by user. |
| `Discover` | Reads from Discover query. |
| `LowRead` | Low priority reads executed on the background. |

### Parameters of probabilistic distribution {#params}

An interval written as a repeated `TIntervalInfo` field is calculated by the following algorithm:

- An element from the `TIntervalInfo` array is selected at random with the probability proportionate to its weight.
- For an element of the `TIntervalUniform` type, the value is chosen with equal probability in the range Min-Max. `Min-Max` (if `MinMs/MaxMs` is used, the value is in milliseconds; if `MinUs/MaxUs` is used, the value is in microseconds).
- For an element of the `TIntervalPoisson` type, the interval is selected using the formula `Min(log(-x / Frequency), MaxIntervalMs)`, where `x` is a random value in the interval `[0, 1]`. As a result, the intervals follow the Poisson distribution with the given `Frequency`, but with the interval within `MaxIntervalMs`.

A similar approach is used for the probabilistic distribution of the size of the written data. However, in this case, only the data size follows a uniform probability distribution, within the interval `[Min, Max]`.

### Parameters of load with hard rate {#hard-rate-dispatcher}

| Parameter | Description |
| --- | --- |
| `RequestRateAtStart` | Requests per second at the moment of load start. If load duration limit is not set then the request rate will remain the same and equal to the value of this parameter. |
| `RequestRateOnFinish` | Requests per second at the moment of load finish. |

### Parameters of initial data allocation {#initial-allocation}

| Parameter | Description |
| --- | --- |
| `TotalSize` | Total size of allocated data. This parameter and `BlobsNumber` are mutually exclusive. |
| `BlobsNumber` | Total number of allocated blobs. |
| `BlobSizes` | Size of the blobs to write. It is selected randomly for each request from the `Min`-`Max` range. You can set multiple `WriteSizes` ranges, in which case a value from a specific range will be selected based on its `Weight`. |
| `MaxWritesInFlight` | Maximum number of simultaneously processed write requests. If this parameter is not set then the number of simultaneously processed requests is not limited. |
| `MaxWriteBytesInFlight` | Maximum number of total amount of simultaneously processed write requests' data. If this parameter is not set then the total amount of data being written concurrently is unlimited. |
| `PutHandleClass` | [Class of data writes](load-actors-storage.md#write-class) to the disk subsystem. |
| `DelayAfterCompletionSec` | The amount of time in seconds the actor will wait upon completing the initial data allocation before starting the main load cycle. If its value is `0` or not set the load will start immediately after the completion of the data allocaion. |

An interval written as a repeated `TIntervalInfo` field is calculated by the following algorithm:

- An element from the `TIntervalInfo` array is selected at random with the probability proportionate to its weight.
- For an element of the `TIntervalUniform` type, the value is chosen with equal probability in the range Min-Max. `Min-Max` (if `MinMs/MaxMs` is used, the value is in milliseconds; if `MinUs/MaxUs` is used, the value is in microseconds).
- For an element of the `TIntervalPoisson` type, the interval is selected using the formula `Min(log(-x / Frequency), MaxIntervalMs)`, where `x` is a random value in the interval `[0, 1]`. As a result, the intervals follow the Poisson distribution with the given `Frequency`, but with the interval within `MaxIntervalMs`.

A similar approach is used for the probabilistic distribution of the size of the written data. However, in this case, only the data size follows a uniform probability distribution, within the interval `[Min, Max]`.

## Examples

### Write load {#write}

The following actor writes data to the group with the ID `2181038080` during `60` seconds. The size per write is `4096` bytes, the number of in-flight requests is no more than `256` (continuous load):

```proto
StorageLoad: {
    DurationSeconds: 60
    Tablets: {
        Tablets: { TabletId: 1000 Channel: 0 GroupId: 2181038080 Generation: 1 }
        WriteSizes: { Weight: 1.0 Min: 4096 Max: 4096 }
        WriteIntervals: { Weight: 1.0 Uniform: { MinUs: 0 MaxUs: 0 } }
        MaxInFlightWriteRequests: 256
        FlushIntervals: { Weight: 1.0 Uniform: { MinUs: 10000000 MaxUs: 10000000 } }
        PutHandleClass: TabletLog
    }
}
```

When viewing test results, the following values should be of most interest to you:

- `Writes per second`: Number of writes per second, e.g., `28690.29`.
- `Speed@ 100%`: 100 percentile of write speed in MB/s, e.g., `108.84`.

### Read load {#read}

To generate a read load, you need to write data first. Data is written by requests of `4096` bytes every `50` ms with no more than `1` in-flight request (interval load). If a request fails to complete within `50` ms, the actor will wait until it is complete and run another request in `50` ms. Data older than `10`s is deleted. Data reads are performed by requests of `4096` bytes with `16` in-flight requests allowed (continuous load):

```proto
StorageLoad: {
    DurationSeconds: 60
    Tablets: {
        Tablets: { TabletId: 5000 Channel: 0 GroupId: 2181038080 Generation: 1 }
        WriteSizes: { Weight: 1.0 Min: 4096 Max: 4096}
        WriteIntervals: { Weight: 1.0 Uniform: { MinUs: 50000 MaxUs: 50000 } }
        MaxInFlightWriteRequests: 1

        ReadSizes: { Weight: 1.0 Min: 4096 Max: 4096 }
        ReadIntervals: { Weight: 1.0 Uniform: { MinUs: 0 MaxUs: 0 } }
        MaxInFlightReadRequests: 16
        FlushIntervals: { Weight: 1.0 Uniform: { MinUs: 10000000 MaxUs: 10000000 } }
        PutHandleClass: TabletLog
        GetHandleClass: FastRead
    }
}
```

When viewing test results, the following value should be of most interest to you:

- `ReadSpeed@ 100%`: 100 percentile of read speed in MB/s, e.g., `60.86`.

### Read only {#readonly}

Before the start of the main load cycle the `1 GB` data block of blobs with sizes between `1 MB` and `5 MB` is allocated. To avoid overloading the system with write requests the number of simultaneously processed requests is limited by the value of `5`. After completing the initial data allocation the main cycle is launched. It consists of read requests sent with increasing rate: from `10` to `50` requests per second, the rate will increase gradually for `300` seconds.

```proto
StorageLoad: {
    DurationSeconds: 300
    Tablets: {
        Tablets: { TabletId: 5000 Channel: 0 GroupId: 2181038080 Generation: 1 }

        MaxInFlightReadRequests: 10
        GetHandleClass: FastRead
        ReadHardRateDispatcher {
                RequestsPerSecondAtStart: 10
                RequestsPerSecondOnFinish: 50
        }

        InitialAllocation {
                TotalSize: 1000000000
                BlobSizes: { Weight: 1.0 Min: 1000000 Max: 5000000 }
                MaxWritesInFlight: 5
        }
    }
}
```

Calculated percentiles will only represent the requests of the main load cycle and won't include write requests sent during the initial data allocation. The [graphs in Monitoring](../reference/observability/metrics/grafana-dashboards.md) should be of interest, for example, they allow to trace the request latency degradation caused by the increasing load.
