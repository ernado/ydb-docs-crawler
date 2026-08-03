---
title: "Подключение к YDB с помощью DataGrip"
url: "https://ydb.tech/docs/ru/integrations/gui/datagrip?version=v26.1"
doc_path: "ru/integrations/gui/datagrip"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/gui/datagrip.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/gui/datagrip.md"
description: "DataGrip — это эффективный кросс-платформенный инструмент для работы с реляционными базами данных и NoSQL."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Подключение к YDB с помощью DataGrip

[DataGrip](https://www.jetbrains.com/datagrip/) — это эффективный кросс-платформенный инструмент для работы с реляционными базами данных и NoSQL.

DataGrip позволяет работать с YDB по протоколу Java Database Connectivity ([JDBC](https://ru.wikipedia.org/wiki/Java_Database_Connectivity)). Данная статья демонстрирует, как настроить такую интеграцию.

## Подключение JDBC-драйвера YDB к DataGrip {#datagrip_ydb}

Для подключения к YDB из DataGrip понадобится JDBC-драйвер. Для загрузки JDBC-драйвера выполните следующие шаги:

1. Перейдите в [репозиторий ydb-jdbc-driver](https://github.com/ydb-platform/ydb-jdbc-driver/releases).
2. Выберите последний релиз (отмечен тегом `Latest`) и сохраните файл `ydb-jdbc-driver-shaded-<driver-version>.jar`.

Для подключения загруженного JDBC-драйвера выполните следующие шаги:

1. Выберите в верхнем меню DataGrip пункт **File**, а затем подпункт **Data Sources…**.

   Откроется диалоговое окно **Data Sources and Drivers**.

2. Чтобы создать новый драйвер, в открывшемся окне **Data Sources and Drivers** перейдите на вкладку **Drivers** и нажмите кнопку **+**.

3. В поле **Name**, укажите `YDB`.

4. В разделе **Driver Files**, нажмите кнопку **+**, в выпадающем списке выберите **Custom JARs…**, укажите путь к скачанному ранее JDBC-драйверу YDB (файлу `ydb-jdbc-driver-shaded-<driver-version>.jar`) и нажмите кнопку **OK**.

5. В выпадающем списке **Class** выберите `tech.ydb.jdbc.YdbDriver`.

   ![драйвер](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/datagrip-ydb-driver.png)

6. Нажмите кнопку **OK**.

## Создание подключения к YDB {#datagrip_ydb_connection}

Для создания подключения необходимо выполнить следующие шаги:

1. Выберите в верхнем меню DataGrip пункт **File**, а затем подпункт **Data Sources…**.

   Откроется диалоговое окно **Data Sources and Drivers**.

2. Чтобы создать новое соединение, в открывшемся окне **Data Sources and Drivers** на вкладке **Data Sources** нажмите кнопку **+** и укажите тип соединения `YDB`.

3. В выпадающем списке **Authentication** укажите тип аутентификации.

4. Если вы выбрали `User & Password` в качестве метода аутентификации, в поля **User** и **Password** введите логин и пароль для подключения к базе данных YDB.

5. В поле **URL**, укажите следующую строку соединения:

   ```text
   jdbc:ydb:<ydb_endpoint>/<ydb_database>?useQueryService=true
   ```

   Где:

   - `ydb_endpoint` — [эндпойнт](../../concepts/connect.md#endpoint) кластера YDB, к которому будут выполняться подключение.
   - `ydb_database` — путь к [базе данных](../../concepts/glossary.md#database) в кластере YDB, к которой будут выполняться запросы.

6. Нажмите кнопку **Test Connection** для проверки настроек.

   Если все настройки указаны верно, то появится сообщение об успешном тестировании соединения.

   ![соединение](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/datagrip-ydb-connection.png)

7. Нажмите кнопку **OK** для сохранения соединения.

## Работа с YDB {#dbeaver_ydb_connection}

С помощью DataGrip можно просматривать список и структуру таблиц:

![список таблиц](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/datagrip-list-tables.png)

А также выполнять запросы к данным:

![выполнение SQL](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/datagrip-run-sql.png)
