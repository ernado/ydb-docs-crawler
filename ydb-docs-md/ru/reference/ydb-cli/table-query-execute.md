---
title: "Выполнение запроса"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/table-query-execute?version=v26.1"
doc_path: "ru/reference/ydb-cli/table-query-execute"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/table-query-execute.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/table-query-execute.md"
description: "Важно. Данная команда устарела. Рекомендуемый инструмент для выполнения запросов в YDB CLI — это команда ydb sql."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Выполнение запроса

> [!WARNING]
> Данная команда устарела.
>  Рекомендуемый инструмент для выполнения запросов в YDB CLI — это команда [ydb sql](sql.md).

Подкоманда `table query execute` предназначена для надежного исполнения YQL-запросов. Подкоманда обеспечивает успешное исполнение запроса при кратковременной недоступности отдельных партиций таблиц, например, связанной с [их разделением или слиянием](../../concepts/datamodel/table.md#partitioning), за счет применения встроенных политик повторных попыток (retry policies).

Общий вид команды:

```bash
ydb [global options...] table query execute [options...]
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](table-query-execute.md#options).

Посмотрите описание команды выполнения YQL-запроса:

```bash
ydb table query execute --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--timeout` | Время, в течение которого должна быть выполнена операция на сервере. |
| `-t`, `--type` | Тип запроса.  <br> Возможные значения:<br>- `data` — YQL-запрос, содержащий [DML](https://ru.wikipedia.org/wiki/Data_Manipulation_Language) операции, допускает как изменение данных в базе, так и получение нескольких выборок с ограничением в 1000 строк в каждой выборке.<br>- `scan` — YQL-запрос типа [скан](../../concepts/query_execution/scan_query.md), допускает только чтение данных из базы, может вернуть только одну выборку, но без ограничения на количество записей в ней. Алгоритм исполнения запроса типа `scan` на сервере более сложный по сравнению с `data`, поэтому в отсутствие требований по возврату более 1000 строк эффективнее использовать тип запроса `data`.<br>- `scheme` — YQL-запрос, содержащий [DDL](https://ru.wikipedia.org/wiki/Data_Definition_Language) операции.<br>Значение по умолчанию — `data`. |
| `--stats` | Режим сбора статистики.  <br> Возможные значения:<br>- `none` — не собирать;<br>- `basic` — собирать по основным событиям;<br>- `full` — собирать по всем событиям.<br>Значение по умолчанию — `none`. |
| `-s` | Включить сбор статистики в режиме `basic`. |
| `--tx-mode` | [Режим транзакций](../../concepts/transactions.md#modes) (для запросов типа `data`).  <br> Возможные значения:<br>`serializable-rw` — результат успешно выполненных параллельных транзакций эквивалентен определенному последовательному порядку их выполнения;<br>`online-ro` — каждое из чтений в транзакции читает последние на момент своего выполнения данные;<br>`stale-ro` — чтения данных в транзакции возвращают результаты с возможным отставанием от актуальных (доли секунды).Значение по умолчанию — `serializable-rw`. |
| `-q`, `--query` | Текст YQL-запроса для выполнения. |
| `-f,` `--file` | Путь к файлу с текстом YQL-запроса для выполнения. |
| `--format` | Формат вывода.  <br> Возможные значения:<br>- `pretty` (по умолчанию) — человекочитаемый формат;<br>- `json-unicode` — вывод в формате [JSON](https://ru.wikipedia.org/wiki/JSON), бинарные строки закодированы в [юникод](https://ru.wikipedia.org/wiki/%D0%AE%D0%BD%D0%B8%D0%BA%D0%BE%D0%B4), каждая строка JSON выводится в отдельной строке;<br>- `json-unicode-array` — вывод в формате JSON, бинарные строки закодированы в Юникод, результат выводится в виде массива строк JSON, каждая строка JSON выводится в отдельной строке;<br>- `json-base64` — вывод в формате JSON, бинарные строки закодированы в [Base64](https://ru.wikipedia.org/wiki/Base64), каждая строка JSON выводится в отдельной строке;<br>- `json-base64-array` — вывод в формате JSON, бинарные строки закодированы в Base64, результат выводится в виде массива строк JSON, каждая строка JSON выводится в отдельной строке;<br>- `parquet`: вывод в формате [Apache Parquet](https://parquet.apache.org/docs/).<br>- `csv` — вывод в формате [CSV](https://ru.wikipedia.org/wiki/CSV);<br>- `tsv` — вывод в формате [TSV](https://ru.wikipedia.org/wiki/TSV). |

### Работа с параметризованными запросами {#parameterized-query}

Ниже приведена краткая справка, расширенное описание с примерами смотрите в статье [Выполнение параметризованных YQL-запросов и скриптов](parameterized-queries-cli.md).

| Имя | Описание |
| --- | --- |
| `-p, --param` | Значение одного параметра YQL-запроса в формате `$name=value`, где `$name` — имя параметра, а `value` — его значение (корректный [JSON value](https://www.json.org/json-ru.html)). |
| `--param-file` | Имя файла в формате [JSON](https://ru.wikipedia.org/wiki/JSON) в кодировке [UTF-8](https://ru.wikipedia.org/wiki/UTF-8), в котором заданы значения параметров, сопоставляемые с параметрами YQL-запроса по именам ключей. |
| `--input-format` | Формат представления значений параметров. Действует на все способы их передачи (через параметр команды, файл или `stdin`).  <br>Возможные значения:<br>- `json-unicode` (по умолчанию) — [JSON](https://ru.wikipedia.org/wiki/JSON).<br>- `json-base64` — [JSON](https://ru.wikipedia.org/wiki/JSON), в котором значения параметров с типом «бинарная строка» (`DECLARE $par AS String`) представлены в кодировке [Base64](https://ru.wikipedia.org/wiki/Base64). |
| `--stdin-format` | Формат представления параметров и фрейминг для `stdin`. Чтобы задать оба значения, укажите параметр дважды.  <br>**Формат представления параметров на `stdin`**  <br>Возможные значения:<br>- `json-unicode` — [JSON](https://ru.wikipedia.org/wiki/JSON).<br>- `json-base64` — [JSON](https://ru.wikipedia.org/wiki/JSON), в котором значения параметров с типом «бинарная строка» (`DECLARE $par AS String`) представлены в кодировке [Base64](https://ru.wikipedia.org/wiki/Base64).<br>- `raw` — бинарные данные, имя параметра задается опцией `--stdin-par`.<br>- `csv` — формат [CSV](https://ru.wikipedia.org/wiki/CSV).<br>- `tsv` — формат [TSV](https://ru.wikipedia.org/wiki/TSV).<br>Если формат представления параметров на `stdin` не задан, то применяется формат, заданный параметром `--input-format`.  <br>  <br>**Разделение наборов параметров (фрейминг) для `stdin`**  <br>Возможные значения:<br>- `no-framing` (по умолчанию) — фрейминг не применяется<br>- `newline-delimited` — символ перевода строки отмечает на `stdin` окончание одного набора параметров, отделяя его от следующего. |
| `--columns` | Строка с именами колонок, заменяющими header CSV/TSV документа, читаемого со stdin'а. Имена колонок должны быть в том же формате, что и сам документ. |
| `--skip-rows` | Число строк с начала данных, читаемых со stdin'a, которые нужно пропустить, не включая строку header'a. |
| `--stdin-par` | Имя параметра, значение которого будет передано через `stdin`, указывается без символа `$`. |
| `--batch` | Режим пакетирования значений наборов параметров, получаемых через `stdin`.  <br>Возможные значения:<br>- `iterative` (по умолчанию) — пакетирование выключено<br>- `full` - полный пакет<br>- `adaptive` - адаптивное пакетирование |
| `--batch-limit` | Максимальное количество наборов параметров в пакете для адаптивного режима пакетирования. Установка в `0` снимает ограничение.  <br>  <br>Значение по умолчанию — `1000`. |
| `--batch-max-delay` | Максимальная задержка отправки на обработку полученного набора параметров для адаптивного режима пакетирования. Задается в виде числа с размерностью времени - `s`, `ms`, `m`.  <br>  <br>Значение по умолчанию — `1s` (1 секунда). |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

### Создание таблиц {#examples-create-tables}

```bash
ydb -p quickstart table query execute \
  --type scheme \
  -q '
  CREATE TABLE series (series_id Uint64 NOT NULL, title Utf8, series_info Utf8, release_date Date, PRIMARY KEY (series_id));
  CREATE TABLE seasons (series_id Uint64, season_id Uint64, title Utf8, first_aired Date, last_aired Date, PRIMARY KEY (series_id, season_id));
  CREATE TABLE episodes (series_id Uint64, season_id Uint64, episode_id Uint64, title Utf8, air_date Date, PRIMARY KEY (series_id, season_id, episode_id));
  '
```

### Заполнение таблиц данными {#examples-upsert}

```bash
ydb -p quickstart table query execute \
  -q '
UPSERT INTO series (series_id, title, release_date, series_info) VALUES
  (1, "IT Crowd", Date("2006-02-03"), "The IT Crowd is a British sitcom produced by Channel 4, written by Graham Linehan, produced by Ash Atalla and starring Chris O'"'"'Dowd, Richard Ayoade, Katherine Parkinson, and Matt Berry."),
  (2, "Silicon Valley", Date("2014-04-06"), "Silicon Valley is an American comedy television series created by Mike Judge, John Altschuler and Dave Krinsky. The series focuses on five young men who founded a startup company in Silicon Valley.");

UPSERT INTO seasons (series_id, season_id, title, first_aired, last_aired) VALUES
    (1, 1, "Season 1", Date("2006-02-03"), Date("2006-03-03")),
    (1, 2, "Season 2", Date("2007-08-24"), Date("2007-09-28")),
    (2, 1, "Season 1", Date("2014-04-06"), Date("2014-06-01")),
    (2, 2, "Season 2", Date("2015-04-12"), Date("2015-06-14"));

UPSERT INTO episodes (series_id, season_id, episode_id, title, air_date) VALUES
    (1, 1, 1, "Yesterday'"'"'s Jam", Date("2006-02-03")),
    (1, 1, 2, "Calamity Jen", Date("2006-02-03")),
    (2, 1, 1, "Minimum Viable Product", Date("2014-04-06")),
    (2, 1, 2, "The Cap Table", Date("2014-04-13"));
'
```

### Простая выборка данных {#examples-simple-query}

```bash
ydb -p quickstart table query execute -q '
    SELECT season_id, episode_id, title
    FROM episodes
    WHERE series_id = 1
  '
```

Результат:

```text
┌───────────┬────────────┬───────────────────┐
| season_id | episode_id | title             |
├───────────┼────────────┼───────────────────┤
| 1         | 1          | "Yesterday's Jam" |
├───────────┼────────────┼───────────────────┤
| 1         | 2          | "Calamity Jen"    |
└───────────┴────────────┴───────────────────┘
```

### Неограниченная по размеру выборка для автоматизированной обработки {#examples-query-stream}

Выборка данных запросом, текст которого сохранен в файле, без ограничения на количество строк в выборке, с выводом в формате [Newline-delimited JSON stream](https://en.wikipedia.org/wiki/JSON_streaming).

Запишем текст запроса в файл `request1.yql`:

```bash
echo 'SELECT season_id, episode_id, title FROM episodes' > request1.yql
```

Выполним запрос:

```bash
ydb -p quickstart table query execute -f request1.yql --type scan --format json-unicode
```

Результат:

```text
{"season_id":1,"episode_id":1,"title":"Yesterday's Jam"}
{"season_id":1,"episode_id":2,"title":"Calamity Jen"}
{"season_id":1,"episode_id":1,"title":"Minimum Viable Product"}
{"season_id":1,"episode_id":2,"title":"The Cap Table"}
```

### Передача параметров {#examples-params}

Примеры исполнения параметризованных запросов, включая потоковое исполнение, приведены в статье [Передача параметров в команды исполнения YQL](parameterized-queries-cli.md).
