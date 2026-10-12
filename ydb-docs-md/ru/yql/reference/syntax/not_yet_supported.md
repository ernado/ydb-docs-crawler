---
title: "Неподдерживаемые конструкции из классического SQL"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/not_yet_supported?version=v26.1"
doc_path: "ru/yql/reference/syntax/not_yet_supported"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/not_yet_supported.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/not_yet_supported.md"
description: "Коррелированные EXISTS и NOT EXISTS."
revision: "665607947c838b4f199a3b30499a54d29413ee4f"
---

# Неподдерживаемые конструкции из классического SQL

## Коррелированные EXISTS и NOT EXISTS {#not-exists}

`EXISTS` и `NOT EXISTS` можно использовать с некоррелированными подзапросами. Коррелированные подзапросы не поддерживаются. Для отбора строк по наличию или отсутствию совпадающих строк используйте `LEFT SEMI JOIN` или `LEFT ONLY JOIN`. Подробнее см. в разделе [Коррелированные подзапросы, EXISTS и NOT EXISTS](correlated-subqueries.md).

## INTERSECT и EXCEPT {#intersect-except}

YQL не поддерживает `INTERSECT` и `EXCEPT`.

## NATURAL JOIN

Доступный альтернативный вариант — явно перечислить совпадающие с обеих сторон колонки.

## NOW() / CURRENT_TIME() {#now}

Доступный альтернативный вариант — воспользоваться функциями [CurrentUtcDate, CurrentUtcDatetime и CurrentUtcTimestamp](../builtins/basic.md#current-utc).
