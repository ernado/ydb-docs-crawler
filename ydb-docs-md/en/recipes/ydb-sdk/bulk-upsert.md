---
title: "Bulk upsert of data"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/bulk-upsert?version=v26.1"
doc_path: "en/recipes/ydb-sdk/bulk-upsert"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/bulk-upsert.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/bulk-upsert.md"
description: "YDB supports bulk insert of many rows without atomicity guarantees. The write is split into several independent transactions, each touching a single partition,"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Bulk upsert of data

YDB supports bulk insert of many rows without atomicity guarantees. The write is split into several independent transactions, each touching a single partition, with parallel execution. This makes the approach more efficient than plain YQL. On success, the `BulkUpsert` method guarantees that all data passed in the request is inserted.

> [!WARNING]
> When you load data to [column-oriented tables](../../concepts/datamodel/table.md#column-oriented-tables) using `BulkUpsert`, you must provide values for **all** columns, even `NULL` values.

Below are examples of using the YDB SDK built-in tools for bulk insert:

{% list tabs %}

- Go

  {% list tabs %}

  - Native SDK

  {% endlist %}

- Native SDK

- Java

  {% list tabs %}

  - Native SDK

  {% endlist %}

- Native SDK

- Python

  {% list tabs %}

  - Native SDK

    ```python
    import posixpath
    import ydb

    def bulk_upsert(driver: ydb.Driver, path: str):
        column_types = (
            ydb.BulkUpsertColumns()
            .add_column("id", ydb.PrimitiveType.Uint64)
            .add_column("val", ydb.OptionalType(ydb.PrimitiveType.Utf8))
        )
        rows = [
            {"id": 1, "val": "1"},
            {"id": 2, "val": "2"},
            {"id": 3, "val": "3"},
        ]
        driver.table_client.bulk_upsert(posixpath.join(path, "tablename"), rows, column_types)
    ```

  - Native SDK (Asyncio)

    ```python
    import os
    import posixpath
    import ydb
    import asyncio

    async def bulk_upsert(driver: ydb.aio.Driver, path: str):
        column_types = (
            ydb.BulkUpsertColumns()
            .add_column("id", ydb.PrimitiveType.Uint64)
            .add_column("val", ydb.OptionalType(ydb.PrimitiveType.Utf8))
        )
        rows = [
            {"id": 1, "val": "1"},
            {"id": 2, "val": "2"},
            {"id": 3, "val": "3"},
        ]
        await driver.table_client.bulk_upsert(
            posixpath.join(path, "tablename"), rows, column_types
        )

    async def main():
        async with ydb.aio.Driver(
            connection_string=os.environ["YDB_CONNECTION_STRING"],
            credentials=ydb.credentials_from_env_variables(),
        ) as driver:
            await driver.wait()
            await bulk_upsert(driver, "/local")

    asyncio.run(main())
    ```

  - SQLAlchemy

    ```python
    import os
    import sqlalchemy as sa
    import ydb

    engine = sa.create_engine(os.environ["YDB_SQLALCHEMY_URL"])
    with engine.connect() as connection:
        dbapi_conn = connection.connection

        column_types = (
              ydb.BulkUpsertColumns()
              .add_column("id", ydb.PrimitiveType.Uint64)
              .add_column("val", ydb.OptionalType(ydb.PrimitiveType.Utf8))
          )
        rows = [
            {"id": 1, "val": "1"},
            {"id": 2, "val": "2"},
            {"id": 3, "val": "3"},
        ]

        dbapi_conn.bulk_upsert("tablename", rows, column_types)
    ```

  {% endlist %}

- Native SDK

  ```python
  import posixpath
  import ydb

  def bulk_upsert(driver: ydb.Driver, path: str):
      column_types = (
          ydb.BulkUpsertColumns()
          .add_column("id", ydb.PrimitiveType.Uint64)
          .add_column("val", ydb.OptionalType(ydb.PrimitiveType.Utf8))
      )
      rows = [
          {"id": 1, "val": "1"},
          {"id": 2, "val": "2"},
          {"id": 3, "val": "3"},
      ]
      driver.table_client.bulk_upsert(posixpath.join(path, "tablename"), rows, column_types)
  ```

- Native SDK (Asyncio)

  ```python
  import os
  import posixpath
  import ydb
  import asyncio

  async def bulk_upsert(driver: ydb.aio.Driver, path: str):
      column_types = (
          ydb.BulkUpsertColumns()
          .add_column("id", ydb.PrimitiveType.Uint64)
          .add_column("val", ydb.OptionalType(ydb.PrimitiveType.Utf8))
      )
      rows = [
          {"id": 1, "val": "1"},
          {"id": 2, "val": "2"},
          {"id": 3, "val": "3"},
      ]
      await driver.table_client.bulk_upsert(
          posixpath.join(path, "tablename"), rows, column_types
      )

  async def main():
      async with ydb.aio.Driver(
          connection_string=os.environ["YDB_CONNECTION_STRING"],
          credentials=ydb.credentials_from_env_variables(),
      ) as driver:
          await driver.wait()
          await bulk_upsert(driver, "/local")

  asyncio.run(main())
  ```

- SQLAlchemy

  ```python
  import os
  import sqlalchemy as sa
  import ydb

  engine = sa.create_engine(os.environ["YDB_SQLALCHEMY_URL"])
  with engine.connect() as connection:
      dbapi_conn = connection.connection

      column_types = (
            ydb.BulkUpsertColumns()
            .add_column("id", ydb.PrimitiveType.Uint64)
            .add_column("val", ydb.OptionalType(ydb.PrimitiveType.Utf8))
        )
      rows = [
          {"id": 1, "val": "1"},
          {"id": 2, "val": "2"},
          {"id": 3, "val": "3"},
      ]

      dbapi_conn.bulk_upsert("tablename", rows, column_types)
  ```

{% endlist %}
