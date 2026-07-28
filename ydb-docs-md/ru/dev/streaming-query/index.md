---
title: "Потоковые запросы"
url: "https://ydb.tech/docs/ru/dev/streaming-query/?version=v26.1"
doc_path: "ru/dev/streaming-query/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/streaming-query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/streaming-query/index.md"
description: "Практические аспекты работы с потоковыми запросами: Типичные шаблоны — минимальные примеры для быстрого старта."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Потоковые запросы

Практические аспекты работы с [потоковыми запросами](../../concepts/glossary.md#streaming-query):

- [Типичные шаблоны](patterns.md) — минимальные примеры для быстрого старта
- [Запись в таблицы](table-writing.md) — как потоковые запросы позволяют записывать данные в таблицы YDB в режиме реального времени.
- [Обогащение данных](enrichment.md) — способы обогащения данных в потоке с использованием внешних источников.
- [Форматы данных при чтении/записи топиков](streaming-query-formats.md) — поддерживаемые форматы данных при работе с топиками, примеры их использования.
- [Гарантии доставки данных](guarantees.md) — уровень гарантий, наблюдаемые аномалии при оконной агрегации и рекомендации.
- [Чекпоинты](checkpoints.md) — механизм сохранения состояния обработки потока для обеспечения отказоустойчивости и возможности восстановления.
- [Watermarks](watermarks.md) — механизм отслеживания прогресса времени в потоке данных.

## См. также {#sm-takzhe}

- [Рецепты работы с потоковыми запросами](../../recipes/streaming_queries/index.md)
- [Описание потоковых запросов](../../concepts/streaming-query/streaming-query.md)
