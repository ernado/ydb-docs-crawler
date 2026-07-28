---
title: "Отмена фоновой операции"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/operation-cancel?version=v26.1"
doc_path: "ru/reference/ydb-cli/operation-cancel"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/operation-cancel.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/operation-cancel.md"
description: "С помощью подкоманды ydb operation cancel вы можете инициировать отмену указанной фоновой операции. Можно отменить только незавершенную операцию."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Отмена фоновой операции

С помощью подкоманды `ydb operation cancel` вы можете инициировать отмену указанной фоновой операции. Можно отменить только незавершенную операцию.

Общий вид команды:

```bash
ydb [global options...] operation cancel <id>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `id` — идентификатор фоновой операции. Идентификатор содержит символы, которые могут быть интерпретированы вашей командной оболочкой. При необходимости используйте экранирование, например `'<id>'` для bash.

Посмотрите описание команды получения статуса фоновой операции:

```bash
ydb operation cancel --help
```

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).
