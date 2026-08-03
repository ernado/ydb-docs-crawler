---
title: "Удаление топика"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/topic-drop?version=v26.1"
doc_path: "ru/reference/ydb-cli/topic-drop"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/topic-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/topic-drop.md"
description: "С помощью подкоманды topic drop вы можете удалить созданный ранее топик. Примечание. При удалении топика также будут удалены все добавленные для него читатели."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Удаление топика

С помощью подкоманды `topic drop` вы можете удалить [созданный ранее](topic-create.md) топик.

> [!NOTE]
> При удалении топика также будут удалены все добавленные для него читатели.

Общий вид команды:

```bash
ydb [global options...] topic drop <topic-path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `topic-path` — путь топика.

Посмотрите описание команды удаления топика:

```bash
ydb topic drop --help
```

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Удалите [созданный ранее](topic-create.md) топик:

```bash
ydb -p quickstart topic drop my-topic
```
