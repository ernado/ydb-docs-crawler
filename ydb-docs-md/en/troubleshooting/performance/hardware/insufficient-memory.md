---
title: "Insufficient memory (RAM)"
url: "https://ydb.tech/docs/en/troubleshooting/performance/hardware/insufficient-memory?version=v26.1"
doc_path: "en/troubleshooting/performance/hardware/insufficient-memory"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/hardware/insufficient-memory.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/hardware/insufficient-memory.md"
description: "If swap (paging of anonymous memory) is disabled on the server running YDB, insufficient memory activates another kernel feature called the OOM killer, which te"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Insufficient memory (RAM)

If [swap](https://en.wikipedia.org/wiki/Memory_paging#Unix_and_Unix-like_systems) (paging of anonymous memory) is disabled on the server running YDB, insufficient memory activates another kernel feature called the [OOM killer](https://en.wikipedia.org/wiki/Out_of_memory), which terminates the most memory-intensive processes (often the database itself). This feature also interacts with [cgroups](https://en.wikipedia.org/wiki/Cgroups) if multiple cgroups are configured.

If swap is enabled, insufficient memory may cause the database to rely heavily on disk I/O, which is significantly slower than accessing data directly from memory.

> [!WARNING]
> If YDB nodes are running on servers with swap enabled, disable it. YDB is a distributed system, so if a node restarts due to lack of memory, the client will simply connect to another node and continue accessing data as if nothing happened. Swap would allow the query to continue on the same node but with degraded performance from increased disk I/O, which is generally less desirable.

Even though the reasons and mechanics of performance degradation due to insufficient memory might differ, the symptoms of increased latencies during query execution and data retrieval are similar in all cases.

Additionally, which components within the YDB process consume memory may also be significant.

## Diagnostics

1. Determine whether any YDB nodes recently restarted for unknown reasons. Exclude cases of YDB version upgrades and other planned maintenance. This could reveal nodes terminated by OOM killer and restarted by `systemd`.

   1. Open [Embedded UI](../../../reference/embedded-ui/index.md).

   2. On the **Nodes** tab, look for nodes that have low uptime.

   3. Chose a recently restarted node and log in to the server hosting it. Run the `dmesg` command to check if the kernel has recently activated the OOM killer mechanism.

      Look for the lines like this:

      ```plaintext
      [ 2203.393223] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=user.slice,mems_allowed=0,global_oom,task_memcg=/user.slice/user-1000.slice/session-1.scope,task=ydb,pid=1332,uid=1000
      [ 2203.393263] Out of memory: Killed process 1332 (ydb) total-vm:14219904kB, anon-rss:1771156kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:4736kB oom_score_adj:0
      ```

   Additionally, review the `ydbd` logs for relevant details.

2. Determine whether memory usage reached 100% of capacity.

   1. Open the **[DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** dashboard in Grafana.
   2. Analyze the charts in the **Memory** section.

3. Determine whether the user load on YDB has increased. Analyze the following charts on the **[DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** dashboard in Grafana:

   - **Requests** chart
   - **Request size** chart
   - **Response size** chart

4. Determine whether new releases or data access changes occurred in your applications working with YDB.

## Recommendation

Consider the following solutions for addressing insufficient memory:

- If the load on YDB has increased due to new usage patterns or increased query rate, try optimizing the application to reduce the load on YDB or add more YDB nodes.
- If the load on YDB has not changed but nodes are still restarting, consider adding more YDB nodes or raising the hard memory limit for the nodes. For more information about memory management in YDB, see [memory_controller_config](../../../reference/configuration/memory_controller_config.md).
