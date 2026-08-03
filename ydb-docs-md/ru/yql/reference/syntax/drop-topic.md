---
title: "DROP TOPIC"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-topic?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-topic"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-topic.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-topic.md"
description: "С помощью оператора DROP TOPIC можно удалить топик. Синтаксис. DROP TOPIC topic_path; Примеры. Следующая команда удалит топик с именем my_topic:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP TOPIC

С помощью оператора `DROP TOPIC` можно удалить [топик](../../../concepts/datamodel/topic.md).

## Синтаксис {#sintaksis}

```yql
DROP TOPIC topic_path;
```

## Примеры {#primery}

Следующая команда удалит топик с именем `my_topic`:

```yql
DROP TOPIC `my_topic`;
```

## См. также {#sm-takzhe}

- [CREATE TOPIC](create-topic.md)
- [ALTER TOPIC](alter-topic.md)
