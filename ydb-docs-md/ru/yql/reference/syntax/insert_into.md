---
title: "INSERT INTO"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/insert_into?version=v26.1"
doc_path: "ru/yql/reference/syntax/insert_into"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/insert_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/insert_into.md"
description: "Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# INSERT INTO

> [!WARNING]
> В настоящее время одновременное использование [колоночных](../../../concepts/glossary.md#column-oriented-table) и [строковых](../../../concepts/glossary.md#row-oriented-table) таблиц поддерживается в транзакциях, в которых данные только читаются, но не изменяются. Поддержка транзакций с возможностью модификации данных при одновременном использовании строковых и колоночных таблиц находится в разработке.
>
> Если попытаться выполнить операцию записи в транзакции, в которой задействованы и колоночные, и строковые таблицы, транзакция завершится с ошибкой: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Добавляет строки в таблицу. При попытке вставить в таблицу строку с уже существующим значением первичного ключа операция завершится ошибкой с кодом `PRECONDITION_FAILED` и текстом `Operation aborted due to constraint violation: insert_pk`.

`INSERT INTO` позволяет выполнять следующие операции:

- Добавление константных значений с помощью [`VALUES`](values.md).

  ```yql
  INSERT INTO my_table (Key1, Key2, Value1, Value2)
  VALUES (345987,'ydb', 'Яблочный край', 1414);
  COMMIT;
  ```

  ```yql
  INSERT INTO my_table (key, value)
  VALUES ("foo", 1), ("bar", 2);
  ```

- Сохранение результата выборки `SELECT`.

  ```yql
  INSERT INTO my_table
  SELECT Key AS Key1, "Empty" AS Key2, Value AS Value1
  FROM my_table1;
  ```

При работе с [внешними файловыми источниками данных](../../../concepts/datamodel/external_data_source.md) можно дополнительно указывать ряд параметров:

- `FORMAT` - формат хранимых данных в файловых хранилищах в [федеративных запросах](../../../concepts/query_execution/federated_query/s3/formats.md). Допустимые значения: `csv_with_names`, `tsv_with_names`, `json_list`, `json_each_row`, `json_as_string`, `parquet`, `raw`.
- `COMPRESSION` - формат сжатия файлов в файловых хранилищах в [федеративных запросах](../../../concepts/query_execution/federated_query/s3/partition_projection.md). Допустимые значения: [gzip](https://ru.wikipedia.org/wiki/Gzip), [zstd](https://ru.wikipedia.org/wiki/Zstandard), [lz4](https://ru.wikipedia.org/wiki/LZ4), [brotli](https://ru.wikipedia.org/wiki/Brotli), [bzip2](https://ru.wikipedia.org/wiki/Bzip2), [xz](https://ru.wikipedia.org/wiki/XZ).
- `PARTITIONED_BY` - список [колонок партиционирования](../../../concepts/query_execution/federated_query/s3/partitioning.md) данных в файловых хранилищах в федеративных запросах. Содержит список колонок в порядке их размещения в файловом хранилище.
- `projection.enabled` - флаг включения [расширенного партиционирования данных](../../../concepts/query_execution/federated_query/s3/partition_projection.md). Допустимые значения: `true`, `false`.
- `projection.<field_name>.type` - тип поля [расширенного партиционирования данных](../../../concepts/query_execution/federated_query/s3/partition_projection.md). Допустимые значения: `integer`, `enum`, `date`.
- `projection.<field_name>.<options>` - расширенные свойства поля [расширенного партиционирования данных](../../../concepts/query_execution/federated_query/s3/partition_projection.md).

## Пример {#primer}

```yql
INSERT INTO `connection`.`test/`
WITH
(
  FORMAT = "csv_with_names"
)
SELECT
    "value" AS value, "name" AS name
```

Где:

- `connection` — название соединения с S3 (Yandex Object Storage).
- `test/`— путь внутри бакета, куда будут записаны данные. При записи создаются файлы со случайными именами.

## INSERT INTO ... RETURNING {#insert-into-returning-{insert-into-returning}}

Используется для вставки строк и одновременного возврата значений из них. Это позволяет получить информацию о вставленных записях за один запрос, избавляя от необходимости выполнять последующий SELECT.

### Примеры {#primery}

- Возврат всех значений вставленной строки

```yql
INSERT INTO some_table (id, year, color, price)
VALUES (1103, 2023, 'blue', 400)
RETURNING *;
```

- Возврат конкретных столбцов

```yql
INSERT INTO some_table (id, color, price)
VALUES
    (1101, 'red', 200),
    (1102, 'green', 300)
RETURNING id, price;
```
