---
title: "Команды управления кластером в режиме bridge"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/bridge/?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/bridge/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/bridge/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/bridge/index.md"
description: "Функциональность Корпоративной СУБД Яндекса. Данная функциональность доступна только в Корпоративной СУБД Яндекса. В open-source версии YDB она отсутствует."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Команды управления кластером в режиме bridge

> [!NOTE]
> **Функциональность Корпоративной СУБД Яндекса**
>
> Данная функциональность доступна только в [Корпоративной СУБД Яндекса](../../../../downloads/yandex-enterprise-database.md). В open-source версии YDB она отсутствует.

Команды управления кластером в режиме [bridge](../../../../concepts/bridge.md) позволяют просматривать состояние [pile](../../../../concepts/glossary.md#pile), выполнять плановую и аварийную смену PRIMARY, временно выводить pile на обслуживание и возвращать его в кластер.

> [!CAUTION]
> Команды из этого раздела могут нанести вред вашему кластеру при неправильном использовании. Из-за потенциально опасного характера этих команд **ВСЕ** глобальные параметры должны быть заданы явно. Профили отключены по умолчанию и используются только при явном указании (`--profile <имя-профиля>`). Некоторые команды не требуют глобальных опций, которые в противном случае являются обязательными.

Общий синтаксис вызова команд управления кластером в режиме bridge:

```bash
ydb [global options...] admin cluster bridge [command options...] <subcommand>
```

где:

- `ydb` — команда запуска YDB CLI из командной строки операционной системы;
- `[global options]` — глобальные параметры, одинаковые для всех команд YDB CLI;
- `admin cluster bridge` — команда управления конфигурацией кластера;
- `[command options]` — параметры команды, специфичные для каждой команды и подкоманды;
- `<subcommand>` — подкоманда.

## Команды {#list}

Ниже представлен список доступных подкоманд для управления кластером в режиме bridge. Любую команду можно вызвать с опцией `--help` для получения справки по ней.

| Команда / подкоманда | Краткое описание |
| --- | --- |
| [admin cluster bridge list](list.md) | Вывод состояния pile |
| [admin cluster bridge switchover](switchover.md) | Плановая смена `PRIMARY` |
| [admin cluster bridge failover](failover.md) | Аварийное переключение |
| [admin cluster bridge takedown](takedown.md) | Вывод pile из кластера |
| [admin cluster bridge rejoin](rejoin.md) | Возвращение pile в кластер |
