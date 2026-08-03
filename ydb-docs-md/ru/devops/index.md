---
title: "YDB для DevOps-инженеров"
url: "https://ydb.tech/docs/ru/devops/?version=v26.1"
doc_path: "ru/devops/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/index.md"
description: "В этом разделе документации YDB описано всё, что нужно знать для работы с кластерами YDB."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# YDB для DevOps-инженеров

В этом разделе документации YDB описано всё, что нужно знать для работы с кластерами YDB.

Перед началом работы рекомендуется ознакомиться с [системными требованиями YDB](concepts/system-requirements.md).

Основные подразделы:

- [Концепции для DevOps-инженеров](concepts/index.md) — дополнения к общему разделу [концепций](../concepts/index.md), актуальные для DevOps-инженеров.

- [Конфигурация кластеров YDB](configuration-management/index.md) — управление конфигурацией кластеров YDB.

- [Способы развёртывания YDB](deployment-options/index.md) — способы развёртывания кластеров YDB.

  - **[Ansible](deployment-options/ansible/index.md)**: для развертываний на физическом оборудовании и виртуальных машинах.
  - **[Kubernetes](deployment-options/kubernetes/index.md)**: для развёртываний в контейнерах.
  - **[Вручную](deployment-options/manual/index.md)**: развертывание кластера вручную.

- [Обзор наблюдаемости](observability/index.md) — инструменты для наблюдения за кластерами YDB.

- [Резервное копирование и восстановление](backup-and-recovery/index.md) — резервное копирование и восстановление кластеров YDB.
