---
title: "Тестовое приложение"
url: "https://ydb.tech/docs/ru/dev/example-app/?version=v26.1"
doc_path: "ru/dev/example-app/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/example-app/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/example-app/index.md"
description: "Тестовое приложение."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Тестовое приложение

В данном разделе разбирается код однотипного тестового приложения, реализованного с использованием YDB SDK на разных языках программирования:

- [C++](example-cpp.md)
- [С#](example-dotnet.md)
- [Go](go/index.md)
- [Java](java/index.md)
- [JavaScript](example-js.md)
- [Python](python/index.md)
- [Rust](rust/index.md)

Дополнительную информацию о том, как работают эти примеры приложений, можно найти в [справочной документации YDB SDK](../../reference/ydb-sdk/index.md).

Тестовое приложение выполняет следующие шаги:

## Инициализация соединения с базой данных {#init}

Для взаимодействия с YDB создается экземпляр драйвера, клиента и сессии:

- Драйвер YDB отвечает за взаимодействие приложения и YDB на транспортном уровне. Драйвер должен существовать на всем протяжении жизненного цикла работы с YDB и должен быть инициализирован перед созданием клиента и сессии.
- Клиент YDB работает поверх драйвера YDB и отвечает за работу с сущностями и транзакциями.
- Сессия YDB содержит информацию о выполняемых транзакциях и подготовленных запросах и содержится в контексте клиента YDB.

[C++](example-cpp.md#init) | [C#](example-dotnet.md#init) | [Go](go/index.md#init) | [Java](java/index.md#init) | JavaScript | [PHP](example-php.md#init) | [Python](python/index.md#init) | [Rust](rust/index.md#download)

## Создание строковых таблиц {#create-table}

Выполняется создание строковых таблиц, которые используются в дальнейших операциях тестового приложения. В результате исполнения шага в базе данных будут созданы строковые таблицы модели данных справочника сериалов:

- `series` - Сериалы
- `seasons` - Сезоны
- `episodes` - Эпизоды

После создания вызывается метод получения информации об объекте схемы данных, и выводится результат его выполнения.

[C++](example-cpp.md#create-table) | [C#](example-dotnet.md#create-table) | [Go](go/index.md#create-table) | [Java](java/index.md#create-table) | JavaScript | [PHP](example-php.md#create-table) | [Python](python/index.md#create-table) | [Rust](rust/index.md#query-client)

## Запись данных {#write-queries}

Выполняется запись данных в созданные строковые таблицы с использованием команды [`UPSERT`](../../yql/reference/syntax/upsert_into.md) языка запросов [YQL](../../yql/reference/index.md). Применяется режим передачи запроса на изменение данных с автоматическим подтверждением транзакции в одном запросе к серверу.

[C++](example-cpp.md#write-queries) | [C#](example-dotnet.md#write-queries) | Go | [Java](java/index.md#write-queries) | JavaScript | [PHP](example-php.md#write-queries) | [Python](python/index.md#write-queries) | [Rust](rust/index.md#query-client)

## Получение выборки данных {#query-processing}

Выполняется запрос на получение выборки данных с использованием команды [`SELECT`](../../yql/reference/syntax/select/index.md) языка запросов [YQL](../../yql/reference/index.md). Демонстрируется обработка полученной выборки в приложении.

[C++](example-cpp.md#query-processing) | [C#](example-dotnet.md#query-processing) | [Go](go/index.md#query-processing) | [Java](java/index.md#query-processing) | JavaScript | [PHP](example-php.md#query-processing) | [Python](python/index.md#query-processing) | [Rust](rust/index.md#query-client)

## Параметризованные запросы {#param-queries}

Выполняется запрос к данным с использованием параметров. Этот вариант выполнения запросов является предпочтительным, так как позволяет серверу переиспользовать план исполнения запроса при последующих его вызовах, а также спасает от уязвимостей вида [SQL Injection](https://ru.wikipedia.org/wiki/%D0%92%D0%BD%D0%B5%D0%B4%D1%80%D0%B5%D0%BD%D0%B8%D0%B5_SQL-%D0%BA%D0%BE%D0%B4%D0%B0).

[C++](example-cpp.md#param-queries) | [C#](example-dotnet.md#param-queries) | [Go](go/index.md#param-queries) | [Java](java/index.md#param-queries) | JavaScript | [PHP](example-php.md#param-queries) | [Python](python/index.md#param-queries) | [Rust](rust/index.md#query-client)

## Многошаговые транзакции {#multistep-transactions}

Выполняется несколько команд в рамках одной многошаговой транзакции. Между выполнением запросов допустимо выполнение работы кода клиентского приложения. Использование транзакции позволяет гарантировать, что выполненные в её контексте выборки консистентны между собой.

[C++](example-cpp.md#multistep-transactions) | C# | Go | [Java](java/index.md#multistep-transactions) | JavaScript | PHP | Python

## Управление транзакциями {#tcl}

Выполняются вызовы операторов управления транзакциями [TCL](../../concepts/transactions.md) - Begin и Commit.

В большинстве случаев вместо явного использования вызовов Begin и Commit лучше использовать параметры контроля транзакций в вызовах execute. Это позволит избежать лишних обращений к YDB и эффективней выполнять запросы.

[C++](example-cpp.md#tcl) | C# | Go | [Java](java/index.md#tcl) | JavaScript | PHP | [Python](python/index.md#tcl) | [Rust](rust/index.md#query-client)

## Обработка ошибок {#error-handling}

Подробно об обработке ошибок написано в разделе [Обработка ошибок в API](../../reference/ydb-sdk/error_handling.md).
