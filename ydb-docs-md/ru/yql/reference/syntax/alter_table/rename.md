---
title: "Переименование таблицы"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table/rename?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table/rename"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/rename.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/rename.md"
description: "ALTER TABLE old_table_name RENAME TO new_table_name; Примечание. При выборе имени для таблицы учитывайте общие правила именования схемных объектов."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Переименование таблицы

```yql
ALTER TABLE old_table_name RENAME TO new_table_name;
```

> [!NOTE]
> При выборе имени для таблицы учитывайте общие [правила именования схемных объектов](../../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

Если таблица с новым именем существует, будет возвращена ошибка. Возможность транзакционной подмены таблицы под нагрузкой поддерживается специализированными методами в CLI и SDK.

> [!WARNING]
> Если в YQL запросе содержится несколько команд `ALTER TABLE ... RENAME TO ...`, то каждая будет выполнена в режиме автокоммита в отдельной транзакции. С точки зрения внешнего процесса, таблицы будут переименованы последовательно одна за другой. Чтобы переименовать несколько таблиц в одной транзакции, используйте специализированные методы, доступные в CLI и SDK.

Переименование может использоваться для перемещения таблицы из одной директории внутри БД в другую, например:

```yql
ALTER TABLE `table1` RENAME TO `/backup/table1`;
```
