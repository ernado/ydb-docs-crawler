---
title: "MemoryLoad"
url: "https://ydb.tech/docs/en/contributor/load-actors-memory?version=v26.1"
doc_path: "en/contributor/load-actors-memory"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-memory.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-memory.md"
description: "Allocates memory blocks of the specified size at certain intervals. After the load is removed, the allocated memory is released. Using this actor, you can test"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# MemoryLoad

Allocates memory blocks of the specified size at certain intervals. After the load is removed, the allocated memory is released. Using this actor, you can test the logic, e.g., whether a certain trigger is fired when the [RSS](https://en.wikipedia.org/wiki/Resident_set_size) limit is reached.

> [!NOTE]
> This ad-hoc actor is used for testing specific functionality. This is not a load actor. It is designed to check whether something works properly.

## Actor parameters {#options}

| Parameter | Description |
| --- | --- |
| `DurationSeconds` | Load duration in seconds. |
| `BlockSize` | Allocated block size in bytes. |
| `IntervalUs` | Interval between block allocations in microseconds. |

## Examples

The following actor allocates blocks of `1048576` bytes every `9000000` microseconds during `3600` seconds and takes up 32 GB while running:

```proto
MemoryLoad: {
    DurationSeconds: 3600
    BlockSize: 1048576
    IntervalUs: 9000000
}
```
