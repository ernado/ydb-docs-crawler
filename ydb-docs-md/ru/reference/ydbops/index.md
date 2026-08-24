---
title: "Обзор утилиты ydbops"
url: "https://ydb.tech/docs/ru/reference/ydbops/?version=v26.1"
doc_path: "ru/reference/ydbops/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydbops/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydbops/index.md"
description: "Примечание. Утилита ydbops находится в активной разработке. В редких случаях обратная совместимость может быть нарушена."
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# Обзор утилиты ydbops

> [!NOTE]
> Утилита `ydbops` находится в активной разработке. В редких случаях обратная совместимость может быть нарушена.

Утилита `ydbops` облегчает выполнение объемных сценариев на кластерах YDB. Утилита поддерживает кластеры, развернутые с помощью [Ansible](../../devops/deployment-options/ansible/index.md), [Kubernetes](../../devops/deployment-options/kubernetes/index.md) или [вручную](../../devops/deployment-options/manual/index.md).

## Смотрите также {#smotrite-takzhe}

- Для установки утилиты следуйте [инструкциям](install.md).
- Для настройки утилиты смотрите [справочник по конфигурации](configuration.md).
- Исходный код `ydbops` доступен [на GitHub](https://github.com/ydb-platform/ydbops).

## Поддерживаемые сценарии {#podderzhivaemye-scenarii}

- Выполнение [перезагрузки кластера](rolling-restart-scenario.md).

## Сценарии в разработке {#scenarii-v-razrabotke}

- Запрос разрешения на вывод узлов YDB на обслуживание без нарушения инвариантов модели отказа YDB.
