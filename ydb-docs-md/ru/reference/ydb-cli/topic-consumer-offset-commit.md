---
title: "Сохранение позиции чтения"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/topic-consumer-offset-commit?version=v26.1"
doc_path: "ru/reference/ydb-cli/topic-consumer-offset-commit"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/topic-consumer-offset-commit.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/topic-consumer-offset-commit.md"
description: "Каждый читатель топика обладает позицией чтения. С помощью команды topic consumer offset commit можно сохранить позицию чтения добавленного ранее читателя."
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# Сохранение позиции чтения

Каждый читатель топика обладает [позицией чтения](../../concepts/datamodel/topic.md#consumer-offset).

С помощью команды `topic consumer offset commit` можно сохранить позицию чтения [добавленного ранее](topic-consumer-add.md) читателя.

Общий вид команды:

```bash
ydb [global options...] topic consumer offset commit [options...] <topic-path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](topic-consumer-offset-commit.md#options).
- `topic-path` — путь топика.

Посмотреть описание команды:

```bash
ydb topic consumer offset commit --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--consumer <значение>` | Имя читателя. |
| `--partition <значение>` | Номер партиции. |
| `--offset <значение>` | Устанавливаемое значение смещения. |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Установить для читателя с именем `my-consumer` смещение 123456789 в топике `my-topic` и партиции `1`:

```bash
ydb -p db1 topic consumer offset commit \
  --consumer my-consumer \
  --partition 1 \
  --offset 123456789 \
  my-topic
```
