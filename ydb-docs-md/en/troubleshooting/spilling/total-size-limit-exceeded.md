---
title: "Total Size Limit Exceeded"
url: "https://ydb.tech/docs/en/troubleshooting/spilling/total-size-limit-exceeded?version=v26.1"
doc_path: "en/troubleshooting/spilling/total-size-limit-exceeded"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/spilling/total-size-limit-exceeded.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/spilling/total-size-limit-exceeded.md"
description: "The maximum total size of spilling files has been exceeded (parameter max_total_size ). This occurs when the total size of all spilling files reaches the config"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Total Size Limit Exceeded

The maximum total size of spilling files has been exceeded (parameter [`max_total_size`](../../reference/configuration/table_service_config.md#local-file-config-max-total-size)). This occurs when the total size of all spilling files reaches the configured limit, preventing new spilling operations.

## Diagnostics

Check the current spilling usage:

- Monitor the total size of spilling files in the spilling directory.
- Check the current value of the `max_total_size` parameter.
- Review available disk space in the spilling directory location.
- Check if there are any stuck spilling files that should have been cleaned up.

## Recommendations

To resolve this issue:

1. **Increase the spilling size limit:**

   - If there is sufficient free disk space, increase the [`max_total_size`](../../reference/configuration/table_service_config.md#local-file-config-max-total-size) parameter in the configuration.
   - Increase the value by 20–50% from the current one.

2. **Expand disk space:**

   - If there is insufficient free disk space, add additional disk space.
   - Ensure that the spilling directory is located on a disk with sufficient capacity.

3. **Try repeating the query:**

   - Wait for other resource-intensive queries to complete.
   - Repeat the query execution during less busy times.
