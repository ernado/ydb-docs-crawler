---
title: "YDB Cluster Configuration"
url: "https://ydb.tech/docs/en/reference/configuration/?version=v26.1"
doc_path: "en/reference/configuration/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/index.md"
description: "The cluster configuration is specified in the YAML file passed in the --yaml-config parameter when the cluster nodes are run. This article provides an overview"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# YDB Cluster Configuration

The cluster configuration is specified in the YAML file passed in the `--yaml-config` parameter when the cluster nodes are run. This article provides an overview of the main configuration sections and links to detailed documentation for each section.

Each configuration section serves a specific purpose in defining how the YDB cluster operates, from hardware resource allocation to security settings and feature flags. The configuration is organized into logical groups that correspond to different aspects of cluster management and operation.

## Configuration Sections

The following top-level configuration sections are available, listed in alphabetical order:

|  |  |  |
| --- | --- | --- |
| **Section** | **Required** | **Description** |
| [actor_system_config](actor_system_config.md) | Yes | CPU resource allocation across actor system pools |
| [auth_config](auth_config.md) | No | Authentication and authorization settings |
| [blob_storage_config](blob_storage_config.md) | No | Static cluster group configuration for system tablets |
| [bridge_config](bridge_config.md) | No | Cluster piles for bridge mode |
| [client_certificate_authorization](client_certificate_authorization.md) | No | Client certificate authentication |
| [cms_config](cms_config.md) | No | Cluster Management System configuration |
| [domains_config](domains_config.md) | No | Cluster domain configuration including Blob Storage and State Storage |
| [feature_flags](feature_flags.md) | No | Feature flags to enable or disable specific YDB features |
| [healthcheck_config](healthcheck_config.md) | No | Health check service thresholds and timeout settings |
| [hive_config](hive.md) | No | Hive component configuration for tablet management |
| [host_configs](host_configs.md) | No | Typical host configurations for cluster nodes |
| [hosts](hosts.md) | Yes | Static cluster nodes configuration |
| [kafka_proxy_config](kafka.md) | No | [Kafka Proxy](../kafka-api/index.md) configuration |
| [log_config](log_config.md) | No | Logging configuration and parameters |
| [memory_controller_config](memory_controller_config.md) | No | Memory allocation and limits for database components |
| [node_broker_config](node_broker_config.md) | No | Stable node names configuration |
| [query_service_config](query_service_config.md) | No | Federated query connector configuration |
| [resource_broker_config](resource_broker_config.md) | No | Resource broker for controlling CPU and memory consumption |
| [security_config](security_config.md) | No | Security configuration settings |
| [`table_service_config` configuration section](table_service_config.md) | No | Query processing configuration |
| [tli_config](tli_config.md) | No | [Transaction lock invalidation](../../concepts/glossary.md#tli) (TLI) diagnostics parameters |
| [tls](tls.md) | No | TLS configuration for secure connections |

## Practical Guidelines

While this documentation section focuses on complete reference documentation for available settings, practical recommendations on what to tune and when can be found in the following places:

- As part of the initial YDB cluster deployment:

  - [Ansible](../../devops/deployment-options/ansible/initial-deployment/index.md)
  - [Kubernetes](../../devops/deployment-options/kubernetes/initial-deployment.md)
  - [Manual](../../devops/deployment-options/manual/initial-deployment/index.md)

- As part of [troubleshooting](../../troubleshooting/index.md)

- As part of [security hardening](../../security/index.md)

## Sample Cluster Configurations

You can find model cluster configurations for deployment in the [repository](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/). Check them out before deploying a cluster.
