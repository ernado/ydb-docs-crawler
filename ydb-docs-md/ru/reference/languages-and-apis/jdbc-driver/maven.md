---
title: "Использование JDBC-драйвера с Maven"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/jdbc-driver/maven?version=v26.1"
doc_path: "ru/reference/languages-and-apis/jdbc-driver/maven"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/jdbc-driver/maven.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/jdbc-driver/maven.md"
description: "Рекомендованный способ использования JDBC-драйвера для YDB в проекте — это добавить драйвер как зависимость в Maven. Укажите JDBC-драйвер для YDB в секции depen"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Использование JDBC-драйвера с Maven

Рекомендованный способ использования JDBC-драйвера для YDB в проекте — это добавить драйвер как зависимость в Maven. Укажите JDBC-драйвер для YDB в секции `dependencies` файла `pom.xml`:

```xml
<dependencies>
    <dependency>
        <groupId>tech.ydb.jdbc</groupId>
        <artifactId>ydb-jdbc-driver</artifactId>
        <version><!-- актуальная версия --></version>
    </dependency>
</dependencies>
```
