---
title: "Графики"
url: "https://ydb.tech/docs/ru/reference/embedded-ui/charts?version=v26.1"
doc_path: "ru/reference/embedded-ui/charts"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/embedded-ui/charts.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/embedded-ui/charts.md"
description: "Просмотр графиков осуществляется через Grafana. Основные метрики системы выведены на дашборд:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Графики

Просмотр графиков осуществляется через Grafana.

Основные метрики системы выведены на дашборд:

- **CPU Usage** — суммарная загрузка CPU на всех узлах (1 000 000 = 1 CPU);
- **Memory Usage** — потребление оперативной памяти по узлам;
- **Disk Space Usage** — потребление дискового пространства по узлам;
- **SelfPing** — наибольшее за интервал измерений фактическое время доставки отложенных сообщений в актор-системе. Измеряется для сообщений с отложенной на 10 мс доставкой. Рост данной величины может быть признаком микроберстов нагрузки, высокой утилизации CPU, вытеснения процесса YDB с ядер процессора другими процессами.
