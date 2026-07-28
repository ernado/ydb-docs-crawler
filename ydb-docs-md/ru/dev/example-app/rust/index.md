---
title: "Пример приложения в Rust"
url: "https://ydb.tech/docs/ru/dev/example-app/rust/?version=v26.1"
doc_path: "ru/dev/example-app/rust/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/example-app/rust/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/example-app/rust/index.md"
description: "На этой странице подробно разбирается код тестового приложения, использующего YDB Rust SDK. Получение и запуск."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Пример приложения в Rust

На этой странице подробно разбирается код [тестового приложения](https://github.com/ydb-platform/ydb-rs-sdk/tree/master/ydb/examples/basic), использующего YDB [Rust SDK](https://github.com/ydb-platform/ydb-rs-sdk).

## Получение и запуск {#download}

Нужны [Git](https://git-scm.com/downloads) и [Rust](https://www.rust-lang.org/tools/install) 1.85+. Об установке SDK — см. [Установка SDK](../../../reference/ydb-sdk/install.md).

Клонируйте репозиторий:

```bash
git clone https://github.com/ydb-platform/ydb-rs-sdk.git
```

Запуск примера:

{% list tabs %}

- Локальный Docker

  Для подключения к локальной базе YDB в сценарии [Docker](../../../quickstart.md) выполните:

  ```bash
  export YDB_CONNECTION_STRING=grpc://localhost:2136/local
  cd ydb-rs-sdk/ydb
  cargo run --example basic
  ```

- Любая база

  Для запуска примера на любой доступной базе YDB укажите [endpoint](../../../concepts/connect.md#endpoint) и [путь к базе](../../../concepts/connect.md#database).

  Если включена аутентификация, выберите [режим аутентификации](../../../security/authentication.md) и задайте переменные окружения.

  ```bash
  export <auth_mode_var>="<auth_mode_value>"
  export YDB_CONNECTION_STRING="<endpoint>/<database>"
  cd ydb-rs-sdk/ydb
  cargo run --example basic
  ```

  где

  - `<endpoint>` — [endpoint](../../../concepts/connect.md#endpoint).
  - `<database>` — [путь к базе](../../../concepts/connect.md#database).
  - `<auth_mode_var>` — [переменная окружения](../../../reference/ydb-sdk/auth.md#env) для режима аутентификации.
  - `<auth_mode_value>` — значение учётных данных.

  Например:

  ```bash
  export YDB_ACCESS_TOKEN_CREDENTIALS="t1.9euelZqOnJuJlc..."
  export YDB_CONNECTION_STRING="grpcs://ydb.example.com:2135/somepath/somelocation"
  cd ydb-rs-sdk/ydb
  cargo run --example basic
  ```

{% endlist %}

## Инициализация соединения с базой данных {#init}

Для взаимодействия с YDB создается экземпляр драйвера, клиента и сессии:

- Драйвер YDB отвечает за взаимодействие приложения и YDB на транспортном уровне. Драйвер должен существовать на всем протяжении жизненного цикла работы с YDB и должен быть инициализирован перед созданием клиента и сессии.
- Клиент YDB работает поверх драйвера YDB и отвечает за работу с сущностями и транзакциями.
- Сессия YDB содержит информацию о выполняемых транзакциях и подготовленных запросах и содержится в контексте клиента YDB.

Импорт и инициализация клиента:

```rust
use ydb::{ClientBuilder, YdbResult};

#[tokio::main]
async fn main() -> YdbResult<()> {
    let connection_string = std::env::var("YDB_CONNECTION_STRING")
        .unwrap_or_else(|_| "grpc://localhost:2136/local".to_string());

    let client = ClientBuilder::new_from_connection_string(connection_string)?.client()?;
    client.wait().await?;

    let mut qc = client.query_client().clone_with_idempotent_operations(true);
    // ...
    Ok(())
}
```

`ClientBuilder::new_from_connection_string` принимает строку подключения (`grpc://host:port/database`). `client.wait()` ждёт discovery эндпоинтов. `query_client()` — вход в API Query Service.

Для локального Docker по умолчанию используется анонимная аутентификация. Для токена — [`ClientBuilder::with_credentials`](https://docs.rs/ydb/latest/ydb/struct.ClientBuilder.html), см. [рецепты аутентификации](../../../recipes/ydb-sdk/auth.md).

## Клиент Query Service {#query-client}

Одноразовые запросы — awaitable builders на [`QueryClient`](https://docs.rs/ydb/latest/ydb/struct.QueryClient.html):

- `qc.exec(yql)` — без результирующего набора (DDL, DML).
- `qc.query_row(yql)` — одна строка.
- `qc.query(yql).await?` — потоковый [`QueryStream`](https://docs.rs/ydb/latest/ydb/struct.QueryStream.html).

Повторы при ошибках: `clone_with_idempotent_operations(true)` для идемпотентных чтений и DDL.

## Создание строковых таблиц {#create-table}

Выполняется создание строковых таблиц, которые используются в дальнейших операциях тестового приложения. В результате исполнения шага в базе данных будут созданы строковые таблицы модели данных справочника сериалов:

- `series` - Сериалы
- `seasons` - Сезоны
- `episodes` - Эпизоды

После создания вызывается метод получения информации об объекте схемы данных, и выводится результат его выполнения.

Создание таблицы (implicit session, DDL без явного tx_control):

```rust
qc.exec(format!(
    "CREATE TABLE IF NOT EXISTS `{}` (
        series_id Bytes,
        title Text,
        series_info Text,
        release_date Date,
        comment Text,
        PRIMARY KEY(series_id)
    )",
    "native/query/series"
))
.await?;
```

## Запись данных {#write-queries}

Выполняется запись данных в созданные строковые таблицы с использованием команды [`UPSERT`](../../../yql/reference/syntax/upsert_into.md) языка запросов [YQL](../../../yql/reference/index.md). Применяется режим передачи запроса на изменение данных с автоматическим подтверждением транзакции в одном запросе к серверу.

Пакетная загрузка через `AS_TABLE`:

```rust
use ydb::{Value, ydb_struct};

let rows: Vec<Value> = /* ... */;
let list = Value::list_from(example_row, rows)?;
qc.exec("UPSERT INTO ... FROM AS_TABLE($seriesData);")
    .param("$seriesData", list)
    .await?;
```

## Получение выборки данных {#query-processing}

Выполняется запрос на получение выборки данных с использованием команды [`SELECT`](../../../yql/reference/syntax/select/index.md) языка запросов [YQL](../../../yql/reference/index.md). Демонстрируется обработка полученной выборки в приложении.

Чтение материализованного результата в режиме изоляции snapshot read-only:

```rust
use ydb::QueryTxMode;

let mut result = qc
    .query("SELECT series_id, title, release_date FROM `native/query/series`")
    .with_tx_mode(QueryTxMode::SnapshotReadOnly)
    .idempotent(true)
    .await?;

while let Some(result_set) = result.next_result_set().await? {
    for mut row in result_set {
        // извлечение колонок из row
    }
}
result.close().await?;
```

## Параметризованные запросы {#param-queries}

Выполняется запрос к данным с использованием параметров. Этот вариант выполнения запросов является предпочтительным, так как позволяет серверу переиспользовать план исполнения запроса при последующих его вызовах, а также спасает от уязвимостей вида [SQL Injection](https://ru.wikipedia.org/wiki/%D0%92%D0%BD%D0%B5%D0%B4%D1%80%D0%B5%D0%BD%D0%B8%D0%B5_SQL-%D0%BA%D0%BE%D0%B4%D0%B0).

Параметры задаются функцией `.param(name, value)` или макросом `ydb_params!`:

```rust
use ydb::ydb_params;

// по одному параметру
qc.exec("UPSERT INTO `native/query/series` (series_id, title) VALUES ($id, $title)")
    .param("$id", b"series-1".to_vec())
    .param("$title", "Example title")
    .await?;

// несколько параметров через макрос
qc.exec("UPSERT INTO `native/query/series` (series_id, title) VALUES ($id, $title)")
    .params(ydb_params!(
        "$id" => b"series-2".to_vec(),
        "$title" => "Another title",
    ))
    .await?;
```

## Управление транзакциями {#tcl}

Выполняются вызовы операторов управления транзакциями [TCL](../../../concepts/transactions.md) - Begin и Commit.

В большинстве случаев вместо явного использования вызовов Begin и Commit лучше использовать параметры контроля транзакций в вызовах execute. Это позволит избежать лишних обращений к YDB и эффективней выполнять запросы.

В Rust SDK явное управление транзакциями (через `Begin` и `Commit`) недоступно для клиентского кода. Вместо этого используйте `retry_transaction` с [`QueryTransactionOptions`](https://docs.rs/ydb/latest/ydb/struct.QueryTransactionOptions.html) для интерактивных транзакций. Для одиночного SQL-запроса режим изоляции задаётся через `.with_tx_mode(...)`.

Один запрос в режиме snapshot read-only:

```rust
use ydb::QueryTxMode;

let mut row = qc
    .query_row("SELECT title FROM `native/query/series` WHERE series_id = $id")
    .param("$id", b"series-1".to_vec())
    .with_tx_mode(QueryTxMode::SnapshotReadOnly)
    .idempotent(true)
    .await?;
```

Интерактивная транзакция с несколькими операциями:

```rust
use ydb::{QueryTransactionOptions, QueryTxMode};

let mut qc = qc.clone_with_transaction_options(
    QueryTransactionOptions::new().with_mode(QueryTxMode::SerializableReadWrite),
);

let title: String = qc
    .retry_transaction(async |tx| {
        let mut row = tx
            .query_row("SELECT title FROM `native/query/series` WHERE series_id = $id")
            .param("$id", b"series-1".to_vec())
            .await?;
        Ok(row.remove_field_by_name("title")?.try_into()?)
    })
    .await?;
```

По умолчанию для запросов на query-клиенте используется режим ImplicitTx, реальный режим изоляции определяет серверная сторона YDB.
