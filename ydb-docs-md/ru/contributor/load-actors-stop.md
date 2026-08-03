---
title: "Stop"
url: "https://ydb.tech/docs/ru/contributor/load-actors-stop?version=v26.1"
doc_path: "ru/contributor/load-actors-stop"
version: "v26.1"
lang: "ru"
source_path: "ru/core/contributor/load-actors-stop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/contributor/load-actors-stop.md"
description: "С помощью этой команды можно остановить всю или только указанную нагрузку. Параметры актора Параметр Описание. Tag."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Stop

С помощью этой команды можно остановить всю или только указанную нагрузку.

## Параметры актора {#options}

| Параметр | Описание |
| --- | --- |
| `Tag` | Тег нагружающего актора, который нужно остановить. Тег можно посмотреть в Embedded UI кластера. |
| `RemoveAllTags` | При значении параметра `True` будут остановлены все нагружающие акторы. |

## Примеры {#examples}

Следующая команда остановит нагрузку с тегом `123`:

```proto
Stop: {
    Tag: 123
}
```

Команда для остановки всей нагрузки:

```proto
Stop: {
    RemoveAllTags: true
}
```

> [!TIP]
> **Хотите присоединиться к команде разработки YDB?**
>
> Ознакомьтесь с разделами о [команде YDB и открытых вакансиях](https://ydb.tech/ru/careers/), а также о [возможностях для студентов](https://ydb.tech/ru/students/).
