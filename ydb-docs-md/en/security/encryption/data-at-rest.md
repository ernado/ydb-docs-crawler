---
title: "Data at rest encryption"
url: "https://ydb.tech/docs/en/security/encryption/data-at-rest?version=v26.1"
doc_path: "en/security/encryption/data-at-rest"
version: "v26.1"
lang: "en"
source_path: "en/core/security/encryption/data-at-rest.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/security/encryption/data-at-rest.md"
description: "YDB supports transparent data encryption at the DS proxy level using the ChaCha8 algorithm. YDB includes two implementations of this algorithm, which switch dep"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Data at rest encryption

YDB supports transparent data encryption at the [DS proxy](../../concepts/glossary.md#ds-proxy) level using the [ChaCha8](https://cr.yp.to/chacha/chacha-20080128.pdf) algorithm. YDB includes two implementations of this algorithm, which switch depending on the availability of the AVX-512F instruction set.

By default, data at rest encryption is disabled. For instructions on enabling it, refer to the [Blob Storage Configuration](../../reference/configuration/domains_config.md#domains-blob) section.

For more details on the implementation, refer to [ydb/core/blobstorage/dsproxy/dsproxy_encrypt.cpp](https://github.com/ydb-platform/ydb/blob/main/ydb/core/blobstorage/dsproxy/dsproxy_encrypt.cpp) and [ydb/core/blobstorage/crypto](https://github.com/ydb-platform/ydb/tree/main/ydb/core/blobstorage/crypto).
