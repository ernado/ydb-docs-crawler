---
title: "KeyValueLoad"
url: "https://ydb.tech/docs/en/contributor/load-actors-key-value?version=v26.1"
doc_path: "en/contributor/load-actors-key-value"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-key-value.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-key-value.md"
description: "Loads a key-value tablet. Actor configuration."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# KeyValueLoad

Loads a key-value tablet.

## Actor configuration {#options}

```proto
message TKeyValueLoad {
    message TWorkerConfig {
        optional string KeyPrefix = 1;
        optional uint32 MaxInFlight = 2;
        optional uint32 Size = 11; // data size, bytes
        optional bool IsInline = 9 [default = false];
        optional uint32 LoopAtKeyCount = 10 [default = 0]; // 0 means "do not loop"
    }
    optional uint64 Tag = 1;
    optional uint64 TargetTabletId = 2;
    optional uint32 DurationSeconds = 5;
    repeated TWorkerConfig Workers = 7;
}
```
