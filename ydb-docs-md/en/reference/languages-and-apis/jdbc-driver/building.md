---
title: "Building the JDBC driver for YDB"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/jdbc-driver/building?version=v26.1"
doc_path: "en/reference/languages-and-apis/jdbc-driver/building"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/jdbc-driver/building.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/jdbc-driver/building.md"
description: "To execute all tests in the project, run the mvn test command."
revision: "5783baf4a26ccb796054e5b5f3109cb157158102"
---

# Building the JDBC driver for YDB

To execute all tests in the project, run the `mvn test` command.

By default, all tests are run using a local YDB instance in Docker (if the host has Docker or Docker Machine installed).

To disable these tests, run: `mvn test -DYDB_DISABLE_INTEGRATION_TESTS=true`
