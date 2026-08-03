---
title: "Spilling Service not started"
url: "https://ydb.tech/docs/ru/troubleshooting/spilling/service-not-started?version=v26.1"
doc_path: "ru/troubleshooting/spilling/service-not-started"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/spilling/service-not-started.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/spilling/service-not-started.md"
description: "Попытка использования спиллинга при выключенном Spilling Service. Это происходит, когда сервис спиллинга неправильно настроен или отключен в конфигурации."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Spilling Service not started

Попытка использования спиллинга при выключенном Spilling Service. Это происходит, когда сервис спиллинга неправильно настроен или отключен в конфигурации.

## Диагностика {#diagnostika}

Проверьте конфигурацию сервиса спиллинга:

- Убедитесь, что [`table_service_config.spilling_service_config.local_file_config.enable`](../../reference/configuration/table_service_config.md#local-file-config-enable) установлен в `true`.

## Рекомендации {#rekomendacii}

Для включения спиллинга:

1. Установите [`table_service_config.spilling_service_config.local_file_config.enable`](../../reference/configuration/table_service_config.md#local-file-config-enable): `true` в вашей конфигурации.

> [!NOTE]
> Подробнее об архитектуре спиллинга см. в разделе [Архитектура спиллинга в YDB](../../concepts/query_execution/spilling.md#architecture).
