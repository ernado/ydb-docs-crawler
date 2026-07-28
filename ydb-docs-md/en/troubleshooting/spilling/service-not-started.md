---
title: "Spilling Service Not Started"
url: "https://ydb.tech/docs/en/troubleshooting/spilling/service-not-started?version=v26.1"
doc_path: "en/troubleshooting/spilling/service-not-started"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/spilling/service-not-started.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/spilling/service-not-started.md"
description: "An attempt to use spilling occurs when the Spilling Service is disabled. This happens when the spilling service is not properly configured or has been disabled"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Spilling Service Not Started

An attempt to use spilling occurs when the Spilling Service is disabled. This happens when the spilling service is not properly configured or has been disabled in the configuration.

## Diagnostics

Check the spilling service configuration:

- Verify that [`table_service_config.spilling_service_config.local_file_config.enable`](../../reference/configuration/table_service_config.md#local-file-config-enable) is set to `true`.

## Recommendations

To enable spilling:

1. Set [`table_service_config.spilling_service_config.local_file_config.enable`](../../reference/configuration/table_service_config.md#local-file-config-enable): `true` in your configuration.

> [!NOTE]
> Read more about the spilling architecture in [Spilling in YDB](../../concepts/query_execution/spilling.md#spilling-in-ydb-short-name).
