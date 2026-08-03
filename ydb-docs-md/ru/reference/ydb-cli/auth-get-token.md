---
title: "Получение токена аутентификации"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/auth-get-token?version=v26.1"
doc_path: "ru/reference/ydb-cli/auth-get-token"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/auth-get-token.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/auth-get-token.md"
description: "С помощью подкоманды auth get-token вы можете получить токен аутентификации на основе параметров аутентификации, указанных в профиле, переменных окружения или п"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Получение токена аутентификации

С помощью подкоманды `auth get-token` вы можете получить токен аутентификации на основе параметров аутентификации, указанных в профиле, переменных окружения или параметрах командной строки.

Общий вид команды:

```bash
ydb [global options...] auth get-token [options...]
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](auth-get-token.md#options).

Посмотрите описание команды получения токена:

```bash
ydb auth get-token --help
```

## Параметры подкоманды {#options}

| Параметр | Описание |
| --- | --- |
| `-f, --force` | Вывести токен без запроса подтверждения. |
| `--timeout` | Время ожидания ответа клиента в миллисекундах. После истечения этого времени нет смысла ждать результат. |

## Примеры {#examples}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

### Получение токена с подтверждением {#with-prompt}

По умолчанию команда запрашивает подтверждение перед выводом токена, так как токен будет выведен в консоль:

```bash
ydb -p quickstart auth get-token
```

Результат:

```text
Caution: Your auth token will be printed to console. Use "--force" ("-f") option to print without prompting.
Do you want to proceed? (y/N): y
t1.eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Получение токена без подтверждения {#without-prompt}

Для автоматизации или использования в скриптах используйте опцию `--force` для вывода токена без запроса подтверждения:

```bash
ydb -p quickstart auth get-token --force
```

Результат:

```text
t1.eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Использование в скриптах {#in-scripts}

Команда может быть использована для получения токена в скриптах:

```bash
TOKEN=$(ydb -p quickstart auth get-token --force)
echo "Token: $TOKEN"
```
