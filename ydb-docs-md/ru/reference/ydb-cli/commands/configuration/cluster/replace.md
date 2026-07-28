---
title: "admin cluster config replace"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/configuration/cluster/replace?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/configuration/cluster/replace"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/configuration/cluster/replace.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/configuration/cluster/replace.md"
description: "С помощью команды admin cluster config replace вы можете загрузить конфигурацию на кластер YDB. Внимание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster config replace

С помощью команды `admin cluster config replace` вы можете загрузить [конфигурацию](../../../../../devops/configuration-management/configuration-v2/index.md) на кластер YDB.

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

В зависимости от используемой кластером [версии конфигурации](../../../../../devops/configuration-management/compare-configs.md), команда заменяет:

- V1 — только [динамическую конфигурацию](../../../../../devops/configuration-management/configuration-v1/dynamic-config.md);
- V2 — всю конфигурацию.

Общий вид команды:

```bash
ydb [global options...] admin cluster config replace [options...]
```

- `global options` — глобальные параметры.
- `options` — [параметры подкоманды](replace.md#options).

Посмотрите описание команды замены конфигурации:

```bash
ydb admin cluster config replace --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `-f`, `--filename` | Путь к файлу, содержащему конфигурацию. |
| `--allow-unknown-fields` | Разрешить наличие неизвестных полей в конфигурации.<br>Если флаг не указан, наличие неизвестных полей в конфигурации приводит к ошибке. |
| `--ignore-local-validation` | Игнорировать базовую валидацию конфигурации на стороне клиента.<br>Если флаг не указан, YDB CLI проводит базовую валидацию конфигурации. |

## Примеры {#examples}

Загрузите файл конфигурации на кластер:

```bash
ydb admin cluster config replace --filename config.yaml
```

Загрузите файл конфигурации на кластер, игнорируя локальные проверки применимости:

```bash
ydb admin cluster config replace -f config.yaml --ignore-local-validation
```

Загрузите файл конфигурации на кластер, игнорируя проверку конфигурации на неизвестные поля:

```bash
ydb admin cluster config replace -f config.yaml --allow-unknown-fields
```
