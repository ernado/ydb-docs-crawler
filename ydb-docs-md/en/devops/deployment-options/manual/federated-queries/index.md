---
title: "Deploying YDB with Federated Query functionality"
url: "https://ydb.tech/docs/en/devops/deployment-options/manual/federated-queries/?version=v26.1"
doc_path: "en/devops/deployment-options/manual/federated-queries/"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/manual/federated-queries/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/manual/federated-queries/index.md"
description: "Warning. This functionality is in the \"Experimental\" mode. General Installation Scheme."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Deploying YDB with Federated Query functionality

> [!WARNING]
> This functionality is in the "Experimental" mode.

## General Installation Scheme {#general-scheme}

YDB can perform [federated queries](../../../../concepts/query_execution/federated_query/index.md) to external sources, for example, object storages or relational DBMS, without the need to move the data from external sources directly into YDB. This section describes the changes that are required in the configuration of YDB and the surrounding infrastructure to enable federated queries.

> [!NOTE]
> A special microservice called [connector](../../../../concepts/query_execution/federated_query/architecture.md#connectors) must be deployed to access some of data sources. Check the [list of supported sources](../../../../concepts/query_execution/federated_query/architecture.md#supported-datasources) to determine if you need to install a connector.

The YDB cluster and external data sources in a production installation should be deployed on different physical or virtual servers, including clouds. If access to a specific source requires a connector, it should be deployed on the same servers as the dynamic nodes of YDB. In other words, each `ydbd` process running in dynamic node mode should have one local connector process.

The following requirements must be met:

- The external data source must be accessible over the network to queries from YDB database nodes or from the connector, if present.
- The connector must be accessible over the network from YDB database nodes.

> [!TIP]
> The easiest way to make the connector accessible from YDB nodes is to run them on the same set of hosts.

![YDB FQ Installation](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/devops/deployment-options/manual/federated-queries/_images/ydb_fq_onprem.png "YDB FQ Installation")

> [!NOTE]
> Currently, we do not support deploying the connector in Kubernetes, but we plan to add it shortly.

## Step-by-Step Guide

1. Follow the steps in the dynamic node YDB deployment guide up to and including [preparing the configuration files](../initial-deployment/deployment-configuration-v1.md#config).

2. If a connector must be deployed to access the desired source, do so [according to the instructions](connector-deployment.md).

3. If a connector needs to be deployed to access your desired source, add the `generic` subsection to the `query_service_config` section of the YDB configuration file as shown below. Specify the network address of the connector in the `connector.endpoint.host` and `connector.endpoint.port` fields (default values are `localhost` and `2130`). When co-locating the connector and the YDB dynamic node on the same server, encrypted connections between them are *not required*. If necessary, you can enable encryption by setting `connector.use_ssl` to `true` and specifying the path to the CA certificate that is used to sign the connector's TLS keys in `connector.ssl_ca_crt`:

   ```yaml
   query_service_config:
       generic:
           connector:
               endpoint:
                   host: localhost                 # hostname where the connector is deployed
                   port: 2130                      # port number for the connector's listening socket
               use_ssl: false                      # flag to enable encrypted connections
               ssl_ca_crt: "/opt/ydb/certs/ca.crt" # (optional) path to the CA certificate
           default_settings:
               - name: DateTimeFormat
                 value: string
               - name: UsePredicatePushdown
                 value: "true"
   ```

4. Add the following `feature_flags` section to the YDB configuration file:

   ```yaml
   feature_flags:
       enable_external_data_sources: true
       enable_script_execution_operations: true
   ```

5. Continue deploying YDB database nodes. See the [instructions](../initial-deployment/index.md).
