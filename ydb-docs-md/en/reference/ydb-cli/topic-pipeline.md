---
title: "Message pipeline processing"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-pipeline?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-pipeline"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-pipeline.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-pipeline.md"
description: "The use of the topic read and topic write commands with standard I/O devices and support for reading messages in streaming mode lets you build full-featured int"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Message pipeline processing

The use of the `topic read` and `topic write` commands with standard I/O devices and support for reading messages in streaming mode lets you build full-featured integration scenarios with message transfer across topics and their conversion. This section describes a number of these scenarios.

- Transferring a single message from `topic1` in the `quickstart` database to `topic2` in `db2`, waiting for it to appear in the source topic

  ```bash
  ydb -p quickstart topic read topic1 -c c1 -w | ydb -p db2 topic write topic2
  ```

- Transferring all one-line messages that appear in `topic1` in the `quickstart` database to `topic2` in `db2` in background mode. You can use this scenario if it's guaranteed that there are no `0x0A` bytes (newline) in source messages.

  ```bash
  ydb -p quickstart topic read topic1 -c c1 --format newline-delimited -w | \
  ydb -p db2 topic write topic2 --format newline-delimited
  ```

- Transferring an exact binary copy of all messages that appear in `topic1` in the `quickstart` database to `topic2` in `db2` in background mode with base64-encoding of messages in the transfer stream.

  ```bash
  ydb -p quickstart topic read topic1 -c c1 --format newline-delimited -w --transform base64 | \
  ydb -p quickstart topic write topic2 --format newline-delimited --transform base64
  ```

- Transferring a limited batch of one-line messages filtered by the `ERROR` substring

  ```bash
  ydb -p quickstart topic read topic1 -c c1 --format newline-delimited | \
  grep ERROR | \
  ydb -p db2 topic write topic2 --format newline-delimited
  ```

- Writing YQL query results as messages to `topic1`

  ```bash
  ydb -p quickstart yql -s "select * from series" --format json-unicode | \
  ydb -p quickstart topic write topic1 --format newline-delimited
  ```

## Running an SQL query with the transmission of messages from the topic as parameters {#example-read-to-yql-param}

- Running a YQL, passing each message read from `topic1` as a parameter

  ```bash
  ydb -p quickstart topic read topic1 -c c1 --format newline-delimited -w | \
  ydb -p quickstart sql -s 'declare $s as String;select Len($s) as Bytes' \
  --input-framing newline-delimited --input-param-name s --input-format raw
  ```

- Running a YQL query involving adaptive batching of parameters from messages read from `topic1`

  ```bash
  ydb -p quickstart topic read topic1 -c c1 --format newline-delimited -w | \
  ydb -p quickstart sql \
  -s 'declare $s as List<String>;select ListLength($s) as Count, $s as Items' \
  --input-framing newline-delimited --input-param-name s --input-format raw \
  --input-batch adaptive
  ```
