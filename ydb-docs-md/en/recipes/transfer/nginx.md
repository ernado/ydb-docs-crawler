---
title: "Transfer — streaming NGINX access logs to a table"
url: "https://ydb.tech/docs/en/recipes/transfer/nginx?version=v26.1"
doc_path: "en/recipes/transfer/nginx"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/transfer/nginx.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/transfer/nginx.md"
description: "This guide explains how to set up streaming of NGINX access logs to a YDB table for further analysis. It covers the default NGINX access log format. To learn mo"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Transfer — streaming NGINX access logs to a table

This guide explains how to set up streaming of NGINX access logs to a YDB [table](../../concepts/datamodel/table.md) for further analysis. It covers the default NGINX access log format. To learn more about the NGINX log format and how to configure it, see the [NGINX documentation](https://docs.nginx.com/nginx/admin-guide/monitoring/logging/#set-up-the-access-log).

The default NGINX access log format is as follows:

```txt
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
```

Example:

```txt
::1 - - [01/Sep/2025:15:02:47 +0500] "GET /favicon.ico HTTP/1.1" 404 181 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36"
::1 - - [01/Sep/2025:15:02:51 +0500] "GET / HTTP/1.1" 200 409 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36"
::1 - - [01/Sep/2025:15:02:51 +0500] "GET /favicon.ico HTTP/1.1" 404 181 "http://localhost/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36"
```

This guide covers the following steps:

- [creating a table](nginx.md#step1) to write the data to;
- [creating the transfer](nginx.md#step2);
- [verifying the table contents](nginx.md#step3).

## Prerequisites

To complete the examples in this guide, it needs:

- A YDB cluster, version 25.2 or later. For instructions on how to install a single-node YDB cluster, see the [guide](../../quickstart.md). For recommendations on deploying YDB for production use, see this [guide](../../devops/deployment-options/index.md).
- An installed [NGINX HTTP server](https://nginx.org/) with access logging enabled, or access to NGINX access logs from another server.
- A configured process to stream NGINX access logs from a file to the `transfer_recipe/access_log_topic` topic. For example, you can use [Kafka Connect](../../reference/kafka-api/connect/index.md) [configured](../../reference/kafka-api/connect/connect-examples.md#file-to-topic) to stream data from a file to a topic.

## Step 1. Create a table {#step1}

Create a [table](../../concepts/datamodel/table.md) that will receive data from the `transfer_recipe/access_log_topic` topic. You can do this using a [YQL query](../../yql/reference/syntax/create_table/index.md):

```yql
CREATE TABLE `transfer_recipe/access_log` (
  partition Uint32 NOT NULL,
  offset Uint64 NOT NULL,
  line Uint64 NOT NULL,
  remote_addr String,
  remote_user String,
  time_local Timestamp,
  request_method String,
  request_path String,
  request_protocol String,
  status Uint32,
  body_bytes_sent Uint64,
  http_referer String,
  http_user_agent Utf8,
  PRIMARY KEY (partition, offset, line)
);
```

The `transfer_recipe/access_log` table has three service columns:

- `partition` — the ID of the topic [partition](../../concepts/glossary.md#partition) the message was received from;
- `offset` — [the sequence number](../../concepts/glossary.md#offset) that identifies the message within its partition;
- `line` — the sequence number of the log line within the message.

Together the `partition`, `offset` and `line` columns uniquely identify each line from the access log file.

If you need to store access log data for a limited time, you can configure the [automatic deletion](../../concepts/ttl.md) of old table rows. For example, to set a retention period of 24 hours, you can use a [YQL query](../../yql/reference/recipes/ttl.md):

```yql
ALTER TABLE `transfer_recipe/access_log` SET (TTL = Interval("PT24H") ON time_local);
```

## Step 2. Create a transfer {#step2}

After creating the topic and the table, you need to create a data [transfer](../../concepts/transfer.md) that will move messages from the topic to the table. You can do this using a [YQL query](../../yql/reference/syntax/create-transfer.md):

```yql
$transformation_lambda = ($msg) -> {
    -- Function to convert a log line into a table row
    $line_lambda = ($line) -> {
        -- First, split the line by the " (double quote) character to separate strings that may contain spaces.
        -- The strings themselves cannot contain double quotes; instead, they are replaced with the \x22 character sequence.
        $parts = String::SplitToList($line.1, '"');
        -- Split each resulting part that isn't a quoted string by spaces.
        $info_parts = String::SplitToList($parts[0], " ");
        $request_parts = String::SplitToList($parts[1], " ");
        $response_parts = String::SplitToList($parts[2], " ");
        -- Convert the date to the Datetime type
        $dateParser = DateTime::Parse("%d/%b/%Y:%H:%M:%S");
        $date = $dateParser(SUBSTRING($info_parts[3], 1));

        -- Return a structure where each named field corresponds to a table column.
        -- Important: The data types of the named fields must match the data types of the table columns. For example, if a column is of type Uint32,
        -- the value of the named field must also be of type Uint32. Otherwise, an explicit CAST is required.
        -- Values for NOT NULL columns must be extracted from optional types using the Unwrap function.
        return <|
            partition: $msg._partition,
            offset: $msg._offset,
            line: $line.0,
            remote_addr: $info_parts[0],
            remote_user: $info_parts[2],
            time_local: DateTime::MakeTimestamp($date),
            request_method: $request_parts[0],
            request_path: $request_parts[1],
            request_protocol: $request_parts[2],
            status: CAST($response_parts[1] AS Uint32),
            body_bytes_sent: CAST($response_parts[2] AS Uint64),
            http_referer: $parts[3],
            http_user_agent: CAST(String::CgiUnescape($parts[5]) AS Utf8) -- Explicitly cast to Utf8, because the http_user_agent column is of type Utf8, not String
        |>;
    };

    $split = String::SplitToList($msg._data, "\n"); -- If a message contains multiple log lines, split it into individual lines
    $lines = ListFilter($split, ($line) -> { -- Filter out empty lines, which can be caused by a trailing \n character
        return LENGTH($line) > 0;
    });

    -- Convert each access log line into a table row
    return ListMap(ListEnumerate($lines), $line_lambda);
};

CREATE TRANSFER `transfer_recipe/access_log_transfer`
  FROM `transfer_recipe/access_log_topic` TO `transfer_recipe/access_log`
  USING $transformation_lambda;
```

In this example:

- `$transformation_lambda` - a transformation rule for converting a topic message into table columns. Each access log line within the message is processed individually using `line_transformation_lambda`;
- `$line_lambda` - a transformation rule for converting a single access log line into a table row;
- `$msg` - variable that contains the topic message being processed.

## Step 3. Verify the table contents {#step3}

After writing messages to the `transfer_recipe/access_log_topic` topic, records will appear in the `transfer_recipe/access_log` table after a short delay. You can verify this using a [YQL query](../../yql/reference/syntax/select/index.md):

```yql
SELECT *
FROM `transfer_recipe/access_log`;
```

Query result:

| # | partition | offset | line | remote_addr | remote_user | time_local | request_method | request_path | request_protocol | status | body_bytes_sent | http_referer | http_user_agent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 0 | ::1 | - | 2025-09-01T15:02:51.000000Z | GET | /favicon.ico | HTTP/1.1 | 404 | 181 | `http://localhost/` | Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36 |
| 2 | 0 | 1 | 0 | ::1 | - | 2025-09-01T15:02:51.000000Z | GET | / | HTTP/1.1 | 200 | 409 | - | Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36 |
| 3 | 0 | 0 | 0 | ::1 | - | 2025-09-01T15:02:47.000000Z | GET | /favicon.ico | HTTP/1.1 | 404 | 181 | - | Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36 |

Rows are not added to the table for each message received from the topic; instead, they are buffered and inserted in batches. By default, data is written to the table every 60 seconds or when the volume of accumulated data reaches 8 MB. These parameters can be explicitly configured when [creating](../../yql/reference/syntax/create-transfer.md) a transfer or [modified](../../yql/reference/syntax/alter-transfer.md) later.

## Conclusion

This guide demonstrates how to stream NGINX access logs to a YDB table. You can process logs of any other text format in a similar way: create a table to store the required data from the log, and write a [lambda function](../../yql/reference/syntax/expressions.md#lambda) to correctly transform the log lines into table rows.

## See Also

- [Data transfer](../../concepts/transfer.md)
- [Transfer — quick start](quickstart.md)
- [Lambda function](../../yql/reference/syntax/expressions.md#lambda)
- [CREATE TABLE](../../yql/reference/syntax/create_table/index.md)
- [CREATE TOPIC](../../yql/reference/syntax/create-topic.md)
- [CREATE TRANSFER](../../yql/reference/syntax/create-transfer.md)
- [UNWRAP function](../../yql/reference/builtins/basic.md#unwrap)
- [COALESCE function](../../yql/reference/builtins/basic.md#coalesce)
