---
title: "admin cluster bridge rejoin"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/bridge/rejoin?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/bridge/rejoin"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/bridge/rejoin.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/bridge/rejoin.md"
description: "Функциональность Корпоративной СУБД Яндекса. Данная функциональность доступна только в Корпоративной СУБД Яндекса. В open-source версии YDB она отсутствует."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster bridge rejoin

> [!NOTE]
> **Функциональность Корпоративной СУБД Яндекса**
>
> Данная функциональность доступна только в [Корпоративной СУБД Яндекса](../../../../downloads/yandex-enterprise-database.md). В open-source версии YDB она отсутствует.

С помощью команды `admin cluster bridge rejoin` можно [вернуть](../../../../concepts/bridge.md#rejoin) указанный pile в кластер после обслуживания или восстановления. После выполнения команды ожидается переход pile из состояния `DISCONNECTED` в состояние `NOT_SYNCHRONIZED`, последующая автоматическая синхронизация и переход в состояние `SYNCHRONIZED`.

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

Общий вид команды:

```bash
ydb [global options...] admin cluster bridge rejoin [options...]
```

- `global options` — глобальные параметры.
- `options` — [параметры подкоманды](rejoin.md#options).

Просмотр справки по команде:

```bash
ydb admin cluster bridge rejoin --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--pile <pile>` | Имя pile, который нужно вернуть в кластер. |

## Требования {#requirements}

- Pile перед возвращением должен быть в состоянии `DISCONNECTED`.

## Примеры {#examples}

Возврат pile `pile-a` из состояния `DISCONNECTED`:

```bash
ydb admin cluster bridge rejoin --pile pile-a
```

## Проверка результата {#verify}

Сразу после выполнения команды ожидается переход pile в состояние `NOT_SYNCHRONIZED`. Проверьте результат с помощью команды [list](list.md):

```bash
ydb admin cluster bridge list

pile-a: NOT_SYNCHRONIZED
pile-b: PRIMARY
```

После завершения синхронизации pile переходит в состояние `SYNCHRONIZED`:

```bash
ydb admin cluster bridge list

pile-a: SYNCHRONIZED
pile-b: PRIMARY
```
