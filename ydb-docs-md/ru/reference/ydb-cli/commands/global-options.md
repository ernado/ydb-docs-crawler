---
title: "Глобальные параметры"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/global-options?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/global-options"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/global-options.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/global-options.md"
description: "Опции соединения с БД. Опции соединения с БД описаны в статье Соединение с БД и аутентификация. Сервисные опции."
revision: "8c7501e02fd7c6de0c7110aafa90f78948400f1e"
---

# Глобальные параметры

## Опции соединения с БД {#connection-options}

Опции соединения с БД описаны в статье [Соединение с БД и аутентификация](../connect.md#command-line-pars).

## Сервисные опции {#service-options}

- `--profile <name>` — указывает на использование профиля соединения с БД с заданным именем при выполнении какой-либо команды YDB CLI. В профиле может быть сохранено большинство параметров соединения.
- `-v, --verbose` — вывод детальной информации обо всех выполняемых операциях. Указание данной опции полезно для локализации проблем при соединении с БД.
- `--profile-file` — использовать профили из указанного файла. По умолчанию используются профили из файла `~/.ydb/config/config.yaml`.
