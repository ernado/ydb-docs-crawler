---
title: "Обзор управления дисковой подсистемой кластера"
url: "https://ydb.tech/docs/ru/maintenance/manual/?version=v26.1"
doc_path: "ru/maintenance/manual/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/maintenance/manual/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/maintenance/manual/index.md"
description: "Управление дисковой подсистемой кластера включает следующие действия: Изменение конфигурации: Расширение кластера. Добавление групп хранения. Обслуживание:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обзор управления дисковой подсистемой кластера

Управление дисковой подсистемой кластера включает следующие действия:

- Изменение конфигурации:

  - [Расширение кластера](../../devops/configuration-management/configuration-v2/cluster-expansion.md).
  - [Добавление групп хранения](adding_storage_groups.md).

- Обслуживание:

  - [Замена FQDN узла](../../devops/configuration-management/configuration-v2/replacing-nodes.md).
  - [Включение и выключение Scrubbing](scrubbing.md).
  - [Работа с SelfHeal](selfheal.md).
  - [Декомиссия части кластера](../../devops/deployment-options/manual/decommissioning.md).
  - [Декомиссия групп с использованием виртуальных групп](virtual_storage_groups_decommit.md).
  - [Перевоз VDisk'ов](moving_vdisks.md).

- Решение проблем:

  - [Предотвращение выхода за модель отказа](failure_model.md).
  - [Балансировка нагрузки на диски](balancing_load.md).
  - [Освобождение места на физических устройствах](disk_end_space.md).
