---
title: "Apache Spark™"
url: "https://ydb.tech/docs/ru/integrations/query-engines/spark?version=v26.1"
doc_path: "ru/integrations/query-engines/spark"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/query-engines/spark.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/query-engines/spark.md"
description: "Apache Spark™ — распределённая система обработки данных с открытым исходным кодом, предназначенная для обработки больших объёмов данных. Она использует кеширова"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Apache Spark™

Apache Spark™ — распределённая система обработки данных с открытым исходным кодом, предназначенная для обработки больших объёмов данных. Она использует кеширование в оперативной памяти и обеспечивает оптимальное выполнение запросов для быстрого анализа данных любого размера. Предоставляется API для разработки на Java, Scala, Python и R, а также поддерживается повторное использование кода в различных сценариях: пакетная обработка, интерактивные запросы, аналитика в реальном времени, машинное обучение и обработка графов. Apache Spark™ может работать с YDB с помощью [YDB Spark Connector](https://github.com/ydb-platform/ydb-spark-connector) — специального модуля, предоставляющего реализацию основных примитивов Apache Spark™. Поддерживаются:

- Распределение операций по партициям таблиц YDB;
- Параллельная запись и чтение таблиц YDB;
- Автоматическое создание таблиц при их отсутствии.

> [!NOTE]
> Для более быстрой работы YDB Spark Connector может потребоваться увеличить объем памяти, доступной для каждого исполнителя Apache Spark™. Рекомендуется указывать 4 ГБ или больше на один [executor](https://spark.apache.org/docs/latest/configuration.html#application-properties).

## Где взять и как использовать {#usage}

Для использования YDB в Apache Spark™ необходимо добавить YDB Spark Connector в [драйвер Apache Spark™](https://spark.apache.org/docs/latest/cluster-overview.html). Это можно сделать несколькими способами:

- Загрузить коннектор напрямую из Maven Central с помощью опции `--packages`. Рекомендуется использовать последнюю опубликованную [версию](https://central.sonatype.com/artifact/tech.ydb.spark/ydb-spark-connector):

  {% list tabs %}

  - Spark Shell

    ```shell
    ~ $ spark-shell --master <master-url> --packages tech.ydb.spark:ydb-spark-connector-shaded:2.0.1 --conf spark.executor.memory=4g
    ```

  - PySpark

    ```shell
    ~ $ pyspark --master <master-url> --packages tech.ydb.spark:ydb-spark-connector-shaded:2.0.1 --conf spark.executor.memory=4g
    ```

  - Spark SQL

    ```shell
    ~ $ spark-sql --master <master-url> --packages tech.ydb.spark:ydb-spark-connector-shaded:2.0.1 --conf spark.executor.memory=4g
    ```

  {% endlist %}

- Скачать последнюю версию shaded-сборки (вариант коннектора, включающий все зависимости) из [GitHub](https://github.com/ydb-platform/ydb-spark-connector/releases) или [Maven Central](https://central.sonatype.com/artifact/tech.ydb.spark/ydb-spark-connector-shaded) и указать скачанный артефакт в опции `--jars`:

  {% list tabs %}

  - Spark Shell

    ```shell
    ~ $ spark-shell --master <master-url> --jars ~/Download/ydb-spark-connector-shaded-2.0.1.jar --conf spark.executor.memory=4g
    ```

  - PySpark

    ```shell
    ~ $ pyspark --master <master-url> --jars ~/Download/ydb-spark-connector-shaded-2.0.1.jar  --conf spark.executor.memory=4g
    ```

  - Spark SQL

    ```shell
    ~ $ spark-sql --master <master-url> --jars ~/Download/ydb-spark-connector-shaded-2.0.1.jar  --conf spark.executor.memory=4g
    ```

  {% endlist %}

- Также скачанную shaded-сборку можно скопировать в папку `jars` дистрибутива Apache Spark™. В таком случае никаких опций указывать не требуется.

### Работа через DataFrame API {#dataframe-api}

[DataFrame API](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html) позволяет работать с YDB в интерактивных `spark-shell` или `pyspark`, а также при написании кода на `Java`, `Scala` или `Python` для `spark-submit`.

Для создания `DataFrame` нужно указать формат `ydb`, передать набор [опций подключения](spark.md#connection-options) и путь к таблице YDB:

{% list tabs %}

- Scala

  ```scala
  val ydb_df = spark.read.format("ydb").options(<options>).load("<table-path>")
  ```

- Python

  ```python
  ydb_df = spark.read.format("ydb").options(<options>).load("<table-path>")
  ```

{% endlist %}

Для сохранения любого `DataFrame` в таблицу YDB аналогично нужно указать формат `ydb`, [опции подключения](spark.md#connection-options) и путь к таблице:

{% list tabs %}

- Scala

  ```scala
  any_dataframe.write.format("ydb").options(<options>).mode("append").save("<table-path>")
  ```

- Python

  ```python
  any_dataframe.write.format("ydb").options(<options>).mode("append").save("<table-path>")
  ```

{% endlist %}

> [!NOTE]
> При записи данных в YDB рекомендуется использовать режим `append`, который использует [пакетную загрузку данных](../../dev/batch-upload.md). Если указанная в методе `save()` таблица не существует, она будет создана в соответствии с опциями [автосоздания таблиц](spark.md#autocreate-options).

Более подробный пример приведён в разделе [Пример работы с YDB в spark-shell](spark.md#example-spark-shell).

### Работа через Catalog API {#catalog-api}

С помощью каталогов возможна работа с YDB в интерактивном режиме `spark-sql` или при выполнении SQL-запросов через метод `spark.sql`.  
 В этом случае для доступа к YDB нужно добавить каталог, указав следующие [опции Apache Spark™](https://spark.apache.org/docs/latest/configuration.html#spark-properties) (можно определить несколько каталогов с разными именами для разных баз данных YDB):

```properties
# Обязательный параметр типа каталога
spark.sql.catalog.<catalog_name>=tech.ydb.spark.connector.YdbCatalog
# Обязательный параметр url
spark.sql.catalog.<catalog_name>.url=<ydb-connection-url>
# Все остальные параметры не обязательны и указываются только при необходимости
spark.sql.catalog.<catalog_name>.<param-name>=<param-value>
```

После задания каталогов можно работать с таблицами YDB через стандартные SQL-запросы Apache Spark™. Обратите внимание, что в качестве разделителя в пути к таблице нужно использовать `.`:

```sql
SELECT * FROM <catalog_name>.<table-path> LIMIT 10;
```

Более подробный пример приведён в разделе [Пример работы с YDB в spark-sql](spark.md#example-spark-sql).

## Список параметров YDB Spark Connector {#options}

Поведение YDB Spark Connector настраивается с помощью опций, которые могут передаваться в виде одного набора с помощью метода `options` или указываться по одной с помощью метода `option`. При этом каждый `DataFrame` и даже каждая отдельная операция над `DataFrame` может иметь свой набор опций.

### Опции подключения {#connection-options}

- `url` — обязательный параметр с адресом подключения к YDB. Имеет вид `grpc[s]://<endpoint>:<port>/<database>[?<options>]`.
   Примеры использования:

  - Локальный Docker-контейнер с анонимной аутентификацией и без TLS:
    `grpc://localhost:2136/local`

  - Удалённый кластер, размещённый на собственном сервере:
    `grpcs://my-private-cluster:2135/Root/my-database?secureConnectionCertificate=~/myCertificate.cer`

  - Экземпляр облачной базы данных с токеном:
    `grpcs://ydb.my-cloud.com:2135/my_folder/test_database?tokenFile=~/my_token`

  - Экземпляр облачной базы данных с файлом сервисного аккаунта:
    `grpcs://ydb.my-cloud.com:2135/my_folder/test_database?saKeyFile=~/sa_key.json`

- `ca.text` — указывает значение [сертификата](../../concepts/connect.md#tls-cert) для установки TLS-соединения.

- `ca.file` — указывает путь к [сертификату](../../concepts/connect.md#tls-cert) для установки TLS-соединения. Может быть указан прямо в `url` в виде опции `secureConnectionCertificate`.

- `auth.use_env` — если указано `true`, используется режим аутентификации на основе [переменных среды окружения](../../reference/ydb-sdk/auth.md#env).

- `auth.use_metadata` — если указано `true`, используется режим аутентификации [Metadata](../../security/authentication.md#iam). Может быть указан прямо в `url` в виде опции `useMetadata`.

- `auth.login` и `auth.password` — логин и пароль для [статической аутентификации](../../security/authentication.md#static-credentials).

- `auth.token` — аутентификация с использованием указанного [Access Token](../../security/authentication.md#iam).

- `auth.token.file` — аутентификация с использованием [Access Token](../../security/authentication.md#iam) из указанного файла. Может быть указан прямо в `url` в виде опции `tokenFile`.

- `auth.sakey.text` — можно указать содержимое ключа для аутентификации [по ключу сервисного аккаунта](../../security/authentication.md#iam).

- `auth.sakey.file` — можно указать путь к файлу ключа для аутентификации [по ключу сервисного аккаунта](../../security/authentication.md#iam). Может быть указан прямо в `url` в виде опции `saKeyFile`.

### Опции автоматического создания таблиц {#autocreate-options}

> [!TIP]
> Если вам нужно настроить параметры таблицы, создайте её вручную заранее с помощью [CREATE TABLE](../../yql/reference/syntax/create_table/index.md) или измените их позже с помощью [ALTER TABLE](../../yql/reference/syntax/alter_table/index.md).

- `table.autocreate` — если указано `true`, то при записи в несуществующую таблицу она будет создана автоматически. По умолчанию включено.

- `table.type` — тип автоматически создаваемой таблицы. Возможные варианты:

  - `row` — для создания строчной таблицы (по умолчанию);
  - `column` — для создания колоночной таблицы;

- `table.primary_keys` — разделённый запятой список колонок для использования в качестве первичного ключа. При отсутствии этой опции для ключа будет автоматически создана новая колонка.

- `table.auto_pk_name` — имя колонки для автоматически создаваемого ключа. Эта колонка будет создана с типом `Utf8` и будет заполняться случайными [UUID v4](<https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)>) значениями. По умолчанию `_spark_key`.

## Пример работы с YDB в spark-shell и pyspark {#example-spark-shell}

В качестве примера покажем, как загрузить в YDB список всех постов StackOverflow за 2020 год. Эти данные доступны в виде Parquet-файла, расположенного по адресу [https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/parquet/posts/2020.parquet](https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/parquet/posts/2020.parquet):

{% list tabs %}

- Spark Shell

  ```shell
  ~ $ spark-shell --master <master-url> --packages tech.ydb.spark:ydb-spark-connector-shaded:2.0.1 --conf spark.executor.memory=4g
  Spark session available as 'spark'.
  Welcome to
        ____              __
      / __/__  ___ _____/ /__
      _\ \/ _ \/ _ `/ __/  '_/
    /___/ .__/\_,_/_/ /_/\_\   version 3.5.4
        /_/

  Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 17.0.15)
  Type in expressions to have them evaluated.
  Type :help for more information.
  ```

- PySpark

  ```shell
  ~ $ pyspark --master <master-url> --packages tech.ydb.spark:ydb-spark-connector-shaded:2.0.1 --conf spark.executor.memory=4g
  Welcome to
        ____              __
      / __/__  ___ _____/ /__
      _\ \/ _ \/ _ `/ __/  '_/
    /__ / .__/\_,_/_/ /_/\_\   version 3.5.4
        /_/

  Using Python version 3.10.12 (main, May 27 2025 17:12:29)
  SparkSession available as 'spark'.
  ```

{% endlist %}

Выведем схему файла с данными и посмотрим количество строк в нём:

{% list tabs %}

- Spark Shell

  ```shell
  scala> val so_posts2020 = spark.read.format("parquet").load("/home/username/2020.parquet")
  so_posts2020: org.apache.spark.sql.DataFrame = [Id: bigint, PostTypeId: bigint ... 20 more fields]

  scala> so_posts2020.printSchema
  root
  |-- Id: long (nullable = true)
  |-- PostTypeId: long (nullable = true)
  |-- AcceptedAnswerId: long (nullable = true)
  |-- CreationDate: timestamp (nullable = true)
  |-- Score: long (nullable = true)
  |-- ViewCount: long (nullable = true)
  |-- Body: binary (nullable = true)
  |-- OwnerUserId: long (nullable = true)
  |-- OwnerDisplayName: binary (nullable = true)
  |-- LastEditorUserId: long (nullable = true)
  |-- LastEditorDisplayName: binary (nullable = true)
  |-- LastEditDate: timestamp (nullable = true)
  |-- LastActivityDate: timestamp (nullable = true)
  |-- Title: binary (nullable = true)
  |-- Tags: binary (nullable = true)
  |-- AnswerCount: long (nullable = true)
  |-- CommentCount: long (nullable = true)
  |-- FavoriteCount: long (nullable = true)
  |-- ContentLicense: binary (nullable = true)
  |-- ParentId: binary (nullable = true)
  |-- CommunityOwnedDate: timestamp (nullable = true)
  |-- ClosedDate: timestamp (nullable = true)

  scala> so_posts2020.count
  res1: Long = 4304021
  ```

- PySpark

  ```shell
  >>> so_posts2020 = spark.read.format("parquet").load("/home/username/2020.parquet")
  >>> so_posts2020.printSchema()
  root
  |-- Id: long (nullable = true)
  |-- PostTypeId: long (nullable = true)
  |-- AcceptedAnswerId: long (nullable = true)
  |-- CreationDate: timestamp (nullable = true)
  |-- Score: long (nullable = true)
  |-- ViewCount: long (nullable = true)
  |-- Body: binary (nullable = true)
  |-- OwnerUserId: long (nullable = true)
  |-- OwnerDisplayName: binary (nullable = true)
  |-- LastEditorUserId: long (nullable = true)
  |-- LastEditorDisplayName: binary (nullable = true)
  |-- LastEditDate: timestamp (nullable = true)
  |-- LastActivityDate: timestamp (nullable = true)
  |-- Title: binary (nullable = true)
  |-- Tags: binary (nullable = true)
  |-- AnswerCount: long (nullable = true)
  |-- CommentCount: long (nullable = true)
  |-- FavoriteCount: long (nullable = true)
  |-- ContentLicense: binary (nullable = true)
  |-- ParentId: binary (nullable = true)
  |-- CommunityOwnedDate: timestamp (nullable = true)
  |-- ClosedDate: timestamp (nullable = true)

  >>> so_posts2020.count()
  4304021
  ```

{% endlist %}

Добавим к данному DataFrame новую колонку с годом и запишем всё это в колоночную таблицу YDB:

{% list tabs %}

- Spark Shell

  ```shell
  scala> val my_ydb = Map("url" -> "grpcs://ydb.my-host.net:2135/preprod/spark-test?tokenFile=~/.token")
  my_ydb: scala.collection.immutable.Map[String,String] = Map(url -> grpcs://ydb.my-host.net:2135/preprod/spark-test?tokenFile=~/.token)

  scala> so_posts2020.withColumn("Year", lit(2020)).write.format("ydb").options(my_ydb).option("table.type", "column").option("table.primary_keys", "Id").mode("append").save("stackoverflow/posts");
  ```

- PySpark

  ```shell
  >>> from pyspark.sql.functions import col,lit
  >>> my_ydb = {"url": "grpcs://ydb.my-host.net:2135/preprod/spark-test?tokenFile=~/.token"}
  >>> so_posts2020.withColumn("Year", lit(2020)).write.format("ydb").options(**my_ydb).option("table.type", "column").option("table.primary_keys", "Id").mode("append").save("stackoverflow/posts")
  ```

{% endlist %}

В итоге мы можем прочитать записанные данные из YDB и, например, подсчитать количество постов c подтверждённым ответом:

{% list tabs %}

- Spark Shell

  ```shell
  scala> val ydb_posts2020 = spark.read.format("ydb").options(my_ydb).load("stackoverflow/posts")
  ydb_posts2020: org.apache.spark.sql.DataFrame = [Id: bigint, PostTypeId: bigint ... 21 more fields]

  scala> ydb_posts2020.printSchema
  root
  |-- Id: long (nullable = false)
  |-- PostTypeId: long (nullable = true)
  |-- AcceptedAnswerId: long (nullable = true)
  |-- CreationDate: timestamp (nullable = true)
  |-- Score: long (nullable = true)
  |-- ViewCount: long (nullable = true)
  |-- Body: binary (nullable = true)
  |-- OwnerUserId: long (nullable = true)
  |-- OwnerDisplayName: binary (nullable = true)
  |-- LastEditorUserId: long (nullable = true)
  |-- LastEditorDisplayName: binary (nullable = true)
  |-- LastEditDate: timestamp (nullable = true)
  |-- LastActivityDate: timestamp (nullable = true)
  |-- Title: binary (nullable = true)
  |-- Tags: binary (nullable = true)
  |-- AnswerCount: long (nullable = true)
  |-- CommentCount: long (nullable = true)
  |-- FavoriteCount: long (nullable = true)
  |-- ContentLicense: binary (nullable = true)
  |-- ParentId: binary (nullable = true)
  |-- CommunityOwnedDate: timestamp (nullable = true)
  |-- ClosedDate: timestamp (nullable = true)
  |-- Year: integer (nullable = true)

  scala> ydb_posts2020.count
  res3: Long = 4304021

  scala> ydb_posts2020.filter(col("AcceptedAnswerId") > 0).count
  res4: Long = 843780
  ```

- PySpark

  ```shell
  >>> ydb_posts2020 = spark.read.format("ydb").options(**my_ydb).load("stackoverflow/posts")
  >>> ydb_posts2020.printSchema()
  root
  |-- Id: long (nullable = true)
  |-- PostTypeId: long (nullable = true)
  |-- AcceptedAnswerId: long (nullable = true)
  |-- CreationDate: timestamp (nullable = true)
  |-- Score: long (nullable = true)
  |-- ViewCount: long (nullable = true)
  |-- Body: binary (nullable = true)
  |-- OwnerUserId: long (nullable = true)
  |-- OwnerDisplayName: binary (nullable = true)
  |-- LastEditorUserId: long (nullable = true)
  |-- LastEditorDisplayName: binary (nullable = true)
  |-- LastEditDate: timestamp (nullable = true)
  |-- LastActivityDate: timestamp (nullable = true)
  |-- Title: binary (nullable = true)
  |-- Tags: binary (nullable = true)
  |-- AnswerCount: long (nullable = true)
  |-- CommentCount: long (nullable = true)
  |-- FavoriteCount: long (nullable = true)
  |-- ContentLicense: binary (nullable = true)
  |-- ParentId: binary (nullable = true)
  |-- CommunityOwnedDate: timestamp (nullable = true)
  |-- ClosedDate: timestamp (nullable = true)
  |-- Year: integer (nullable = true)

  >>> ydb_posts2020.count()
  4304021
  >>> ydb_posts2020.filter(col("AcceptedAnswerId") > 0).count()
  843780
  ```

{% endlist %}

## Пример работы с YDB в spark-sql {#example-spark-sql}

В качестве примера покажем, как загрузить в YDB список всех постов StackOverflow за 2020 год. Эти данные доступны в виде Parquet-файла, расположенного по адресу [https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/parquet/posts/2020.parquet](https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/parquet/posts/2020.parquet):

Для начала запустим `spark-sql` с настроенным каталогом `my_ydb`:

```shell
~ $ spark-sql --master <master-url> --packages tech.ydb.spark:ydb-spark-connector-shaded:2.0.1 \
     --conf spark.sql.catalog.my_ydb=tech.ydb.spark.connector.YdbCatalog \
     --conf spark.sql.catalog.my_ydb.url=grpcs://ydb.my-host.net:2135/preprod/spark-test \
     --conf spark.sql.catalog.my_ydb.auth.token.file=~/.token \
     --conf spark.executor.memory=4g
spark-sql (default)>
```

Просмотрим текущее содержимое подключенной базы данных и убедимся в отсутствии таблицы `stackoverflow/posts`:

```shell
spark-sql (default)> SHOW NAMESPACES FROM my_ydb;
stackoverflow
Time taken: 0.11 seconds, Fetched 1 row(s)
spark-sql (default)> SHOW TABLES FROM my_ydb.stackoverflow;
Time taken: 0.041 seconds
```

Подсчитаем количество строк в оригинальном файле:

```shell
spark-sql (default)> SELECT COUNT(*) FROM parquet.`/home/username/2020.parquet`;
4304021
```

Добавим новую колонку с годом и запишем всё это в таблицу YDB:

```shell
spark-sql (default)> CREATE TABLE my_ydb.stackoverflow.posts OPTIONS(table.primary_keys='Id') AS SELECT *, 2020 as Year FROM parquet.`/home/username/2020.parquet`;
Time taken: 85.225 seconds
```

Убедимся, что новая таблица появилась в базе данных YDB:

```shell
spark-sql (default)> SHOW TABLES FROM my_ydb.stackoverflow;
posts
Time taken: 0.07 seconds, Fetched 1 row(s)
spark-sql (default)> DESCRIBE TABLE my_ydb.stackoverflow.posts;
Id                    bigint
PostTypeId            bigint
AcceptedAnswerId      bigint
CreationDate          timestamp
Score                 bigint
ViewCount             bigint
Body                  binary
OwnerUserId           bigint
OwnerDisplayName      binary
LastEditorUserId      bigint
LastEditorDisplayName binary
LastEditDate          timestamp
LastActivityDate      timestamp
Title                 binary
Tags                  binary
AnswerCount           bigint
CommentCount          bigint
FavoriteCount         bigint
ContentLicense        binary
ParentId              binary
CommunityOwnedDate    timestamp
ClosedDate            timestamp
Year                  int
```

В итоге мы можем прочитать записанные данные из YDB и, например, подсчитать количество постов с подтверждённым ответом:

```shell
spark-sql (default)> SELECT COUNT(*) FROM my_ydb.stackoverflow.posts;
4304021
Time taken: 19.726 seconds, Fetched 1 row(s)
spark-sql (default)> SELECT COUNT(*) FROM my_ydb.stackoverflow.posts WHERE AcceptedAnswerId > 0;
843780
Time taken: 6.599 seconds, Fetched 1 row(s)
```
