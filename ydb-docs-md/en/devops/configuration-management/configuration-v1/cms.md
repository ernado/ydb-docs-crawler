---
title: "Changing Configurations via CMS"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v1/cms?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v1/cms"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v1/cms.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/cms.md"
description: "Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Changing Configurations via CMS

> [!NOTE]
> This method of changing configuration is deprecated. The recommended configuration method for V1 is described in the [cluster dynamic configuration](dynamic-config.md) section.

## Get Current Settings

The following command will get current settings for the cluster or tenant.

```bash
ydbd -s <endpoint> admin console configs load --out-dir <config-folder>
```

```bash
ydbd -s <endpoint> admin console configs load --out-dir <config-folder> --tenant <tenant-name>
```

## Update Settings

First, you need to download the required config as indicated above, then you need to prepare a protobuf file with a change request.

```proto
Actions {
  AddConfigItem {
    ConfigItem {
      Cookie: "<cookie>"
      UsageScope {
        TenantAndNodeTypeFilter {
          Tenant: "<tenant-name>"
        }
      }
      Config {
          <config-name> {
              <full-config>
          }
      }
    }
  }
}
```

The UsageScope field is optional and is needed to apply settings for a specific tenant.

```bash
ydbd -s <endpoint> admin console configs update <protobuf-file>
```
