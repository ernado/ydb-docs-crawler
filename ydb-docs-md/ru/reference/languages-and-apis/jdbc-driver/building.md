---
title: "Сборка JDBC-драйвера для YDB"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/jdbc-driver/building?version=v26.1"
doc_path: "ru/reference/languages-and-apis/jdbc-driver/building"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/jdbc-driver/building.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/jdbc-driver/building.md"
description: "Для запуска всех тестов проекта используется команда mvn test."
revision: "6cf79b202d43efced4776d730126c3952ec44c6d"
---

# Сборка JDBC-драйвера для YDB

Для запуска всех тестов проекта используется команда `mvn test`.

По умолчанию все тесты выполняются на локальном экземпляре YDB в Docker (при условии, что на хосте установлен Docker или Docker Machine).

Чтобы отключить эти тесты, выполните команду: `mvn test -DYDB_DISABLE_INTEGRATION_TESTS=true`.
