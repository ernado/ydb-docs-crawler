---
title: "Обновление исполняемого файла YDB"
url: "https://ydb.tech/docs/ru/devops/deployment-options/manual/update-executable?version=v26.1"
doc_path: "ru/devops/deployment-options/manual/update-executable"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/manual/update-executable.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/manual/update-executable.md"
description: "YDB распределенная система, поддерживающая плавное обновление (rolling restart) без даунтайма и деградации производительности. Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Обновление исполняемого файла YDB

YDB распределенная система, поддерживающая плавное обновление (rolling restart) без даунтайма и деградации производительности.

> [!WARNING]
> У YDB существуют специфические правила относительно совместимости версий. Важно ознакомиться с [руководством по именованию версий YDB и их совместимости](../../concepts/versioning.md) и [списком изменений](../../../changelog-server.md), чтобы правильно выбрать новую версию для обновления и подготовиться к возможным нюансам.

## Порядок обновления {#upgrade-order}

Базовым сценарием является обновление исполняемого файла и затем последовательный рестарт каждого узла:

1. Обновление и рестарт [узлов хранения](../../../concepts/glossary.md#storage-node);
2. Обновление и рестарт [узлов баз данных](../../../concepts/glossary.md#database-node).

Процесс остановки и запуска описан на странице [Безопасные рестарт и выключение узлов](../../../maintenance/manual/node_restarting.md).  
 Узлы YDB следует обновлять последовательно по одному, после каждого шага контролировать состояние кластера через [YDB Monitoring](../../../reference/embedded-ui/ydb-monitoring.md) - на вкладке `Storage` не должно быть пулов в состоянии `Degraded` (как на примере ниже). В противном случае обновление необходимо остановить.

![Monitoring_storage_state](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/reference/embedded-ui/_assets/monitoring_storage_state.png)

## Проверка результата обновления {#upgrade_check}

Проверить версии узлов после обновления можно на странице `Nodes` мониторинга.
