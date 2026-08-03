---
title: "Stop"
url: "https://ydb.tech/docs/en/contributor/load-actors-stop?version=v26.1"
doc_path: "en/contributor/load-actors-stop"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/load-actors-stop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/load-actors-stop.md"
description: "Using this command, you can stop either entire load or only the specified part of it. Actor parameters Parameter Description. Tag."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Stop

Using this command, you can stop either entire load or only the specified part of it.

## Actor parameters {#options}

| Parameter | Description |
| --- | --- |
| `Tag` | Tag of the load actor to stop. You can view the tag in the cluster Embedded UI. |
| `RemoveAllTags` | If this parameter value is set to `True`, all the load actors are stopped. |

## Examples

The command below stops the load tagged `123`:

```proto
Stop: {
    Tag: 123
}
```

To stop the entire load, run this command:

```proto
Stop: {
    RemoveAllTags: true
}
```
