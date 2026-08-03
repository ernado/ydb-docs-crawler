---
title: "Quick start with JDBC driver"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/jdbc-driver/quickstart?version=v26.1"
doc_path: "en/reference/languages-and-apis/jdbc-driver/quickstart"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/jdbc-driver/quickstart.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/jdbc-driver/quickstart.md"
description: "Download the JDBC driver for YDB. Copy the.jar file to the directory specified in the CLASSPATH environment variable or load the.jar file in your IDE."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Quick start with JDBC driver

1. Download the [JDBC driver for YDB](https://github.com/ydb-platform/ydb-jdbc-driver/releases).

2. Copy the `.jar` file to the directory specified in the `CLASSPATH` environment variable or load the `.jar` file in your IDE.

3. Connect to YDB. JDBC URL examples:

   - Local Docker container with anonymous authentication and without TLS:
     `jdbc:ydb:grpc://localhost:2136/local`

   - Remote self-hosted cluster:
     `jdbc:ydb:grpcs://<host>:2135/Root/<testdb>?secureConnectionCertificate=file:~/<myca>.cer`

   - A cloud database instance with a token:
     `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?token=file:~/my_token`

   - A cloud database instance with a service account:
     `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?saFile=file:~/sa_key.json`

4. Execute queries, for example, [YdbDriverExampleTest.java](https://github.com/ydb-platform/ydb-jdbc-driver/blob/master/jdbc/src/test/java/tech/ydb/jdbc/YdbDriverExampleTest.java).
