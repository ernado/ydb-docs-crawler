---
title: "GRANT"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/grant?version=v26.1"
doc_path: "ru/yql/reference/syntax/grant"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/grant.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/grant.md"
description: "Команда GRANT позволяет установить права доступа к объектам схемы для пользователя или группы пользователей. Синтаксис:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# GRANT

Команда `GRANT` позволяет установить права доступа к объектам схемы для пользователя или группы пользователей.

Синтаксис:

```yql
GRANT {{permission_name} [, ...] | ALL [PRIVILEGES]} ON {path_to_scheme_object [, ...]} TO {role_name [, ...]} [WITH GRANT OPTION]
```

- `permission_name` - имя права доступа к объектам схемы, которое нужно назначить.
- `path_to_scheme_object` - путь до объекта схемы, на который выдаются права.
- `role_name` - имя пользователя или группы, для которого выдаются права на объект схемы.

`WITH GRANT OPTION` - использование этой конструкции наделяет пользователя или группу пользователей правом управлять правами доступа - назначать или отзывать определенные права. Конструкция имеет функциональность аналогичную выдаче права `"ydb.access.grant"` или `GRANT`.  
 Субъект, обладающий правом `ydb.access.grant`, не может выдавать права шире, чем обладает сам на объекте доступа `path_to_scheme_object`.

## Права доступа {#permissions-list}

В качестве имён прав доступа можно использовать имена YDB прав или соответствующие им ключевые слова YQL.  
 В таблице ниже перечислены возможные имена прав.

| YDB право | Ключевое слово YQL | Описание |
| --- | --- | --- |
| Права уровня баз данных |  |  |
| `ydb.database.connect` | `CONNECT` | Право подключаться к базе данных |
| `ydb.database.create` | `CREATE` | Право создавать новые базы данных в кластере |
| `ydb.database.drop` | `DROP` | Право удалять базы данных в кластере |
| Элементарные права на объекты базы данных |  |  |
| `ydb.granular.select_row` | `SELECT ROW` | Право читать строки из таблицы (select), читать сообщения из топиков, использовать значения секретов |
| `ydb.granular.update_row` | `UPDATE ROW` | Право обновлять строки в таблице (insert, update, upsert, replace), писать сообщения в топики |
| `ydb.granular.erase_row` | `ERASE ROW` | Право удалять строки из таблицы (delete) |
| `ydb.granular.create_directory` | `CREATE DIRECTORY` | Право создавать и удалять директории, в том числе существующие и вложенные |
| `ydb.granular.create_table` | `CREATE TABLE` | Право создавать таблицы (в том числе индексные, внешние, колоночные), представления, последовательности |
| `ydb.granular.create_queue` | `CREATE QUEUE` | Право создавать топики |
| `ydb.granular.remove_schema` | `REMOVE SCHEMA` | Право удалять объекты (директории, таблицы, топики), которые были созданы посредством использования прав |
| `ydb.granular.describe_schema` | `DESCRIBE SCHEMA` | Право просмотра имеющихся прав доступа (ACL) на объект доступа, просмотра описания объектов доступа (директории, таблицы, топики) |
| `ydb.granular.alter_schema` | `ALTER SCHEMA` | Право изменять объекты доступа (директории, таблицы, топики), в том числе права пользователей на объекты доступа |
| Дополнительные флаги |  |  |
| `ydb.access.grant` | `GRANT` | Право предоставлять или отзывать права у других пользователей в объёме, не превышающем текущий объём прав пользователя на объекте доступа |
| Права, основанные на других правах |  |  |
| `ydb.tables.modify` | `MODIFY TABLES` | `ydb.granular.update_row` + `ydb.granular.erase_row` |
| `ydb.tables.read` | `SELECT TABLES` | Синоним `ydb.granular.select_row` |
| `ydb.generic.list` | `LIST` | Синоним `ydb.granular.describe_schema` |
| `ydb.generic.read` | `SELECT` | `ydb.granular.select_row` + `ydb.generic.list` |
| `ydb.generic.write` | `INSERT` | `ydb.granular.update_row` + `ydb.granular.erase_row` + `ydb.granular.create_directory` + `ydb.granular.create_table` + `ydb.granular.create_queue` + `ydb.granular.remove_schema` + `ydb.granular.alter_schema` |
| `ydb.generic.use_legacy` | `USE LEGACY` | `ydb.generic.read` + `ydb.generic.write` + `ydb.access.grant` |
| `ydb.generic.use` | `USE` | `ydb.generic.use_legacy` + `ydb.database.connect` |
| `ydb.generic.manage` | `MANAGE` | `ydb.database.create` + `ydb.database.drop` |
| `ydb.generic.full_legacy` | `FULL LEGACY` | `ydb.generic.use_legacy` + `ydb.generic.manage` |
| `ydb.generic.full` | `FULL` | `ydb.generic.use` + `ydb.generic.manage` |

- `ALL [PRIVILEGES]` - используется для указания всех возможных прав на объекты схемы для пользователей или групп. `PRIVILEGES` является необязательным ключевым словом, необходимым для совместимости с SQL стандартом.

> [!NOTE]
> Права `ydb.database.connect`, `ydb.granular.describe_schema`, `ydb.granular.select_row`, `ydb.granular.update_row` необходимо рассматривать как слои прав.
>
> Например, для изменения строк необходимо не только право `ydb.granular.update_row`, но и все вышележащие права.

## Примеры {#primery}

- Назначить право `ydb.generic.read` на таблицу `/shop_db/orders` для пользователя `user1`:

  ```yql
  GRANT 'ydb.generic.read' ON `/shop_db/orders` TO user1;
  ```

  Та же команда, с использованием ключевого слова

  ```yql
  GRANT SELECT ON `/shop_db/orders` TO user1;
  ```

- Назначить права `ydb.database.connect`, `ydb.generic.list` на корень базы `/shop_db` для пользователя `user2` и группы `group1`:

  ```yql
  GRANT LIST, CONNECT ON `/shop_db` TO user2, group1;
  ```

- Назначить право `ydb.generic.use` на таблицы `/shop_db/orders` и `/shop_db/sellers` для пользователей `user1@domain`, `user2@domain`:

  ```yql
  GRANT 'ydb.generic.use' ON `/shop_db/orders`, `/shop_db/sellers` TO `user1@domain`, `user2@domain`;
  ```

- Назначить все права на таблицу `/shop_db/sellers` для пользователя `admin_user`:

  ```yql
  GRANT ALL ON `/shop_db/sellers` TO admin_user;
  ```
