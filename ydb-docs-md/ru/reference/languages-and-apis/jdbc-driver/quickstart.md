---
title: "Быстрый старт"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/jdbc-driver/quickstart?version=v26.1"
doc_path: "ru/reference/languages-and-apis/jdbc-driver/quickstart"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/jdbc-driver/quickstart.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/jdbc-driver/quickstart.md"
description: "Скачайте JDBC-драйвер для YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Быстрый старт

1. Скачайте [JDBC-драйвер для YDB](https://github.com/ydb-platform/ydb-jdbc-driver/releases).

2. Скопируйте JAR-файл в директорию, указанную в переменной окружения `CLASSPATH`, или загрузите JAR-файл в интегрированной среде разработки (IDE).

3. Установите соединение с YDB. Примеры JDBC URL:

   - Локальный Docker контейнер с анонимной аутентификацией и без TLS:
     `jdbc:ydb:grpc://localhost:2136/local`

   - Удаленный кластер, размещенный на собственном сервере:
     `jdbc:ydb:grpcs://<host>:2135/Root/<testdb>?secureConnectionCertificate=file:~/<myca>.cer`

   - Экземпляр облачной базы данных с токеном:
     `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?token=file:~/my_token`

   - Экземпляр облачной базы данных с файлом сервисного аккаунта:
     `jdbc:ydb:grpcs://<host>:2135/<path/to/database>?saFile=file:~/sa_key.json`

4. Выполните проверочный запрос к базе данных YDB. См. пример [YdbDriverExampleTest.java](https://github.com/ydb-platform/ydb-jdbc-driver/blob/master/jdbc/src/test/java/tech/ydb/jdbc/YdbDriverExampleTest.java).
