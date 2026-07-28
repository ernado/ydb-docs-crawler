---
title: "FLATTEN"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/flatten?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/flatten"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/flatten.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/flatten.md"
description: "FLATTEN BY. Преобразует строки исходной таблицы с помощью вертикального разворачивания контейнеров переменной длины (списков или словарей). Например:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# FLATTEN

## FLATTEN BY

Преобразует строки исходной таблицы с помощью вертикального разворачивания [контейнеров](../../types/containers.md) переменной длины (списков или словарей).

Например:

- Исходная таблица:

  | \[a, b, c\] | 1 |
  | --- | --- |
  | \[d\] | 2 |
  | \[\] | 3 |

- Таблица после вызова `FLATTEN BY` к левому столбцу:

  | a | 1 |
  | --- | --- |
  | b | 1 |
  | c | 1 |
  | d | 2 |

В таблицах YDB не поддерживаются контейнерные типы, поэтому функция FLATTEN BY может применяться только над переменными табличных типов, создаваемых в рамках YQL запроса.

### Пример {#primer}

```yql
$sample = AsList(
    AsStruct(AsList('a','b','c') AS value, CAST(1 AS Uint32) AS id),
    AsStruct(AsList('d') AS value, CAST(2 AS Uint32) AS id),
    AsStruct(AsList() AS value, CAST(3 AS Uint32) AS id)
);

SELECT value, id FROM as_table($sample) FLATTEN BY (value);
```

Такое преобразование может быть удобным в следующих случаях:

- Когда по ячейкам из столбца-контейнера необходимо вывести статистику (например, через [`GROUP BY`](group-by.md)).
- Когда в ячейках столбца-контейнера хранятся идентификаторы из другой таблицы, которую нужно присоединить с помощью [`JOIN`](join.md).

### Синтаксис {#sintaksis}

- `FLATTEN BY` указывается после `FROM`, но перед `GROUP BY`, если `GROUP BY` присутствует в запросе.
- Тип столбца-результата зависит от типа исходного столбца:

| Тип контейнера | Тип результата | Комментарий |
| --- | --- | --- |
| `List<X>` | `X` | Тип ячейки списка |
| `Dict<X,Y>` | `Tuple<X,Y>` | Кортеж из двух элементов с парами «ключ—значение» |
| `Optional<X>` | `X` | Результат практически эквивалентен конструкции `WHERE foo IS NOT NULL`, но тип колонки `foo` будет изменен на `X` |

- По умолчанию столбец с результатом заменяет исходный. Используйте `FLATTEN BY foo AS bar` для сохранения исходного контейнера. В результате исходный контейнер останется доступным в `foo`, а построенный — в `bar`.
- Чтобы построить декартово произведение нескольких столбцов-контейнеров, используйте конструкцию `FLATTEN BY (a, b, c)`. Скобки обязательны, чтобы избежать конфликтов в грамматике.
- В `FLATTEN BY` можно использовать только имена столбцов из входной таблицы. Чтобы применить `FLATTEN BY` к результату вычисления, используйте подзапрос.
- В `FLATTEN BY` можно использовать не только столбцы, но и произвольные именованные выражения (в отличие от столбцов `AS` обязательно). Из-за грамматических неоднозначностей выражения после `FLATTEN BY` должны быть заключены в скобки: `... FLATTEN BY (ListSkip(col, 1) AS col) ...`
- Если в исходном столбце были вложенные контейнеры, например `List<Dict<X,Y>>`, `FLATTEN BY` развернет только внешний уровень. Чтобы полностью развернуть вложенные контейнеры, используйте подзапрос.

> [!NOTE]
> `FLATTEN BY` интерпретирует [опциональные типы данных](../../types/optional.md) как списки длины 0 или 1. Строки таблицы с `NULL` пропускаются, и тип столбца меняется на аналогичный неопциональный.
>
> `FLATTEN BY` делает только одно преобразование за раз, поэтому на опциональных контейнерах, например, `Optional<List<String>>` следует использовать `FLATTEN LIST BY` или `FLATTEN OPTIONAL BY`.

### Уточнение типа контейнера {#flatten-by-specific-type}

Чтобы уточнить тип контейнера, по которому необходимо произвести преобразование, можно использовать:

- `FLATTEN LIST BY`

  Для `Optional<List<T>>` операция `FLATTEN LIST BY` будет разворачивать список, интерпретируя `NULL`-значение как пустой список.

- `FLATTEN DICT BY`

  Для `Optional<Dict<T>>` операция `FLATTEN DICT BY` будет разворачивать словарь, интерпретируя `NULL`-значение как пустой словарь.

- `FLATTEN OPTIONAL BY`

  Чтобы фильтровать `NULL`-значения без размножения, необходимо уточнить операцию до `FLATTEN OPTIONAL BY`.

#### Примеры {#primery}

```yql
SELECT
  t.item.0 AS key,
  t.item.1 AS value,
  t.dict_column AS original_dict,
  t.other_column AS other
FROM my_table AS t
FLATTEN DICT BY dict_column AS item;
```

```yql
SELECT * FROM (
    SELECT
        AsList(1, 2, 3) AS a,
        AsList("x", "y", "z") AS b
) FLATTEN LIST BY (a, b);
```

```yql
SELECT * FROM (
    SELECT
        "1;2;3" AS a,
        AsList("x", "y", "z") AS b
) FLATTEN LIST BY (String::SplitToList(a, ";") as a, b);
```

### Аналоги FLATTEN BY для других СУБД {#flatten-other-dmb}

- PostgreSQL: `unnest`;
- Hive: `LATERAL VIEW`;
- MongoDB: `unwind`;
- Google BigQuery: `FLATTEN`;
- ClickHouse: `ARRAY JOIN / arrayJoin`;

## FLATTEN COLUMNS

Преобразует таблицу, в которой все столбцы должны являться структурами, в таблицу со столбцами, соответствующими каждому элементу каждой структуры из исходных столбцов.

Имена исходных столбцов-структур не используются и не возвращаются в результате. Имена элементов структур не должны повторяться в исходных столбцах.

### Пример {#primer1}

```yql
SELECT x, y, z
FROM (
  SELECT
    AsStruct(
        1 AS x,
        "foo" AS y),
    AsStruct(
        false AS z)
) FLATTEN COLUMNS;
```
