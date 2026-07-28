---
title: "Директории"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/dir?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/dir"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/dir.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/dir.md"
description: "Директории. База данных YDB поддерживает внутри иерархическую структуру директорий, в которых могут размещаться объекты БД."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Директории

База данных YDB поддерживает внутри иерархическую структуру [директорий](../../../concepts/datamodel/dir.md), в которых могут размещаться объекты БД.

YDB CLI поддерживает операции изменения структуры директорий, а также указание директории при обращении к объектам схемы.

## Создание директории {#mkdir}

Команда `scheme mkdir` создает директории:

```bash
ydb [connection options] scheme mkdir <path>
```

, где `[connection options]` — опции [соединения с БД](../connect.md#command-line-pars)

В параметре `path` указывается относительный путь создаваемой директории от корня директорий базы данных. Будут созданы все директории на этом пути, которые не существовали до момента вызова команды.

Если конечная директория на пути уже существовала, то выполнение команды завершится успешно (код результата 0) с выдачей предупреждения о том, что никаких изменений не было произведено:

```text
Status: SUCCESS
Issues:
<main>: Error: dst path fail checks, path: /<database>/<path>: path exist, request accepts it,
pathId: [OwnerId: <some>, LocalPathId: <some>], path type: EPathTypeDir, path state: EPathStateNoChanges
```

Также поддерживается синтаксис указания полного пути, начинающегося с символа `/`, который должен в этом случае содержать в начале [путь базы данных](../../../concepts/connect.md#database), указанной в параметрах соединения, или с которой разрешаются операции через установленное соединение с кластером.

Примеры:

- Создание директории в корне базы данных

  ```bash
  ydb --profile quickstart scheme mkdir dir1
  ```

- Создание директорий на указанном пути от корня базы данных

  ```bash
  ydb --profile quickstart scheme mkdir dir1/dir2/dir3
  ```

## Удаление директории {#rmdir}

Команда `scheme rmdir` удаляет директорию:

```bash
ydb [global options...] scheme rmdir [options...] <path>
```

- `global options` — [глобальные параметры](global-options.md).
- `options` — [параметры подкоманды](dir.md#rmdir-options).
- `path` — путь до удаляемой директории.

Посмотрите описание команды для удаления директории:

```bash
ydb scheme rmdir --help
```

### Параметры подкоманды {#rmdir-options}

| Имя | Описание |
| --- | --- |
| `-r`, `--recursive` | Рекурсивное удаление директории вместе с дочерними объектами (поддиректориями, таблицами, топиками). При указании этого параметра по умолчанию будет запрошено подтверждение. |
| `-f`, `--force` | Не запрашивать никаких подтверждений. |
| `-i` | Запрашивать подтверждение на удаление каждого объекта. |
| `-I` | Однократно запросить подтверждение. |
| `--timeout <значение>` | Таймаут операции, мс. |

При попытке удалить непустую директорию без указания параметра `-r` или `--recursive` команда не будет выполнена с выдачей ошибки:

```text
Status: SCHEME_ERROR
Issues:
<main>: Error: path table fail checks, path: /<database>/<path>: path has children, request
doesn't accept it, pathId: [OwnerId: <some>, LocalPathId: <some>], path type:
EPathTypeDir, path state: EPathStateNoChanges, alive children: <count>
```

### Примеры {#rmdir-examples}

- Удаление пустой директории:

  ```bash
  ydb scheme rmdir dir1
  ```

- Удаление пустой директории с запросом подтверждения:

  ```bash
  ydb scheme rmdir -I dir1
  ```

- Рекурсивное удаление непустой директории с запросом подтверждения:

  ```bash
  ydb scheme rmdir -r dir1
  ```

- Рекурсивное удаление непустой директории без запроса подтверждения:

  ```bash
  ydb scheme rmdir -rf dir1
  ```

- Рекурсивное удаление непустой директории с запросом подтверждения на каждый объект:

  ```bash
  ydb scheme rmdir -ri dir1
  ```

## Использование директорий в других командах CLI {#use}

Во всех командах CLI, в которые передается параметром имя объекта, оно может быть указано с директорией, например в [`scheme describe`](scheme-describe.md):

```bash
ydb --profile quickstart scheme describe dir1/table_a
```

Команда [`scheme ls`](scheme-ls.md) поддерживает передачу пути к директории в качестве параметра:

```bash
ydb --profile quickstart scheme ls dir1/dir2
```

## Использование директорий в YQL {#yql}

Имена объектов в запросах на [языке YQL](../../../yql/reference/index.md) могут содержать путь к директории, где находится этот объект. Этот путь будет конкатенирован с базовым путем, задаваемым [прагмой `TablePathPrefix`](../../../yql/reference/syntax/pragma.md#table-path-prefix). Если прагма не указана, имя объекта разрешается относительно корня базы данных.

## Неявное создание директорий при импорте {#import}

При выполнении команды импорта данных создается дерево директорий по образцу каталога, из которого выполняется импорт.
