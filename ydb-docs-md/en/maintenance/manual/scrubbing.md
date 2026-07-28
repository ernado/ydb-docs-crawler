---
title: "Enabling/disabling Scrubbing"
url: "https://ydb.tech/docs/en/maintenance/manual/scrubbing?version=v26.1"
doc_path: "en/maintenance/manual/scrubbing"
version: "v26.1"
lang: "en"
source_path: "en/core/maintenance/manual/scrubbing.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/maintenance/manual/scrubbing.md"
description: "Scrubbing is a process that reads data, checks its integrity, and restores it if needed. The process is run by default. The interval between completing a scrub"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Enabling/disabling Scrubbing

Scrubbing is a process that reads data, checks its integrity, and restores it if needed. The process is run by default. The interval between completing a scrub and starting the next one is 1 month. You can change the interval using [YDB DSTool](../../reference/ydb-dstool/index.md). The process checks data that was accessed before the previous scrub. Scrubbing is started and stopped for the entire YDB cluster. Scrubbing is performed in the background without overloading the system.

To set a 48-hour interval, run the command:

```bash
ydb-dstool -e <bs_endpoint> cluster set --scrub-periodicity 48h
```

You can also set the maximum number of cluster disks to be scrubbed at a time. For example, to only scrub one disk at a time, run the command:

```bash
ydb-dstool -e <bs_endpoint> cluster set --max-scrubbed-disks-at-once
```

To stop cluster scrubbing, run the command:

```bash
ydb-dstool -e <bs_endpoint> cluster set --scrub-periodicity disable
```
