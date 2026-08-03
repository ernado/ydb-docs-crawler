---
title: "Secrets"
url: "https://ydb.tech/docs/en/concepts/datamodel/secrets?version=v26.1"
doc_path: "en/concepts/datamodel/secrets"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/datamodel/secrets.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/datamodel/secrets.md"
description: "Various access credentials are used for authentication in external systems. These credentials are stored in separate objects called secrets. Secrets are only av"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Secrets

Various access credentials are used for authentication in external systems. These credentials are stored in separate objects called secrets. Secrets are only available for writing and updating; their values cannot be retrieved.  
 In YDB, secrets are used, for example, in [federated queries](../query_execution/federated_query/index.md) and [data transfers](../transfer.md).

## Syntax

The following YQL operators are used to manage secrets:

- [CREATE SECRET](../../yql/reference/syntax/create-secret.md) — create a secret.
- [ALTER SECRET](../../yql/reference/syntax/alter-secret.md) — modify an existing secret.
- [DROP SECRET](../../yql/reference/syntax/drop-secret.md) — delete a secret.

## Usage {#secret-usage}

Examples of using secrets and working with them are provided in the following sections:

- [Configuring Time to Live (TTL)](../../yql/reference/recipes/ttl.md)
- [Import and export of data to column tables](../../recipes/import-export-column-tables.md)

## Access management {#secret_access}

Secrets are schema objects, so rights to them are granted using the [GRANT](../../yql/reference/syntax/grant.md) command and revoked using the [REVOKE](../../yql/reference/syntax/revoke.md) command. To use a secret in a query, for example, when creating an [external data source](../../yql/reference/syntax/create-external-data-source.md) or [data transfer](../../yql/reference/syntax/create-transfer.md), the [right](../../yql/reference/syntax/grant.md#permissions-list) `SELECT ROW` is required.
