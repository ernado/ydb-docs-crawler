---
title: "Изменение колонок"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table/columns?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table/columns"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/columns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/columns.md"
description: "YDB поддерживает возможность добавлять колонки в строковые и колоночные таблицы, удалять неключевые колонки из таблиц, а также изменять свойства существующих ко"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Изменение колонок

YDB поддерживает возможность добавлять колонки в строковые и колоночные таблицы, удалять неключевые колонки из таблиц, а также изменять свойства существующих колонок.

## ADD COLUMN

Строит новую колонку с указанными именем, типом и опциями для указанной таблицы.

```yql
ALTER TABLE table_name ADD COLUMN column_name column_data_type [FAMILY <family_name>] [NULL | NOT NULL] [DEFAULT <default_value>] [COMPRESSION([algorithm=<algorithm_name>[, level=<value>]])];
```

## Параметры запроса {#parametry-zaprosa}

### table_name {#table_name}

Путь таблицы, для которой требуется добавить новую колонку.

### column_name {#column_name}

Имя колонки, которая будет добавлена в указанную таблицу. При выборе имени для колонки учитывайте общие [правила именования колонок](../../../../concepts/datamodel/table.md#column-naming-rules).

### column_data_type {#column_data_type}

Тип данных колонки. Полный список типов данных, которые поддерживает YDB доступен в разделе [Типы данных YQL](../../types/index.md).

### FAMILY \<family_name> (настройка колонки) {#family-lessfamily_namegreater-nastrojka-kolonki}

Указание принадлежности данной колонки к указанной группе колонок. Подробнее в разделе [Группы колонок](../create_table/family.md).

### DEFAULT \<default_value> {#default-lessdefault_valuegreater}

> [!WARNING]
> Опция `DEFAULT` поддерживается:
>
> - Только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.
> - Только с литеральными значениями. Поддержка функциональности для вычислимых выражений находится в разработке.

Позволяет задать значение по умолчанию для колонки. Если при вставке строки значение для данной колонки не указано, будет использовано указанное значение по умолчанию. Значение по умолчанию должно соответствовать типу данных колонки.

Конструкция `DEFAULT false NOT NULL` недопустима по причине неоднозначности интерпретации. В таком случае следует использовать перечисление через запятые или изменить порядок опций.

### NULL

Данная колонка может содержать значения `NULL` (по умолчанию).

### NOT NULL

Данная колонка не принимает значения `NULL`.

### COMPRESSION(\[algorithm=\<algorithm_name>\[, level=\]\]) {#]]}

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц.

Для колонок можно задать следующие параметры сжатия:

- `algorithm` — алгоритм сжатия данных. Допустимые значения: `off` (отключение сжатия), `lz4`, `zstd`.
- `level` — уровень сжатия, поддерживается только для алгоритма `zstd` (допустимы значения от 0 до 22).

Если `COMPRESSION()` указан без параметров, для колонки используется сжатие по умолчанию. Сейчас это `lz4`; в будущих версиях появится возможность настраивать сжатие по умолчанию на уровне кластера или таблицы.

## Пример {#primer}

Приведённый ниже код добавит к таблице `episodes` колонку `views` с типом данных `Uint64`.

```yql
ALTER TABLE episodes ADD COLUMN views Uint64;
```

Приведённый ниже код добавит к таблице `episodes` колонку `rate` с типом данных `Double` и значением по умолчанию `5.0`.

```yql
ALTER TABLE episodes ADD COLUMN rate Double NOT NULL DEFAULT 5.0;
ALTER TABLE episodes ADD COLUMN rate Double (DEFAULT 5.0, NOT NULL); -- альтернативный синтаксис
```

## ALTER COLUMN

Изменяет свойства существующей колонки в указанной таблице. Изменение свойства происходит без пересоздания колонки. Некоторые свойства применяются только к свежим записанным данным или в процессе компакшена (детали можно найти в описании конкретного свойства)

```yql
ALTER TABLE table_name ALTER COLUMN column_name {SET | DROP} [FAMILY <family_name>] [NULL | NOT NULL] [DEFAULT <default_value>] [COMPRESSION([algorithm=<algorithm_name>[, level=<value>]])];
```

### Параметры запроса {#parametry-zaprosa1}

#### table_name {#table_name1}

Путь к таблице, в которой требуется изменить колонку.

#### column_name {#column_name1}

Имя колонки, которая будет изменена в указанной таблице.

#### SET

Установить параметр колонки

#### DROP

Удалить параметр колонки. На текущий момент поддерживается только удаление `NOT NULL`.

### FAMILY \<family_name> (настройка колонки) {#family-lessfamily_namegreater-nastrojka-kolonki1}

Указание принадлежности данной колонки к указанной группе колонок. Подробнее в разделе [Группы колонок](../create_table/family.md).

### DEFAULT \<default_value> {#default-lessdefault_valuegreater1}

> [!WARNING]
> Опция `DEFAULT` поддерживается:
>
> - Только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.
> - Только с литеральными значениями. Поддержка функциональности для вычислимых выражений находится в разработке.

Позволяет задать значение по умолчанию для колонки. Если при вставке строки значение для данной колонки не указано, будет использовано указанное значение по умолчанию. Значение по умолчанию должно соответствовать типу данных колонки.

Конструкция `DEFAULT false NOT NULL` недопустима по причине неоднозначности интерпретации. В таком случае следует использовать перечисление через запятые или изменить порядок опций.

### NULL {#null1}

Данная колонка может содержать значения `NULL` (по умолчанию).

### NOT NULL {#not-null1}

Данная колонка не принимает значения `NULL`.

### COMPRESSION(\[algorithm=\<algorithm_name>\[, level=\]\]) {#]]1}

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц.

Для колонок можно задать следующие параметры сжатия:

- `algorithm` — алгоритм сжатия данных. Допустимые значения: `off` (отключение сжатия), `lz4`, `zstd`.
- `level` — уровень сжатия, поддерживается только для алгоритма `zstd` (допустимы значения от 0 до 22).

Если `COMPRESSION()` указан без параметров, для колонки используется сжатие по умолчанию. Сейчас это `lz4`; в будущих версиях появится возможность настраивать сжатие по умолчанию на уровне кластера или таблицы.

### Примеры {#primery}

Приведённый ниже код запретит пустые значения в колонке `title` из таблицы `episodes`.

```yql
ALTER TABLE episodes ALTER COLUMN title SET NOT NULL;
```

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц.

Сброс настроек сжатия колонки

```yql
ALTER TABLE compressed_table ALTER COLUMN info SET COMPRESSION();
```

После выполнения запроса для колонки снова действует алгоритм сжатия по умолчанию (см. описание опции `COMPRESSION` выше).

## DROP COLUMN

Удаляет колонку из таблицы с указанным именем.

```yql
ALTER TABLE table_name DROP COLUMN column_name;
```

### Параметры запроса {#parametry-zaprosa2}

#### table_name {#table_name2}

Путь к таблице, в которой требуется удалить колонку.

#### column_name {#column_name2}

Имя колонки, которая будет удалена из указанной таблицы.

### Пример {#primer1}

Приведённый ниже код удалит колонку `views` из таблицы `episodes`.

```yql
ALTER TABLE episodes DROP COLUMN views;
```
