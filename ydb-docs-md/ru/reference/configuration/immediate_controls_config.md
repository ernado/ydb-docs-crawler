---
title: "immediate_controls_config"
url: "https://ydb.tech/docs/ru/reference/configuration/immediate_controls_config?version=v26.1"
doc_path: "ru/reference/configuration/immediate_controls_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/immediate_controls_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/immediate_controls_config.md"
description: "Конфигурация immediate_controls_config — это набор динамических параметров для настройки компонентов YDB, таких как DataShard, Coordinator, SchemeShard, BlobSto"
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# immediate_controls_config

Конфигурация `immediate_controls_config` — это набор динамических параметров для настройки компонентов YDB, таких как [DataShard](../../concepts/glossary.md#data-shard), [Coordinator](../../concepts/glossary.md#coordinator), [SchemeShard](../../concepts/glossary.md#scheme-shard), [BlobStorage](../../concepts/glossary.md#distributed-storage) и другие. Эти настройки позволяют адаптировать поведение кластера под специфичные сценарии, например, настроив пороги автоматического разделения шардов при росте данных или увеличении нагрузки.

## Синтаксис {#sintaksis}

```yaml
immediate_controls_config:
  ...
  scheme_shard_controls:
    force_shard_split_data_size: 2147483648
    ...
```

## Параметры {#parametry}

| Параметр | Минимальное значение | Максимальное значение | Значение по умолчанию | Описание |
| --- | --- | --- | --- | --- |
| `scheme_shard_controls.force_shard_split_data_size` | 10 МиБ | 16 ГиБ | 2 ГиБ | Партиция таблицы будет принудительно разделена при достижении заданного размера, даже если настроенные для таблицы [порог размера партиции или максимальное количество партиций](../../concepts/datamodel/table.md#partitioning_row_table) не допускают разделение. Значение задаётся в байтах. |
