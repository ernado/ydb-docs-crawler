---
title: "Список объектов"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/scheme-ls?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/scheme-ls"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/scheme-ls.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/scheme-ls.md"
description: "Список объектов. Команда scheme ls позволяет получить список схемных объектов в базе данных: ydb [connection options] scheme ls [path] [-lR1]."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Список объектов

Команда `scheme ls` позволяет получить список [схемных объектов](../../../concepts/glossary.md#scheme-object) в базе данных:

```bash
ydb [connection options] scheme ls [path] [-lR1]
```

, где `[connection options]` — опции [соединения с БД](../connect.md#command-line-pars)

При запуске без параметров выводится перечень имен объектов в корневой директории базы данных в сжатом формате.

Параметром `path` можно задать [директорию](dir.md), для которой нужно вывести перечень объектов.

Для команды доступны следующие опции:

- `-l` — полная информация об атрибутах каждого объекта;
- `-R` — рекурсивный обход всех поддиректорий;
- `-1` — выводить по одному объекту схемы на строку (например, для последующей обработки в скрипте).

## Примеры {#primery}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](../profile/create.md#quickstart).

- Получение объектов в корневой директории базы данных в сжатом формате

```bash
ydb --profile quickstart scheme ls
```

- Получение объектов во всех директориях базы данных в сжатом формате

```bash
ydb --profile quickstart scheme ls -R
```

- Получение объектов в заданной директории базы данных в сжатом формате

```bash
ydb --profile quickstart scheme ls dir1
ydb --profile quickstart scheme ls dir1/dir2
```

- Получение объектов во всех поддиректориях заданной директории базы данных в сжатом формате

```bash
ydb --profile quickstart scheme ls dir1 -R
ydb --profile quickstart scheme ls dir1/dir2 -R
```

- Получение полной информации по объектам в корневой директории базы данных

```bash
ydb --profile quickstart scheme ls -l
```

- Получение полной информации по объектам в заданной директории базы данных

```bash
ydb --profile quickstart scheme ls dir1 -l
ydb --profile quickstart scheme ls dir2/dir3 -l
```

- Получение полной информации по объектам во всех директориях базы данных

```bash
ydb --profile quickstart scheme ls -lR
```

- Получение полной информации по объектам во всех поддиректориях заданной директории базы данных

```bash
ydb --profile quickstart scheme ls dir1 -lR
ydb --profile quickstart scheme ls dir2/dir3 -lR
```
