---
title: "BI-аналитика и визуализация данных"
url: "https://ydb.tech/docs/ru/concepts/analytics/concepts/bi?version=v26.1"
doc_path: "ru/concepts/analytics/concepts/bi"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/analytics/concepts/bi.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/analytics/concepts/bi.md"
description: "Интерактивность BI-дешбордов напрямую зависит от производительности базы данных, на которой они построены. YDB спроектирована как высокопроизводительная аналити"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# BI-аналитика и визуализация данных

Интерактивность BI-дешбордов напрямую зависит от производительности базы данных, на которой они построены. YDB спроектирована как высокопроизводительная аналитическая платформа, выполняющая запросы за доли секунды, что позволяет аналитикам работать с данными в интерактивном режиме.

Это достигается за счёт ключевых архитектурных особенностей:

- Колоночное хранение: запросы считывают с диска только те столбцы, которые указаны в запросе, что сокращает объём операций ввода-вывода.
- MPP-архитектура: каждый запрос распараллеливается по всем доступным вычислительным узлам кластера, что позволяет задействовать все ресурсы для его выполнения.
- Децентрализованная архитектура: отсутствие единого мастер-узла позволяет эффективно обрабатывать множество параллельных запросов от пользователей BI-систем.

## Производительность в независимых бенчмарках {#proizvoditelnost-v-nezavisimyh-benchmarkah}

Хотя синтетические тесты не всегда отражают реальную нагрузку, они служат хорошей отправной точкой для сравнения производительности. [ClickBench](https://benchmark.clickhouse.com/#system=+Rf%7Cnof%7CYD&type=-&machine=-ca2%7Cgle%7C6ax%7Cae-%7C6ale%7Cgel%7C3al&cluster_size=-&opensource=-&tuned=+n&metric=hot&queries=-) — независимый бенчмарк для аналитических СУБД, разработанный создателями ClickHouse.

На наборе из 43 аналитических запросов YDB показывает конкурентоспособные результаты, опережая многие популярные open-source и облачные аналитические базы данных. Это подтверждает высокую производительность движка на типовых OLAP-запросах.

![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/concepts/analytics/concepts/_includes/clickbench.png)

## Интеграции с BI-платформами {#integracii-s-bi-platformami}

YDB поддерживает следующие BI-платформы:

- [Yandex DataLens](../../../integrations/visualization/datalens.md);
- [Apache Superset](../../../integrations/visualization/superset.md);
- [Grafana](../../../integrations/visualization/grafana.md);
- [Polymatica](https://wiki.polymatica.ru/display/PDTNUG1343/YDB+Server).
