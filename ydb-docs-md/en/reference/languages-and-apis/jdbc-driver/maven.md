---
title: "Using the JDBC driver with Maven"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/jdbc-driver/maven?version=v26.1"
doc_path: "en/reference/languages-and-apis/jdbc-driver/maven"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/jdbc-driver/maven.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/jdbc-driver/maven.md"
description: "The recommended way to use the YDB JDBC driver in a project is to include it as a Maven dependency. Specify the YDB JDBC driver in the dependencies section of p"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Using the JDBC driver with Maven

The recommended way to use the YDB JDBC driver in a project is to include it as a Maven dependency. Specify the YDB JDBC driver in the `dependencies` section of `pom.xml`:

```xml
<dependencies>
    <dependency>
        <groupId>tech.ydb.jdbc</groupId>
        <artifactId>ydb-jdbc-driver</artifactId>
        <version><!-- actual version --></version>
    </dependency>
</dependencies>
```
