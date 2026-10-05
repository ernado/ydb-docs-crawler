---
title: "Потоковая обработка данных"
url: "https://ydb.tech/docs/ru/concepts/streaming-query/?version=v26.1"
doc_path: "ru/concepts/streaming-query/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/streaming-query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/streaming-query/index.md"
description: "Данный раздел описывает ключевые концепции потоковой обработки ( stream processing ) в YDB:"
revision: "259414a47522df8faa233e3f6fd5c97bc5325d93"
---

# Потоковая обработка данных

Данный раздел описывает ключевые концепции потоковой обработки ([stream processing](https://en.wikipedia.org/wiki/Stream_processing)) в YDB:

- [Потоковые запросы](streaming-query.md) — тип запросов для непрерывной обработки входящих событий. Описываются источники и приёмники данных, гарантии доставки, ограничения и управление запросами.
- [Watermarks](watermarks.md) — механизм отслеживания прогресса обработки событий по времени.
