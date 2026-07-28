---
title: "admin cluster bridge failover"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/bridge/failover?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/bridge/failover"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/bridge/failover.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/bridge/failover.md"
description: "Функциональность Корпоративной СУБД Яндекса. Данная функциональность доступна только в Корпоративной СУБД Яндекса. В open-source версии YDB она отсутствует."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster bridge failover

> [!NOTE]
> **Функциональность Корпоративной СУБД Яндекса**
>
> Данная функциональность доступна только в [Корпоративной СУБД Яндекса](../../../../downloads/yandex-enterprise-database.md). В open-source версии YDB она отсутствует.

С помощью команды `admin cluster bridge failover` можно выполнить [аварийное отключение](../../../../concepts/bridge.md#failover) pile, когда он недоступен. При необходимости можно указать pile, который станет новым `PRIMARY`.

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

Общий вид команды:

```bash
ydb [global options...] admin cluster bridge failover [options...]
```

- `global options` — [глобальные параметры](../global-options.md) CLI.
- `options` — [параметры подкоманды](failover.md#options).

Просмотр справки по команде:

```bash
ydb admin cluster bridge failover --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--pile <pile>` | Имя недоступного pile. |
| `--new-primary <pile>` | Имя pile, который должен стать новым `PRIMARY` pile. Укажите, если недоступный pile был `PRIMARY`. |

## Требования {#requirements}

- Если недоступен текущий `PRIMARY`, обязательно укажите `--new-primary` и выберите pile в состоянии `SYNCHRONIZED`. При отсутствии `--new-primary` или выборе pile в состоянии, отличном от `SYNCHRONIZED`, команда вернёт ошибку без каких‑либо изменений.
- Кластер не перейдёт в невалидное состояние: при нарушении требований команда ничего не изменяет и сообщает об ошибке.
- Если pile не вышел из строя, но его нужно отключить, используйте [плановое отключение](../../../../concepts/bridge.md#takedown) — команду [`takedown`](takedown.md).

## Примеры {#examples}

Выполнение аварийного отключения для недоступного pile под названием `pile-a`:

```bash
ydb admin cluster bridge failover --pile pile-a
```

Выполнение аварийного отключения для недоступного `PRIMARY` pile и назначение новым `PRIMARY` синхронизированного pile:

```bash
ydb admin cluster bridge failover --pile pile-a --new-primary pile-b
```

### Проверка результата {#verify}

С помощью команды [list](list.md) проверьте, что недоступный pile переведён в состояние `DISCONNECTED` и (если был указан `--new-primary`) выбран новый `PRIMARY` pile :

```bash
ydb admin cluster bridge list

pile-a: DISCONNECTED
pile-b: PRIMARY
```
