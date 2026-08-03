---
title: "Проверка аутентификации"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/discovery-whoami?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/discovery-whoami"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/discovery-whoami.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/discovery-whoami.md"
description: "Проверка аутентификации. Информационная команда discovery whoami позволяет проверить, от имени какой учетной записи воспринимает запросы сервер:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Проверка аутентификации

Информационная команда `discovery whoami` позволяет проверить, от имени какой учетной записи воспринимает запросы сервер:

```bash
ydb [connection options] discovery whoami [-g]
```

, где `[connection options]` — опции [соединения с БД](../connect.md#command-line-pars)

В ответ выводится имя учетной записи (User SID) и, если указана опция `-g`, то информация о принадлежности учетной записи группам.

Если на сервере YDB не включена аутентификация (что может применяться, например, при самостоятельном локальном развертывании), то выполнение команды завершится с ошибкой.

Поддержка опции `-g` зависит от конфигурации сервера. Если она не включена, то вы будете получать в ответ `User has no groups` вне зависимости от фактического включения вашей учетной записи в какие-либо группы.

## Пример {#primer}

```bash
$ ydb -p quickstart discovery whoami -g
User SID: aje5kkjdgs0puc18976co@as

User has no groups
```
