---
title: "Удаление читателя топика"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/topic-consumer-drop?version=v26.1"
doc_path: "ru/reference/ydb-cli/topic-consumer-drop"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/topic-consumer-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/topic-consumer-drop.md"
description: "С помощью команды topic consumer drop вы можете удалить добавленного ранее читателя. Общий вид команды:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Удаление читателя топика

С помощью команды `topic consumer drop` вы можете удалить [добавленного ранее](topic-consumer-add.md) читателя.

Общий вид команды:

```bash
ydb [global options...] topic consumer drop [options...] <topic-path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](topic-consumer-drop.md#options).
- `topic-path` — путь топика.

Посмотрите описание команды удаления читателя:

```bash
ydb topic consumer drop --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--consumer VAL` | Имя читателя, которого нужно удалить. |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Удалите [созданного ранее](topic-consumer-add.md) читателя с именем `my-consumer` для топика `my-topic`:

```bash
ydb -p quickstart topic consumer drop \
  --consumer my-consumer \
  my-topic
```
