---
title: "Сборка JDBC-драйвера для YDB"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/jdbc-driver/building?version=v26.1"
doc_path: "ru/reference/languages-and-apis/jdbc-driver/building"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/jdbc-driver/building.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/jdbc-driver/building.md"
description: "Для запуска всех тестов проекта используется команда mvn test."
revision: "259414a47522df8faa233e3f6fd5c97bc5325d93"
---

# Сборка JDBC-драйвера для YDB

Для запуска всех тестов проекта используется команда `mvn test`.

По умолчанию все тесты выполняются на локальном экземпляре YDB в Docker (при условии, что на хосте установлен Docker или Docker Machine).

Чтобы отключить эти тесты, выполните команду: `mvn test -DYDB_DISABLE_INTEGRATION_TESTS=true`.
