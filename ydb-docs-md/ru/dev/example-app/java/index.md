---
title: "Приложение на Java"
url: "https://ydb.tech/docs/ru/dev/example-app/java/?version=v26.1"
doc_path: "ru/dev/example-app/java/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/example-app/java/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/example-app/java/index.md"
description: "На этой странице подробно разбирается код тестового приложения, доступного в составе Java SDK Examples YDB. Скачивание SDK Examples и запуск примера."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Приложение на Java

На этой странице подробно разбирается код [тестового приложения](https://github.com/ydb-platform/ydb-java-examples/tree/master/query-example), доступного в составе [Java SDK Examples](https://github.com/ydb-platform/ydb-java-examples) YDB.

## Скачивание SDK Examples и запуск примера {#download}

Приведенный ниже сценарий запуска использует [git](https://git-scm.com/downloads) и [Maven](https://maven.apache.org/download.html).

Создайте рабочую директорию и выполните в ней из командной строки команду клонирования репозитория с GitHub:

```bash
git clone https://github.com/ydb-platform/ydb-java-examples
```

Далее выполните сборку SDK Examples

```bash
mvn package -f ./ydb-java-examples
```

Далее из этой же рабочей директории выполните команду запуска тестового приложения, которая будет отличаться в зависимости от того, к какой базе данных необходимо подключиться.

{% list tabs %}

- Local Docker

  Для соединения с развернутой локальной базой данных YDB по сценарию [Docker](../../../quickstart.md) в конфигурации по умолчанию выполните следующую команду:

  ```bash
  YDB_ANONYMOUS_CREDENTIALS=1 java -jar ydb-java-examples/query-example/target/ydb-query-example.jar grpc://localhost:2136/local
  ```

- Любая база данных

  Для выполнения примера с использованием любой доступной базы данных YDB вам потребуется знать [эндпоинт](../../../concepts/connect.md#endpoint) и [путь базы данных](../../../concepts/connect.md#database).

  Если в базе данных включена аутентификация, то вам также понадобится выбрать [режим аутентификации](../../../security/authentication.md) и получить секреты - токен или логин/пароль.

  Выполните команду по следующему образцу:

  ```bash
  <auth_mode_var>="<auth_mode_value>" java -jar ydb-java-examples/query-example/target/ydb-query-example.jar grpcs://<endpoint>:<port>/<database>
  ```

  , где

  - `<endpoint>` - [эндпоинт](../../../concepts/connect.md#endpoint).
  - `<database>` - [путь базы данных](../../../concepts/connect.md#database).
  - `<auth_mode_var`> - [переменная окружения](../../../reference/ydb-sdk/auth.md#env), определяющая режим аутентификации.
  - `<auth_mode_value>` - значение параметра аутентификации для выбранного режима.

  Например:

  ```bash
  YDB_ACCESS_TOKEN_CREDENTIALS="..." java -jar ydb-java-examples/query-example/target/ydb-query-example.jar grpcs://ydb.example.com:2135/somepath/somelocation
  ```

{% endlist %}

## Инициализация соединения с базой данных {#init}

Для взаимодействия с YDB создается экземпляр драйвера, клиента и сессии:

- Драйвер YDB отвечает за взаимодействие приложения и YDB на транспортном уровне. Драйвер должен существовать на всем протяжении жизненного цикла работы с YDB и должен быть инициализирован перед созданием клиента и сессии.
- Клиент YDB работает поверх драйвера YDB и отвечает за работу с сущностями и транзакциями.
- Сессия YDB содержит информацию о выполняемых транзакциях и подготовленных запросах и содержится в контексте клиента YDB.

Основные параметры инициализации драйвера:

- Cтрока подключения с информацией об [эндпоинте](../../../concepts/connect.md#endpoint) и [базе данных](../../../concepts/connect.md#database). Единственный обязательный параметр.
- Провайдер [аутенфикации](../../../recipes/ydb-sdk/auth.md##auth-provider). В случае отсутствия прямого указания будет использоваться [анонимное подключение](../../../security/authentication.md).
- Настройки [пула сессий](../../../recipes/ydb-sdk/session-pool-limit.md).

Фрагмент кода приложения для инициализации драйвера:

```java
this.transport = GrpcTransport.forConnectionString(connectionString)
        .withAuthProvider(CloudAuthHelper.getAuthProviderFromEnviron())
        .build();
this.queryClient = QueryClient.newClient(transport).build();
```

Все операции с YDB [рекомендуется](../../../recipes/ydb-sdk/retry.md) выполнять с помощью класса-хелпера `SessionRetryContext`, который обеспечивает корректное повторное выполнение операции в случае частичной недоступности. Фрагмент кода для инициализации контекста ретраев:

```java
this.retryCtx = SessionRetryContext.create(queryClient).build();
```

## Создание строковых таблиц {#create-table}

Выполняется создание строковых таблиц, которые используются в дальнейших операциях тестового приложения. В результате исполнения шага в базе данных будут созданы строковые таблицы модели данных справочника сериалов:

- `series` - Сериалы
- `seasons` - Сезоны
- `episodes` - Эпизоды

После создания вызывается метод получения информации об объекте схемы данных, и выводится результат его выполнения.

Для создания таблиц используется режим транзакции `TxMode.NONE`, который позволяет выполнять схемные запросы:

```java
private void createTables() {
    retryCtx.supplyResult(session -> session.createQuery(""
            + "CREATE TABLE series ("
            + "  series_id UInt64,"
            + "  title Text,"
            + "  series_info Text,"
            + "  release_date Date,"
            + "  PRIMARY KEY(series_id)"
            + ")", TxMode.NONE).execute()
    ).join().getStatus().expectSuccess("Can't create table series");

    retryCtx.supplyResult(session -> session.createQuery(""
            + "CREATE TABLE seasons ("
            + "  series_id UInt64,"
            + "  season_id UInt64,"
            + "  title Text,"
            + "  first_aired Date,"
            + "  last_aired Date,"
            + "  PRIMARY KEY(series_id, season_id)"
            + ")", TxMode.NONE).execute()
    ).join().getStatus().expectSuccess("Can't create table seasons");

    retryCtx.supplyResult(session -> session.createQuery(""
            + "CREATE TABLE episodes ("
            + "  series_id UInt64,"
            + "  season_id UInt64,"
            + "  episode_id UInt64,"
            + "  title Text,"
            + "  air_date Date,"
            + "  PRIMARY KEY(series_id, season_id, episode_id)"
            + ")", TxMode.NONE).execute()
    ).join().getStatus().expectSuccess("Can't create table episodes");
}
```

## Запись данных {#write-queries}

Выполняется запись данных в созданные строковые таблицы с использованием команды [`UPSERT`](../../../yql/reference/syntax/upsert_into.md) языка запросов [YQL](../../../yql/reference/index.md). Применяется режим передачи запроса на изменение данных с автоматическим подтверждением транзакции в одном запросе к серверу.

Для выполнения YQL-запросов используется метод `QuerySession.createQuery()`. Он создаёт новый объект `QueryStream`, который позволяет выполнить запрос и подписаться на получение данных от сервера с результатами. Поскольку в запросах на запись никаких результатов не ожидается, используется метод `QueryStream.execute()` без параметров — он просто выполняет запрос и ждёт завершения стрима.  
 Фрагмент кода, демонстрирующий эту логику:

```java
private void upsertSimple() {
    String query
            = "UPSERT INTO episodes (series_id, season_id, episode_id, title) "
            + "VALUES (2, 6, 1, \"TBD\");";

    // Executes data query with specified transaction control settings.
    retryCtx.supplyResult(session -> session.createQuery(query, TxMode.SERIALIZABLE_RW).execute())
        .join().getValue();
```

## Получение выборки данных {#query-processing}

Выполняется запрос на получение выборки данных с использованием команды [`SELECT`](../../../yql/reference/syntax/select/index.md) языка запросов [YQL](../../../yql/reference/index.md). Демонстрируется обработка полученной выборки в приложении.

Прямое использование класса `QueryStream` для получения результатов не всегда может быть удобным — он подразумевает асинхронное получение данных от сервера через callback в методе `QueryStream.execute()`. Если ожидаемое количество строк в результате невелико, можно воспользоваться встроенным в SDK хелпером `QueryReader`, который сначала самостоятельно вычитывает все данные из стрима, а затем передаёт их пользователю в упорядоченном виде.

```java
private void selectSimple() {
    String query
            = "SELECT series_id, title, release_date "
            + "FROM series WHERE series_id = 1;";

    // Executes data query with specified transaction control settings.
    QueryReader result = retryCtx.supplyResult(
            session -> QueryReader.readFrom(session.createQuery(query, TxMode.SERIALIZABLE_RW))
    ).join().getValue();

    logger.info("--[ SelectSimple ]--");

    ResultSetReader rs = result.getResultSet(0);
    while (rs.next()) {
        logger.info("read series with id {}, title {} and release_date {}",
                rs.getColumn("series_id").getUint64(),
                rs.getColumn("title").getText(),
                rs.getColumn("release_date").getDate()
        );
    }
}
```

В результате исполнения запроса формируется объект класса `QueryReader`, который может содержать несколько выборок, получаемых методом `getResultSet( <index> )`. Так как запрос содержал только одну команду `SELECT`, то результат содержит только одну выборку под индексом `0`. Приведенный фрагмент кода при запуске выводит на консоль текст:

```bash
12:06:36.548 INFO  App - --[ SelectSimple ]--
12:06:36.559 INFO  App - read series with id 1, title IT Crowd and release_date 2006-02-03
```

## Параметризованные запросы {#param-queries}

Выполняется запрос к данным с использованием параметров. Этот вариант выполнения запросов является предпочтительным, так как позволяет серверу переиспользовать план исполнения запроса при последующих его вызовах, а также спасает от уязвимостей вида [SQL Injection](https://ru.wikipedia.org/wiki/%D0%92%D0%BD%D0%B5%D0%B4%D1%80%D0%B5%D0%BD%D0%B8%D0%B5_SQL-%D0%BA%D0%BE%D0%B4%D0%B0).

Фрагмент кода, приведенный ниже, демонстрирует использование параметризованных запросов и класс `Params` для формирования параметров и передачи их методу `QuerySession.createQuery`.

```java
private void selectWithParams(long seriesID, long seasonID) {
    String query
            = "DECLARE $seriesId AS Uint64; "
            + "DECLARE $seasonId AS Uint64; "
            + "SELECT sa.title AS season_title, sr.title AS series_title "
            + "FROM seasons AS sa INNER JOIN series AS sr ON sa.series_id = sr.series_id "
            + "WHERE sa.series_id = $seriesId AND sa.season_id = $seasonId";

    // Begin new transaction with SerializableRW mode
    TxControl txControl = TxControl.serializableRw().setCommitTx(true);

    // Type of parameter values should be exactly the same as in DECLARE statements.
    Params params = Params.of(
            "$seriesId", PrimitiveValue.newUint64(seriesID),
            "$seasonId", PrimitiveValue.newUint64(seasonID)
    );

    DataQueryResult result = retryCtx.supplyResult(session -> session.executeDataQuery(query, txControl, params))
            .join().getValue();

    logger.info("--[ SelectWithParams ] -- ");

    ResultSetReader rs = result.getResultSet(0);
    while (rs.next()) {
        logger.info("read season with title {} for series {}",
                rs.getColumn("season_title").getText(),
                rs.getColumn("series_title").getText()
        );
    }
}
```

## Асинхронное чтение {#async-requests}

Если ожидаемое количество данных от запроса велико, не следует пытаться загружать их полностью в оперативную память с помощью `QueryReader`. В таком случае лучше использовать более сложную логику, предусматривающую обработку результата по мере получения данных. Важно отметить, что здесь, как и раньше, используется `SessionRetryContext` для повторных попыток выполнения запроса при ошибках. Соответственно, необходимо учитывать, что чтение может быть прервано в любой момент, и в таком случае весь процесс выполнения запроса начнётся заново.

```java
private void asyncSelectRead(long seriesID, long seasonID) {
    String query
            = "DECLARE $seriesId AS Uint64; "
            + "DECLARE $seasonId AS Uint64; "
            + "SELECT ep.title AS episode_title, sa.title AS season_title, sr.title AS series_title "
            + "FROM episodes AS ep "
            + "JOIN seasons AS sa ON sa.season_id = ep.season_id "
            + "JOIN series AS sr ON sr.series_id = sa.series_id "
            + "WHERE sa.series_id = $seriesId AND sa.season_id = $seasonId;";

    // Type of parameter values should be exactly the same as in DECLARE statements.
    Params params = Params.of(
            "$seriesId", PrimitiveValue.newUint64(seriesID),
            "$seasonId", PrimitiveValue.newUint64(seasonID)
    );

    logger.info("--[ ExecuteAsyncQueryWithParams ]--");
    retryCtx.supplyResult(session -> {
        QueryStream asyncQuery = session.createQuery(query, TxMode.SNAPSHOT_RO, params);
        return asyncQuery.execute(part -> {
            ResultSetReader rs = part.getResultSetReader();
            logger.info("read {} rows of result set {}", rs.getRowCount(), part.getResultSetIndex());
            while (rs.next()) {
                logger.info("read episode {} of {} for {}",
                        rs.getColumn("episode_title").getText(),
                        rs.getColumn("season_title").getText(),
                        rs.getColumn("series_title").getText()
                );
            }
        });
    }).join().getStatus().expectSuccess("execute query problem");
}
```

## Многошаговые транзакции {#multistep-transactions}

Выполняется несколько команд в рамках одной многошаговой транзакции. Между выполнением запросов допустимо выполнение работы кода клиентского приложения. Использование транзакции позволяет гарантировать, что выполненные в её контексте выборки консистентны между собой.

Для обеспечения корректности совместной работы транзакций и контекста ретраев каждая транзакция должна выполняться целиком внутри callback, передаваемого в `SessionRetryContext`. Возврат из callback должен происходить после полного завершения транзакции.

Шаблон кода по использованию сложных транзакций в `SessionRetryContext`

```java
private void multiStepTransaction(long seriesID, long seasonID) {
    retryCtx.supplyStatus(session -> {
        QueryTransaction transaction = session.createNewTransaction(TxMode.SNAPSHOT_RO);

        //...

        return CompletableFuture.completedFuture(Status.SUCCESS);
    }).join().expectSuccess("multistep transaction problem");
}
```

Первый шаг — подготовка и выполнение первого запроса:

```java
    String query1
            = "DECLARE $seriesId AS Uint64; "
            + "DECLARE $seasonId AS Uint64; "
            + "SELECT MIN(first_aired) AS from_date FROM seasons "
            + "WHERE series_id = $seriesId AND season_id = $seasonId;";

    // Execute first query to start a new transaction
    QueryReader res1 = QueryReader.readFrom(transaction.createQuery(query1, Params.of(
            "$seriesId", PrimitiveValue.newUint64(seriesID),
            "$seasonId", PrimitiveValue.newUint64(seasonID)
    ))).join().getValue();
```

Затем мы можем выполнить некоторую клиентскую обработку полученных данных:

```java
    // Perform some client logic on returned values
    ResultSetReader resultSet = res1.getResultSet(0);
    if (!resultSet.next()) {
        throw new RuntimeException("not found first_aired");
    }
    LocalDate fromDate = resultSet.getColumn("from_date").getDate();
    LocalDate toDate = fromDate.plusDays(15);
```

И получить текущий `transaction id` для дальшейшей работы в рамках одной транзакции:

```java
    // Get active transaction id
    logger.info("started new transaction {}", transaction.getId());
```

Следующий шаг — создание следующего запроса, использующего результаты выполнения кода на стороне клиентского приложения:

```java
    // Construct next query based on the results of client logic
    String query2
            = "DECLARE $seriesId AS Uint64;"
            + "DECLARE $fromDate AS Date;"
            + "DECLARE $toDate AS Date;"
            + "SELECT season_id, episode_id, title, air_date FROM episodes "
            + "WHERE series_id = $seriesId AND air_date >= $fromDate AND air_date <= $toDate;";

    // Execute second query with commit at end.
    QueryReader res2 = QueryReader.readFrom(transaction.createQueryWithCommit(query2, Params.of(
        "$seriesId", PrimitiveValue.newUint64(seriesID),
        "$fromDate", PrimitiveValue.newDate(fromDate),
        "$toDate", PrimitiveValue.newDate(toDate)
    ))).join().getValue();

    logger.info("--[ MultiStep ]--");
    ResultSetReader rs = res2.getResultSet(0);
    while (rs.next()) {
        logger.info("read episode {} with air date {}",
                rs.getColumn("title").getText(),
                rs.getColumn("air_date").getDate()
        );
    }
```

Приведенные фрагменты кода при запуске выводят на консоль текст:

```bash
12:06:36.850 INFO  App - --[ MultiStep ]--
12:06:36.851 INFO  App - read episode Grow Fast or Die Slow with air date 2018-03-25
12:06:36.851 INFO  App - read episode Reorientation with air date 2018-04-01
12:06:36.851 INFO  App - read episode Chief Operating Officer with air date 2018-04-08
```

## Управление транзакциями {#tcl}

Выполняются вызовы операторов управления транзакциями [TCL](../../../concepts/transactions.md) - Begin и Commit.

В большинстве случаев вместо явного использования вызовов Begin и Commit лучше использовать параметры контроля транзакций в вызовах execute. Это позволит избежать лишних обращений к YDB и эффективней выполнять запросы.

Фрагмент кода, демонстрирующий явное использование вызовов `beginTransaction()` и `transaction.commit()`:

```java
private void tclTransaction() {
    retryCtx.supplyResult(session -> {
        QueryTransaction transaction = session.beginTransaction(TxMode.SERIALIZABLE_RW)
            .join().getValue();

        String query
                = "DECLARE $airDate AS Date; "
                + "UPDATE episodes SET air_date = $airDate WHERE title = \"TBD\";";

        Params params = Params.of("$airDate", PrimitiveValue.newDate(Instant.now()));

        // Execute data query.
        // Transaction control settings continues active transaction (tx)
        QueryReader reader = QueryReader.readFrom(transaction.createQuery(query, params))
            .join().getValue();

        logger.info("get transaction {}", transaction.getId());

        // Commit active transaction (tx)
        return transaction.commit();
    }).join().getStatus().expectSuccess("tcl transaction problem");
}
```
