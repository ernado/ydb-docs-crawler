---
title: "health_check_config"
url: "https://ydb.tech/docs/ru/reference/configuration/healthcheck_config?version=v26.1"
doc_path: "ru/reference/configuration/healthcheck_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/healthcheck_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/healthcheck_config.md"
description: "Секция health_check_config настраивает пороговые значения и таймауты, используемые сервисом Health Check YDB. Эти параметры помогают настраивать обнаружение воз"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# health_check_config

Секция `health_check_config` настраивает пороговые значения и таймауты, используемые [сервисом Health Check](../ydb-sdk/health-check-api.md) YDB. Эти параметры помогают настраивать обнаружение возможных [проблем](../ydb-sdk/health-check-api.md#issues), таких как чрезмерные перезапуски или расхождение по времени между динамическими узлами.

## Синтаксис {#sintaksis}

```yaml
health_check_config:
  thresholds:
    node_restarts_yellow: 10
    node_restarts_orange: 30
    nodes_time_difference_yellow: 5000
    nodes_time_difference_orange: 25000
    tablets_restarts_orange: 30
  timeout: 20000
```

## Параметры {#parametry}

| Параметр | Значение по умолчанию | Описание |
| --- | --- | --- |
| `thresholds.node_restarts_yellow` | `10` | Количество перезапусков узлов для генерации предупреждения уровня `YELLOW` |
| `thresholds.node_restarts_orange` | `30` | Количество перезапусков узлов для генерации предупреждения уровня `ORANGE` |
| `thresholds.nodes_time_difference_yellow` | `5000` | Максимально допустимое расхождение по времени (в µs) между динамическими узлами для уровня `YELLOW` |
| `thresholds.nodes_time_difference_orange` | `25000` | Максимально допустимое расхождение по времени (в µs) между динамическими узлами для уровня `ORANGE` |
| `thresholds.tablets_restarts_orange` | `30` | Количество перезапусков таблеток для генерации предупреждения уровня `ORANGE` |
| `timeout` | `20000` | Максимальное время ответа от healthcheck (в мс) |
