---
title: "Получение списка фоновых операций"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/operation-list?version=v26.1"
doc_path: "ru/reference/ydb-cli/operation-list"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/operation-list.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/operation-list.md"
description: "С помощью подкоманды ydb operation list вы можете получить список фоновых операций указанного типа. Общий вид команды:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Получение списка фоновых операций

С помощью подкоманды `ydb operation list` вы можете получить список фоновых операций указанного типа.

Общий вид команды:

```bash
ydb [global options...] operation list [options...] <kind>
```

- `global options` — [глобальные параметры](commands/global-options.md).

- `options` — [параметры подкоманды](operation-list.md#options).

- `kind` — тип операции. Возможные значения:

  - `buildindex` — операции построения индекса;
  - `compaction` — операции компакшна таблиц;
  - `export/s3` — операции экспорта в S3;
  - `export/nfs` — операции экспорта на NFS;
  - `import/s3` — операции импорта из S3;
  - `import/nfs` — операции импорта с NFS;
  - `scriptexec` — операции выполнения скриптов;
  - `incbackup` — операции инкрементального резервного копирования;
  - `restore` — операции восстановления из резервной копии.

Посмотрите описание команды получения списка фоновых операций:

```bash
ydb operation list --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `-s`, `--page-size` | Количество операций на одной странице. Если список операций содержит больше строк, чем задано в параметре `--page-size`, то вывод будет разделен на несколько страниц. Для получения следующей страницы укажите параметр `--page-token`. |
| `-t`, `--page-token` | Токен страницы. |
| `--format` | Формат вывода.  <br>Значение по умолчанию — `pretty`.  <br>Возможные значения:<br>- `pretty` — человекочитаемый формат;<br>- `proto-json-base64` — вывод Protobuf в формате [JSON](https://ru.wikipedia.org/wiki/JSON), бинарные строки закодированы в [Base64](https://ru.wikipedia.org/wiki/Base64). |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Получите список фоновых операций построение индекса для таблицы `series`:

```bash
ydb -p quickstart operation list \
  buildindex
```

Результат:

```text
┌───────────────────────────────────────┬───────┬─────────┬───────┬──────────┬─────────────────────┬─────────────┐
| id                                    | ready | status  | state | progress | table               | index       |
├───────────────────────────────────────┼───────┼─────────┼───────┼──────────┼─────────────────────┼─────────────┤
| ydb://buildindex/7?id=281489389055514 | true  | SUCCESS | Done  | 100.00%  | /my-database/series | idx_release |
└───────────────────────────────────────┴───────┴─────────┴───────┴──────────┴─────────────────────┴─────────────┘

Next page token: 0
```
