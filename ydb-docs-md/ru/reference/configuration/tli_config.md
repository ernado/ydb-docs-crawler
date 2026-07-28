---
title: "tli_config"
url: "https://ydb.tech/docs/ru/reference/configuration/tli_config?version=v26.1"
doc_path: "ru/reference/configuration/tli_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/tli_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/tli_config.md"
description: "Секция tli_config содержит параметры диагностики инвалидации блокировок транзакций (Transaction Lock Invalidation, TLI)."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# tli_config

Секция `tli_config` содержит параметры диагностики [инвалидации блокировок транзакций](../../concepts/glossary.md#tli) (Transaction Lock Invalidation, TLI).

TLI — это механизм, при котором одна транзакция (нарушитель) ломает [оптимистичные блокировки](../../concepts/glossary.md#optimistic-locking) другой транзакции (жертвы), вынуждая жертву откатиться и повторить выполнение. Подробнее о диагностике TLI см. в разделе [Инвалидация блокировок транзакций](../../troubleshooting/performance/queries/transaction-lock-invalidation.md).

## Параметры конфигурации {#parametry-konfiguracii}

| Параметр | Тип | По умолчанию | Описание |
| --- | --- | --- | --- |
| `ignored_table_regexes` | repeated string | `[]` | Список регулярных выражений путей таблиц, исключённых из TLI-диагностики |

### ignored_table_regexes {#ignored_table_regexes}

Позволяет исключить определённые таблицы из TLI-логирования и статистики. Если каждая таблица, используемая в SQL запросе на котором возникли TLI, соответствуют хотя бы одному из указанных регулярных выражений, TLI-лог для этого конфликта не формируется.

Изменения применяются к новым сессиям без перезапуска узлов.

Типичные сценарии использования:

- снижение объёма логов для системных или служебных таблиц, конфликты в которых ожидаемы;
- исключение таблиц очередей с высокой частотой конфликтов, не требующих диагностики.

Регулярные выражения применяются к полному пути таблицы, например `/Root/mydb/mytable`. Синтаксис соответствует [ECMAScript regex](https://en.cppreference.com/w/cpp/regex/ecmascript).

## Пример конфигурации {#primer-konfiguracii}

```yaml
tli_config:
  ignored_table_regexes:
    - "/Root/.*/queue_.*"
    - "/Root/system/.*"
```

В этом примере из TLI-диагностики исключаются:

- таблицы с именем, начинающимся на `queue_`, в любой базе данных;
- все таблицы в директории `/Root/system/`.

## Смотрите также {#smotrite-takzhe}

- [Инвалидация блокировок транзакций](../../troubleshooting/performance/queries/transaction-lock-invalidation.md)
- [log_config](log_config.md)
- [Логирование в YDB](../../devops/observability/logging.md)
