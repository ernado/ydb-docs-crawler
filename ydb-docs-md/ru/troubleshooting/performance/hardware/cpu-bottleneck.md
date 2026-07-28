---
title: "Недостаточное быстродействие процессора"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/hardware/cpu-bottleneck?version=v26.1"
doc_path: "ru/troubleshooting/performance/hardware/cpu-bottleneck"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/hardware/cpu-bottleneck.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/hardware/cpu-bottleneck.md"
description: "Высокая нагрузка на процессор может привести к медленному выполнению запросов и увеличению задержек. В условиях ограниченного ресурса процессора база данных мож"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Недостаточное быстродействие процессора

Высокая нагрузка на процессор может привести к медленному выполнению запросов и увеличению задержек. В условиях ограниченного ресурса процессора база данных может с трудом справляться со сложными запросами или высоконагруженными транзакционными сценариями использования.

Узлы YDB в основном используют ресурсы процессора на выполнение [акторов](../../../concepts/glossary.md#actor). На каждом узле акторы выполняются с использованием ресурсов одного из [пулов акторной системы](../../../concepts/glossary.md#actor-system-pools). Потребление ресурсов каждого пула измеряется отдельно, что позволяет точнее отслеживать изменения в потреблении ресурсов.

## Диагностика {#diagnostika}

1. Используйте вкладку **Diagnostics** во [встроенном UI](../../../reference/embedded-ui/index.md) для анализа загрузки процессора во всех пулах ресурсов:

   1. Откройте [встроенный UI](../../../reference/embedded-ui/index.md), перейдите на вкладку **Databases** и нажмите на требуемую базу данных.

   2. На вкладке **Navigation** убедитесь, что требуемая база данных выбрана.

   3. Откройте вкладку **Diagnostics**.

   4. На вкладке **Info** нажмите на кнопку **CPU** и проверьте уровни загрузки процессора во всех пулах ресурсов.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/embedded-ui-cpu-system-pool.png)

2. Проанализируйте загрузку процессора во всех пулах ресурсов на графиках Grafana:

   1. Откройте панель мониторинга **[CPU](../../../reference/observability/metrics/grafana-dashboards.md#cpu)** в Grafana.

   2. Проверьте наличие скачков на следующих графиках:

      - **CPU by execution pool**

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/cpu-by-pool.png)

      - **User pool - CPU by host**

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/cpu-user-pool.png)

      - **System pool - CPU by host**

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/cpu-system-pool.png)

      - **Batch pool - CPU by host**

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/cpu-batch-pool.png)

      - **IC pool - CPU by host**

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/cpu-ic-pool.png)

      - **IO pool - CPU by host**

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/cpu-io-pool.png)

3. Если скачки потребления ресурсов процессора обнаружены в пользовательском пуле ресурсов (user pool), проанализируйте изменения пользовательской нагрузки, которые могли бы вызвать недостаток ресурсов процессора. Проверьте следующие графики на панели мониторинга **DB overview** в Grafana:

   - **Requests**

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/requests.png)

   - **Request size**

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/request-size.png)

   - **Response size**

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/response-size.png)

   Также проверьте все графики в секции **Operations** на панели мониторинга **DataShard**.

4. Если скачки потребления ресурсов процессора обнаружены в пакетном пуле ресурсов (batch pool), проверьте, не запущены ли процессы резервного копирования (backups).

## Рекомендации {#rekomendacii}

Добавьте дополнительные [узлы базы данных](../../../concepts/glossary.md#database-node) в кластер или выделите больше процессорных ядер существующим узлам. Если это невозможно, рассмотрите возможность перераспределения ядер процессора между пулами ресурсов.
