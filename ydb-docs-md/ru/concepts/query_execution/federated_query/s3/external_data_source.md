---
title: "Чтение из бакетов S3 через внешние источники данных"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/s3/external_data_source?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/s3/external_data_source"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/s3/external_data_source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/s3/external_data_source.md"
description: "Перед началом работы с S3 необходимо настроить подключение к хранилищу данных. Для этого существует DDL для настройки таких подключений. Далее рассмотрим SQL си"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Чтение из бакетов S3 через внешние источники данных

Перед началом работы с S3 необходимо настроить подключение к хранилищу данных. Для этого существует DDL для настройки таких подключений. Далее рассмотрим SQL синтаксис и управление этими настройками.

Бакеты в S3 бывают двух видов: публичные и приватные. Для подключения к публичному бакету необходимо использовать `AUTH_METHOD="NONE"`, а для подключения к приватному — `AUTH_METHOD="AWS"`. Подробное описание `AWS` можно найти [здесь](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-authentication-methods.html). `AUTH_METHOD="NONE"` означает, что аутентификация не требуется. В случае `AUTH_METHOD="AWS"` необходимо указать несколько дополнительных параметров:

- `AWS_ACCESS_KEY_ID_SECRET_PATH` — [секрет](../../../datamodel/secrets.md), в котором хранится `AWS_ACCESS_KEY_ID`.
- `AWS_SECRET_ACCESS_KEY_SECRET_PATH` — [секрет](../../../datamodel/secrets.md), в котором хранится `AWS_SECRET_ACCESS_KEY`.
- `AWS_REGION` — регион, из которого будет происходить чтение, например `ru-central-1`.

Для настройки соединения с публичным бакетом достаточно выполнить следующий SQL-запрос. Запрос создаст внешний источник данных с именем `s3_data_source`, который будет указывать на конкретный S3-бакет с именем `bucket`.

```yql
CREATE EXTERNAL DATA SOURCE s3_data_source WITH (
  SOURCE_TYPE="ObjectStorage",
  LOCATION="https://s3_storage_domain/bucket/",
  AUTH_METHOD="NONE"
);
```

Для настройки соединения с приватным бакетом необходимо выполнить несколько SQL-запросов. Сначала нужно создать [секреты](../../../datamodel/secrets.md), содержащие `AWS_ACCESS_KEY_ID` и `AWS_SECRET_ACCESS_KEY`.

```yql
CREATE SECRET aws_access_id WITH (value=<id>);
CREATE SECRET aws_access_key WITH (value=<key>);
```

Следующим шагом создаётся внешний источник данных с именем `s3_data_source`, который будет указывать на конкретный S3-бакет с именем `bucket`, а также использовать `AUTH_METHOD="AWS"`, для которого задаются параметры `AWS_ACCESS_KEY_ID_SECRET_PATH`, `AWS_SECRET_ACCESS_KEY_SECRET_PATH`, `AWS_REGION`. Значения этих параметров описаны выше.

```yql
CREATE EXTERNAL DATA SOURCE s3_data_source WITH (
  SOURCE_TYPE="ObjectStorage",
  LOCATION="https://s3_storage_domain/bucket/",
  AUTH_METHOD="AWS",
  AWS_ACCESS_KEY_ID_SECRET_PATH="aws_access_id",
  AWS_SECRET_ACCESS_KEY_SECRET_PATH="aws_access_key",
  AWS_REGION="ru-central-1"
);
```

## Использование внешнего источника данных для S3-бакета {#external-data-source-settings}

При работе с S3-совместимым хранилищем данных с помощью [внешних источников данных](../../../datamodel/external_data_source.md) можно выяснить свойства файлов в бакете S3 до создания [внешних таблиц](../../../datamodel/external_table.md):

- Быстро просмотреть файлы
- Проверить права доступа
- Проверить пути и параметры хранения данных

Пример запроса для чтения данных:

```yql
SELECT
  *
FROM
  s3_data_source.`*.tsv`
WITH
(
  FORMAT = "tsv_with_names",
  SCHEMA =
  (
    ts Uint32,
    action Utf8
  )
);
```

Список поддерживаемых форматов и алгоритмов сжатия данных для чтения из S3-совместимого хранилища данных приведен в разделе [Форматы данных и алгоритмы сжатия](formats.md).

## Модель данных {#data_model}

В S3 данные хранятся в файлах. Для чтения данных необходимо указать формат данных, сжатие, списки полей. Для этого используется следующее SQL-выражение:

