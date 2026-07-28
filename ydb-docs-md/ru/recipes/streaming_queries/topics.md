---
title: "Быстрый старт: чтение и запись в топики"
url: "https://ydb.tech/docs/ru/recipes/streaming_queries/topics?version=v26.1"
doc_path: "ru/recipes/streaming_queries/topics"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/streaming_queries/topics.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/streaming_queries/topics.md"
description: "В этом руководстве вы создадите свой первый потоковый запрос. Запрос будет: читать события из входного топика; отбирать только ошибки;"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Быстрый старт: чтение и запись в топики

В этом руководстве вы создадите свой первый [потоковый запрос](../../concepts/streaming-query/streaming-query.md).

Запрос будет:

- читать события из входного [топика](../../concepts/datamodel/topic.md);
- отбирать только ошибки;
- подсчитывать количество ошибок по каждому серверу за 10 минут;
- записывать результат в выходной топик.

События поступают в формате JSON с полями: время, уровень логирования и имя сервера.

Вы выполните следующие шаги:

- [создание топиков](topics.md#step1);
- [создание внешнего источника данных](topics.md#step2);
- [создание потокового запроса](topics.md#step3);
- [просмотр состояния запроса](topics.md#step4);
- [заполнение входного топика данными](topics.md#step5);
- [проверка содержимого выходного топика](topics.md#step6);
- [удаление потокового запроса](topics.md#step7).

## Предварительные условия {#requirements}

Для выполнения примеров вам потребуется:

- запущенная база YDB — см. [quick start](../../quickstart.md);
- включённые флаги `enable_external_data_sources` и `enable_streaming_queries`.

{% list tabs %}

- Docker

  ```bash
  docker run -d --rm --name ydb-local -h localhost \
    --platform linux/amd64 \
    -p 2135:2135 -p 2136:2136 -p 8765:8765 -p 9092:9092 \
    -v $(pwd)/ydb_certs:/ydb_certs \
    -e GRPC_TLS_PORT=2135 -e GRPC_PORT=2136 -e MON_PORT=8765 \
    -e YDB_FEATURE_FLAGS=enable_external_data_sources,enable_streaming_queries \
    ydbplatform/local-ydb:25.4
  ```

- local_ydb

  ```bash
  ./local_ydb deploy \
    --ydb-working-dir=/absolute/path/to/working/directory \
    --ydb-binary-path=/path/to/kikimr/driver \
    --enable-feature-flag=enable_external_data_sources \
    --enable-feature-flag=enable_streaming_queries
  ```

{% endlist %}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](../../reference/ydb-cli/profile/create.md#quickstart).

## Шаг 1. Создание топиков {#step1}

Создайте входной и выходной [топики](../../concepts/datamodel/topic.md):

```sql
CREATE TOPIC input_topic;
CREATE TOPIC output_topic;
```

Проверьте, что топики созданы:

```bash
./ydb --profile quickstart scheme ls
```

## Шаг 2. Создание внешнего источника данных {#step2}

Создайте [внешний источник данных](../../concepts/datamodel/external_data_source.md) с помощью [CREATE EXTERNAL DATA SOURCE](../../yql/reference/syntax/create-external-data-source.md):

```sql
CREATE EXTERNAL DATA SOURCE ydb_source WITH (
    SOURCE_TYPE = "Ydb",
    LOCATION = "localhost:2136",
    DATABASE_NAME = "/local",
    AUTH_METHOD = "NONE"
);
```

> [!NOTE]
> Укажите значения `LOCATION` и `DATABASE_NAME`, соответствующие вашей базе YDB.

## Шаг 3. Создание потокового запроса {#step3}

Создайте [потоковый запрос](../../concepts/streaming-query/streaming-query.md) с помощью [CREATE STREAMING QUERY](../../yql/reference/syntax/create-streaming-query.md):

```sql
CREATE STREAMING QUERY query_example AS
DO BEGIN

$number_errors = SELECT
    Host,
    COUNT(*) AS ErrorCount,
    CAST(HOP_START() AS String) AS Ts  -- Время начала окна, соответствующего результату агрегации
FROM
    ydb_source.input_topic
WITH (
    FORMAT = json_each_row,
    SCHEMA = (
        Time String NOT NULL,
        Level String NOT NULL,
        Host String NOT NULL
    )
)
WHERE
    Level = "error"
GROUP BY
    HOP(CAST(Time AS Timestamp), "PT600S", "PT600S", "PT0S"),  -- Число ошибок на неперекрывающихся окнах длиной 10 минут
    Host;

INSERT INTO
    ydb_source.output_topic
SELECT
    ToBytes(Unwrap(Yson::SerializeJson(Yson::From(TableRow()))))  -- Сериализация всех колонок в JSON
FROM
    $number_errors;

END DO
```

Подробнее:

- Агрегация `GROUP BY HOP` и функция `HOP_START` — [GROUP BY ... HOP](../../yql/reference/syntax/select/group-by.md#group-by-hop).
- Запись данных в топик — [Форматы при записи данных](../../dev/streaming-query/streaming-query-formats.md#write_formats).
- Сериализация в JSON: [TableRow](../../yql/reference/builtins/basic.md#tablerow), [Yson::From](../../yql/reference/udf/list/yson.md#ysonfrom), [Yson::SerializeJson](../../yql/reference/udf/list/yson.md#ysonserializejson), [Unwrap](../../yql/reference/builtins/basic.md#unwrap), [ToBytes](../../yql/reference/builtins/basic.md#to-from-bytes).

## Шаг 4. Просмотр состояния запроса {#step4}

Проверьте состояние запроса через системную таблицу [streaming_queries](../../dev/system-views.md#streaming_queries):

```sql
SELECT
    Path,
    Status,
    Issues,
    Run
FROM
    `.sys/streaming_queries`
```

Убедитесь, что в поле `Status` значение `RUNNING`. В противном случае проверьте поле `Issues`.

Если запрос находится в статусе `SUSPENDED` или в поле `Issues` есть ошибки, обратитесь к разделу диагностика ошибок.

## Шаг 5. Заполнение входного топика данными {#step5}

Запишите тестовые сообщения в топик с помощью [YDB CLI](../../reference/ydb-cli/index.md):

```bash
echo '{"Time": "2025-01-01T00:00:00.000000Z", "Level": "error", "Host": "host-1"}' | ./ydb --profile quickstart topic write input_topic
echo '{"Time": "2025-01-01T00:04:00.000000Z", "Level": "error", "Host": "host-2"}' | ./ydb --profile quickstart topic write input_topic
echo '{"Time": "2025-01-01T00:08:00.000000Z", "Level": "error", "Host": "host-1"}' | ./ydb --profile quickstart topic write input_topic
echo '{"Time": "2025-01-01T00:12:00.000000Z", "Level": "error", "Host": "host-2"}' | ./ydb --profile quickstart topic write input_topic
echo '{"Time": "2025-01-01T00:12:00.000000Z", "Level": "error", "Host": "host-1"}' | ./ydb --profile quickstart topic write input_topic
```

Результат появится в выходном топике после закрытия 10-минутного окна агрегации.

## Шаг 6. Проверка содержимого выходного топика {#step6}

Прочитайте данные из выходного топика:

```bash
./ydb --profile quickstart topic read output_topic --partition-ids 0 --start-offset 0 --limit 10 --format newline-delimited
```

Ожидаемый результат:

```json
{"ErrorCount":1,"Host":"host-2","Ts":"2025-01-01T00:00:00Z"}
{"ErrorCount":2,"Host":"host-1","Ts":"2025-01-01T00:00:00Z"}
```

## Шаг 7. Удаление запроса {#step7}

Удалите запрос с помощью [DROP STREAMING QUERY](../../yql/reference/syntax/drop-streaming-query.md):

```sql
DROP STREAMING QUERY query_example;
```

## Что дальше {#next-steps}

- Изучите [форматы данных](../../dev/streaming-query/streaming-query-formats.md), поддерживаемые в потоковых запросах.
- Узнайте, как [обогащать данные справочником](../../dev/streaming-query/enrichment.md) из локальной таблицы или из S3.
- Научитесь [записывать результаты в таблицы](../../dev/streaming-query/table-writing.md).

## См. также {#sm-takzhe}

- [Потоковые запросы](../../concepts/streaming-query/streaming-query.md);
- [Форматы данных при чтении/записи из топиков](../../dev/streaming-query/streaming-query-formats.md).
