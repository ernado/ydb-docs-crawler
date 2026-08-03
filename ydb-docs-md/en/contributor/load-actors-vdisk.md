---
title: "VDiskLoad"
url: "https://ydb.tech/docs/en/contributor/load-actors-vdisk?version=v26.1"
doc_path: "en/contributor/load-actors-vdisk"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-vdisk.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-vdisk.md"
description: "Generates a write-only load on the VDisk. Simulates a Distributed Storage Proxy. The test outputs the VDisk write performance in operations per second."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# VDiskLoad

Generates a write-only load on the VDisk. Simulates a Distributed Storage Proxy. The test outputs the VDisk write performance in operations per second.

## Actor parameters {#options}

The basic actor parameters are described below. For the full list of parameters, see the [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) file in the YDB Git repository.

| Parameter | Description |
| --- | --- |
| `VDiskId` | Parameters of the VDisk used to generate load.<br>- `GroupID`: Group ID.<br>- `GroupGeneration`: Group generation.<br>- `Ring`: Group ring ID.<br>- `Domain`: Ring fail domain ID.<br>- `VDisk`: Index of the VDisk in the fail domain. |
| `GroupInfo` | Description of the group hosting the loaded VDisk (of the appropriate generation). |
| `TabletId` | ID of the tablet that generates the load. It must be unique for each load actor. |
| `Channel` | ID of the channel inside the tablet that will be specified in the BLOB write and garbage collection commands. |
| `DurationSeconds` | The total test time in seconds; when it expires, the load stops automatically. |
| `WriteIntervals` | Setting up the [parameters for probabilistic distribution](load-actors-vdisk.md#params) of intervals between the records. |
| `WriteSizes` | Size of the data to write. It is selected randomly for each request from the `Min`-`Max` range. You can set multiple `WriteSizes` ranges, in which case a value from a specific range will be selected based on its `Weight`. |
| `InFlightPutsMax` | Maximum number of concurrent BLOB write queries against the VDisk (TEvVPut queries); if omitted, the number of queries is unlimited. |
| `InFlightPutBytesMax` | Maximum number of bytes in the concurrent BLOB write queries against the VDisk (TEvVPut-requests). |
| `PutHandleClass` | Class of data writes to the disk subsystem. If the `TabletLog` value is set, the write operation has the highest priority. |
| `BarrierAdvanceIntervals` | Setting up the [parameters for probabilistic distribution](load-actors-vdisk.md#params) of intervals between the advance of the garbage collection barrier and the write step. |
| `StepDistance` | Distance between the currently written step `Gen:Step` of the BLOB and its currently collected step. The higher is the value, the more data is stored. Data is written from `Step = X` and deleted from all the BLOBs where `Step = X - StepDistance`. The `Step` is periodically incremented by one (with the `BarrierAdvanceIntervals` period). |

### Parameters of probabilistic distribution {#params}

An interval written as a repeated `TIntervalInfo` field is calculated by the following algorithm:

- An element from the `TIntervalInfo` array is selected at random with the probability proportionate to its weight.
- For an element of the `TIntervalUniform` type, the value is chosen with equal probability in the range Min-Max. `Min-Max` (if `MinMs/MaxMs` is used, the value is in milliseconds; if `MinUs/MaxUs` is used, the value is in microseconds).
- For an element of the `TIntervalPoisson` type, the interval is selected using the formula `Min(log(-x / Frequency), MaxIntervalMs)`, where `x` is a random value in the interval `[0, 1]`. As a result, the intervals follow the Poisson distribution with the given `Frequency`, but with the interval within `MaxIntervalMs`.

A similar approach is used for the probabilistic distribution of the size of the written data. However, in this case, only the data size follows a uniform probability distribution, within the interval `[Min, Max]`.
