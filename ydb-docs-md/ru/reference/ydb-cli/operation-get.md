---
title: "Получение статуса фоновой операции"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/operation-get?version=v26.1"
doc_path: "ru/reference/ydb-cli/operation-get"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/operation-get.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/operation-get.md"
description: "С помощью подкоманды ydb operation get вы можете получить статус указанной фоновой операции. Общий вид команды:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Получение статуса фоновой операции

С помощью подкоманды `ydb operation get` вы можете получить статус указанной фоновой операции.

Общий вид команды:

```bash
ydb [global options...] operation get [options...] <id>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](operation-get.md#options).
- `id` — идентификатор фоновой операции. Идентификатор содержит символы, которые могут быть интерпретированы вашей командной оболочкой. При необходимости используйте экранирование, например `'<id>'` для bash.

Посмотрите описание команды получения статуса фоновой операции:

```bash
ydb operation get --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--format` | Формат вывода.  <br>Значение по умолчанию — `pretty`.  <br>Возможные значения:<br>- `pretty` — человекочитаемый формат;<br>- `proto-json-base64` — вывод Protobuf в формате [JSON](https://ru.wikipedia.org/wiki/JSON), бинарные строки закодированы в [Base64](https://ru.wikipedia.org/wiki/Base64). |

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Получите статус фоновой операции с идентификатором `ydb://buildindex/7?id=281489389055514`:

```bash
ydb -p quickstart operation get \
  'ydb://buildindex/7?id=281489389055514'
```

Результат:

```text
┌───────────────────────────────────────┬───────┬─────────┬───────┬──────────┬─────────────────────┬─────────────┐
| id                                    | ready | status  | state | progress | table               | index       |
├───────────────────────────────────────┼───────┼─────────┼───────┼──────────┼─────────────────────┼─────────────┤
| ydb://buildindex/7?id=281489389055514 | true  | SUCCESS | Done  | 100.00%  | /my-database/series | idx_release |
└───────────────────────────────────────┴───────┴─────────┴───────┴──────────┴─────────────────────┴─────────────┘
```
