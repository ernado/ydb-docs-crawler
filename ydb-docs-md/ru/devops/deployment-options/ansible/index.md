---
title: "Работа с YDB с помощью Ansible"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/index.md"
description: "Этот раздел документации YDB содержит набор статей, предназначенных для работы DevOps-инженеров с кластерами YDB при помощи Ansible. Это рекомендуемый подход к"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Работа с YDB с помощью Ansible

Этот раздел документации YDB содержит набор статей, предназначенных для работы DevOps-инженеров с кластерами YDB при помощи [Ansible](https://www.ansible.com/). Это рекомендуемый подход к запуску produciton кластеров YDB непосредственно на виртуальных машинах и физических серверах. Для контейнерных окружений вместо Ansible рекомендуется использовать [Kubernetes](../kubernetes/index.md).

Ключевые статьи для начала работы с этим разделом:

- [Развёртывание YDB кластера с помощью Ansible](initial-deployment/index.md)

- [Развёртывание инфраструктуры для кластера YDB с помощью Terraform](preparing-vms-with-terraform.md)

- [Перезапуск кластеров YDB, развёрнутых с помощью Ansible](restart.md)

- Наблюдаемость:

  - [Логирование в кластерах, развёрнутых с помощью Ansible](observability/logging.md)
