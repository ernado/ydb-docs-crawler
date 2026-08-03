---
title: "blob_storage_config"
url: "https://ydb.tech/docs/ru/reference/configuration/blob_storage_config?version=v26.1"
doc_path: "ru/reference/configuration/blob_storage_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/blob_storage_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/blob_storage_config.md"
description: "Укажите конфигурацию статической группы кластера. Статическая группа необходима для работы базовых таблеток кластера, в том числе Hive, SchemeShard, Blobstorage"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# blob_storage_config

Укажите конфигурацию статической группы кластера. Статическая группа необходима для работы базовых таблеток кластера, в том числе `Hive`, `SchemeShard`, `BlobstorageController`.  
 Обычно данные таблетки не хранят много информации, поэтому мы не рекомендуем создавать более одной статической группы.

Для статической группы необходимо указать информацию о дисках и узлах, на которых будет размещена статическая группа. Например, для модели `erasure: none` конфигурация может быть такой:

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
# ...
```

Для конфигурации, расположенной в 3 зонах доступности, необходимо указать 3 кольца. Для конфигураций, расположенных в одной зоне доступности, указывается ровно одно кольцо.
