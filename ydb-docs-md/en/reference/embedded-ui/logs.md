---
title: "Logs"
url: "https://ydb.tech/docs/en/reference/embedded-ui/logs?version=v26.1"
doc_path: "en/reference/embedded-ui/logs"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/embedded-ui/logs.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/embedded-ui/logs.md"
description: "Logging levels Level Numeric value Value. TRACE. 8. Very detailed debugging information. DEBUG. 7. Debugging information for developers. INFO. 6."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Logs

## Logging levels {#log_levels}

| Level | Numeric value | Value |
| --- | --- | --- |
| TRACE | 8 | Very detailed debugging information. |
| DEBUG | 7 | Debugging information for developers. |
| INFO | 6 | Debugging information for collecting statistics. |
| NOTICE | 5 | An event essential for the system or the user has occurred. |
| WARN | 4 | This is a warning, it should be responded to and fixed unless it's temporary. |
| ERROR | 3 | A non-critical error. |
| CRIT | 2 | A critical state. |
| ALERT | 1 | System degradation is possible, system components may fail. |
| EMERG | 0 | System outage (for example, cluster failure) is possible. |

The logging level for different YDB components can be configured individually. For each component, either an explicitly set value or a default logging level value can be applied. The default logging level value can also be changed.

## Changing the logging level {#change_log_level}

To change the logging level:

1. Follow the link in the format

   ```text
   http://<endpoint>:8765/cms
   ```

   The `Cluster Management System` page opens.

2. On the **Configs** tab, click on the `LogConfigItems` line. The `Create new item` button will show up along with a list of already created configuration elements.

3. Click `Create new item` to create a new configuration item (or click the pencil button to edit a previously created item).

4. To change the default logging level, select the desired logging level from the `Level` drop-down list under `Default log settings`. The default global setting is `NOTICE`.

5. To change the logging level for individual components, use the table under `Component log settings`. In the line with the name of the component whose logging level you want to change, in the `Component` column, select the desired logging level from the drop-down list in the `Log level` column.

6. To save changes, click `Submit`
