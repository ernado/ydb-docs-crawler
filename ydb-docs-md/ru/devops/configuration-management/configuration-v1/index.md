---
title: "Конфигурация V1"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/index.md"
description: "В этом разделе документации YDB описана Конфигурация V1, являющаяся основным способом конфигурирования кластеров YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Конфигурация V1

В этом разделе документации YDB описана Конфигурация V1, являющаяся основным способом конфигурирования кластеров YDB.

Конфигурация V1 — двухуровневая система конфигурации кластера YDB, состоящая из [cтатической конфигурации](static-config.md) и [динамической конфигурации](dynamic-config.md):

1. **Статическая конфигурация**: файл в формате YAML, который располагается локально на каждом статическом узле и используется при запуске процесса `ydbd server`. Эта конфигурация содержит, в том числе, настройки [статической группы](../../../concepts/glossary.md#static-group) и [State Storage](../../../concepts/glossary.md#state-storage).
2. **Динамическая конфигурация**: файл в формате YAML, являющийся расширенной версией статической конфигурации. Загружается через [CLI](../../../recipes/ydb-cli/index.md) и надёжно сохраняется в [таблетке Console](../../../concepts/glossary.md#console), которая затем распространяет конфигурацию на все динамические узлы кластера. Использование динамической конфигурации опционально.

Подробнее о Конфигурации V1 можно узнать в разделе [Обзор конфигурации V1](config-overview.md).

Основные материалы:

- [Обзор конфигурации V1](config-overview.md)
- [Статическая конфигурация](static-config.md)
- [Динамическая конфигурация кластера](dynamic-config.md)
- [Временные конфигурации](dynamic-config-volatile-config.md)
- [DSL конфигурация кластера](dynamic-config-selectors.md)
- [Изменение конфигураций через CMS](cms.md)
- [Изменение конфигурации актор-системы](change_actorsystem_configs.md)
- [Расширение кластера](cluster-expansion.md)
- [Перемещение State Storage](state-storage-move.md)
- [Перемещение статической группы](static-group-move.md)
- [Замена FQDN узла](replacing-nodes.md)
- [Аутентификация и авторизация узлов баз данных](node-authorization.md)
