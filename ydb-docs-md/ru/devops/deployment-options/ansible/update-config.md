---
title: "Обновление конфигурации кластеров YDB, развёрнутых с Ansible"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/update-config?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/update-config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/update-config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/update-config.md"
description: "Во время первоначального развёртывания Ansible playbook использует предоставленный конфигурационный файл для создания начальной конфигурации кластера. Техническ"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Обновление конфигурации кластеров YDB, развёрнутых с Ansible

Во время [первоначального развёртывания](initial-deployment/index.md) Ansible playbook использует предоставленный конфигурационный файл для создания начальной конфигурации кластера. Технически, он генерирует два варианта конфигурационного файла на основе исходного и размещает их на всех хостах через механизм Ansible для копирования файлов между серверами. В этой статье рассматриваются доступные способы для изменения конфигурации кластера после первоначального развёртывания.

## Обновление конфигурации через Ansible playbook {#obnovlenie-konfiguracii-cherez-ansible-playbook}

В репозитории [ydb-ansible](https://github.com/ydb-platform/ydb-ansible) есть playbook под названием `ydb_platform.ydb.update_config`, который можно использовать для обновления конфигурации кластера YDB. Перейдите в ту же директорию, которая использовалась для [первоначального развёртывания](initial-deployment/index.md) кластера, отредактируйте файл `files/config.yaml` по необходимости и затем запустите этот playbook:

```bash
ansible-playbook ydb_platform.ydb.update_config
```

Этот playbook развернёт новую версию конфигурационных файлов и затем выполнит [постепенную перезагрузку](restart.md) кластера.

### Фильтрация по типу узла {#filtraciya-po-tipu-uzla}

Задачи в playbook `ydb_platform.ydb.update_config` помечены типами узлов, поэтому вы можете использовать функциональность тегов Ansible для фильтрации узлов по их типу.

Эти две команды эквивалентны и изменят конфигурацию всех [узлов хранения](../../../concepts/glossary.md#storage-node):

```bash
ansible-playbook ydb_platform.ydb.update_config --tags storage
ansible-playbook ydb_platform.ydb.update_config --tags static
```

Эти две команды эквивалентны и изменят конфигурацию всех [узлов баз данных](../../../concepts/glossary.md#database-node):

```bash
ansible-playbook ydb_platform.ydb.update_config --tags database
ansible-playbook ydb_platform.ydb.update_config --tags dynamic
```

### Пропуск перезагрузки {#propusk-perezagruzki}

Также есть тег `no_restart`, который позволяет только обновить конфигурационные файлы и пропустить перезагрузку кластера. Это может быть полезно, если кластер будет [перезагружен](restart.md) позже вручную или в рамках других задач по обслуживанию. Пример запуска:

```bash
ansible-playbook ydb_platform.ydb.update_config --tags no_restart
```
