---
title: "Команды управления конфигурацией кластера"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/configuration/cluster/?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/configuration/cluster/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/configuration/cluster/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/configuration/cluster/index.md"
description: "Команды управления конфигурацией кластера предназначены для работы с конфигурацией на уровне всего кластера YDB. Эти команды позволяют администраторам просматри"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Команды управления конфигурацией кластера

Команды управления конфигурацией кластера предназначены для работы с конфигурацией на уровне всего кластера YDB. Эти команды позволяют администраторам просматривать, изменять и управлять [настройками](../../../../configuration/index.md), которые применяются ко всем узлам кластера.

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

Общий синтаксис вызова команд управления конфигурацией кластера:

```bash
ydb [global options] admin cluster config [command options] <subcommand>
```

где:

- `ydb` — команда запуска YDB CLI из командной строки операционной системы;
- `[global options]` — глобальные опции, одинаковые для всех команд YDB CLI;
- `admin cluster config` — команда управления конфигурацией кластера;
- `[command options]` — опции команды, специфичные для каждой команды и подкоманды;
- `<subcommand>` — подкоманда.

## Команды {#list}

Ниже представлен список доступных подкоманд для управления конфигурацией кластера. Любую команду можно вызвать с опцией `--help` для получения справки по ней.

| Команда / подкоманда | Краткое описание |
| --- | --- |
| [admin cluster config fetch](fetch.md) | Получение текущей конфигурации (псевдонимы: `get`, `dump`) |
| [admin cluster config replace](replace.md) | Замена текущей конфигурации |
| [admin cluster config generate](generate.md) | Генерация [конфигурации V2](../../../../../devops/configuration-management/configuration-v2/index.md) из [конфигурации V1](../../../../../devops/configuration-management/configuration-v1/index.md) |
| admin cluster config vesion | Отображение версии конфигурации узлов (V1/V2) |
