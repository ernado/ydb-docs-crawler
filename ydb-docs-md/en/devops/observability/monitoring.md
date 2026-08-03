---
title: "Setting Up YDB Cluster Monitoring"
url: "https://ydb.tech/docs/en/devops/observability/monitoring?version=v26.1"
doc_path: "en/devops/observability/monitoring"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/observability/monitoring.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/observability/monitoring.md"
description: "This page explains how to set up monitoring for a YDB cluster."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Setting Up YDB Cluster Monitoring

This page explains how to set up monitoring for a YDB cluster.

YDB provides numerous system state metrics. Instant metric values can be viewed in the web interface:

```text
http://<ydb-server-address>:<ydb-port>/counters/
```

where:

- `<ydb-server-address>` – YDB server address.

  For a local single-node YDB cluster started using the [Quick start](../../quickstart.md) instructions, use the address `localhost`.

- `<ydb-port>` – YDB port. Default value: 8765.

Related metrics are grouped into subgroups (for example `counters auth`). To view metric values for a specific subgroup only, navigate to a URL of the following form:

```text
http://<ydb-server-address>:<ydb-port>/counters/counters=<servicename>/
```

- `<servicename>` — metric subgroup name.

For example, server hardware resource utilization data is available at the following URL:

```text
http://<ydb-server-address>:<ydb-port>/counters/counters=utils
```

To collect metric values, you can use the popular open-source tool [Prometheus](https://prometheus.io/) or any other system that supports this format. YDB metric values in [Prometheus format](https://prometheus.io/docs/instrumenting/exposition_formats/) are available at URLs of the following form:

```text
http://<ydb-server-address>:<ydb-port>/counters/counters=<servicename>/prometheus
```

- `<servicename>` — metric subgroup name.

Data can be visualized using any system that supports the Prometheus format, such as [Grafana](https://grafana.com/), [Zabbix](https://www.zabbix.com/ru/) or [Amazon CloudWatch](https://aws.amazon.com/ru/cloudwatch/):

![grafana-actors](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/_assets/grafana-actors.png)

## Setting Up Monitoring with Prometheus and Grafana {#prometheus-grafana}

To set up YDB cluster monitoring using [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/):

1. [Install](https://prometheus.io/docs/prometheus/latest/getting_started) Prometheus.

2. Edit the Prometheus [configuration files](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/prometheus):

   1. In the `targets` section of [`ydbd-storage.yml`](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/prometheus/ydbd-storage.yml), specify the addresses of all YDB cluster servers and the ports of storage nodes running on the servers.

      ```json
      - labels:
          container: ydb-static
        targets:
        - "ydb-s1.example.com:8765"
        - "ydb-s2.example.com:8765"
        - "ydb-s3.example.com:8765"
      ```

      For a local single-node YDB cluster, specify one address in the targets section:

      ```json
      - labels:
          container: ydb-static
        targets:
        - "localhost:8765"
      ```

   2. In the `targets` section of [`ydbd-database.yml`](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/prometheus/ydbd-database.yml), specify the addresses of all YDB cluster servers and the ports of all database nodes running on the servers.

      ```json
      - labels:
          container: ydb-dynamic
        targets:
        - "ydb-s1.example.com:31002"
        - "ydb-s1.example.com:31012"
        - "ydb-s1.example.com:31022"
        - "ydb-s2.example.com:31002"
        - "ydb-s2.example.com:31012"
        - "ydb-s2.example.com:31022"
        - "ydb-s3.example.com:31002"
        - "ydb-s3.example.com:31012"
        - "ydb-s3.example.com:31022"
      ```

      For a local single-node YDB cluster, specify one address in the targets section:

      ```json
      - labels:
          container: ydb-dynamic
        targets:
        - "localhost:8765"
      ```

   3. If necessary, in the `tls_config` section of [`prometheus_ydb.yml`](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/prometheus/prometheus_ydb.yml), specify the [Certificate Authority (CA) certificate](../deployment-options/manual/initial-deployment/deployment-preparation.md#tls-certificates) that signed the other TLS certificates of the YDB cluster:

      ```json
      scheme: https
      tls_config:
          ca_file: '<ydb-ca-file>'
      ```

3. [Start](https://prometheus.io/docs/prometheus/latest/getting_started/#starting-prometheus) Prometheus using `prometheus_ydb.yml` as a configuration file.

4. [Install and start](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) Grafana.

5. [Create](https://prometheus.io/docs/visualization/grafana/#creating-a-prometheus-data-source) a data source with type `prometheus` in Grafana and connect it to the running Prometheus instance.

6. Upload [YDB dashboards](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/helm/ydb-prometheus/dashboards) to Grafana.

   You can upload dashboards using the Grafana UI [Import](https://grafana.com/docs/grafana/latest/dashboards/export-import/#import-dashboard) tool or run the [script](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/grafana_dashboards/local_upload_dashboards.sh). Note that the script uses [basic authentication](https://grafana.com/docs/grafana/latest/http_api/create-api-tokens-for-org/#authentication) in Grafana. For other cases, modify the script.

   See the [Grafana dashboards reference](../../reference/observability/metrics/grafana-dashboards.md).
