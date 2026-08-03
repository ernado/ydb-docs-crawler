---
title: "Подключение к YDB с помощью DBeaver"
url: "https://ydb.tech/docs/ru/integrations/gui/dbeaver?version=v26.1"
doc_path: "ru/integrations/gui/dbeaver"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/gui/dbeaver.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/gui/dbeaver.md"
description: "DBeaver — бесплатный кроссплатформенный инструмент управления базами данных с открытым исходным кодом, обеспечивающий визуальный интерфейс для подключения к раз"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Подключение к YDB с помощью DBeaver

[DBeaver](https://dbeaver.com) — бесплатный кроссплатформенный инструмент управления базами данных с открытым исходным кодом, обеспечивающий визуальный интерфейс для подключения к различным базам данных и выполнения SQL-запросов. Он поддерживает множество систем управления базами данных, включая MySQL, PostgreSQL, Oracle и SQLite.

DBeaver позволяет работать с YDB по протоколу Java DataBase Connectivity ([JDBC](https://ru.wikipedia.org/wiki/Java_Database_Connectivity)). Данная статья демонстрирует, как настроить такую интеграцию.

## Подключение JDBC-драйвера YDB к DBeaver {#dbeaver_ydb}

Для подключения к YDB из DBeaver понадобится JDBC-драйвер. Для загрузки JDBC-драйвера выполните следующие шаги:

1. Перейдите в [репозиторий ydb-jdbc-driver](https://github.com/ydb-platform/ydb-jdbc-driver/releases).
2. Выберите последний релиз (отмечен тегом `Latest`) и сохраните файл `ydb-jdbc-driver-shaded-<driver-version>.jar`.

Для подключения загруженного JDBC-драйвера выполните следующие шаги:

1. Выберите в верхнем меню DBeaver пункт **База данных**, а затем подпункт **Управление драйверами**:

   ![управление драйверами](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-driver-management_ru.png)

2. Чтобы создать новый драйвер, в открывшемся окне **Менеджер Драйверов** нажмите кнопку **Новый**:

   ![создание нового драйвера](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-driver-create-new-driver_ru.png)

3. В открывшемся окне **Создать драйвер**, в поле **Имя драйвера**, укажите `YDB`:

   ![выбор имени](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-driver-create-new-driver-set-name_ru.png)

4. Перейдите в раздел **Библиотеки**, нажмите кнопку **Добавить файл**, укажите путь к скачанному ранее JDBC-драйверу YDB (файлу `ydb-jdbc-driver-shaded-<driver-version>.jar`) и нажмите кнопку **OK**:

   ![управление драйверами](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-driver-management-driver_ru.png)

5. В списке драйверов появится пункт **YDB**. Дважды кликните по новому драйверу и перейдите на вкладку **Библиотеки**, нажмите кнопку **Найти Класс** и в выпадающем списке выберите `tech.ydb.jdbc.YdbDriver`.

   > [!WARNING]
   > Обязательно явно выберите пункт выпадающего списка `tech.ydb.jdbc.YdbDriver`, нажав на него. В противном случае DBeaver будет считать, что драйвер не был выбран.

   ![выбор драйвера](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-driver-management-driver_set.png)

## Создание подключения к YDB {#dbeaver_ydb_connection}

Для создания подключения необходимо выполнить следующие шаги:

1. В DBeaver создайте новое соединение, указав тип соединения `YDB`.

2. В открывшемся окне перейдите в раздел **Главное**.

3. В подразделе **Общие**, в поле ввода **JDBC URL**, укажите следующую строку соединения:

   ```text
   jdbc:ydb:<ydb_endpoint>/<ydb_database>?useQueryService=true
   ```

   Где:

   - `ydb_endpoint` — [эндпойнт](../../concepts/connect.md#endpoint) кластера YDB, к которому будут выполняться подключение.
   - `ydb_database` — путь к [базе данных](../../concepts/glossary.md#database) в кластере YDB, к которой будут выполняться запросы.

   ![соединение](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-ydb-connection.png)

4. В поля **Пользователь** и **Пароль** введите логин и пароль для подключения к базе данных. Полный список способов аутентификации и строк подключения к YDB приведён в описании [JDBC-драйвера](https://github.com/ydb-platform/ydb-jdbc-driver).

> [!NOTE]
> В Managed-инсталляциях YDB недоступна аутентификация по логину и паролю.

1. Нажмите кнопку **Тест соединения ...** для проверки настроек.

   Если все настройки указаны верно, то появится сообщение об успешном тестировании соединения:

   ![проверка соединения](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-connection-test.png)

2. Нажмите кнопку **Готово** для сохранения соединения.

## Работа с YDB {#dbeaver_ydb_connection1}

С помощью DBeaver можно просматривать список и структуру таблиц:

![структура таблиц](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-table-structure.png)

А также выполнять запросы к данным:

![выполнение запроса](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/gui/_assets/dbeaver-query.png)
