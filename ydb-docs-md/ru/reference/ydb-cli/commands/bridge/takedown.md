---
title: "admin cluster bridge takedown"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/bridge/takedown?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/bridge/takedown"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/bridge/takedown.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/bridge/takedown.md"
description: "Функциональность Корпоративной СУБД Яндекса. Данная функциональность доступна только в Корпоративной СУБД Яндекса. В open-source версии YDB она отсутствует."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster bridge takedown

> [!NOTE]
> **Функциональность Корпоративной СУБД Яндекса**
>
> Данная функциональность доступна только в [Корпоративной СУБД Яндекса](../../../../downloads/yandex-enterprise-database.md). В open-source версии YDB она отсутствует.

С помощью команды `admin cluster bridge takedown` можно выполнить [плановое отключение](../../../../concepts/bridge.md#takedown) pile. Если отключается текущий `PRIMARY`, необходимо указать новый `PRIMARY`.

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

Общий вид команды:

```bash
ydb [global options...] admin cluster bridge takedown [options...]
```

- `global options` — глобальные параметры.
- `options` — [параметры подкоманды](takedown.md#options).

Просмотр справки по команде:

```bash
ydb admin cluster bridge takedown --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--pile <pile>` | Имя pile, который нужно аккуратно остановить. |
| `--new-primary <pile>` | Имя pile, который должен стать новым `PRIMARY`, если отключается текущий `PRIMARY`. |

## Требования {#requirements}

- Если отключается текущий `PRIMARY`, обязательно укажите `--new-primary` и выберите pile в состоянии `SYNCHRONIZED`.

## Примеры {#examples}

Вывод `SYNCHRONIZED` pile `pile-b` из кластера:

```bash
ydb admin cluster bridge takedown --pile pile-b
```

Вывод `PRIMARY` pile `pile-a` из кластера с переключением pile `pile-b` из состояния `SYNCHRONIZED` в состояние `PRIMARY`:

```bash
ydb admin cluster bridge takedown --pile pile-a --new-primary pile-b
```

## Проверка результата {#verify}

Проверьте итоговые состояния pile с помощью команды [list](list.md):

```bash
ydb admin cluster bridge list

pile-a: PRIMARY
pile-b: DISCONNECTED
```

Если отключался текущий `PRIMARY` с указанием `--new-primary`, убедитесь, что выбранный pile стал `PRIMARY`:

```bash
ydb admin cluster bridge list

pile-a: DISCONNECTED
pile-b: PRIMARY
```
