---
title: "Недостаточное дисковое пространство"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/hardware/disk-space?version=v26.1"
doc_path: "ru/troubleshooting/performance/hardware/disk-space"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/hardware/disk-space.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/hardware/disk-space.md"
description: "Нехватка места на диске может привести к невозможности сохранения новых данных, когда база переходит в режим только для чтения. Эта проблема может также приводи"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Недостаточное дисковое пространство

Нехватка места на диске может привести к невозможности сохранения новых данных, когда база переходит в режим только для чтения. Эта проблема может также приводить к замедлению работы, когда система пытается освободить дисковое пространство, активнее приводя данные к более компактному виду в фоне.

## Диагностика {#diagnostika}

1. Проверьте наличие скачков на графиках панели мониторинга **[DB overview > Storage](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** в Grafana.

2. Во [встроенном UI](../../../reference/embedded-ui/index.md) на вкладке **Storage** проанализируйте список доступных групп хранения и их потребление места на диске.

   > [!TIP]
   > Используйте фильтр **Out of Space**, чтобы отображать только группы хранения с заполненными дисками.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/storage-groups-disk-space.png)

> [!NOTE]
> Чтобы получить эту информацию, можно также использовать [Healthcheck API](../../../reference/ydb-sdk/health-check-api.md).

## Рекомендации {#rekomendacii}

Добавьте больше [групп хранения](../../../concepts/glossary.md#storage-group) в базу данных.

Если у кластера нет свободных групп хранения, необходимо их предварительно сконфигурировать. При необходимости добавьте дополнительные [узлы хранения](../../../concepts/glossary.md#storage-node).
