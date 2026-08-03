---
title: "Ещё не поддерживаемые конструкции из классического SQL"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/not_yet_supported?version=v26.1"
doc_path: "ru/yql/reference/syntax/not_yet_supported"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/not_yet_supported.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/not_yet_supported.md"
description: "[NOT] [EXISTS|INTERSECT|EXCEPT]."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Ещё не поддерживаемые конструкции из классического SQL

## \[NOT\] \[EXISTS|INTERSECT|EXCEPT\] {#not-exists}

Доступный альтернативный вариант — `EXISTS` синтаксически доступен, но из-за отсутствия поддержки коррелированных подзапросов не очень полезен. Также можно переписать через `JOIN`.

## NATURAL JOIN

Доступный альтернативный вариант — явно перечислить совпадающие с обеих сторон колонки.

## NOW() / CURRENT_TIME() {#now}

Доступный альтернативный вариант — воспользоваться функциями [CurrentUtcDate, CurrentUtcDatetime и CurrentUtcTimestamp](../builtins/basic.md#current-utc).
