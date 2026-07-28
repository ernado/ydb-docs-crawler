---
title: "JDBC driver properties"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/jdbc-driver/properties?version=v26.1"
doc_path: "en/reference/languages-and-apis/jdbc-driver/properties"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/jdbc-driver/properties.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/jdbc-driver/properties.md"
description: "The JDBC driver for YDB supports the following configuration properties, which can be specified in the JDBC URL or passed via additional properties:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# JDBC driver properties

The JDBC driver for YDB supports the following configuration properties, which can be specified in the [JDBC URL](properties.md#jdbc-url-examples) or passed via additional properties:

- `saFile` — service account key for authentication. The valid value is either the content of the JSON file or a file reference.

- `iamEndpoint` — custom IAM endpoint for authentication using a service account key.

- `token` — token value for authentication. The valid value is either the token content or a token file reference.

- `useMetadata` — indicates whether to use metadata authentication. Valid values are:

  - `true` — use metadata authentication.
  - `false` — do not use metadata authentication.

  Default value: `false`.

- `metadataURL` — custom metadata endpoint.

- `localDatacenter` — the name of the data center local to the application being connected.

- `secureConnection` — indicates whether to use TLS. Valid values are:

  - `true` — enforce TLS.
  - `false` — do not enforce TLS.

  The primary way to indicate whether a connection is secure or not is by using the `grpcs://` scheme for secure connections and `grpc://` for insecure connections in the JDBC URL. This property allows overriding it.

- `secureConnectionCertificate` — custom CA certificate for TLS connections. The valid value is either the certificate content or a certificate file reference.

> [!NOTE]
> File references for `saFile`, `token`, or `secureConnectionCertificate` must be prefixed with the `file:` URL scheme, for example:
>
> - `saFile=file:~/mysakey1.json`
> - `token=file:/opt/secret/token-file`
> - `secureConnectionCertificate=file:/etc/ssl/cacert.cer`

## Using the QueryService mode

By default, the JDBC driver currently uses a legacy API for running queries to be compatible with a broader range of YDB versions. However, that API has some extra [limitations](../../../concepts/limits-ydb.md#query). To turn off this behavior and use a modern API called "Query Service", add the `useQueryService=true` property to the JDBC URL.

## JDBC URL examples

- Local Docker container with anonymous authentication and without TLS:
  `jdbc:ydb:grpc://localhost:2136/local`

- Remote self-hosted cluster:
  `jdbc:ydb:grpcs://<host>:2135/Root/<testdb>?secureConnectionCertificate=file:~/<myca>.cer`

- A cloud database instance with a token:
  `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?token=file:~/my_token`

- A cloud database instance with a service account:
  `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?saFile=file:~/sa_key.json`
