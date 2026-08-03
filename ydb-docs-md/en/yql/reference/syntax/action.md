---
title: "ACTION"
url: "https://ydb.tech/docs/en/yql/reference/syntax/action?version=v26.1"
doc_path: "en/yql/reference/syntax/action"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/action.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/action.md"
description: "DEFINE ACTION. Specifies a named action that is a parameterizable block of multiple top-level expressions. Syntax. DEFINE ACTION: action definition."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ACTION

## DEFINE ACTION

Specifies a named action that is a parameterizable block of multiple top-level expressions.

### Syntax

1. `DEFINE ACTION`: action definition.
2. [Action name](expressions.md#named-nodes) that will be used to access the defined action further in the query.
3. The values of parameter names are listed in parentheses.
4. `AS` keyword.
5. List of top-level expressions.
6. `END DEFINE`: The marker of the last expression inside the action.

One or more of the last parameters can be marked with a question mark `?` as optional. If they are omitted during the call, they will be assigned the `NULL` value.

## DO

Executes an `ACTION` with the specified parameters.

### Syntax {#syntax1}

1. `DO`: Executing an action.
2. The named expression for which the action is defined.
3. The values to be used as parameters are listed in parentheses.

`EMPTY_ACTION`: An action that does nothing.

### Example

```yql
DEFINE ACTION $hello_world($name, $suffix?) AS
    $name = $name ?? ($suffix ?? "world");
    SELECT "Hello, " || $name || "!";
END DEFINE;

DO EMPTY_ACTION();
DO $hello_world(NULL);
DO $hello_world("John");
DO $hello_world(NULL, "Earth");
```

## BEGIN .. END DO {#begin}

Performing an action without declaring it (anonymous action).

### Syntax {#syntax2}

1. `BEGIN`.
2. List of top-level expressions.
3. `END DO`.

An anonymous action can't include any parameters.

### Example {#example1}

```yql
DO BEGIN
    SELECT 1;
    SELECT 2 -- here and in the previous example, you might omit ';' before END
END DO
```
