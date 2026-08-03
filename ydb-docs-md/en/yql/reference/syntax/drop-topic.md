---
title: "DROP TOPIC"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-topic?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-topic"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-topic.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-topic.md"
description: "DROP TOPIC deletes the specified topic. Syntax. DROP TOPIC <topic_path>; Examples. The following command will delete the topic named my_topic:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP TOPIC

`DROP TOPIC` deletes the specified [topic](../../../concepts/datamodel/topic.md).

## Syntax

```yql
DROP TOPIC <topic_path>;
```

## Examples

The following command will delete the topic named `my_topic`:

```yql
DROP TOPIC my_topic;
```

## See also

- [CREATE TOPIC](create-topic.md)
- [ALTER TOPIC](alter-topic.md)
