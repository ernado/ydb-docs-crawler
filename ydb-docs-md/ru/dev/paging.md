---
title: "Постраничный вывод"
url: "https://ydb.tech/docs/ru/dev/paging?version=v26.1"
doc_path: "ru/dev/paging"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/paging.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/paging.md"
description: "В разделе приведены рекомендации по организации постраничного вывода данных."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Постраничный вывод

В разделе приведены рекомендации по организации постраничного вывода данных.

Для организации постраничного вывода рекомендуется последовательно выбирать данные, отсортированные по первичному ключу, ограничивая количество строк ключевым словом LIMIT.

> [!NOTE]
> `$lastCity, $lastNumber` - значения первичного ключа, полученные в результате предыдущего запроса.

Запрос c примером рекомендованного способа организации постраничного вывода:

```yql
--  Table `schools`:
-- ┌─────────┬─────────┬─────┐
-- | Name    | Type    | Key |
-- ├─────────┼─────────┼─────┤
-- | city    | Utf8?   | K0  |
-- | number  | Uint32? | K1  |
-- | address | Utf8?   |     |
-- └─────────┴─────────┴─────┘

DECLARE $limit AS Uint64;
DECLARE $lastCity AS Utf8;
DECLARE $lastNumber AS Uint32;

SELECT * FROM schools
WHERE (city, number) > ($lastCity, $lastNumber)
ORDER BY city, number
LIMIT $limit;
```

В примере запроса, приведенном выше, в операторе `WHERE` применено сравнение кортежей для отбора очередного множества строк. Сравнение кортежей выполняется поэлементно слева направо, поэтому порядок указания полей в кортеже должен совпадать с порядком указания полей в первичном ключе, чтобы избежать полного сканирования таблицы при выполнении запроса.

> [!WARNING]
> **Значение NULL в ключевой колонке**
>
> В YDB все колонки, включая ключевые, могут иметь значение NULL. Несмотря на это использование NULL в качестве значений в ключевых колонках крайне не рекомендуется, так как по SQL стандарту NULL нельзя сравнивать. Как следствие, лаконичные SQL конструкции с простыми операторами сравнения будут работать некорректно. Вместо них придется использовать громоздкие конструкции с IS NULL/IS NOT NULL выражениями.

## Примеры реализации постраничного вывода {#primery-realizacii-postranichnogo-vyvoda}

- [C++](https://github.com/ydb-platform/ydb/tree/main/ydb/public/sdk/cpp/examples/pagination)
- [Java](https://github.com/ydb-platform/ydb-java-examples/tree/master/ydb-cookbook/src/main/java/tech/ydb/examples/pagination)
- [Python](https://github.com/ydb-platform/ydb-python-sdk/tree/main/examples/pagination)
- [Go](https://github.com/ydb-platform/ydb-go-examples/tree/master/pagination)
