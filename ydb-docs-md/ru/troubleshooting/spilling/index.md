---
title: "Устранение неполадок спиллинга"
url: "https://ydb.tech/docs/ru/troubleshooting/spilling/?version=v26.1"
doc_path: "ru/troubleshooting/spilling/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/spilling/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/spilling/index.md"
description: "Этот раздел предоставляет информацию по устранению неполадок для распространенных проблем со спиллингом в YDB. Спиллинг — это механизм управления памятью, котор"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# Устранение неполадок спиллинга

Этот раздел предоставляет информацию по устранению неполадок для распространенных проблем со спиллингом в YDB. Спиллинг — это механизм управления памятью, который временно сохраняет промежуточные вычислительные данные на диск при нехватке оперативной памяти. Эти ошибки могут возникать во время выполнения запросов, когда система пытается использовать функциональность спиллинга, и могут наблюдаться в логах и ответах запросов.

## Частые проблемы {#chastye-problemy}

- [Permission denied](permission-denied.md) - Недостаточные права доступа к директории спиллинга
- [Spilling Service not started](service-not-started.md) - Попытка использования спиллинга при выключенном Spilling Service
- [Total size limit exceeded](total-size-limit-exceeded.md) - Превышен максимальный суммарный размер файлов спиллинга
- [Can not run operation](can-not-run-operation.md) - Переполнение очереди операций в пуле потоков I/O

## См. также {#sm-takzhe}

- [Конфигурация спиллинга](../../reference/configuration/table_service_config.md)
- [Концепция спиллинга](../../concepts/query_execution/spilling.md)
- [Конфигурация контроллера памяти](../../reference/configuration/memory_controller_config.md)
- [Мониторинг YDB](../../devops/observability/monitoring.md)
- [Диагностика производительности](../performance/index.md)
