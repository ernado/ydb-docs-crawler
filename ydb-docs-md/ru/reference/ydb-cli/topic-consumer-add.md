---
title: "Добавление читателя топика"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/topic-consumer-add?version=v26.1"
doc_path: "ru/reference/ydb-cli/topic-consumer-add"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/topic-consumer-add.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/topic-consumer-add.md"
description: "С помощью команды topic consumer add вы можете добавить читателя для созданного ранее топика. Общий вид команды:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Добавление читателя топика

С помощью команды `topic consumer add` вы можете добавить читателя для [созданного ранее](topic-create.md) топика.

Общий вид команды:

```bash
ydb [global options...] topic consumer add [options...] <topic-path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](topic-consumer-add.md#options).
- `topic-path` — путь топика.

Посмотрите описание команды добавления читателя:

```bash
ydb topic consumer add --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--consumer VAL` | Имя читателя, которого нужно добавить. |
| `--starting-message-timestamp VAL` | Время в формате [UNIX timestamp](https://ru.wikipedia.org/wiki/Unix-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F) (секунды с 1970.01.01) или в формате ISO-8601 (например, `2020-07-10T15:00:00Z`). Чтение начнется с первого [сообщения](../../concepts/datamodel/topic.md#message), полученного после указанного времени. Если время не задано, то чтение начнется с самого старого сообщения в топике. |
| `--supported-codecs` | Поддерживаемые методы сжатия данных.  <br>Значение по умолчанию — `raw`.  <br>Возможные значения:<br>- `RAW` — без сжатия;<br>- `ZSTD` — сжатие [zstd](https://ru.wikipedia.org/wiki/Zstandard);<br>- `GZIP` — сжатие [gzip](https://ru.wikipedia.org/wiki/Gzip);<br>- `LZOP` — сжатие [lzop](https://ru.wikipedia.org/wiki/Lzop). |
| `--important` | Указывает, является ли читатель [важным](../../concepts/datamodel/topic.md#important-consumer).  <br>Значение по умолчанию — `false`.  <br>Для важных читателей:<br>- не применяется ограничение по периоду доступности (`--availability-period`);<br>- данные в топике не удаляются, пока они не обработаны всеми важными читателями;<br>- это влияет на процесс очистки данных в топике.<br>Используйте этот параметр для критически важных читателей, которые должны гарантированно прочитать и обработать все сообщения. |
| `--availability-period VAL` | Время доступности данных в топике для необработанных сообщений.  <br>Опция позволяет продлить время хранения сообщений в топике с [времени хранения `retention-period`](topic-create.md#options) вплоть до указанного времени доступности, если читатель не подтверждает их обработку.  <br>Формат: положительное число с указанием единицы измерения времени (без пробелов).  <br>Поддерживаются следующие единицы измерения:<br>- `s` — секунды (например, `30s`, `120s`);<br>- `m` — минуты (например, `5m`, `1440m`);<br>- `h` — часы (например, `1h`, `72h`);<br>- `d` — дни (например, `1d`, `7d`).<br>Примеры: `72h`, `1440m`, `2d`, `3600s`.  <br>Для важных читателей (с параметром `--important`) этот параметр не применяется. |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

### Создайте читателя с именем `my-consumer` для [созданного ранее](topic-create.md) топика `my-topic`, чтение начнется с первого сообщения, полученного после 15 августа 2022 13:00:00 GMT {#,-chtenie-nachnetsya-s-pervogo-soobsheniya,-poluchennogo-posle-15-avgusta-2022-130000-gmt}

```bash
ydb -p quickstart topic consumer add \
  --consumer my-consumer \
  --starting-message-timestamp 1660568400 \
  my-topic
```

Убедитесь, что читатель создан:

```bash
ydb -p quickstart scheme describe my-topic
```

Результат:

```text
RetentionPeriod: 2h
PartitionsCount: 2
SupportedCodecs: RAW, GZIP

Consumers:
┌──────────────┬─────────────────┬───────────────────────────────┬───────────┐
| ConsumerName | SupportedCodecs | ReadFrom                      | Important |
├──────────────┼─────────────────┼───────────────────────────────┼───────────┤
| my-consumer  | RAW, GZIP       | Mon, 15 Aug 2022 16:00:00 MSK | 0         |
└──────────────┴─────────────────┴───────────────────────────────┴───────────┘
```

### Создайте читателя с именем `backup-consumer` для топика `my-topic` с периодом доступности данных 3 дня {#s-periodom-dostupnosti-dannyh-3-dnya}

```bash
ydb -p quickstart topic consumer add \
  --consumer backup-consumer \
  --availability-period 3d \
  my-topic
```

Если читатель успевает обрабатывать данные, то сообщения в топике будут храниться в течение 2-х часов, в соответствии со значением параметра `retention-period` топика.  
 Однако при временной остановке чтения, время хранения данных в топике, для которых читатель `backup-consumer` ещё не подтвердил обработку, будет увеличено вплоть до 3-х дней, в соответствии с параметром `availability-period`.

### Создайте важного читателя с именем `critical-consumer` для топика `my-topic` с дополнительной поддержкой кодека `ZSTD` {#s-dopolnitelnoj-podderzhkoj-kodeka}

```bash
ydb -p quickstart topic consumer add \
  --consumer critical-consumer \
  --important \
  --supported-codecs raw,gzip,zstd \
  my-topic
```

Обратите внимание, что для важного читателя параметр `--availability-period` не применяется, даже если он указан.
