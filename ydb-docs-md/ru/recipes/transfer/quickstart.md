---
title: "Трансфер — быстрый старт"
url: "https://ydb.tech/docs/ru/recipes/transfer/quickstart?version=v26.1"
doc_path: "ru/recipes/transfer/quickstart"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/transfer/quickstart.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/transfer/quickstart.md"
description: "Эта статья поможет быстро начать работу с трансфером в YDB на простейшем модельном примере. В статье рассматриваются следующие шаги работы с трансфером:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Трансфер — быстрый старт

Эта статья поможет быстро начать работу с [трансфером](../../concepts/transfer.md) в YDB на простейшем модельном примере.

В статье рассматриваются следующие шаги работы с трансфером:

- [создание топика](quickstart.md#step1), из которого будет читать трансфер;
- [создание таблицы](quickstart.md#step2), в которую будут записываться данные;
- [создание трансфера](quickstart.md#step3);
- [заполнение топика данными](quickstart.md#step4);
- [проверка содержимого таблицы](quickstart.md#step5).

## Шаг 1. Создание топика {#step1}

Сначала нужно создать [топик](../../concepts/datamodel/topic.md) в YDB, из которого трансфер будет читать данные. Это можно сделать с помощью [SQL-запроса](../../yql/reference/syntax/create-topic.md):

```yql
CREATE TOPIC `transfer_recipe/source_topic`;
```

Топик `transfer_recipe/source_topic` позволяет передавать любые неструктурированные данные.

## Шаг 2. Создание таблицы {#step2}

После создания топика следует создать [таблицу](../../concepts/datamodel/table.md), в которую будут поступать данные из топика `source_topic`. Это можно сделать с помощью [SQL-запроса](../../yql/reference/syntax/create_table/index.md):

```yql
CREATE TABLE `transfer_recipe/target_table` (
  partition Uint32 NOT NULL,
  offset Uint64 NOT NULL,
  data String,
  PRIMARY KEY (partition, offset)
);
```

Таблица `transfer_recipe/target_table` имеет три столбца:

- `partition` — идентификатор [партиции](../../concepts/glossary.md#partition) топика, из которой получено сообщение;
- `offset` — [порядковый номер](../../concepts/glossary.md#offset), идентифицирующий сообщение внутри партиции;
- `data` — тело сообщения.

## Шаг 3. Создание трансфера {#step3}

После создания топика и таблицы нужно добавить [трансфер](../../concepts/transfer.md) данных, который будет переносить сообщения из топика в таблицу. Это можно сделать с помощью [SQL-запроса](../../yql/reference/syntax/create-transfer.md):

```yql
$transformation_lambda = ($msg) -> {
    return [
        <|
            partition: $msg._partition,
            offset: $msg._offset,
            data: $msg._data
        |>
    ];
};

CREATE TRANSFER `transfer_recipe/example_transfer`
  FROM `transfer_recipe/source_topic` TO `transfer_recipe/target_table`
  USING $transformation_lambda;
```

В этом примере:

- `$transformation_lambda` — это правило преобразования сообщения из топика в колонки таблицы. В данном случае сообщение из топика переносится в таблицу без изменений. Подробнее о настройке правил преобразования вы можете узнать в [документации](../../yql/reference/syntax/create-transfer.md#lambda);
- `$msg` — переменная, содержащая обрабатываемое сообщение из топика.

## Шаг 4. Заполнение топика данными {#step4}

После создания трансфера можно записать в топик сообщения, например, с помощью [YDB CLI](../../reference/ydb-cli/index.md).

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](../../reference/ydb-cli/profile/create.md#quickstart).

```bash
echo "Message 1" | ydb --profile quickstart topic write 'transfer_recipe/source_topic'
echo "Message 2" | ydb --profile quickstart topic write 'transfer_recipe/source_topic'
echo "Message 3" | ydb --profile quickstart topic write 'transfer_recipe/source_topic'
```

## Шаг 5. Проверка содержимого таблицы {#step5}

После записи сообщении в топик `source_topic` спустя некоторое время появятся записи в таблице `transfer_recipe/target_table`. Проверить их наличие можно с помощью [SQL-запроса](../../yql/reference/syntax/select/index.md):

```yql
SELECT *
FROM `transfer_recipe/target_table`;
```

Результат выполнения запроса:

| partition | offset | data |
| --- | --- | --- |
| 0 | 0 | Message 1 |
| 0 | 1 | Message 2 |
| 0 | 2 | Message 3 |

Строки в таблицу добавляются не для каждого сообщения, полученного из топика, а пакетно с буферизацией. По умолчанию данные записываются в таблицу каждые 60 секунд или при достижении объёма накопленных данных в 8 МБ. Эти параметры можно явно задать при [создании](../../yql/reference/syntax/create-transfer.md) трансфера или [изменить](../../yql/reference/syntax/alter-transfer.md) их позже.

## Заключение {#zaklyuchenie}

Данная статья приводит простой пример работы с трансфером: создание топика, таблицы и трансфера, записи в топик и проверки результата работы трансфера.

Эти примеры призваны проиллюстрировать синтаксис при работе с трансфером. Более реалистичный пример см. в [статье](nginx.md) описывающей поставку access лога NGINX.

См. также:

- [Трансфер данных](../../concepts/transfer.md)
- [Трансфер — поставка access-логов NGINX в таблицу](nginx.md)
