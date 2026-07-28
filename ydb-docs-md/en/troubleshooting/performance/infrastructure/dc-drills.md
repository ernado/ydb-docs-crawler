---
title: "Data center maintenance and drills"
url: "https://ydb.tech/docs/en/troubleshooting/performance/infrastructure/dc-drills?version=v26.1"
doc_path: "en/troubleshooting/performance/infrastructure/dc-drills"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/infrastructure/dc-drills.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/infrastructure/dc-drills.md"
description: "Planned maintenance or drills, exercises conducted to prepare personnel for potential emergencies or outages, can also affect query performance. Depending on th"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Data center maintenance and drills

Planned maintenance or drills, exercises conducted to prepare personnel for potential emergencies or outages, can also affect query performance. Depending on the maintenance scope or drill scenario, some YDB nodes might become unavailable, which leads to the same impact as an [outage](dc-outage.md).

## Diagnostics

Check the planned maintenance and drills schedules to see if their timelines match with observed performance issues, otherwise, check the [datacenter outage recommendations](dc-outage.md).

## Recommendations

Contact the person responsible for the current maintenance or drill to discuss whether the performance impact is severe enough for it to be finished/canceled early, if possible.
