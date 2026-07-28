---
title: "blob_storage_config"
url: "https://ydb.tech/docs/en/reference/configuration/blob_storage_config?version=v26.1"
doc_path: "en/reference/configuration/blob_storage_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/blob_storage_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/blob_storage_config.md"
description: "The blob_storage_config section specifies a static cluster group's configuration. A static group is necessary for the operation of the basic cluster tablets, in"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# blob_storage_config

The `blob_storage_config` section specifies a static cluster group's configuration. A static group is necessary for the operation of the basic cluster tablets, including `Hive`, `SchemeShard`, and `BlobstorageController`. As a rule, these tablets do not store a lot of data, so we don't recommend creating more than one static group.

For a static group, specify the disks and nodes that the static group will be placed on. For example, a configuration for the `erasure: none` model can be as follows:

```bash
blob_storage_config:
  service_set:
    groups:
    - erasure_species: none
      rings:
      - fail_domains:
        - vdisk_locations:
          - node_id: 1
            path: /dev/disk/by-partlabel/ydb_disk_ssd_02
            pdisk_category: SSD
....
```

For a configuration located in 3 availability zones, specify 3 rings. For a configuration within a single availability zone, specify exactly one ring.
