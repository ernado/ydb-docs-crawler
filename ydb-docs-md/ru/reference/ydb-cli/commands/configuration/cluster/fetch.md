---
title: "admin cluster config fetch"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/configuration/cluster/fetch?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/configuration/cluster/fetch"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/configuration/cluster/fetch.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/configuration/cluster/fetch.md"
description: "С помощью команды admin cluster config fetch вы можете получить текущую конфигурацию кластера YDB. В зависимости от используемой кластером версии конфигурации,"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster config fetch

С помощью команды `admin cluster config fetch` вы можете получить текущую [конфигурацию](../../../../../devops/configuration-management/index.md) кластера YDB. В зависимости от используемой кластером [версии конфигурации](../../../../../devops/configuration-management/compare-configs.md), команда возвращает:

- V1 — только [динамическую конфигурацию](../../../../../devops/configuration-management/configuration-v1/dynamic-config.md);
- V2 — всю конфигурацию.

Общий вид команды:

```bash
ydb [global options...] admin cluster config fetch
```

- `global options` — глобальные параметры.

Посмотрите описание команды получения конфигурации:

```bash
ydb admin cluster config fetch --help
```

## Примеры {#examples}

Получите текущую конфигурацию кластера:

```bash
ydb --endpoint grpc://localhost:2135 admin cluster config fetch > config.yaml
```
