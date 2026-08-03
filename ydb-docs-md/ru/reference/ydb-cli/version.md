---
title: "Вывод версии YDB CLI"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/version?version=v26.1"
doc_path: "ru/reference/ydb-cli/version"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/version.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/version.md"
description: "С помощью подкоманды version вы можете узнать версию установленного YDB CLI, а также управлять автоматической проверкой доступности новой версии."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Вывод версии YDB CLI

С помощью подкоманды `version` вы можете узнать версию установленного YDB CLI, а также управлять автоматической проверкой доступности новой версии.

Автоматическая проверка доступности новой версии происходит при выполнении любой команды YDB CLI кроме `ydb version --enable-checks` и `ydb version --disable-checks`, но не чаще одного раза в сутки. Результат и время последней проверки сохраняются в конфигурационном файле YDB CLI.

Общий вид команды:

```bash
ydb [global options...] version [options...]
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `options` — [параметры подкоманды](version.md#options).

Посмотрите описание команды:

```bash
ydb version --help
```

## Параметры подкоманды {#options}

| Параметр | Описание |
| --- | --- |
| `--semantic` | Вывести только номер версии. |
| `--check` | Проверить доступность новой версии. |
| `--disable-checks` | Отключить проверку доступности новой версии. |
| `--enable-checks` | Включить проверку доступности новой версии. |

## Примеры {#examples}

### Отключить проверку доступности новой версии {#disable-checks}

При выполнении команд YDB CLI происходит автоматическая проверка доступности новой версии. Если хост, на котором выполняется команда, не имеет доступа в интернет, это приводит к нежелательной задержке и выводу предупреждения при выполнении команды. Чтобы отключить автоматическую проверку обновления, выполните команду:

```bash
ydb version --disable-checks
```

Результат:

```text
Latest version checks disabled
```

### Вывести только номер версии {#semantic}

Для более удобной обработки в скриптах вы можете ограничить вывод номером версии YDB CLI:

```bash
ydb version --semantic
```

Результат:

```text
1.9.1
```
