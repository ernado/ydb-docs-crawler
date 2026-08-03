---
title: "Known issues"
url: "https://ydb.tech/docs/en/faq/known-issues?version=v26.1"
doc_path: "en/faq/known-issues"
version: "v26.1"
lang: "en"
source_path: "en/core/faq/known-issues.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/faq/known-issues.md"
description: "Known issues Table partitions are not merging when autopartitioning is enabled."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Known issues

## Table partitions are not merging when autopartitioning is enabled {#table-partitions-are-not-merging}

For tables created in earlier versions of YDB, the autopartitioning mechanism does not merge partitions even when merge conditions based on load or size are met. This can result in an excessive number of partitions in the table.

This issue is specific to tables that meet the following two criteria:

- The table was created on a YDB cluster prior to version 22.2.
- The table had no minimum partition count value set, either at creation time or afterwards.

To resolve the issue, explicitly set a minimum partition count value for the table. For example, use the [AUTO_PARTITIONING_MIN_PARTITIONS_COUNT](../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) parameter:

```yql
ALTER TABLE `my_table` SET (AUTO_PARTITIONING_MIN_PARTITIONS_COUNT = 1);
```
