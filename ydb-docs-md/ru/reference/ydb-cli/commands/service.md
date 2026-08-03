---
title: "Сервисные команды"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/service?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/service"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/service.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/service.md"
description: "Сервисные команды."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Сервисные команды

Данные команды относятся к самому клиентскому приложению YDB CLI и не предполагают установки соединения с БД. Они могут быть выражены как в виде параметра, так и в виде опции.

| Имя | Описание |
| --- | --- |
| `-?`, `-h`, `--help` | Вывод справки о синтаксисе YDB CLI |
| `version` | Вывод информации о версии YDB CLI (для публичных сборок) |
| `update` | Обновление YDB CLI до последней версии (для публичных сборок) |
| `config info` | Просмотр [параметров соединения](../connect.md) |
| `--license` | Показать лицензию (для публичных сборок) |
| `--credits` | Показать лицензии сторонних продуктов (для публичных сборок) |

Если неизвестно, является ли используемая сборка YDB CLI публичной, то уточнить поддержку той или иной сервисной команды в ней можно вызовом справки.
