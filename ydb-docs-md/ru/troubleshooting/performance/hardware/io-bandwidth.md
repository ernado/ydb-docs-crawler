---
title: "Недостаточная пропускная способность ввода-вывода"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/hardware/io-bandwidth?version=v26.1"
doc_path: "ru/troubleshooting/performance/hardware/io-bandwidth"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/hardware/io-bandwidth.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/hardware/io-bandwidth.md"
description: "Высокая скорость операций чтения/записи может перегрузить дисковую систему и приводить к увеличению задержек доступа к данным. Когда распределённое хранилище не"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Недостаточная пропускная способность ввода-вывода

Высокая скорость операций чтения/записи может перегрузить дисковую систему и приводить к увеличению задержек доступа к данным. Когда распределённое хранилище не может читать или записывать данные с достаточной скоростью, запросы к базе данных, требующие доступа к диску, могут замедляться.

## Диагностика {#diagnostika}

1. Откройте панель мониторинга **[Distributed Storage Overview](../../../reference/observability/metrics/grafana-dashboards.md)** в Grafana.

2. На графике **DiskTimeAvailable and total Cost relation** проверьте, пересекают ли всплески **Total Cost** уровень **DiskTimeAvailable**.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/disk-time-available--disk-cost.png)

   Этот график показывает ориентировочную суммарную пропускную способность системы хранения в условных единицах (зелёный) и суммарную стоимость использования в условных единицах (синий). Когда суммарная стоимость использования системы хранения превышает суммарную пропускную способность, система хранения YDB перегружается, и задержки выполнения запросов растут.

3. На графике **Total burst duration** проверьте наличие всплесков в системе хранения. Этот график показывает микровсплески нагрузки на систему хранения, в микросекундах.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/hardware/_assets/microbursts.png)

   > [!NOTE]
   > Этот график может выявить микровсплески нагрузки, которые не проявляются на графике со средней стоимостью использования **Cost and DiskTimeAvailable relation**.

## Рекомендации {#rekomendacii}

Добавьте в базу данных дополнительные [группы хранения](../../../concepts/glossary.md#storage-group).

В случае с частыми микровсплесками нагрузки может помочь балансировка нагрузки по группам хранения.
