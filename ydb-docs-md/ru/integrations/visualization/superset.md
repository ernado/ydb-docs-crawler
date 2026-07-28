---
title: "Apache Superset"
url: "https://ydb.tech/docs/ru/integrations/visualization/superset?version=v26.1"
doc_path: "ru/integrations/visualization/superset"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/visualization/superset.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/visualization/superset.md"
description: "Apache Superset — современная платформа для анализа и визуализации данных. В этой статье описано, как создавать визуализации на основе данных, хранящихся в YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Apache Superset

[Apache Superset](https://superset.apache.org/) — современная платформа для анализа и визуализации данных. В этой статье описано, как создавать визуализации на основе данных, хранящихся в YDB.

## Установка необходимых зависимостей {#prerequisites}

Для работы с YDB необходимо установить драйвер [ydb-sqlalchemy](https://pypi.org/project/ydb-sqlalchemy).

Способ установки зависит от способа развёртывания Superset. Дополнительную информацию см. в [официальной документации Superset](https://superset.apache.org/docs/configuration/databases/#installing-drivers-in-docker-images).

## Создание подключения к YDB {#add-database-connection}

### Нативное подключение с помощью SQLAlchemy-драйвера {#nativnoe-podklyuchenie-s-pomoshyu-sqlalchemy-drajvera}

Чтобы создать подключение к YDB из Apache Superset **версии 5.0.0 и выше**, выполните следующие шаги:

1. В верхнем меню Apache Superset наведите курсор на **Settings** и выберите в выпадающем списке пункт **Database Connections**.

2. Нажмите кнопку **+ DATABASE**.

   Откроется окно мастера **Connect a database**.

3. На первом шаге мастера выберите **YDB** из списка **Supported databases**. Если опция **YDB** недоступна, убедитесь, что [установлены все необходимые компоненты](superset.md#prerequisites).

4. На втором шаге мастера введите данные для подключения к YDB в следующие поля:

   - **Display Name** — наименование соединения с YDB в Apache Superset;
   - **SQLAlchemy URI** — строка вида `ydb://{host}:{port}/{database_name}`, где **host** и **port** — соответствующие значения из [эндпоинта](../../concepts/connect.md#endpoint) кластера YDB, **database_name** — путь к [базе данных](../../concepts/glossary.md#database).

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/visualization/_assets/superset-ydb-connection-details.png)

5. Опционально, с помощью поля `Secure Extra` на вкладке `Advanced / Security` можно указать параметры аутентификации.

   Определите параметры следующим образом:

   {% list tabs %}

   - Пароль

     ```json
     {
         "credentials": {
             "username": "...",
             "password": "..."
         }
     }
     ```

   - Токен

     ```json
     {
         "credentials": {
             "token": "...",
         }
     }
     ```

   - Сервисный аккаунт

     ```json
     {
         "credentials": {
             "service_account_json": {
                 "id": "...",
                 "service_account_id": "...",
                 "created_at": "...",
                 "key_algorithm": "...",
                 "public_key": "...",
                 "private_key": "..."
             }
         }
     }
     ```

   {% endlist %}

6. Нажмите кнопку **CONNECT**.

7. Нажмите кнопку **FINISH**, чтобы сохранить подключение.

Для дополнительной информации о возможностях конфигурации соединения обратитесь к [разделу YDB официальной документации](https://superset.apache.org/docs/configuration/databases#ydb).

## Создание набора данных (dataset) {#create-dataset}

Чтобы создать набор данных из таблицы YDB, выполните следующие шаги:

1. В верхнем меню Apache Superset наведите курсор на кнопку **+** и выберите в выпадающем списке пункт **SQL query**.

2. В выпадающем списке **DATABASE** выберите подключение к YDB.

3. Введите текст SQL-запроса в правой части страницы. Например, `SELECT * FROM <наименование_таблицы>`.

   > [!TIP]
   > Если вы хотите создать набор данных из таблицы, которая расположена в поддиректории YDB, необходимо указать путь к таблице в самом наименовании таблицы. Например:
   >
   > ```yql
   > SELECT * FROM "<путь/к/таблице/наименование_таблицы>";
   > ```

4. Нажмите кнопку **RUN**, чтобы проверить SQL-запрос.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/visualization/_assets/superset-sql-query.png)

5. Нажмите на стрелку рядом с кнопкой **SAVE** и выберите **Save dataset** в выпадающем списке.

   Откроется диалоговое окно **Save or Overwrite Dataset**.

6. В открывшемся окне **Save or Overwrite Dataset** выберите **Save as new**, введите наименование набора данных и нажмите **SAVE & EXPLORE**.

После создания наборов данных вы можете использовать данные из YDB для создания диаграмм в Apache Superset. См. документацию [Apache Superset](https://superset.apache.org/docs/intro/).

## Создание диаграммы {#create-chart}

Теперь давайте создадим пример диаграммы с использованием набора данных из таблицы `episodes`, которая описана в [Туториале по YQL](../../dev/yql-tutorial/index.md).

Таблица `episodes` содержит следующие колонки:

- series_id;
- season_id;
- episode_id;
- title;
- air_date.

Предположим, что мы хотим построить круговую диаграмму, в которой бы было видно, сколько серий содержит каждый сезон сериала.

Чтобы создать диаграмму, выполните следующие шаги:

1. В верхнем меню Apache Superset наведите курсор на **+** и выберите в выпадающем списке пункт **Chart**.

2. В выпадающем списке **Choose a dataset**, выберите набор данных из таблицы `episodes`.

3. На панели **Choose chart type**, выберите тип диаграммы `Pie chart`.

4. Нажмите кнопку **CREATE NEW CHART**.

5. На панели **Query** настройте диаграмму:

   - В выпадающем списке **DIMENSIONS** выберите колонку `season_id`.
   - В поле **METRIC** введите функцию `COUNT(title)`.
   - В поле **FILTERS** введите фильтр `series_id in (2)`.

6. Нажмите кнопку **CREATE CHART**.

   Круговая диаграмма появится на панели справа.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/visualization/_assets/superset-sample-chart.png)

7. Нажмите кнопку **SAVE**.

   Откроется диалоговое окно **Save chart**.

8. В открывшемся окне **Save chart** в поле **CHART NAME** введите наименование диаграммы.

9. Нажмите кнопку **SAVE**.
