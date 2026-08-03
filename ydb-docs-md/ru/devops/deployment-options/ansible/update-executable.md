---
title: "Обновление версии YDB на кластерах, развёрнутых с помощью Ansible"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/update-executable?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/update-executable"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/update-executable.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/update-executable.md"
description: "Во время начального развёртывания Ansible playbook предоставляет на выбор несколько вариантов, какой именно серверный исполняемый файл YDB ( ydbd ) использовать"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обновление версии YDB на кластерах, развёрнутых с помощью Ansible

Во время [начального развёртывания](initial-deployment/index.md) Ansible playbook предоставляет на выбор несколько вариантов, какой именно серверный исполняемый файл YDB (`ydbd`) использовать. В этой статье объясняются доступные варианты изменения [версии](../../../downloads/index.md) кластера после начального развёртывания.

> [!WARNING]
> У YDB существуют специфические правила относительно совместимости версий. Важно ознакомиться с [руководством по именованию версий YDB и их совместимости](../../concepts/versioning.md) и [списком изменений](../../../changelog-server.md), чтобы правильно выбрать новую версию для обновления и подготовиться к возможным нюансам.

## Обновление исполняемых файлов через Ansible playbook {#obnovlenie-ispolnyaemyh-fajlov-cherez-ansible-playbook}

Репозиторий [ydb-ansible](https://github.com/ydb-platform/ydb-ansible) содержит playbook под названием `ydb_platform.ydb.update_executable`, который можно использовать для обновления или понижения версии кластера YDB. Перейдите в ту же директорию, которая использовалась для [начального развёртывания](initial-deployment/index.md), отредактируйте файл `inventory/50-inventory.yaml`, чтобы указать целевую версию YDB для установки (обычно через переменные `ydb_version` или `ydb_git_version`), а затем выполните этот playbook:

```bash
ansible-playbook ydb_platform.ydb.update_executable
```

Playbook получает новый бинарный файл и затем разворачивает его на кластере с помощью кросс-серверного копирования Ansible. После этого он выполняет [постепенную перезагрузку](restart.md) кластера.

### Фильтрация по типу узла {#filtraciya-po-tipu-uzla}

Задачи в playbook `ydb_platform.ydb.update_executable` помечены типами узлов, поэтому можно использовать функциональность тегов Ansible для фильтрации узлов по их типу.

Эти две команды эквивалентны и изменят конфигурацию всех [узлов хранения](../../../concepts/glossary.md#storage-node):

```bash
ansible-playbook ydb_platform.ydb.update_executable --tags storage
ansible-playbook ydb_platform.ydb.update_executable --tags static
```

Эти две команды эквивалентны и изменят конфигурацию всех [узлов баз данных](../../../concepts/glossary.md#database-node):

```bash
ansible-playbook ydb_platform.ydb.update_executable --tags database
ansible-playbook ydb_platform.ydb.update_executable --tags dynamic
```

### Пропуск перезагрузки {#propusk-perezagruzki}

Существует тег `no_restart`, чтобы только развернуть исполняемые файлы, а перезагрузку кластера пропустить. Это может быть полезно, если кластер будет [перезагружен](restart.md) позже вручную или в рамках других задач по обслуживанию. Пример запуска:

```bash
ansible-playbook ydb_platform.ydb.update_executable --tags no_restart
```
