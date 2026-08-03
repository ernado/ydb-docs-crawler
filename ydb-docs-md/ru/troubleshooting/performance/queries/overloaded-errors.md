---
title: "Ошибки «overloaded»"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/queries/overloaded-errors?version=v26.1"
doc_path: "ru/troubleshooting/performance/queries/overloaded-errors"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/queries/overloaded-errors.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/queries/overloaded-errors.md"
description: "YDB возвращает ошибки OVERLOADED в следующих случаях: Перегруженные партиции таблиц, у которых в очереди на выполнение более 15000 запросов."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Ошибки «overloaded»

YDB возвращает ошибки `OVERLOADED` в следующих случаях:

- Перегруженные партиции таблиц, у которых в очереди на выполнение более 15000 запросов.
- Превышен лимит размера выходной очереди [CDC](../../../concepts/glossary.md#cdc) в 10000 элементов или 125 МБ.
- Партиции таблиц не находятся в нормальном состоянии, например, разделяются/объединяются.
- Количество открытых сессий с узлом YDB достигло лимита в 1000.

## Диагностика {#diagnostika}

1. Откройте панель мониторинга Grafana **[DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)**.

2. В разделе **API details** проверьте, есть ли всплески частоты запросов со статусом `OVERLOADED` на диаграмме **Soft errors (retriable)**.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/queries/_assets/soft-errors.png)

3. Чтобы проверить, не связаны ли всплески ошибок `OVERLOADED` с превышением лимита в 15000 запросов на партицию таблицы:

   1. Во [Встроенном UI](../../../reference/embedded-ui/index.md) перейдите на вкладку **Databases** и нажмите на базу данных.
   2. На вкладке **Navigation** убедитесь, что требуемая база данных выбрана.
   3. Откройте вкладку **Diagnostics**.
   4. Откройте вкладку **Top shards**.
   5. На вкладках **Immediate** и **Historical** отсортируйте таблетки по столбцу **InFlightTxCount** и проверьте, не превышают ли максимальные значения лимит в 15000 запросов.

4. Чтобы проверить, не связаны ли всплески ошибок `OVERLOADED` со слишком частыми слияниями и разделениями таблеток, см. [Избыточные разделения и слияния партиций таблиц](../schemas/splits-merges.md).

5. Чтобы проверить, не связаны ли всплески ошибок `OVERLOADED` с превышением лимита в 1000 открытых сессий, см. диаграмму **Session count by host** на панели мониторинга Grafana **[DB status](../../../reference/observability/metrics/grafana-dashboards.md#dbstatus)**.

6. См. статью [Перегруженные таблетки data shard](../schemas/overloaded-shards.md).

## Рекомендации {#rekomendacii}

Если YQL-запрос возвращает ошибку `OVERLOADED`, выполните запрос повторно с экспоненциальной задержкой. YDB SDK предлагает встроенный механизм для обработки временных ошибок. Для получения дополнительной информации см. [Обработка ошибок](../../../reference/ydb-sdk/error_handling.md).

Превышение лимита открытых сессий на узле может указывать на проблему в логике приложения.
