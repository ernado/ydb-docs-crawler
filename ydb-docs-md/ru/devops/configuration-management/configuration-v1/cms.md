---
title: "Изменение конфигураций через CMS"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/cms?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/cms"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/cms.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/cms.md"
description: "Примечание. Данный способ изменения конфигурации является устаревшим. Рекомендуемый способ конфигурирования описан в разделе динамическая конфигурация кластера."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Изменение конфигураций через CMS

> [!NOTE]
> Данный способ изменения конфигурации является устаревшим. Рекомендуемый способ конфигурирования описан в разделе [динамическая конфигурация кластера](dynamic-config.md).

## Получить текущие настройки {#poluchit-tekushie-nastrojki}

Следующая команда позволит получить текущие настройки по кластеру или по тенанту.

```bash
ydbd -s <endpoint> admin console configs load --out-dir <config-folder>
```

```bash
ydbd -s <endpoint> admin console configs load --out-dir <config-folder> --tenant <tenant-name>
```

## Обновить настройки {#obnovit-nastrojki}

Сначала надо выкачать нужный конфиг как указано выше, после чего требуется подготовить protobuf файл с запросом на изменение.

```proto
Actions {
  AddConfigItem {
    ConfigItem {
      Cookie: "<cookie>"
      UsageScope {
        TenantAndNodeTypeFilter {
          Tenant: "<tenant-name>"
        }
      }
      Config {
          <config-name> {
              <full-config>
          }
      }
    }
  }
}
```

Поле UsageScope необязательно, и нужно для применения настроек для определенного тенанта.

```bash
ydbd -s <endpoint> admin console configs update <protobuf-file>
```
