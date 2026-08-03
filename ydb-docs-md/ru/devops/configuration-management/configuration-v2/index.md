---
title: "Конфигурация V2"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v2/?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v2/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v2/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v2/index.md"
description: "В этом разделе документации описан способ конфигурации кластеров YDB под названием V2, являющаяся экспериментальным способом конфигурирования кластеров YDB верс"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Конфигурация V2

В этом разделе документации описан способ конфигурации кластеров YDB под названием V2, являющаяся экспериментальным способом конфигурирования кластеров YDB версий YDB v25.1 и выше.

> [!WARNING]
> Эта статья посвящена кластерам YDB, в которых используется [конфигурация V2](index.md). Данный способ конфигурирования пока является экспериментальным и доступен только для версий YDB начиная с v25.1. Для использования в продакшене мы рекомендуем выбирать [конфигурацию V1](../index.md) — она является основной и официально поддерживаемой для всех кластеров YDB.

Основные материалы:

- [Обзор конфигурации V2](config-overview.md)
- [Обновление конфигурации кластеров YDB](update-config.md)
- [DSL конфигурации кластера](dynamic-config-selectors.md)
- [Параметры конфигурации](config-settings.md)
- [Расширение кластера](cluster-expansion.md)
- [Перемещение State Storage](state-storage-move.md)
- [Перемещение статической группы](static-group-move.md)
- [Замена FQDN узла](replacing-nodes.md)
- [Аутентификация и авторизация узлов баз данных](node-authorization.md)
