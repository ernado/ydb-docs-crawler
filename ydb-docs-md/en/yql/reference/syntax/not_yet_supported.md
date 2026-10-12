---
title: "Unsupported classic SQL constructs"
url: "https://ydb.tech/docs/en/yql/reference/syntax/not_yet_supported?version=v26.1"
doc_path: "en/yql/reference/syntax/not_yet_supported"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/not_yet_supported.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/not_yet_supported.md"
description: "Correlated EXISTS and NOT EXISTS."
revision: "665607947c838b4f199a3b30499a54d29413ee4f"
---

# Unsupported classic SQL constructs

## Correlated EXISTS and NOT EXISTS {#not-exists}

`EXISTS` and `NOT EXISTS` can be used with uncorrelated subqueries. Correlated subqueries are not supported. To select rows based on the presence or absence of matching rows, use `LEFT SEMI JOIN` or `LEFT ONLY JOIN`. For details, see [Correlated subqueries, EXISTS, and NOT EXISTS](correlated-subqueries.md).

## INTERSECT and EXCEPT {#intersect-except}

YQL does not support `INTERSECT` or `EXCEPT`.

## NATURAL JOIN

An alternative is to explicitly list the matching columns on both sides.

## NOW() / CURRENT_TIME() {#now}

An alternative is to use the functions [CurrentUtcDate, CurrentUtcDatetime and CurrentUtcTimestamp](../builtins/basic.md#current-utc).
