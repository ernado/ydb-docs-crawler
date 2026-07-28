---
title: "Создание и изменение групп колонок"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table/family?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table/family"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/family.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/family.md"
description: "Важно. Поддерживается только для строковых таблиц."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Создание и изменение групп колонок

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц.

Механизм [групп](../../../../concepts/datamodel/table.md#column-groups) колонок позволяет увеличить производительность операций неполного чтения строк путем разделения хранения колонок строковой таблицы на несколько групп. Наиболее часто используемый сценарий — организация хранения редко используемых атрибутов в отдельной группе колонок.

## Создание группы колонок {#sozdanie-gruppy-kolonok}

`ADD FAMILY` — создаёт новую группу колонок в строковой таблице. Приведенный ниже код создаст в таблице `series_with_families` группу колонок `family_small`.

```yql
ALTER TABLE series_with_families ADD FAMILY family_small (
    DATA = "ssd",
    COMPRESSION = "off"
);
```

## Изменение групп колонок {#izmenenie-grupp-kolonok}

При помощи команды `ALTER COLUMN` можно изменить группу колонок для указанной колонки. Приведённый ниже код для колонки `release_date` в таблице `series_with_families` сменит группу колонок на `family_small`.

```yql
ALTER TABLE series_with_families ALTER COLUMN release_date SET FAMILY family_small;
```

Две предыдущие команды можно объединить в один вызов `ALTER TABLE`. Приведённый ниже код создаст в таблице `series_with_families` группу колонок `family_small` и установит её для колонки `release_date`.

```yql
ALTER TABLE series_with_families
  ADD FAMILY family_small (
      DATA = "ssd",
      COMPRESSION = "off"
  ),
  ALTER COLUMN release_date SET FAMILY family_small;
```

При помощи команды `ALTER FAMILY` можно изменить параметры группы колонок.

### Изменение типа хранилища {#izmenenie-tipa-hranilisha}

Приведённый ниже код для группы колонок `default` в таблице `series_with_families` сменит тип хранилища на `rot`:

```yql
ALTER TABLE series_with_families ALTER FAMILY default SET DATA "rot";
```

> [!NOTE]
> Доступные типы устройств хранения зависят от конфигурации кластера YDB.

### Изменение кодека сжатия {#izmenenie-kodeka-szhatiya}

Приведённый ниже код для группы колонок `default` в таблице `series_with_families` сменит кодек сжатия на `lz4`:

```yql
ALTER TABLE series_with_families ALTER FAMILY default SET COMPRESSION "lz4";
```

### Изменение режима кэширования {#izmenenie-rezhima-keshirovaniya}

При переключении режима кэширования на `in_memory` для существующей таблицы через команду `ALTER TABLE`, все страницы, которые ещё не находятся в памяти, будут подгружены автоматически.

Если для таблицы ранее был активирован режим `in_memory`, а затем через `ALTER TABLE` установлен режим кэширования `regular`, все находящиеся в памяти страницы сохраняются, но впоследствии могут вытесняться из памяти согласно общей политике кэширования.

Приведённый ниже код для группы колонок `default` в таблице `series_with_families` сменит [режим кэширования](../../../../concepts/datamodel/table.md#cache-modes) на `in_memory`:

```yql
ALTER TABLE series_with_families ALTER FAMILY default SET CACHE_MODE "in_memory";
```

Могут быть указаны все параметры группы колонок, описанные в команде [`CREATE TABLE`](../create_table/secondary_index.md)
