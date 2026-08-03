---
title: "Создание топика"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/topic-create?version=v26.1"
doc_path: "ru/reference/ydb-cli/topic-create"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/topic-create.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/topic-create.md"
description: "С помощью подкоманды topic create вы можете создать новый топик. Общий вид команды: ydb [global options...] topic create [options...] <topic-path>."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Создание топика

С помощью подкоманды `topic create` вы можете создать новый топик.

Общий вид команды:

```bash
ydb [global options...] topic create [options...] <topic-path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](topic-create.md#options).
- `topic-path` — путь топика.

Посмотрите описание команды создания топика:

```bash
ydb topic create --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--partitions-count` | Количество [партиций](../../concepts/datamodel/topic.md#partitioning) топика.  <br>Значение по умолчанию — `1`. |
| `--retention-period` | Время хранения данных в топике. Положительное число с указанием единицы измерения.  <br>Поддерживаются следующие единицы:<br>- `s` – секунды;<br>- `m` – минуты;<br>- `h` – часы;<br>- `d` – дни.<br>Значение по умолчанию — `18h`. |
| `--partition-write-speed-kbps` | Максимальная скорость записи в [партицию](../../concepts/datamodel/topic.md#partitioning), задается в КБ/с.  <br>Значение по умолчанию — `1024`. |
| `--retention-storage-mb` | Максимальный объем хранения для топика, задается в МБ. При достижении ограничения будут удаляться самые старые данные. При включенном автоматическом партиционировании потребляемое место может превышать установленное значение.  <br>Значение по умолчанию — `0` (ограничение не задано). |
| `--supported-codecs` | Поддерживаемые методы сжатия данных. Задаются через запятую.  <br>Значение по умолчанию — `raw`.  <br>Возможные значения:<br>- `RAW` — без сжатия;<br>- `ZSTD` — сжатие [zstd](https://ru.wikipedia.org/wiki/Zstandard);<br>- `GZIP` — сжатие [gzip](https://ru.wikipedia.org/wiki/Gzip);<br>- `LZOP` — сжатие [lzop](https://ru.wikipedia.org/wiki/Lzop). |
| `--metering-mode` | Режим тарификации топика для serverless базы данных.  <br>Возможные значения:<br>- `request-units` — по фактическому использованию.<br>- `reserved-capacity` — по выделенным ресурсам. |

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Создание топика с 2 партициями, методами сжатия `RAW` и `GZIP`, временем хранения сообщений 2 часа и путем `my-topic`:

```bash
ydb -p quickstart topic create \
  --partitions-count 2 \
  --supported-codecs raw,gzip \
  --retention-period 2h \
  my-topic
```

Посмотрите параметры созданного топика:

```bash
ydb -p quickstart scheme describe my-topic
```

Результат:

```text
RetentionPeriod: 2h
PartitionsCount: 2
SupportedCodecs: RAW, GZIP
```
