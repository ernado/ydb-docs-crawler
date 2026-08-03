---
title: "Получение информации о профиле"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/profile/list-and-get?version=v26.1"
doc_path: "ru/reference/ydb-cli/profile/list-and-get"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/profile/list-and-get.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/profile/list-and-get.md"
description: "Получение информации о профиле Получение списка профилей. Получение списка профилей: ydb config profile list."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Получение информации о профиле

## Получение списка профилей {#list}

Получение списка профилей:

```bash
ydb config profile list
```

Если существует текущий [активированный профиль](activate.md), он будет помечен как `(active)` в выведенном списке, например:

```text
prod
test (active)
local
```

## Получение подробной информации о профиле {#get}

Получение параметров, сохраненных в заданном профиле:

```bash
ydb config profile get <profile_name>
```

Например:

```bash
$ ydb config profile get local1
  endpoint: grpcs://ydb.serverless.yandexcloud.net:2135
  database: /rul1/b1g8skp/etn02099
  sa-key-file: /Users/username/secrets/sa_key_test.json
```

## Получение профилей с содержимым {#get-all}

Полная информация по всем профилям и сохраненным в них параметрам:

```bash
ydb config profile list --with-content
```

Вывод данной команды объединяет вывод команды получения списка (с пометкой активного профиля) и параметров каждого профиля в следующих строках после его имени.
