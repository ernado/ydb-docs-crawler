---
title: "Удаление фоновой операции из списка"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/operation-forget?version=v26.1"
doc_path: "ru/reference/ydb-cli/operation-forget"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/operation-forget.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/operation-forget.md"
description: "С помощью подкоманды ydb operation forget вы можете удалить информацию об указанной фоновой операции из списка. Операция должна быть завершена."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Удаление фоновой операции из списка

С помощью подкоманды `ydb operation forget` вы можете удалить информацию об указанной фоновой операции из списка. Операция должна быть завершена.

Общий вид команды:

```bash
ydb [global options...] operation forget <id>
```

- `global options` — [глобальные параметры](commands/global-options.md).
- `id` — идентификатор фоновой операции. Идентификатор содержит символы, которые могут быть интерпретированы вашей командной оболочкой. При необходимости используйте экранирование, например `'<id>'` для bash.

Посмотрите описание команды удаления информации об указанной фоновой операции:

```bash
ydb operation forget --help
```

## Примеры {#primery-{examples}}

> [!NOTE]
> В примерах используется профиль `quickstart`, подробнее смотрите в [Создание профиля для соединения с тестовой БД](profile/create.md#quickstart).

Удалите из списка фоновую операцию с идентификатором `ydb://buildindex/7?id=281489389055514`:

```bash
ydb -p quickstart operation forget \
  'ydb://buildindex/7?id=281489389055514'
```
