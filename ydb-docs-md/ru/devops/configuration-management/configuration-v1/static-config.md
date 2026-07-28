---
title: "Параметры конфигурации кластера"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/static-config?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/static-config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/static-config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/static-config.md"
description: "Параметры конфигурации кластера."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Параметры конфигурации кластера

Конфигурация кластера задается в YAML-файле, который передается в параметре `--yaml-config` при запуске узлов кластера. В данной статье приведено описание основных разделов конфигурации и ссылки на подробную документацию по каждому разделу.

Каждый раздел конфигурации служит определенной цели в настройке работы кластера YDB, от распределения аппаратных ресурсов до настроек безопасности и функциональных флагов. Конфигурация организована в логические группы, соответствующие различным аспектам управления кластером и его работы.

## Разделы конфигурации {#razdely-konfiguracii}

Доступны следующие разделы конфигурации, расположенные в алфавитном порядке:

|  |  |  |
| --- | --- | --- |
| **Раздел** | **Обязателен** | **Описание** |
| [actor_system_config](../../../reference/configuration/actor_system_config.md) | Да | Распределение CPU-ресурсов по пулам акторной системы |
| [auth_config](../../../reference/configuration/auth_config.md) | Нет | Настройки аутентификации и авторизации |
| [blob_storage_config](../../../reference/configuration/blob_storage_config.md) | Нет | Конфигурация статической группы кластера для системных таблеток |
| [bridge_config](../../../reference/configuration/bridge_config.md) | Нет | Конфигурация [режима bridge](../../../concepts/bridge.md) |
| [client_certificate_authorization](../../../reference/configuration/client_certificate_authorization.md) | Нет | Аутентификация с помощью клиентских сертификатов |
| [cms_config](../../../reference/configuration/cms_config.md) | Нет | Конфигурация Cluster Management System (CMS) |
| [domains_config](../../../reference/configuration/domains_config.md) | Нет | Конфигурация домена кластера, включая Blob Storage и State Storage |
| [feature_flags](../../../reference/configuration/feature_flags.md) | Нет | Функциональные флаги для включения или отключения определённых возможностей YDB |
| [health_check_config](../../../reference/configuration/healthcheck_config.md) | Нет | Пороговые значения и таймауты сервиса Health Check |
| [hive_config](../../../reference/configuration/hive_config.md) | Нет | Конфигурация запуска таблеток |
| [host_configs](../../../reference/configuration/host_configs.md) | Нет | Типовые конфигурации хостов для узлов кластера |
| [hosts](../../../reference/configuration/hosts.md) | Да | Конфигурация статических узлов кластера |
| [kafka_proxy_config](../../../reference/configuration/kafka_proxy_config.md) | Нет | Конфигурация [Kafka Proxy](../../../reference/kafka-api/index.md) |
| [log_config](../../../reference/configuration/log_config.md) | Нет | Конфигурация и параметры логирования |
| [memory_controller_config](../../../reference/configuration/memory_controller_config.md) | Нет | Распределение памяти и лимиты для компонентов базы данных |
| [monitoring_config](../../../reference/configuration/monitoring_config.md) | Нет | Параметры [YDB Monitoring](../../../reference/embedded-ui/ydb-monitoring.md) |
| [node_broker_config](../../../reference/configuration/node_broker_config.md) | Нет | Конфигурация стабильных имен узлов |
| [query_service_config](../../../reference/configuration/query_service_config.md) | Нет | Конфигурация внешних источников для федеративных запросов |
| [resource_broker_config](../../../reference/configuration/resource_broker_config.md) | Нет | Брокер ресурсов для контроля потребления CPU и памяти |
| [security_config](../../../reference/configuration/security_config.md) | Нет | Настройки конфигурации безопасности |
| [system_tablet_backup_config](../../../reference/configuration/system_tablet_backup_config.md) | Нет | Конфигурация резервного копирования системных таблеток |
| [table_service_config](../../../reference/configuration/table_service_config.md) | Нет | Настройки конфигурации выполнения запросов |
| [tli_config](../../../reference/configuration/tli_config.md) | Нет | Параметры диагностики [инвалидации блокировок транзакций](../../../concepts/glossary.md#tli) (TLI) |
| [tls](../../../reference/configuration/tls.md) | Нет | Конфигурация TLS для безопасных соединений |

## Практические рекомендации {#prakticheskie-rekomendacii}

Этот раздел документации посвящён полному описанию доступных настроек, а практические рекомендации по тому, что и когда настраивать, можно найти в следующих местах:

- В рамках первоначального развёртывания кластера YDB:
- [Ansible](../../deployment-options/ansible/initial-deployment/index.md)
- [Kubernetes](../../deployment-options/kubernetes/initial-deployment.md)
- [Вручную](../../deployment-options/manual/initial-deployment/index.md)
- В рамках [поиска и устранения неисправностей](../../../troubleshooting/index.md)
- В рамках [усиления безопасности](../../../security/index.md)

## Примеры конфигураций кластеров {#primery-konfiguracij-klasterov}

Модельные конфигурации кластера для развертывания можно найти в [репозитории](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/). Изучите их перед развертыванием кластера.
