---
title: "Группы колонок"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/family?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/family"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/family.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/family.md"
description: "Колонки одной таблицы можно объединять в группы, чтобы задать следующие параметры:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Группы колонок

Колонки одной таблицы можно объединять в группы, чтобы задать следующие параметры:

- `DATA` — тип устройства хранения для данных колонок этой группы. Допустимые значения: `"ssd"`, `"rot"`.

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц.

- `COMPRESSION` — кодек сжатия данных. Допустимые значения: `"off"`, `"lz4"`, `"zstd"`.

> [!WARNING]
> Кодек `"zstd"` поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц.

- `COMPRESSION_LEVEL` — уровень сжатия кодека, если кодек поддерживает уровень сжатия.

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц.

- `CACHE_MODE` — [режим кэширования](../../../../concepts/datamodel/table.md#cache-modes). Допустимые значения: `"in_memory"`, `"regular"`.

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц.

По умолчанию все колонки находятся в одной группе с именем `default`. При необходимости параметры этой группы тоже можно переопределить. В противном случае применяются предопределённые значения.

В примерах ниже для создаваемых таблиц добавляется группа колонок `family_large`, которая устанавливается для колонки `series_info`, а также переопределяются параметры для группы `default`, которая по умолчанию применяется ко всем остальным колонкам.

{% list tabs %}

- Создание строковой таблицы

  ```sql
  CREATE TABLE series_with_families (
      series_id Uint64,
      title Utf8,
      series_info Utf8 FAMILY family_large,
      release_date Uint64,
      PRIMARY KEY (series_id),
      FAMILY default (
          DATA = "ssd",
          COMPRESSION = "off",
          CACHE_MODE = "in_memory"
      ),
      FAMILY family_large (
          DATA = "rot",
          COMPRESSION = "lz4",
          CACHE_MODE = "regular"
      )
  );
  ```

- Создание колоночной таблицы

  ```sql
  CREATE TABLE series_with_families (
      series_id Uint64 NOT NULL,
      title Utf8,
      series_info Utf8 FAMILY family_large,
      release_date Uint64,
      PRIMARY KEY (series_id),
      FAMILY default (
          COMPRESSION = "lz4"
      ),
      FAMILY family_large (
          COMPRESSION = "zstd",
          COMPRESSION_LEVEL = 5
      )
  )
  WITH (STORE = COLUMN);
  ```

{% endlist %}

> [!NOTE]
> Доступные типы устройств хранения зависят от конфигурации кластера YDB.
