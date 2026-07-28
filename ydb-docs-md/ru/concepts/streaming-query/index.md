---
title: "Потоковая обработка данных"
url: "https://ydb.tech/docs/ru/concepts/streaming-query/?version=v26.1"
doc_path: "ru/concepts/streaming-query/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/streaming-query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/streaming-query/index.md"
description: "Данный раздел описывает ключевые концепции потоковой обработки ( stream processing ) в YDB:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Потоковая обработка данных

Данный раздел описывает ключевые концепции потоковой обработки ([stream processing](https://en.wikipedia.org/wiki/Stream_processing)) в YDB:

- [Потоковые запросы](streaming-query.md) — тип запросов для непрерывной обработки входящих событий. Описываются источники и приёмники данных, гарантии доставки, ограничения и управление запросами.
- [Watermarks](watermarks.md) — механизм отслеживания прогресса обработки событий по времени.
