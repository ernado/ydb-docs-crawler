---
title: "Spilling Troubleshooting"
url: "https://ydb.tech/docs/en/troubleshooting/spilling/?version=v26.1"
doc_path: "en/troubleshooting/spilling/"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/spilling/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/spilling/index.md"
description: "This section provides troubleshooting information for common spilling issues in YDB. Spilling is a memory management mechanism that temporarily saves intermedia"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Spilling Troubleshooting

This section provides troubleshooting information for common spilling issues in YDB. Spilling is a memory management mechanism that temporarily saves intermediate computation data to disk when the system runs out of RAM. These errors can occur during query execution when the system attempts to use spilling functionality and can be observed in logs and query responses.

## Common Issues

- [Permission denied](permission-denied.md) - Insufficient access permissions to the spilling directory
- [Spilling Service not started](service-not-started.md) - Attempt to use spilling when the Spilling Service is disabled
- [Total size limit exceeded](total-size-limit-exceeded.md) - Maximum total size of spilling files exceeded
- [Can not run operation](can-not-run-operation.md) - I/O thread pool operation queue overflow

## See Also

- [Spilling Configuration](../../reference/configuration/table_service_config.md)
- [Spilling Concept](../../concepts/query_execution/spilling.md)
- [Memory Controller Configuration](../../reference/configuration/memory_controller_config.md)
- [YDB Monitoring](../../devops/observability/monitoring.md)
- [Performance Diagnostics](../performance/index.md)
