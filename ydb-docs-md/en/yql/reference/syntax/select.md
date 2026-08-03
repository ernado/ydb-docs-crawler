---
title: "SELECT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select?version=v26.1"
doc_path: "en/yql/reference/syntax/select"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/index.md"
description: "SELECT. Returns the result of evaluating the expressions specified after SELECT. It can be used in combination with other operations to obtain other effect."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# SELECT

Returns the result of evaluating the expressions specified after `SELECT`.

It can be used in combination with other operations to obtain other effect.

## Examples

```yql
SELECT "Hello, world!";
```

```yql
SELECT 2 + 2;
```

## SELECT execution procedure {#selectexec}

The `SELECT` query result is calculated as follows:

- Determine the set of input tables by evaluating the [FROM](select/from.md) clauses.
- Execute [FLATTEN COLUMNS](select/flatten.md#flatten-columns) or [FLATTEN BY](select/flatten.md); aliases set in `FLATTEN BY` become visible after this point.
- Execute every [JOIN](select/join.md).
- Add to (or replace in) the data the columns listed in [GROUP BY ... AS ...](select/group-by.md).
- Execute [WHERE](select/where.md) — Discard all the data mismatching the predicate.
- Execute [GROUP BY](select/group-by.md), evaluate aggregate functions.
- Apply the filter [HAVING](select/group-by.md#having).
- Evaluate [window functions](select/window.md);
- Evaluate expressions in `SELECT`.
- Assign names set by aliases to expressions in `SELECT`.
- Apply top-level [DISTINCT](select/distinct.md) to the resulting columns.
- Execute similarly every subquery inside [UNION ALL](select/union.md#union-all), combine them (see [PRAGMA AnsiOrderByLimitInUnionAll](pragma.md#pragmas)).
- Perform sorting with [ORDER BY](select/order_by.md).
- Apply [OFFSET and LIMIT](select/limit_offset.md) to the result.

## Column order in YQL {#orderedcolumns}

The standard SQL is sensitive to the order of columns in projections (that is, in `SELECT`). While the order of columns must be preserved in the query results or when writing data to a new table, some SQL constructs use this order.  
 This applies, for example, to [UNION ALL](select/union.md#union-all) and positional [ORDER BY](select/order_by.md) (ORDER BY ordinal).

The column order is ignored in YQL by default:

- The order of columns in the output tables and query results is undefined
- The data scheme of the `UNION ALL` result is output by column names rather than positions

If you enable `PRAGMA OrderedColumns;`, the order of columns is preserved in the query results and is derived from the order of columns in the input tables using the following rules:

- `SELECT`: an explicit column enumeration dictates the result order.
- `SELECT` with an asterisk (`SELECT * FROM ...`) inherits the order from its input.
- The order of columns after [JOIN](select/join.md): First output the left-hand columns, then the right-hand ones. If the column order in any of the sides in the `JOIN` output is undefined, the column order in the result is also undefined.
- The order in `UNION ALL` depends on the [UNION ALL](select/union.md#union-all) execution mode.
- The column order for [AS_TABLE](select/from_as_table.md) is undefined.

> [!WARNING]
> In the YT table schema, key columns always precede non-key columns. The order of key columns is determined by the order of the composite key.
>  When `PRAGMA OrderedColumns;` is enabled, non-key columns preserve their output order.

## Combining queries

Results of several SELECT statements (or subqueries) can be combined using `UNION` and `UNION ALL` keywords.

```yql
query1 UNION [ALL] query2 (UNION [ALL] query3 ...)
```

Union of more than two queries is interpreted as a left-associative operation, that is

```yql
query1 UNION query2 UNION ALL query3
```

is interpreted as

```yql
(query1 UNION query2) UNION ALL query3
```

If the underlying queries have one of the `ORDER BY/LIMIT/DISCARD/INTO RESULT` operators, the following rules apply:

- `ORDER BY/LIMIT/INTO RESULT` is only allowed after the last query
- `DISCARD` is only allowed before the first query
- the operators apply to the `UNION [ALL]` as a whole, instead of referring to one of the queries
- to apply the operator to one of the queries, enclose the query in parentheses

## Clauses supported in SELECT

- [FROM](select/from.md)
- [FROM AS_TABLE](select/from_as_table.md)
- [FROM SELECT](select/from_select.md)
- [DISTINCT](select/distinct.md)
- [UNIQUE DISTINCT](select/unique_distinct_hints.md)
- [UNION](select/union.md)
- [WITH](select/with.md)
- [WITHOUT](select/without.md)
- [WHERE](select/where.md)
- [ORDER BY](select/order_by.md)
- [ASSUME ORDER BY](select/assume_order_by.md)
- [LIMIT OFFSET](select/limit_offset.md)
- [JOIN](select/join.md)
- [GROUP BY](select/group-by.md)
- [FLATTEN](select/flatten.md)
- [WINDOW](select/window.md)
- [VIEW secondary_index](select/secondary_index.md)
- [VIEW vector_index](select/vector_index.md)
