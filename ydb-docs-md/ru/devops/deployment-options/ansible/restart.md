---
title: "Перезапуск кластеров YDB, развёрнутых с помощью Ansible"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/restart?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/restart"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/restart.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/restart.md"
description: "Кластеры YDB обеспечивают высокие гарантии доступности; поэтому необходимо учитывать модель отказоустойчивости кластера во время любого технического обслуживани"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Перезапуск кластеров YDB, развёрнутых с помощью Ansible

Кластеры YDB обеспечивают высокие гарантии доступности; поэтому необходимо учитывать модель отказоустойчивости кластера во время любого технического обслуживания, включая перезапуск кластера. Существует два типа узлов, которые могут потребовать перезапуска:

- Database узлы (также известные как динамические) не сохраняют состояние; поэтому основное внимание стоит уделять тому, чтобы их было достаточно для обработки нагрузки каждой базы данных. Обычно для динамических узлов достаточно простого поэтапного перезапуска с небольшими задержками.
- Storage узлы (также известные как статические) имеют персистентное состояние и отвечают за безопасное хранение данных. Поэтому они требуют особого обращения для обеспечения доступности данных. Каждый кластер YDB имеет выделенный компонент, который отслеживает все сбои и обслуживание и может определить, безопасно ли сейчас остановить или перезапустить конкретный узел. Поэтому важно запрашивать у него разрешение на каждую операцию, а полный перезапуск узлов хранения часто занимает некоторое время.

## Перезапуск через Ansible playbook {#perezapusk-cherez-ansible-playbook}

Репозиторий [ydb-ansible](https://github.com/ydb-platform/ydb-ansible) содержит playbook под названием `ydb_platform.ydb.restart`, который можно использовать для перезапуска кластера YDB. Запускайте его из той же директории, которая использовалась для [изначального развёртывания](initial-deployment/index.md).

### Перезапуск всех узлов {#perezapusk-vseh-uzlov}

По умолчанию `ydb_platform.ydb.restart` перезапускает все узлы кластера. Сначала идут статические узлы, затем динамические. Команда для его запуска:

```bash
ansible-playbook ydb_platform.ydb.restart
```

### Фильтр по типу узлов {#filtr-po-tipu-uzlov}

Задачи в playbook `ydb_platform.ydb.restart` помечены типами узлов, поэтому вы можете использовать функциональность тегов Ansible для фильтрации узлов по их типу.

Эти две команды эквивалентны и перезапустят все узлы хранения:

```bash
ansible-playbook ydb_platform.ydb.restart --tags storage
ansible-playbook ydb_platform.ydb.restart --tags static
```

Эти две команды эквивалентны и перезапустят все узлы баз данных:

```bash
ansible-playbook ydb_platform.ydb.restart --tags database
ansible-playbook ydb_platform.ydb.restart --tags dynamic
```

### Фильтр по имени хоста {#filtr-po-imeni-hosta}

Чтобы перезапустить конкретный хост или подмножество хостов, используйте аргумент `--limit`:

```bash
ansible-playbook ydb_platform.ydb.restart --limit='<hostname>'
ansible-playbook ydb_platform.ydb.restart --limit='<hostname-1,hostname-2>'
```

Его можно использовать и вместе с тегами:

```bash
ansible-playbook ydb_platform.ydb.restart --tags database --limit='<hostname>'
```

## Перезапуск узлов вручную {#perezapusk-uzlov-vruchnuyu}

Инструмент [ydbops](https://github.com/ydb-platform/ydbops) реализует различные манипуляции с кластерами YDB, включая перезапуск. Описанный выше playbook `ydb_platform.ydb.restart` использует его за сценой, но использование его вручную тоже допустимо.

Больше рекомендаций и информации о том, как это работает, находится в статье [Обслуживание кластера без потери доступности](../../concepts/maintenance-without-downtime.md).
