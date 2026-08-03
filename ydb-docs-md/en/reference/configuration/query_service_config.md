---
title: "query_service_config"
url: "https://ydb.tech/docs/en/reference/configuration/query_service_config?version=v26.1"
doc_path: "en/reference/configuration/query_service_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/query_service_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/query_service_config.md"
description: "The query_service_config section describes the parameters for YDB to work with external data sources using federated queries."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# query_service_config

The `query_service_config` section describes the parameters for YDB to work with external data sources using federated queries.

If access to the required source requires deploying a connector, it must also be configured according to the [instructions](../../devops/deployment-options/manual/federated-queries/connector-deployment.md).

## Parameter description

|  |  |  |
| --- | --- | --- |
| **Parameter** | **Default value** | **Description** |
| `generic.connector.endpoint.host` | `localhost` | Connector host name. |
| `generic.connector.endpoint.port` | `2130` | Connector TCP port. |
| `generic.connector.use_ssl` | `false` | Whether to use connection encryption. When the connector and YDB dynamic node are deployed on the same server, encrypted connection between them is not required, but it can be enabled if needed. |
| `generic.connector.ssl_ca_crt` | empty string | Path to the CA certificate used for encryption. |
| `generic.default_settings.name.UsePredicatePushdown` | `false` | Enables predicate pushdown to external data sources: some parts of SQL queries (for example, filters) will be passed for execution to the external source. This can significantly reduce the volume of data transferred over the network from the data source to federated YDB, save its computational resources, and significantly reduce federated query processing time. |
| `available_external_data_sources` | empty list | List of allowed external data source types. Applied when `all_external_data_sources_are_available: false`.<br>Possible values:<br>- `ObjectStorage`;<br>- `ClickHouse`;<br>- `PostgreSQL`;<br>- `MySQL`;<br>- `Greenplum`;<br>- `MsSQLServer`;<br>- `Ydb`. |
| `all_external_data_sources_are_available` | `false` | Enable all external data source types. When enabled, the `available_external_data_sources` setting is ignored. |

## Examples

### Enabling ClickHouse and MySQL external sources

```yaml
query_service_config:
  generic:
    connector:
      endpoint:
        host: localhost                   # host name where the connector is deployed
        port: 2130                        # connector port number
      use_ssl: false                      # flag to enable connection encryption
      ssl_ca_crt: "/opt/ydb/certs/ca.crt" # path to CA certificate
    default_settings:
    - name: UsePredicatePushdown
      value: "true"
  all_external_data_sources_are_available: false
  available_external_data_sources:
  - ClickHouse
  - MySQL
```

### Enabling all external data source types

```yaml
query_service_config:
  generic:
    connector:
      endpoint:
        host: localhost                   # host name where the connector is deployed
        port: 2130                        # connector port number
      use_ssl: false                      # flag to enable connection encryption
      ssl_ca_crt: "/opt/ydb/certs/ca.crt" # path to CA certificate
    default_settings:
    - name: UsePredicatePushdown
      value: "true"
  all_external_data_sources_are_available: true
```

## See also

- [Deploying YDB with Federated Query functionality](../../devops/deployment-options/manual/federated-queries/index.md)
