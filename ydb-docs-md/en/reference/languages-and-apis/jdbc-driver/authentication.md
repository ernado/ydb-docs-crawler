---
title: "Authentication modes"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/jdbc-driver/authentication?version=v26.1"
doc_path: "en/reference/languages-and-apis/jdbc-driver/authentication"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/jdbc-driver/authentication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/jdbc-driver/authentication.md"
description: "The JDBC Driver for YDB supports the following authentication modes:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Authentication modes

The JDBC Driver for YDB supports the following [authentication modes](../../ydb-sdk/auth.md):

- **Anonymous** is used when a username and password are not specified and no other authentication properties are configured. No authentication credentials are provided.
- **Static credentials** are used when a username and password are specified.
- **Access token** is used when the [`token`](properties.md#token) property is configured. This authentication method requires a YDB authentication token, which can be obtained by executing the following YDB CLI command: `ydb auth get-token`.
- **Metadata** is used when the [`useMetadata`](properties.md#useMetadata) property is set to `true`. This method extracts the authentication data from the metadata of a virtual machine, serverless container, or serverless function running in a cloud environment.
- **Service Account Key** is used when the [`saFile`](properties.md#saFile) property is configured. This method extracts the service account key from a file and uses it for authentication.
