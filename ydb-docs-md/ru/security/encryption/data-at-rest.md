---
title: "Шифрование данных при хранении"
url: "https://ydb.tech/docs/ru/security/encryption/data-at-rest?version=v26.1"
doc_path: "ru/security/encryption/data-at-rest"
version: "v26.1"
lang: "ru"
source_path: "ru/core/security/encryption/data-at-rest.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/security/encryption/data-at-rest.md"
description: "YDB поддерживает прозрачное шифрование данных на уровне прокси распределённого хранилища с использованием алгоритма ChaCha8. YDB включает две реализации этого а"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Шифрование данных при хранении

YDB поддерживает прозрачное шифрование данных на уровне [прокси распределённого хранилища](../../concepts/glossary.md#ds-proxy) с использованием алгоритма [ChaCha8](https://cr.yp.to/chacha/chacha-20080128.pdf). YDB включает две реализации этого алгоритма, которые переключаются в зависимости от доступности набора инструкций AVX-512F.

По умолчанию шифрование данных при хранении отключено. Инструкции по его включению можно найти в разделе [Конфигурация Blob Storage](../../reference/configuration/domains_config.md#domains-blob).

Более подробную информацию о реализации можно найти в [ydb/core/blobstorage/dsproxy/dsproxy_encrypt.cpp](https://github.com/ydb-platform/ydb/blob/main/ydb/core/blobstorage/dsproxy/dsproxy_encrypt.cpp) и [ydb/core/blobstorage/crypto](https://github.com/ydb-platform/ydb/tree/main/ydb/core/blobstorage/crypto).
