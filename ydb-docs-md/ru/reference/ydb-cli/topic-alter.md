---
title: "Изменение топика"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/topic-alter?version=v26.1"
doc_path: "ru/reference/ydb-cli/topic-alter"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/topic-alter.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/topic-alter.md"
description: "С помощью подкоманды topic alter вы можете изменить созданный ранее топик. Общий вид команды: ydb [global options...] topic alter [options...] <topic-path>."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Изменение топика

С помощью подкоманды `topic alter` вы можете изменить [созданный ранее](topic-create.md) топик.

Общий вид команды:

```bash
ydb [global options...] topic alter [options...] <topic-path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](topic-alter.md#options).
- `topic-path` — путь топика.

Посмотрите описание команды изменения топика:

```bash
ydb topic alter --help
```

## Параметры подкоманды {#options}

При исполнении команды будут изменены значения тех параметров, которые заданы в командной строке. Значения остальных параметров останутся без изменений.

| Имя | Описание |
| --- | --- |
| `--partitions-count` | Количество [партиций](../../concepts/datamodel/topic.md#partitioning) топика. Возможно только увеличение количества партиций. |
| `--retention-period` | Время хранения данных в топике. Положительное число с указанием единицы измерения.  <br>Поддерживаются следующие единицы:<br>- `s` – секунды;<br>- `m` – минуты;<br>- `h` – часы;<br>- `d` – дни. |
| `--partition-write-speed-kbps` | Максимальная скорость записи в [партицию](../../concepts/datamodel/topic.md#partitioning), задается в КБ/с.  <br>Значение по умолчанию — `1024`. |
| `--retention-storage-mb` | Максимальный объем хранения для топика, задается в МБ. При достижении ограничения будут удаляться самые старые данные. При включенном автоматическом партиционировании потребляемое место может превышать установленное значение.  <br>Значение по умолчанию — `0` (ограничение не задано). |
| `--supported-codecs` | Поддерживаемые методы сжатия данных.  <br>Возможные значения:<br>- `RAW` — без сжатия;<br>- `ZSTD` — сжатие [zstd](https://ru.wikipedia.org/wiki/Zstandard);<br>- `GZIP` — сжатие [gzip](https://ru.wikipedia.org/wiki/Gzip);<br>- `LZOP` — сжатие [lzop](https://ru.wikipedia.org/wiki/Lzop). |
| `--metering-mode` | Режим тарификации топика для serverless базы данных.  <br>Возможные значения:<br>- `request-units` — по фактическому использованию.<br>- `reserved-capacity` — по выделенным ресурсам. |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Добавьте партицию и метод сжатия `lzop` [созданному ранее](topic-create.md) топику:

```bash
ydb -p quickstart topic alter \
  --partitions-count 3 \
  --supported-codecs raw,gzip,lzop \
  my-topic
```

Убедитесь, что параметры топика изменились:

```bash
ydb -p quickstart scheme describe my-topic
```

Результат:

```text
RetentionPeriod: 2h
PartitionsCount: 3
SupportedCodecs: RAW, GZIP, LZOP
```
