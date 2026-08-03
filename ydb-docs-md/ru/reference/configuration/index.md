---
title: "Параметры конфигурации кластера"
url: "https://ydb.tech/docs/ru/reference/configuration/?version=v26.1"
doc_path: "ru/reference/configuration/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/index.md"
description: "Конфигурация кластера задается в YAML-файле, который передается в параметре --yaml-config при запуске узлов кластера. В данной статье приведено описание основны"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Параметры конфигурации кластера

Конфигурация кластера задается в YAML-файле, который передается в параметре `--yaml-config` при запуске узлов кластера. В данной статье приведено описание основных разделов конфигурации и ссылки на подробную документацию по каждому разделу.

Каждый раздел конфигурации служит определенной цели в настройке работы кластера YDB, от распределения аппаратных ресурсов до настроек безопасности и функциональных флагов. Конфигурация организована в логические группы, соответствующие различным аспектам управления кластером и его работы.

## Разделы конфигурации {#razdely-konfiguracii}

Доступны следующие разделы конфигурации, расположенные в алфавитном порядке:

|  |  |  |
| --- | --- | --- |
| **Раздел** | **Обязателен** | **Описание** |
| [actor_system_config](actor_system_config.md) | Да | Распределение CPU-ресурсов по пулам акторной системы |
| [auth_config](auth_config.md) | Нет | Настройки аутентификации и авторизации |
| [blob_storage_config](blob_storage_config.md) | Нет | Конфигурация статической группы кластера для системных таблеток |
| [bridge_config](bridge_config.md) | Нет | Конфигурация [режима bridge](../../concepts/bridge.md) |
| [client_certificate_authorization](client_certificate_authorization.md) | Нет | Аутентификация с помощью клиентских сертификатов |
| [cms_config](cms_config.md) | Нет | Конфигурация Cluster Management System (CMS) |
| [domains_config](domains_config.md) | Нет | Конфигурация домена кластера, включая Blob Storage и State Storage |
| [feature_flags](feature_flags.md) | Нет | Функциональные флаги для включения или отключения определённых возможностей YDB |
| [health_check_config](healthcheck_config.md) | Нет | Пороговые значения и таймауты сервиса Health Check |
| [hive_config](hive_config.md) | Нет | Конфигурация запуска таблеток |
| [host_configs](host_configs.md) | Нет | Типовые конфигурации хостов для узлов кластера |
| [hosts](hosts.md) | Да | Конфигурация статических узлов кластера |
| [kafka_proxy_config](kafka_proxy_config.md) | Нет | Конфигурация [Kafka Proxy](../kafka-api/index.md) |
| [log_config](log_config.md) | Нет | Конфигурация и параметры логирования |
| [memory_controller_config](memory_controller_config.md) | Нет | Распределение памяти и лимиты для компонентов базы данных |
| [monitoring_config](monitoring_config.md) | Нет | Параметры [YDB Monitoring](../embedded-ui/ydb-monitoring.md) |
| [node_broker_config](node_broker_config.md) | Нет | Конфигурация стабильных имен узлов |
| [query_service_config](query_service_config.md) | Нет | Конфигурация внешних источников для федеративных запросов |
| [resource_broker_config](resource_broker_config.md) | Нет | Брокер ресурсов для контроля потребления CPU и памяти |
| [security_config](security_config.md) | Нет | Настройки конфигурации безопасности |
| [system_tablet_backup_config](system_tablet_backup_config.md) | Нет | Конфигурация резервного копирования системных таблеток |
| [table_service_config](table_service_config.md) | Нет | Настройки конфигурации выполнения запросов |
| [tli_config](tli_config.md) | Нет | Параметры диагностики [инвалидации блокировок транзакций](../../concepts/glossary.md#tli) (TLI) |
| [tls](tls.md) | Нет | Конфигурация TLS для безопасных соединений |

## Практические рекомендации {#prakticheskie-rekomendacii}

Этот раздел документации посвящён полному описанию доступных настроек, а практические рекомендации по тому, что и когда настраивать, можно найти в следующих местах:

- В рамках первоначального развёртывания кластера YDB:
- [Ansible](../../devops/deployment-options/ansible/initial-deployment/index.md)
- [Kubernetes](../../devops/deployment-options/kubernetes/initial-deployment.md)
- [Вручную](../../devops/deployment-options/manual/initial-deployment/index.md)
- В рамках [поиска и устранения неисправностей](../../troubleshooting/index.md)
- В рамках [усиления безопасности](../../security/index.md)

## Примеры конфигураций кластеров {#primery-konfiguracij-klasterov}

Модельные конфигурации кластера для развертывания можно найти в [репозитории](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/). Изучите их перед развертыванием кластера.
