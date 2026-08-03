---
title: "Authentication"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/auth?version=v26.1"
doc_path: "en/recipes/ydb-sdk/auth"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/auth.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/auth.md"
description: "YDB supports multiple authentication methods when connecting to the server side. Each of them is usually specific to a particular pair of environments, that is,"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Authentication

YDB supports multiple authentication methods when connecting to the server side. Each of them is usually specific to a particular pair of environments, that is, depends on where you run your client application (in the trusted YDB zone or outside it) and the YDB server part (in a Docker container, Yandex.Cloud, data cloud, or an independent cluster).

This section contains code recipes with authentication settings in different YDB SDKs. For a general description of the SDK authentication principles, see the [Authentication in an SDK](auth.md).

Table of contents:

- [Using a token](auth-access-token.md)
- [Anonymous](auth-anonymous.md)
- [Service account file](auth-service-account.md)
- [Metadata service](auth-metadata.md)
- [Using environment variables](auth-env.md)
- [Username and password based](auth-static.md)
