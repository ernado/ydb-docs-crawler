---
title: "Getting information about schema objects"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/scheme-describe?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/scheme-describe"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/scheme-describe.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/scheme-describe.md"
description: "Getting information about schema objects. Get information about a schema object: ydb scheme describe episodes --stats. Result:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Getting information about schema objects

Get information about a [schema object](../../../concepts/glossary.md#scheme-object):

```bash
ydb scheme describe episodes --stats
```

Result:

```text
<table> episodes

┌────────────┬─────────┬────────┬─────┐
| Name       | Type    | Family | Key |
├────────────┼─────────┼────────┼─────┤
| air_date   | Uint64? |        |     |
| episode_id | Uint64? |        | K2  |
| season_id  | Uint64? |        | K1  |
| series_id  | Uint64? |        | K0  |
| title      | Utf8?   |        |     |
└────────────┴─────────┴────────┴─────┘

Storage settings:
Internal channel 0 commit log storage pool: ssd
Internal channel 1 commit log storage pool: ssd
Store large values in "external blobs": false

Column families:
┌─────────┬──────┬─────────────┬────────────────┐
| Name    | Data | Compression | Keep in memory |
├─────────┼──────┼─────────────┼────────────────┤
| default | ssd  | None        |                |
└─────────┴──────┴─────────────┴────────────────┘

Auto partitioning settings:
Partitioning by size: true
Partitioning by load: false
Preferred partition size (Mb): 2048

Table stats:
Partitions count: 1
Approximate number of rows: 70
Approximate size of table: 11.05 Kb
Last modified: Thu, 17 Jun 2021 11:01:06 UTC
Created: Thu, 17 Jun 2021 11:00:29 UTC
```
