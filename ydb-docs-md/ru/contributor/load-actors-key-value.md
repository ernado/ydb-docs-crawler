---
title: "KeyValueLoad"
url: "https://ydb.tech/docs/ru/contributor/load-actors-key-value?version=v26.1"
doc_path: "ru/contributor/load-actors-key-value"
version: "v26.1"
lang: "ru"
source_path: "ru/core/contributor/load-actors-key-value.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/contributor/load-actors-key-value.md"
description: "Нагружает Key-value таблетку. Конфигурация актора."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# KeyValueLoad

Нагружает Key-value таблетку.

## Конфигурация актора {#options}

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

> [!TIP]
> **Хотите присоединиться к команде разработки YDB?**
>
> Ознакомьтесь с разделами о [команде YDB и открытых вакансиях](https://ydb.tech/ru/careers/), а также о [возможностях для студентов](https://ydb.tech/ru/students/).
