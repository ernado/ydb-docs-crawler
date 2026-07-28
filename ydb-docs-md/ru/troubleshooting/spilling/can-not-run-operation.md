---
title: "Can not run operation"
url: "https://ydb.tech/docs/ru/troubleshooting/spilling/can-not-run-operation?version=v26.1"
doc_path: "ru/troubleshooting/spilling/can-not-run-operation"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/spilling/can-not-run-operation.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/spilling/can-not-run-operation.md"
description: "Переполнение очереди операций в пуле потоков I/O. Это происходит, когда очередь пула потоков I/O для спиллинга заполнена и не может принимать новые операции, чт"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Can not run operation

Переполнение очереди операций в пуле потоков I/O. Это происходит, когда очередь пула потоков I/O для спиллинга заполнена и не может принимать новые операции, что приводит к сбою операций спиллинга.

## Диагностика {#diagnostika}

Проверьте конфигурацию и использование пула потоков I/O:

- Проверьте параметр `queue_size` в конфигурации `io_thread_pool`.
- Проверьте параметр `workers_count` для пула потоков I/O.

## Рекомендации {#rekomendacii}

Для решения этой проблемы:

1. **Увеличьте размер очереди:**

   - Увеличьте значение `queue_size` в конфигурации `io_thread_pool`.
   - Это позволит поставить в очередь больше операций до возникновения переполнения.

2. **Увеличьте количество рабочих потоков:**

   - Увеличьте значение `workers_count` для более быстрой обработки операций.
   - Большее количество рабочих потоков позволит быстрее обрабатывать операции, уменьшая накопление в очереди.

> [!NOTE]
> Пул потоков I/O обрабатывает операции спиллинга асинхронно. Если очередь переполняется, новые операции спиллинга будут завершаться сбоем до тех пор, пока не освободится место.
