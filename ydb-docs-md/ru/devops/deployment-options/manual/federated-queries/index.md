---
title: "Развёртывание YDB с функцией Federated Query"
url: "https://ydb.tech/docs/ru/devops/deployment-options/manual/federated-queries/?version=v26.1"
doc_path: "ru/devops/deployment-options/manual/federated-queries/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/manual/federated-queries/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/manual/federated-queries/index.md"
description: "Важно. Данная функциональность находится в режиме \"Experimental\". Общая схема инсталляции."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Развёртывание YDB с функцией Federated Query

> [!WARNING]
> Данная функциональность находится в режиме "Experimental".

## Общая схема инсталляции {#general-scheme}

YDB может выполнять [федеративные запросы](../../../../concepts/query_execution/federated_query/index.md) ко внешним источникам (например, объектным хранилищам или реляционным СУБД) без необходимости перемещения их данных непосредственно в YDB. В данном разделе мы рассмотрим изменения, которые необходимо внести в конфигурацию YDB и окружающую инфраструктуру для включения функциональности федеративных запросов.

> [!NOTE]
> Для организации доступа к некоторым из источников данных требуется развёртывание специального микросервиса - [коннектора](../../../../concepts/query_execution/federated_query/architecture.md#connectors). Ознакомьтесь c [перечнем поддерживаемых источников](../../../../concepts/query_execution/federated_query/architecture.md#supported-datasources), чтобы понять, требуется ли вам установка коннектора.

Кластер YDB и внешние источники данных в варианте production-инсталляции должны развёртываться на разных физических или виртуальных серверах, в том числе в облаках. Если для доступа к определённому источнику требуется развёртывание коннектора, это необходимо сделать на тех же серверах, на которых развёрнуты динамические узлы YDB. Иными словами, на каждый процесс `ydbd`, работающий в режиме динамического узла, должен приходиться один локальный процесс коннектора.

При этом должны выполняться следующие требования:

- внешний источник данных должен быть доступен по сети для запросов со стороны YDB или со стороны коннектора (при его наличии);
- коннектор должен быть доступен по сети для запросов со стороны YDB (что достигается тривиальным образом благодаря работе этих процессов на одном и том же хосте).

![Инсталляция YDB FQ](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/deployment-options/manual/federated-queries/_images/ydb_fq_onprem.png "Инсталляция YDB FQ")

> [!NOTE]
> В настоящее время мы не поддерживаем развёртывание коннектора в Kubernetes, но планируем добавить её в ближайшем будущем.

## Пошаговое руководство {#poshagovoe-rukovodstvo}

1. Выполните шаги инструкции по развёртыванию динамического узла YDB до [подготовки конфигурационных файлов](../initial-deployment/index.md#config) включительно.
2. Если для доступа к нужному вам источнику требуется развернуть коннектор, сделайте это [согласно инструкции](connector-deployment.md).
3. [В конфигурационном файле](../../../../reference/configuration/index.md) YDB в секции `feature_flags` включите флаг `enable_external_data_sources`:

```yaml
feature_flags:
  enable_external_data_sources: true
```

4. [В конфигурационный файл](../../../../reference/configuration/index.md) YDB добавьте [настройки внешних источников данных](../../../../reference/configuration/query_service_config.md).

{% list tabs %}

- Без использования коннектора

  ```yaml
  query_service_config:
    generic:
      default_settings:
      - name: UsePredicatePushdown
        value: "true"
    all_external_data_sources_are_available: false
    available_external_data_sources:
    - ObjectStorage
  ```

- С использованием коннектора

  ```yaml
  query_service_config:
    generic:
      connector:
        endpoint:
          host: localhost                   # имя хоста, где развернут коннектор
          port: 2130                        # номер порта коннектора
        use_ssl: false                      # флаг, включающий шифрование соединений
        ssl_ca_crt: "/opt/ydb/certs/ca.crt" # путь к сертификату CA
      default_settings:
      - name: UsePredicatePushdown
        value: "true"
    all_external_data_sources_are_available: false
    available_external_data_sources:
    - ClickHouse
    - MySQL
  ```

{% endlist %}

5. Продолжайте развёртывание динамического узла YDB по [инструкции](../initial-deployment/index.md).
