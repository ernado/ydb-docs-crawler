---
title: "Can not run operation"
url: "https://ydb.tech/docs/en/troubleshooting/spilling/can-not-run-operation?version=v26.1"
doc_path: "en/troubleshooting/spilling/can-not-run-operation"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/spilling/can-not-run-operation.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/spilling/can-not-run-operation.md"
description: "I/O thread pool operation queue overflow. This occurs when the spilling I/O thread pool queue is full and cannot accept new operations, causing spilling operati"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# Can not run operation

I/O thread pool operation queue overflow. This occurs when the spilling I/O thread pool queue is full and cannot accept new operations, causing spilling operations to fail.

## Diagnostics

Check the I/O thread pool configuration and usage:

- Check the `queue_size` parameter in `io_thread_pool` configuration
- Review the `workers_count` parameter for the I/O thread pool

## Recommendations

To resolve this issue:

1. **Increase queue size:**

   - Increase `queue_size` in `io_thread_pool` configuration
   - This allows more operations to be queued before overflow occurs

2. **Increase worker threads:**

   - Increase `workers_count` for faster operation processing
   - More worker threads can process operations faster, reducing queue buildup

> [!NOTE]
> The I/O thread pool processes spilling operations asynchronously. If the queue overflows, new spilling operations will fail until space becomes available.
