---
title: "Watermarks"
url: "https://ydb.tech/docs/ru/dev/streaming-query/watermarks?version=v26.1"
doc_path: "ru/dev/streaming-query/watermarks"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/streaming-query/watermarks.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/streaming-query/watermarks.md"
description: "Watermark — монотонно возрастающая нижняя оценка времён событий в потоке (подробнее о концепции: Watermarks ). В данном разделе описана настройка watermarks в п"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Watermarks

Watermark — монотонно возрастающая нижняя оценка времён событий в потоке (подробнее о концепции: [Watermarks](../../concepts/streaming-query/watermarks.md)). В данном разделе описана настройка watermarks в потоковых запросах YDB.

## Время события {#event-time}

В потоковой обработке каждое событие имеет временную метку, по которой система отслеживает прогресс времени в потоке. В текущей реализации источником времени события может быть только время записи события в [топик](../../concepts/datamodel/topic.md), доступное через системную колонку `__ydb_write_time`.

> [!NOTE]
> Поддержка произвольных выражений для извлечения времени из данных события (например, поля `event.created_at`) планируется в следующих версиях.

## Использование {#usage}

Watermark используется операциями, зависящими от прогресса времени события в потоке. В YDB к таким операциям относится оконная агрегация [HoppingWindow](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) — она определяет скользящие временные окна, по которым группируются события. При получении watermark `HoppingWindow` закрывает все окна, которые полностью покрыты этим значением.

## Вычисление watermark {#watermark-computation}

