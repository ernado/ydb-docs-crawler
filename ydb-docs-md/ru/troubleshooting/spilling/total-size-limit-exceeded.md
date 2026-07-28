---
title: "Total size limit exceeded"
url: "https://ydb.tech/docs/ru/troubleshooting/spilling/total-size-limit-exceeded?version=v26.1"
doc_path: "ru/troubleshooting/spilling/total-size-limit-exceeded"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/spilling/total-size-limit-exceeded.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/spilling/total-size-limit-exceeded.md"
description: "Превышен максимальный суммарный размер файлов спиллинга (параметр max_total_size ). Это происходит, когда общий размер всех файлов спиллинга достигает настроенн"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Total size limit exceeded

Превышен максимальный суммарный размер файлов спиллинга (параметр [`max_total_size`](../../reference/configuration/table_service_config.md#local-file-config-max-total-size)). Это происходит, когда общий размер всех файлов спиллинга достигает настроенного лимита, что препятствует новым операциям спиллинга.

## Диагностика {#diagnostika}

Проверьте текущее использование спиллинга:

- Отслеживайте общий размер файлов спиллинга в директории спиллинга
- Проверьте текущее значение параметра [`max_total_size`](../../reference/configuration/table_service_config.md#local-file-config-max-total-size)
- Просмотрите доступное дисковое пространство в расположении директории спиллинга
- Проверьте, есть ли зависшие файлы спиллинга, которые должны были быть очищены

## Рекомендации {#rekomendacii}

Для решения этой проблемы:

1. **Увеличьте лимит размера спиллинга:**

   - Если на диске достаточно свободного места, увеличьте параметр [`max_total_size`](../../reference/configuration/table_service_config.md#local-file-config-max-total-size) в конфигурации
   - Рекомендуется увеличить значение на 20-50% от текущего

2. **Расширьте дисковое пространство:**

   - Если свободного места на диске недостаточно, добавьте дополнительное дисковое пространство
   - Убедитесь, что директория спиллинга находится на диске с достаточным объемом

3. **Попробуйте повторить запрос:**

   - Дождитесь завершения других ресурсоемких запросов
   - Повторите выполнение запроса в менее загруженное время
