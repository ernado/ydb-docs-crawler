---
title: "admin cluster config generate"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/configuration/cluster/generate?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/configuration/cluster/generate"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/configuration/cluster/generate.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/configuration/cluster/generate.md"
description: "С помощью команды admin cluster config generate вы можете сгенерировать для кластера YDB конфигурацию V2 на основе его текущей конфигурации V1. Это один из шаго"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster config generate

С помощью команды `admin cluster config generate` вы можете сгенерировать для кластера YDB [конфигурацию V2](../../../../../devops/configuration-management/configuration-v2/index.md) на основе его текущей [конфигурации V1](../../../../../devops/configuration-management/configuration-v1/index.md). Это один из шагов при [миграции кластера на конфигурацию V2](../../../../../devops/configuration-management/migration/migration-to-v2.md).

Общий вид команды:

```bash
ydb [global options...] admin cluster config generate
```

- `global options` — глобальные параметры.

Посмотрите описание команды генерации конфигурации V2:

```bash
ydb admin cluster config generate --help
```

## Примеры {#examples}

Сгенерируйте конфигурацию V2 на основе конфигурации V1:

```bash
ydb admin cluster config generate > config.yaml
```

После выполнения данной команды в файле `config.yaml` будет содержаться YAML-документ следующего вида:

```yaml
metadata:
  kind: MainConfig
  cluster: ""
  version: 0
config:
  <настройки кластера>
```

## Использование сгенерированной конфигурации V2 {#ispolzovanie-sgenerirovannoj-konfiguracii-v2}

После генерации конфигурации V2 выполните следующие шаги:

1. Добавьте необходимые параметры конфигурации в конфигурационный файл.
2. Примените конфигурацию к кластеру с помощью команды [`admin cluster config replace`](replace.md).

Если вы используете данную команду для миграции на V2, следуйте указаниям [инструкции](../../../../../devops/configuration-management/migration/migration-to-v2.md).
