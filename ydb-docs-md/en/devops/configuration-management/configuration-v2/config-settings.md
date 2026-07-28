---
title: "YDB Cluster Configuration"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v2/config-settings?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v2/config-settings"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v2/config-settings.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v2/config-settings.md"
description: "YDB Cluster Configuration."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# YDB Cluster Configuration

The cluster configuration is specified in the YAML file passed in the `--yaml-config` parameter when the cluster nodes are run. This article provides an overview of the main configuration sections and links to detailed documentation for each section.

Each configuration section serves a specific purpose in defining how the YDB cluster operates, from hardware resource allocation to security settings and feature flags. The configuration is organized into logical groups that correspond to different aspects of cluster management and operation.

## Configuration Sections

The following top-level configuration sections are available, listed in alphabetical order:

|  |  |  |
| --- | --- | --- |
| **Section** | **Required** | **Description** |
| [actor_system_config](../../../reference/configuration/actor_system_config.md) | Yes | CPU resource allocation across actor system pools |
| [auth_config](../../../reference/configuration/auth_config.md) | No | Authentication and authorization settings |
| [blob_storage_config](../../../reference/configuration/blob_storage_config.md) | No | Static cluster group configuration for system tablets |
| [bridge_config](../../../reference/configuration/bridge_config.md) | No | Cluster piles for bridge mode |
| [client_certificate_authorization](../../../reference/configuration/client_certificate_authorization.md) | No | Client certificate authentication |
| [cms_config](../../../reference/configuration/cms_config.md) | No | Cluster Management System configuration |
| [domains_config](../../../reference/configuration/domains_config.md) | No | Cluster domain configuration including Blob Storage and State Storage |
| [feature_flags](../../../reference/configuration/feature_flags.md) | No | Feature flags to enable or disable specific YDB features |
| [healthcheck_config](../../../reference/configuration/healthcheck_config.md) | No | Health check service thresholds and timeout settings |
| [hive_config](../../../reference/configuration/hive.md) | No | Hive component configuration for tablet management |
| [host_configs](../../../reference/configuration/host_configs.md) | No | Typical host configurations for cluster nodes |
| [hosts](../../../reference/configuration/hosts.md) | Yes | Static cluster nodes configuration |
| [kafka_proxy_config](../../../reference/configuration/kafka.md) | No | [Kafka Proxy](../../../reference/kafka-api/index.md) configuration |
| [log_config](../../../reference/configuration/log_config.md) | No | Logging configuration and parameters |
| [memory_controller_config](../../../reference/configuration/memory_controller_config.md) | No | Memory allocation and limits for database components |
| [node_broker_config](../../../reference/configuration/node_broker_config.md) | No | Stable node names configuration |
| [query_service_config](../../../reference/configuration/query_service_config.md) | No | Federated query connector configuration |
| [resource_broker_config](../../../reference/configuration/resource_broker_config.md) | No | Resource broker for controlling CPU and memory consumption |
| [security_config](../../../reference/configuration/security_config.md) | No | Security configuration settings |
| [`table_service_config` configuration section](../../../reference/configuration/table_service_config.md) | No | Query processing configuration |
| [tli_config](../../../reference/configuration/tli_config.md) | No | [Transaction lock invalidation](../../../concepts/glossary.md#tli) (TLI) diagnostics parameters |
| [tls](../../../reference/configuration/tls.md) | No | TLS configuration for secure connections |

## Practical Guidelines

While this documentation section focuses on complete reference documentation for available settings, practical recommendations on what to tune and when can be found in the following places:

- As part of the initial YDB cluster deployment:

  - [Ansible](../../deployment-options/ansible/initial-deployment/index.md)
  - [Kubernetes](../../deployment-options/kubernetes/initial-deployment.md)
  - [Manual](../../deployment-options/manual/initial-deployment/index.md)

- As part of [troubleshooting](../../../troubleshooting/index.md)

- As part of [security hardening](../../../security/index.md)

## Sample Cluster Configurations

You can find model cluster configurations for deployment in the [repository](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/). Check them out before deploying a cluster.
