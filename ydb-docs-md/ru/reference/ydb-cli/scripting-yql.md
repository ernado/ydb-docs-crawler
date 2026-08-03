---
title: "Выполнение скрипта"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/scripting-yql?version=v26.1"
doc_path: "ru/reference/ydb-cli/scripting-yql"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/scripting-yql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/scripting-yql.md"
description: "Важно. Данная команда устарела. Рекомендуемый инструмент для выполнения запросов в YDB CLI — это команда ydb sql."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Выполнение скрипта

> [!WARNING]
> Данная команда устарела.
>  Рекомендуемый инструмент для выполнения запросов в YDB CLI — это команда [ydb sql](sql.md).

С помощью подкоманды `scripting yql` вы можете выполнить YQL-скрипт. Скрипт может содержать запросы разных типов. В отличие от `yql`, подкоманда `scripting yql` имеет ограничение на количество возвращаемых строк и объем затрагиваемых данных.

Общий вид команды:

```bash
ydb [global options...] scripting yql [options...]
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](scripting-yql.md#options).

Посмотрите описание команды выполнения YQL-скрипта:

```bash
ydb scripting yql --help
```

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--timeout` | Время, в течение которого должна быть выполнена операция на сервере. |
| `--stats` | Режим сбора статистики.  <br> Возможные значения:<br>- `none` — не собирать;<br>- `basic` — собирать по основным событиям;<br>- `full` — собирать по всем событиям.<br>Значение по умолчанию — `none`. |
| `-s`, `--script` | Текст YQL-скрипта для выполнения. |
| `-f`, `--file` | Путь к файлу с текстом YQL-скрипта для выполнения. |
| `--explain` | Показать план выполнения запроса. |
| `--show-response-metadata` | Показать метаданные ответа. |
| `--format` | Формат вывода.  <br> Значение по умолчанию — `pretty`.  <br> Возможные значения:<br>- `pretty` (по умолчанию) — человекочитаемый формат;<br>- `json-unicode` — вывод в формате [JSON](https://ru.wikipedia.org/wiki/JSON), бинарные строки закодированы в [юникод](https://ru.wikipedia.org/wiki/%D0%AE%D0%BD%D0%B8%D0%BA%D0%BE%D0%B4), каждая строка JSON выводится в отдельной строке;<br>- `json-unicode-array` — вывод в формате JSON, бинарные строки закодированы в Юникод, результат выводится в виде массива строк JSON, каждая строка JSON выводится в отдельной строке;<br>- `json-base64` — вывод в формате JSON, бинарные строки закодированы в [Base64](https://ru.wikipedia.org/wiki/Base64), каждая строка JSON выводится в отдельной строке;<br>- `json-base64-array` — вывод в формате JSON, бинарные строки закодированы в Base64, результат выводится в виде массива строк JSON, каждая строка JSON выводится в отдельной строке;<br>- `parquet`: вывод в формате [Apache Parquet](https://parquet.apache.org/docs/). |

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

Скрипт создания строковой таблицы, заполнения её данными, и получения выборки из этой таблицы:

```bash
ydb -p quickstart scripting yql -s '
    CREATE TABLE series (series_id Uint64, title Utf8, series_info Utf8, release_date Date, PRIMARY KEY (series_id));
    COMMIT;
    UPSERT INTO series (series_id, title, series_info, release_date) values (1, "Title1", "Info1", Cast("2023-04-20" as Date));
    COMMIT;
    SELECT * from series;
  '
```

Вывод команды:

```text
┌──────────────┬───────────┬─────────────┬──────────┐
| release_date | series_id | series_info | title    |
├──────────────┼───────────┼─────────────┼──────────┤
| "2023-04-20" | 1         | "Info1"     | "Title1" |
└──────────────┴───────────┴─────────────┴──────────┘
```

Выполнение скрипта из примера выше, записанного в файле `script1.yql`, с выводом результатов в формате `JSON`:

```bash
ydb -p quickstart scripting yql -f script1.yql --format json-unicode
```

Вывод команды:

```text
{"release_date":"2023-04-20","series_id":1,"series_info":"Info1","title":"Title1"}
```

Примеры передачи параметров в скрипты приведены в [статье о передаче параметров в команды исполнения YQL](parameterized-queries-cli.md).
