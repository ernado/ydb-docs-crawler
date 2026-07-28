---
title: "Classic SQL constructs not supported yet"
url: "https://ydb.tech/docs/en/yql/reference/syntax/not_yet_supported?version=v26.1"
doc_path: "en/yql/reference/syntax/not_yet_supported"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/not_yet_supported.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/not_yet_supported.md"
description: "[NOT] [EXISTS|INTERSECT|EXCEPT]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Classic SQL constructs not supported yet

## \[NOT\] \[EXISTS|INTERSECT|EXCEPT\] {#not-exists}

A syntactically available alternative is `EXISTS`, but it's not very useful as it doesn't support correlated subqueries. You can also rewrite it using `JOIN`.

## NATURAL JOIN

An alternative is to explicitly list the matching columns on both sides.

## NOW() / CURRENT_TIME() {#now}

An alternative is to use the functions [CurrentUtcDate, CurrentUtcDatetime and CurrentUtcTimestamp](../builtins/basic.md#current-utc).
