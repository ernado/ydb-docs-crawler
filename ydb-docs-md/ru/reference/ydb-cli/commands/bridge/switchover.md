---
title: "admin cluster bridge switchover"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/bridge/switchover?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/bridge/switchover"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/bridge/switchover.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/bridge/switchover.md"
description: "Функциональность Корпоративной СУБД Яндекса. Данная функциональность доступна только в Корпоративной СУБД Яндекса. В open-source версии YDB она отсутствует."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster bridge switchover

> [!NOTE]
> **Функциональность Корпоративной СУБД Яндекса**
>
> Данная функциональность доступна только в [Корпоративной СУБД Яндекса](../../../../downloads/yandex-enterprise-database.md). В open-source версии YDB она отсутствует.

С помощью команды `admin cluster bridge switchover` выполняется плавное, плановое переключение указанного pile в состояние `PRIMARY` через промежуточное состояние `PROMOTED`. Подробнее см. [описание сценария](../../../../concepts/bridge.md#switchover).

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

Общий вид команды:

```bash
ydb [global options...] admin cluster bridge switchover [options...]
```

- `global options` — [глобальные параметры](../global-options.md) CLI.
- `options` — [параметры подкоманды](switchover.md#options).

Просмотр справки по команде:

```bash
ydb admin cluster bridge switchover --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--new-primary <pile>` | Имя pile, который должен стать новым PRIMARY. |

## Требования {#requirements}

- Целевой pile должен находиться в состоянии `SYNCHRONIZED`.

## Примеры {#examples}

Переключение pile `pile-b` из состояния `SYNCHRONIZED` в состояние `PRIMARY` через промежуточное состояние `PROMOTED`:

```bash
ydb admin cluster bridge switchover --new-primary pile-b
```

## Проверка результата {#verify}

Убедитесь, что спустя некоторое время (через несколько минут) состояния pile изменились корректно, с помощью команды [list](list.md):

```bash
ydb admin cluster bridge list

pile-a: SYNCHRONIZED
pile-b: PRIMARY
```