Когда система получает событие, она обновляет watermark — **продвигает** его вперёд по временной оси. Watermark вычисляется как `максимальное наблюдаемое время события − delay`, где `delay` — величина отставания, заданная в выражении [`WATERMARK`](watermarks.md#configuration) (например, `Interval("PT5S")` в `WATERMARK = __ydb_write_time - Interval("PT5S")`).

События в потоке могут приходить не в хронологическом порядке: событие с временем 10:00:03 может быть обработано после события с временем 10:00:05. Причины: расхождение часов в распределённой системе, сетевые задержки, неравномерная нагрузка на [партиции](../../concepts/datamodel/topic.md#partitioning) топика.

Параметр `delay` задаёт допустимый «запас» времени для событий, поступающих с задержкой. Например, при `delay` в 5 секунд событие с временем 00:00:48 будет принято, даже если уже пришли события с временем 00:00:50: watermark ещё не дошёл до 00:00:48. Если то же событие придёт позже, когда watermark уже продвинулся за 00:00:48, оно будет признано опоздавшим и отброшено.

О компромиссе между точностью и задержкой выдачи результатов: [Компромисс точности и задержки](../../concepts/streaming-query/watermarks.md#tradeoff).

## Простаивающие партиции {#idle-partitions}

Если входной топик содержит несколько [партиций](../../concepts/datamodel/topic.md#partitioning), каждая из них продвигает watermark независимо. Общий watermark запроса не обгоняет самую медленную партицию: окна не закрываются, пока хотя бы одна партиция не достигла соответствующего момента времени.

Если одна из партиций перестаёт получать данные, её watermark перестаёт продвигаться вперёд. Такая партиция называется простаивающей (idle). Пока простаивающая партиция учитывается при вычислении общего watermark, он тоже перестаёт продвигаться, и результаты не выдаются, несмотря на поступление данных от других партиций.

Чтобы избежать этой блокировки, простаивающая партиция исключается из вычисления общего watermark по истечении настраиваемого периода ожидания (параметр `WATERMARK_IDLE_TIMEOUT`, подробнее в разделе [Настройка](watermarks.md#configuration)).

## Настройка {#configuration}

Watermarks включаются и настраиваются в секции [WITH](../../yql/reference/syntax/select/with.md) при чтении из топика.

Параметры настройки:

- `WATERMARK` — выражение для вычисления [watermark](watermarks.md). Сейчас поддерживается только время записи в [топик](../../concepts/datamodel/topic.md) с константной задержкой. Формат: `__ydb_write_time - Interval("<delay>")`, где `<delay>` задаётся в формате [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations).
- `WATERMARK_GRANULARITY` — периодичность генерации watermarks. Чем она меньше, тем больше потребление CPU запросом и тем меньше задержка ответа. Имеет смысл только для [потоковых запросов](index.md). Задаётся в формате [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations). Значение по умолчанию — 1 секунда.
- `WATERMARK_IDLE_TIMEOUT` — период, после которого [простаивающая партиция](watermarks.md#idle-partitions) будет исключена из вычисления объединённого watermark. Имеет смысл только для [потоковых запросов](index.md). Задаётся в формате [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations). Значение по умолчанию — 5 секунд.

> [!WARNING]
> При использовании [HoppingWindow](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) первый параметр (time extractor) и источник времени в выражении WATERMARK должны совпадать. В текущей реализации оба должны использовать `__ydb_write_time`.

## Пример {#example}

Ниже приведён пример потокового запроса с watermark и оконной агрегацией. Запрос читает события из топика, фильтрует их по полю `pass` и агрегирует значения `payload` в окнах по 10 секунд с шагом 5 секунд. Watermark настроен с отставанием в 5 секунд.

### Входные данные {#vhodnye-dannye}

```json
{"pass": 1, "payload": "a"} // время записи: 1970-01-01T00:00:40Z
{"pass": 1, "payload": "b"} // время записи: 1970-01-01T00:00:42Z
{"pass": 0, "payload": "c"} // время записи: 1970-01-01T00:00:50Z
{"pass": 1, "payload": "d"} // время записи: 1970-01-01T00:00:40Z
```

### Запрос {#zapros}

```yql
CREATE STREAMING QUERY example AS
DO BEGIN
    $input = (
        SELECT
            t.*,
            __ydb_write_time AS ts
        FROM
            Input
        WITH (
            FORMAT = json_each_row,
            SCHEMA = (
                pass Int64,
                payload String
            ),
            WATERMARK = __ydb_write_time - Interval("PT5S")
        ) AS t
    );

    $output = (
        SELECT
            AGGREGATE_LIST(payload) AS result,
            CAST(HOP_END() AS String) AS ts
        FROM
            $input
        WHERE pass > 0
        GROUP BY
            HoppingWindow(ts, "PT5S", "PT10S")
    );

    INSERT INTO Output
    SELECT
        ToBytes(Unwrap(Yson2::SerializeJson(Yson::From(TableRow()))))
    FROM $output;
END DO;
```

Где:

- [`CREATE STREAMING QUERY`](../../yql/reference/syntax/create-streaming-query.md) — создаёт именованный потоковый запрос.
- `__ydb_write_time` — системная колонка, содержащая время записи события в [топик](../../concepts/datamodel/topic.md).
- `FORMAT = json_each_row` — [формат данных](streaming-query-formats.md) в топике, каждая строка содержит отдельный JSON-объект.
- `WATERMARK = __ydb_write_time - Interval("PT5S")` — watermark с отставанием 5 секунд. `Interval("PT5S")` задаёт интервал в формате [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations).
- [`AGGREGATE_LIST`](../../yql/reference/builtins/aggregation.md#agg-list) — агрегатная функция, собирающая значения в список.
- [`HOP_END()`](../../yql/reference/syntax/select/group-by.md#group-by-hop) — возвращает временную метку конца текущего окна.
- [`HoppingWindow(ts, "PT5S", "PT10S")`](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) — оконная функция с шагом 5 секунд и размером окна 10 секунд.

### Результат {#rezultat}

```json
{"result": ["a", "b"], "ts": "1970-01-01T00:00:45.000000Z"}
```

### Пояснение {#poyasnenie}

1. Первое событие (`"a"`, время записи 40с) проходит фильтр (`pass > 0`) и попадает в окна `[35; 45)` и `[40; 50)`. Watermark продвигается до 35с и не закрывает ни одного окна.
2. Второе событие (`"b"`, время записи 42с) аналогично попадает в окна `[35; 45)` и `[40; 50)`. Watermark продвигается до 37с.
3. Третье событие (`"c"`, время записи 50с) отбрасывается на фильтре (`pass = 0`). Несмотря на это, событие всё равно продвигает watermark до 45с. Watermark закрывает окно `[35; 45)` — результат `["a", "b"]` выдаётся.
4. Четвёртое событие (`"d"`, время записи 40с) не продвигает watermark: он уже находится на отметке 45с. Событие проходит фильтр, но отбрасывается как опоздавшее — его время записи (40с) меньше текущего watermark (45с). Хотя окно `[40; 50)` ещё открыто, watermark уже обещал, что событий с временем < 45с больше не будет, поэтому `d` не учитывается ни в одном из своих окон.

## См. также {#sm-takzhe}

- [GROUP BY ... HoppingWindow](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) — оконная функция, использующая watermarks.
- [WITH](../../yql/reference/syntax/select/with.md) — секция WITH для настройки параметров чтения из топика.
- [Гарантии доставки данных](guarantees.md) — гарантии доставки данных.
- [Чекпоинты](checkpoints.md) — механизм чекпоинтов.
