---
title: "Apache Superset"
url: "https://ydb.tech/docs/en/integrations/visualization/superset?version=v26.1"
doc_path: "en/integrations/visualization/superset"
version: "v26.1"
lang: "en"
source_path: "en/core/integrations/visualization/superset.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/integrations/visualization/superset.md"
description: "Apache Superset is a modern data exploration and visualization platform. This article explains how to create visualizations using data stored in YDB."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Apache Superset

[Apache Superset](https://superset.apache.org/) is a modern data exploration and visualization platform. This article explains how to create visualizations using data stored in YDB.

## Installation of dependencies {#prerequisites}

To connect to YDB from Superset, install the [ydb-sqlalchemy](https://pypi.org/project/ydb-sqlalchemy) driver.

The installation method depends on your Superset setup. For detailed instructions, see the [official documentation](https://superset.apache.org/docs/configuration/databases/#installing-drivers-in-docker-images).

## Adding a database connection to YDB {#add-database-connection}

### Native connection using SQLAlchemy driver

To connect to YDB from Apache Superset **version 5.0.0 and higher**, follow these steps:

1. In the Apache Superset toolbar, hover over **Settings** and select **Database Connections**.

2. Click the **+ DATABASE** button.

   The **Connect a database** wizard will appear.

3. In **Step 1** of the wizard, choose **YDB** from the **Supported databases** list. If the **YDB** option is not available, make sure that all the steps from [prerequisites](superset.md#prerequisites) are completed.

4. In **Step 2** of the wizard, enter the YDB credentials in the corresponding fields:

   - **Display Name**. The YDB connection name in Apache Superset.
   - **SQLAlchemy URI**. A string in the format `ydb://{host}:{port}/{database_name}`, where **host** and **port** are parts of the [endpoint](../../concepts/connect.md#endpoint) of the YDB cluster to which the connection will be made, and **database_name** is the path to the [database](../../concepts/glossary.md#database).

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/visualization/_assets/superset-ydb-connection-details.png)

5. To enhance security, you can specify credentials parameters in the **Secure Extra** field under the **Advanced / Security** tab.

   Define the parameters as follows:

   {% list tabs %}

   - Password

     ```json
     {
         "credentials": {
             "username": "...",
             "password": "..."
         }
     }
     ```

   - Access Token

     ```json
     {
         "credentials": {
             "token": "...",
         }
     }
     ```

   - Service Account

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

6. Click **CONNECT**.

7. To save the database connection, click **FINISH**.

For more information about configuring a YDB connection, refer to the [YDB section in the official documentation](https://superset.apache.org/docs/configuration/databases#ydb).

## Creating a dataset {#create-dataset}

To create a dataset for a YDB table, follow these steps:

1. In the Apache Superset toolbar, hover over the **+** button and select **SQL query**.

2. In the **DATABASE** drop-down list, select the YDB database connection.

3. Enter the SQL query in the right section of the page. For example, `SELECT * FROM <ydb_table_name>`.

   > [!TIP]
   > To create a dataset for a table located in a subdirectory of a YDB database, specify the table path in the table name. For example:
   >
   > ```yql
   > SELECT * FROM "<path/to/subdirectory/table_name>";
   > ```

   1. Click **RUN** to test the SQL query.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/visualization/_assets/superset-sql-query.png)

   2. Click the down arrow next to the **SAVE** button, then click **Save dataset**.

      The **Save or Overwrite Dataset** dialog box appears.

   3. In the **Save or Overwrite Dataset** dialog box, select **Save as new**, enter the dataset name, and click **SAVE & EXPLORE**.

   After creating datasets, you can use data from YDB to create charts in Apache Superset. For more information, refer to the [Apache Superset](https://superset.apache.org/docs/intro/) documentation.

   ## Creating a chart {#create-chart}

   Let's create a sample chart with the dataset from the `episodes` table that is described in the [YQL tutorial](../../dev/yql-tutorial/index.md).

   The table contains the following columns:

   - series_id
   - season_id
   - episode_id
   - title
   - air_date

   Let's say that we want to make a pie chart to show how many episodes each season contains.

   To create a chart, follow these steps:

   1. In the Apache Superset toolbar, hover over the **+** button and select **Chart**.

   2. In the **Choose a dataset** drop-down list, select a dataset for the `episodes` table.

   3. In the **Choose chart type** pane, select `Pie chart`.

   4. Click **CREATE NEW CHART**.

   5. In the **Query** pane, configure the chart:

      - In the **DIMENSIONS** drop-down list, select the `season_id` column.
      - In the **METRIC** field, specify the `COUNT(title)` function.
      - In the **FILTERS** field, specify the `series_id in (2)` filter.

   6. Click **CREATE CHART**.

      The pie chart will appear in the preview pane on the right.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/visualization/_assets/superset-sample-chart.png)

   7. Click **SAVE**.

      The **Save chart** dialog box will appear.

   8. In the **Save chart** dialog box, in the **CHART NAME** field, enter the chart name.

   9. Click **SAVE**.
