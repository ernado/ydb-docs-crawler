---
title: "ru/yql/reference/syntax/commit"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/commit?version=v26.1"
doc_path: "ru/yql/reference/syntax/commit"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/commit.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/commit.md"
description: "COMMIT. По умолчанию весь YQL запрос выполняется в рамках одной транзакции и независимые его части внутри выполняются по возможности параллельно."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ru/yql/reference/syntax/commit

## COMMIT

По умолчанию весь YQL запрос выполняется в рамках одной транзакции и независимые его части внутри выполняются по возможности параллельно.  
 С помощью ключевого слова `COMMIT;` можно добавить барьер в процесс выполнения, чтобы отложить выполнение идущих следом выражений до тех пор, пока не выполнятся все предшествующие.

Чтобы коммит выполнялся аналогичным образом автоматически после каждого выражения в запросе, можно использовать `PRAGMA autocommit;`.

### Примеры {#primery}

```yql
INSERT INTO result1 SELECT * FROM my_table;
INSERT INTO result2 SELECT * FROM my_table;
COMMIT;
-- В result2 уже будет содержимое SELECT со второй строки:
INSERT INTO result3 SELECT * FROM result2;
```
