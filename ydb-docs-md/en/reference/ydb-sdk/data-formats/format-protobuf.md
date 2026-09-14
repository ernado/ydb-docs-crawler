---
title: "Protobuf (Value) format"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/data-formats/format-protobuf?version=v26.1"
doc_path: "en/reference/ydb-sdk/data-formats/format-protobuf"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/data-formats/format-protobuf.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/data-formats/format-protobuf.md"
description: "This is the default format. Data is returned row by row as Protobuf: each row is a serialized set of named values with their YQL types. The SDK converts values"
revision: "6a967ac39a5eac92f33ed9e017b7e5e4482fb785"
---

# Protobuf (Value) format

This is the default format. Data is returned row by row as [Protobuf](https://protobuf.dev/overview/): each row is a serialized set of named values with their YQL types. The SDK converts values to native types for your language and exposes a type-safe API.

Use this format when you need:

- Transactional ([OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing)) workloads with point reads of individual rows.
- Applications that process small fragments of a table at full row width.
- Native integration with your language’s types.

## YQL type mapping {#type-mapping}

Mapping from YQL types to native language types is implemented in the SDK and depends on the SDK you use. See your SDK’s documentation for the exact mapping.

## Returned schema {#schema}

The schema is a list of columns with their YQL types. That is enough for the SDK to interpret values: given the column type, each value is converted to a native type.

## SDK examples

{% list tabs %}

- Python

  This format is the default when you run queries through QueryService. The example below shows how to set the result format explicitly.

  ```python
  pool = ydb.QuerySessionPool(driver)

  query = """
      SELECT * FROM example ORDER BY Key LIMIT 100;
  """

  result = pool.execute_with_retries(
      query,
      result_set_format=ydb.QueryResultSetFormat.VALUE,
      schema_inclusion_mode=ydb.QuerySchemaInclusionMode.FIRST_ONLY,
  )

  for result_set in result:
      print(f"Record batch with {len(result_set.rows)} rows and {len(result_set.columns)} columns")
  ```

- Java

  This format is the default when you run queries through QueryService.

{% endlist %}