```yql
SELECT
  <expression>
FROM
  <s3_external_datasource_name>.<file_path>
WITH
(
  FORMAT = "<file_format>",
  COMPRESSION = "<compression>",
  SCHEMA = (<schema_definition>),
  <format_settings>
)
WHERE
  <filter>;
```

Где:

- `s3_external_datasource_name` — название внешнего источника данных, ведущего на бакет с S3-совместимым хранилищем данных.
- `file_path` — путь к файлу или файлам внутри бакета. Поддерживаются подстановочные знаки `*`, `?`, `{ ... }`; подробнее [в разделе](external_data_source.md#path_format).
- `file_format` — [формат данных](formats.md#formats) в файлах, обязательно.
- `compression` — [формат сжатия](formats.md#compression_formats) файлов, опционально.
- `schema_definition` — [описание схемы хранимых данных](external_data_source.md#schema) в файлах, обязательно.
- `format_settings` — [параметры форматирования](external_data_source.md#format_settings), опционально.

### Описание схемы данных {#schema}

Описание схемы данных состоит из набора полей:

- Названия поля.
- Типа поля.
- Признака обязательности данных.

Например, схема данных ниже описывает поле схемы с названием `Year` типа `Int32` и требованием наличия этого поля в данных:

```text
Year Int32 NOT NULL
```

Если поле данных помечено как обязательное, `NOT NULL`, но это поле отсутствует в обрабатываемом файле, то работа с таким файлом будет завершена с ошибкой. Если поле помечено как необязательное, `NULL`, то при отсутствии поля в обрабатываемом файле ошибки не возникнет, но поле примет значение `NULL`. Ключевое слово `NULL` в необязательных полях является опциональным.

Список поддерживаемых типов данных, которые можно указать в схеме в зависимости от формата данных, приведён в разделе [Поддерживаемые типы данных](formats.md#types).

### Автоматический вывод схемы данных {#inference}

YDB может автоматически определять схему данных в файлах бакета, чтобы вам не пришлось указывать все поля схемы вручную.

> [!NOTE]
> Автоматический вывод схемы доступен для всех [форматов данных](formats.md#formats), кроме `raw` и `json_as_string`. Для этих форматов придётся [описывать схему данных вручную](external_data_source.md#schema).

Чтобы включить автоматический вывод схемы, используйте параметр `WITH_INFER`:

```yql
SELECT
  <expression>
FROM
  <s3_external_datasource_name>.<file_path>
WITH
(
  FORMAT = "<file_format>",
  COMPRESSION = "<compression>",
  WITH_INFER = "true"
)
WHERE
  <filter>;
```

Где:

- `s3_external_datasource_name` — название внешнего источника данных, ведущего на S3 бакет.
- `file_path` — путь к файлу или файлам внутри бакета. Поддерживаются подстановочные знаки `*`, `?`, `{ ... }`; подробнее [ниже](external_data_source.md#path_format).
- `file_format` — [формат данных](formats.md#formats) в файлах. Поддерживаются все форматы, кроме `raw` и `json_as_string`.
- `compression` — опциональный [формат сжатия](formats.md#compression_formats) файлов.

В результате выполнения такого запроса будут автоматически выведены названия и типы полей.

Ограничения для автоматического вывода схемы:

- Вывод схемы делается по данным только из одного произвольного непустого файла.
- Для форматов данных `csv_with_names`, `tsv_with_names`, `json_list`, `json_each_row` вывод схемы выполняется по первым 10 МБ данных из файла.
- Вывод схемы для файлов с форматом `parquet` возможен только в случае, если размер метаданных файла не превышает 10 МБ.
- Если файлы имеют разную схему, то запрос завершится с ошибкой парсинга данных в случае несовпадения типов колонок или пропуска не опциональных колонок.

### Форматы путей к данным {#path_format}

В YDB поддерживаются следующие пути к данным:

| Формат пути | Описание | Пример |
| --- | --- | --- |
| Путь завершается символом `/` | Путь к каталогу | Путь `/a/` адресует все содержимое каталога:  <br>`/a/b/c/d/1.txt`  <br>`/a/b/2.csv` |
| Путь содержит символ подстановки `?` | Файлы, имеющие путь с возможным отличием в одном символе | Путь `/a?c/1.csv` адресует файлы в каталогах:  <br>`/abc/1.csv`  <br>`/afc/1.csv`  <br>`/adc/1.csv` |
| Путь содержит символ макроподстановки `*` | Любые файлы, вложенные в путь | Путь `/a/*.csv` адресует файлы в каталогах:  <br>`/a/b/c/1.csv`  <br>`/a/2.csv`  <br>`/a/b/c/d/e/f/g/2.csv` |
| Путь содержит символы `{` и `}` | Файлы, имеющие путь, соответствующий одному из вариантов в фигурных скобках | Путь `/{a,b,c}/1.csv` адресует файлы в каталогах:  <br>`/a/1.csv`  <br>`/b/f.csv`  <br>`/c/1.csv` |
| Путь не завершается символом `/` и не содержит символов макроподстановок | Путь к отдельному файлу | Путь `/a/b.csv` адресует конкретный файл `/a/b.csv` |

Такие же значения можно использовать для параметра `file_pattern`.

### Параметры форматирования {#format_settings}

В YDB поддерживаются следующие параметры форматирования:

| Имя параметра | Описание | Принимаемые значения |
| --- | --- | --- |
| `file_pattern` | Шаблон имени файла | Строка шаблона имени. Поддерживаются подстановочные знаки `*`, `?`, `{ ... }`. |
| `data.interval.unit` | Единица измерения для парсинга типа `Interval` | `MICROSECONDS`, `MILLISECONDS`, `SECONDS`, `MINUTES`, `HOURS`, `DAYS`, `WEEKS` |
| `data.datetime.format_name` | Предопределенный формат, в котором записаны данные типа `Datetime` | `POSIX`, `ISO` |
| `data.datetime.format` | Шаблон, определяющий как записаны данные типа `Datetime` | Строка форматирования, например: `%Y-%m-%dT%H-%M` |
| `data.timestamp.format_name` | Предопределенный формат, в котором записаны данные типа `Timestamp` | `POSIX`, `ISO`, `UNIX_TIME_SECONDS`, `UNIX_TIME_MILLISECONDS`, `UNIX_TIME_MICROSECONDS` |
| `data.timestamp.format` | Шаблон, определяющий как записаны данные типа `Timestamp` | Строка форматирования, например: `%Y-%m-%dT%H-%M-%S` |
| `data.date.format` | Формат, в котором записаны данные типа `Date` | Строка форматирования, например: `%Y-%m-%d` |
| `csv_delimiter` | Разделитель данных в формате `csv_with_names` | Любой символ (UTF-8) |

Подробное описание поддерживаемых подстановочных знаков для параметра `file_pattern` приведено [выше](external_data_source.md#path_format). Параметр `file_pattern` можно использовать только в том случае, если `file_path` — путь к каталогу.

В строках форматирования для даты и времени можно использовать любые шаблонные переменные, поддерживаемые функцией [`strftime` (C99)](https://en.cppreference.com/w/c/chrono/strftime). В YDB поддерживаются следующие форматы типов `Datetime` и `Timestamp`:

| Имя | Описание | Пример |
| --- | --- | --- |
| `POSIX` | Строка формата `%Y-%m-%d %H:%M:%S` | 2001-03-26 16:10:00 |
| `ISO` | Формат, соответствующий стандарту [ISO 8601](https://ru.wikipedia.org/wiki/ISO_8601) | 2001-03-26 16:10:00Z |
| `UNIX_TIME_SECONDS` | Количество секунд, прошедших с 1 января 1970 года (00:00:00 UTC) | 985623000 |
| `UNIX_TIME_MILLISECONDS` | Количество миллисекунд, прошедших с 1 января 1970 года (00:00:00 UTC) | 985623000000 |
| `UNIX_TIME_MICROSECONDS` | Количество микросекунд, прошедших с 1 января 1970 года (00:00:00 UTC) | 985623000000000 |

## Пример {#read_example}

Пример запроса для чтения данных из S3-совместимого хранилища данных:

```yql
SELECT
  *
FROM
  external_source.`folder/`
WITH(
  FORMAT = "csv_with_names",
  COMPRESSION = "gzip"
  SCHEMA =
  (
    Id Int32 NOT NULL,
    UserId Int32 NOT NULL,
    TripDate Date NOT NULL,
    TripDistance Double NOT NULL,
    UserComment Utf8
  ),
  FILE_PATTERN = "*.csv.gz",
  `DATA.DATE.FORMAT` = "%Y-%m-%d",
  CSV_DELIMITER = "/"
);
```

Где:

- `external_source` — название внешнего источника данных, ведущего на бакет S3-совместимого хранилища данных.
- `folder/` — путь к папке с данными в бакете S3.
- `SCHEMA` — описание схемы данных в файле.
- `*.csv.gz` — шаблон имени файлов с данными.
- `%Y-%m-%d` — формат записи данных типа `Date` в S3.
