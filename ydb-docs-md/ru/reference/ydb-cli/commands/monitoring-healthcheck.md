---
title: "Проверка состояния базы данных"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/monitoring-healthcheck?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/monitoring-healthcheck"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/monitoring-healthcheck.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/monitoring-healthcheck.md"
description: "YDB имеет встроенную систему самодиагностики, с помощью которой можно получить краткий отчёт о состоянии базы данных и информацию о выявленных проблемах."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Проверка состояния базы данных

YDB имеет встроенную систему самодиагностики, с помощью которой можно получить краткий отчёт о состоянии базы данных и информацию о выявленных проблемах.

Общий вид команды:

```bash
ydb [global options...] monitoring healthcheck [options...]
```

- `global options` — [глобальные параметры](global-options.md),
- `options` — [параметры подкоманды](monitoring-healthcheck.md#options).

## Параметры подкоманды {#options}

|  |  |
| --- | --- |
| Имя | Описание |
| `--timeout` | Время, в течение которого должна быть выполнена операция на сервере, мс. |
| `--format` | Формат вывода. Возможные значения:<br>- `pretty` — обобщенный статус базы данных. Возможные варианты значений приведены в [таблице](../../ydb-sdk/health-check-api.md#selfcheck-result).<br>- `json` — подробный ответ в формате JSON, содержащий иерархический список обнаруженных проблем. Перечень возможных проблем приведен в документации [Healthcheck API](../../ydb-sdk/health-check-api.md#issues).<br>Значение по умолчанию — `pretty`. |
| `--no-merge` | Не объединять записи результата проверки состояния. |
| `--no-cache` | Не использовать кэшированный результат. |

## Примеры {#examples}

### Краткий результат проверки {#example-pretty}

```bash
ydb --profile quickstart monitoring healthcheck --format pretty
```

Проблем с базой не обнаружено:

```bash
Healthcheck status: GOOD
```

Обнаружена деградация базы данных:

```bash
Healthcheck status: DEGRADED
```

### Подробный результат проверки {#example-json}

```bash
ydb --profile quickstart monitoring healthcheck --format json
```

Проблем с базой не обнаружено:

```json
{
 "self_check_result": "GOOD",
 "location": {
  "id": 51059,
  "host": "my-host.net",
  "port": 19001
 }
}
```

Обнаружена деградация базы данных:

```json
{
 "self_check_result": "DEGRADED",
 "issue_log": [
  {
   "id": "YELLOW-b3c0-70fb",
   "status": "YELLOW",
   "message": "Database has multiple issues",
   "location": {
    "database": {
     "name": "/my-cluster/my-database"
    }
   },
   "reason": [
    "YELLOW-b3c0-1ba8",
    "YELLOW-b3c0-1c83"
   ],
   "type": "DATABASE",
   "level": 1
  },
  {
   "id": "YELLOW-b3c0-1ba8",
   "status": "YELLOW",
   "message": "Compute is overloaded",
   "location": {
    "database": {
     "name": "/my-cluster/my-database"
    }
   },
   "reason": [
    "YELLOW-b3c0-343a-51059-User"
   ],
   "type": "COMPUTE",
   "level": 2
  },
  {
   "id": "YELLOW-b3c0-343a-51059-User",
   "status": "YELLOW",
   "message": "Pool usage is over than 99%",
   "location": {
    "compute": {
     "node": {
      "id": 51059,
      "host": "my-host.net",
      "port": 31043
     },
     "pool": {
      "name": "User"
     }
    },
    "database": {
     "name": "/my-cluster/my-database"
    }
   },
   "type": "COMPUTE_POOL",
   "level": 4
  },
  {
   "id": "YELLOW-b3c0-1c83",
   "status": "YELLOW",
   "message": "Storage usage over 75%",
   "location": {
    "database": {
     "name": "/my-cluster/my-database"
    }
   },
   "type": "STORAGE",
   "level": 2
  }
 ],
 "location": {
  "id": 117,
  "host": "my-host.net",
  "port": 19001
 }
}
```
