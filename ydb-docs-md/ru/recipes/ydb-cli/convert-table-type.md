---
title: "Конвертация таблиц между строковой и колоночной ориентацией"
url: "https://ydb.tech/docs/ru/recipes/ydb-cli/convert-table-type?version=v26.1"
doc_path: "ru/recipes/ydb-cli/convert-table-type"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-cli/convert-table-type.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-cli/convert-table-type.md"
description: "YDB поддерживает два основных типа таблиц: строковые и колоночные. Выбранный тип таблицы определяет физическое представление данных на дисках, поэтому изменение"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Конвертация таблиц между строковой и колоночной ориентацией

YDB поддерживает два основных типа таблиц: [строковые](../../concepts/datamodel/table.md#row-oriented-tables) и [колоночные](../../concepts/datamodel/table.md#column-oriented-tables). Выбранный тип таблицы определяет физическое представление данных на дисках, поэтому изменение типа существующей таблицы невозможно. Однако вы можете создать новую таблицу другого типа и скопировать в неё данные. Этот рецепт состоит из следующих шагов:

1. [Подготовка новой таблицы](convert-table-type.md#prepare)
2. [Копирование данных](convert-table-type.md#copy)
3. [Переключение нагрузки](convert-table-type.md#switch) *(опционально)*

Эти инструкции предполагают, что исходная таблица является строковой, и целью является получение аналогичной колоночной таблицы; однако роли таблиц могут быть изменены на противоположные.

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](../../reference/ydb-cli/profile/create.md#quickstart).

## Подготовка новой таблицы {#prepare}

Возьмите копию исходной команды `CREATE TABLE`, использованной для создания исходной таблицы. Проделайте в этом запросе следующие изменения, чтобы создать файл с запросом `CREATE TABLE` для таблицы назначения:

1. Измените имя таблицы на желаемое новое имя.
2. Установите значение параметра `STORE` в `COLUMN`, чтобы сделать таблицу колоночной.

Запустите этот запрос (предполагается, что он сохранён в файле с именем `create_column_oriented_table.yql`):

```bash
$ ydb -p quickstart yql -f create_column_oriented_table.yql
```

<details>
<summary>Примеры схем тестовых таблиц и заполнения их данными</summary>

Исходная строковая таблица:

```yql
CREATE TABLE `row_oriented_table` (
    id Int64 NOT NULL,
    metric_a Double,
    metric_b Double,
    metric_c Double,
    PRIMARY KEY (id)
)
```

Колоночная таблица назначения:

```yql
CREATE TABLE `column_oriented_table` (
    id Int64 NOT NULL,
    metric_a Double,
    metric_b Double,
    metric_c Double,
    PRIMARY KEY (id)
)
PARTITION BY HASH(id)
WITH (STORE = COLUMN)
```

> [!NOTE]
> Обратитесь к документации для разработчиков приложений, чтобы узнать больше о [партицировании колоночных таблиц и выборе ключа их партицирования](../../dev/primary-key/column-oriented.md) (параметр `PARTITION BY`).

Заполнение исходной строковой таблицы случайными данными:

```yql
INSERT INTO `row_oriented_table` (id, metric_a, metric_b, metric_c)
SELECT
    id,
    Random(id + 1),
    Random(id + 2),
    Random(id + 3)
FROM (
    SELECT ListFromRange(1, 1000) AS id
) FLATTEN LIST BY id
```

</details>

## Копирование данных {#copy}

На данный момент рекомендуемый способ копирования данных между YDB таблицами разных типов — это экспорт и импорт:

1. Экспорт данных в локальную файловую систему:

   ```bash
   $ ydb -p quickstart dump -p row_oriented_table -o tmp_backup/
   ```

2. Импорт этих данных в другую таблицу YDB:

   ```bash
   $ ydb -p quickstart import file csv -p column_oriented_table tmp_backup/row_oriented_table/*.csv
   ```

Убедитесь, что у вас достаточно свободного места в файловой системе для хранения всех данных.

## Переключение нагрузки {#switch}

В настоящее время невозможно бесшовно заменить оригинальную таблицу на колоночную. Однако, при необходимости, вы можете постепенно переключить ваши запросы на работу с новой таблицей, заменив путь к оригинальной таблице в запросах на новый.

Если исходная таблица больше не нужна, её можно удалить с помощью `ydb -p quickstart table drop row_oriented_table` или `yql -p quickstart yql -s "DROP TABLE row_oriented_table"`.

## Смотрите также {#smotrite-takzhe}

- [YDB CLI](../../reference/ydb-cli/index.md)
- [YDB для разработчиков приложений](../../dev/index.md)
