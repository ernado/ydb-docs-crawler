---
title: "Установка параметров TTL"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/table-ttl-set?version=v26.1"
doc_path: "ru/reference/ydb-cli/table-ttl-set"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/table-ttl-set.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/table-ttl-set.md"
description: "С помощью подкоманды table ttl set вы можете установить TTL для указанной таблицы. Общий вид команды:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Установка параметров TTL

С помощью подкоманды `table ttl set` вы можете установить [TTL](../../concepts/ttl.md) для указанной таблицы.

Общий вид команды:

```bash
ydb [global options...] table ttl set [options...] <table path>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](table-ttl-set.md#options).
- `table path` — путь таблицы.

Посмотрите описание команды установки TTL:

```bash
ydb table ttl set --help
```

## Параметры подкоманды {#options}

| Имя | Описание |
| --- | --- |
| `--column` | Имя колонки, которая будет использована для вычисления времени жизни строк. Колонка должна иметь тип [числовой](../../yql/reference/types/primitive.md#numeric) или [дата и время](../../yql/reference/types/primitive.md#datetime).  <br>В случае числового типа значение будет интерпретироваться как время, прошедшее с начала [эпохи Unix](https://ru.wikipedia.org/wiki/Unix-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F). Единицы измерения должны быть заданы в параметре `--unit`. |
| `--expire-after` | Дополнительное время до удаления, которое должно пройти после истечения времени жизни строки. Указывается в секундах.  <br>Значение по умолчанию — `0`. |
| `--unit` | Единицы измерения значений колонки, которая указана в параметре `--column`. Обязателен, если колонка имеет [числовой](../../yql/reference/types/primitive.md#numeric) тип.  <br>Возможные значения:<br>- `seconds (s, sec)` — секунды;<br>- `milliseconds (ms, msec)` — миллисекунды;<br>- `microseconds (us, usec)` — микросекунды;<br>- `nanoseconds (ns, nsec)` — наносекунды. |
| `--run-interval` | Интервал запуска операции удаления строк с истекшим TTL. Указывается в секундах. Настройки БД по умолчанию не позволяют задать интервал меньше 15 минут (900 секунд).  <br>Значение по умолчанию — `3600`. |

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Установите TTL для таблицы `series`

```bash
ydb -p quickstart table ttl set \
  --column createtime \
  --expire-after 3600 \
  --run-interval 1200 \
  series
```
