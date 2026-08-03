---
title: "Connecting to YDB with DataGrip"
url: "https://ydb.tech/docs/en/integrations/gui/datagrip?version=v26.1"
doc_path: "en/integrations/gui/datagrip"
version: "v26.1"
lang: "en"
source_path: "en/core/integrations/gui/datagrip.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/integrations/gui/datagrip.md"
description: "DataGrip is a powerful cross-platform tool for relational and NoSQL databases."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Connecting to YDB with DataGrip

[DataGrip](https://www.jetbrains.com/datagrip/) is a powerful cross-platform tool for relational and NoSQL databases.

DataGrip allows you to work with YDB using the Java Database Connectivity ([JDBC](https://en.wikipedia.org/wiki/Java_Database_Connectivity)) protocol. This article demonstrates how to set up this integration.

## Adding the YDB JDBC Driver to DataGrip {#datagrip_ydb}

To connect to YDB from DataGrip, you need the YDB JDBC driver.

To download the YDB JDBC driver, follow these steps:

1. Go to the [ydb-jdbc-driver repository](https://github.com/ydb-platform/ydb-jdbc-driver/releases).
2. Select the latest release (tagged as `Latest`) and save the `ydb-jdbc-driver-shaded-<driver-version>.jar` file.

To add the downloaded JDBC driver to DataGrip, follow these steps:

1. In DataGrip, go to **File | Data Sources…**.

   The **Data Sources and Drivers** dialog box appears.

2. In the **Data Sources and Drivers** dialog box, open the **Drivers** tab and click the **+** button.

3. In the **Name** field, specify `YDB`.

4. In the **Driver Files** section, click the **+** button, choose **Custom JARs…**, specify the path to the previously downloaded YDB JDBC driver (the `ydb-jdbc-driver-shaded-<driver-version>.jar` file), and click **OK**:

5. In the **Class** drop-down list, select `tech.ydb.jdbc.YdbDriver`.

   ![driver](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/datagrip-ydb-driver.png)

6. Click **OK**.

## Creating a Connection to YDB {#datagrip_ydb_connection}

To establish a connection, perform the following steps:

1. In DataGrip, go to **File | Data Sources…**.

   The **Data Sources and Drivers** dialog box appears.

2. In the **Data Sources and Drivers** dialog box, on the **Data Sources** tab, click the **+** button and select `YDB`.

3. In the **Authentication** drop-down list, select an authentication method.

4. If you selected the `User & Password` authentication method, in the **User** and **Password** fields, enter your YDB login and password.

5. On the **General** tab, in the **URL** field, specify the following connection string:

   ```text
   jdbc:ydb:<ydb_endpoint>/<ydb_database>?useQueryService=true
   ```

   Where:

   - `ydb_endpoint` — the [endpoint](../../concepts/connect.md#endpoint) of the YDB cluster.
   - `ydb_database` — the path to the [database](../../concepts/glossary.md#database) in the YDB cluster.

   A complete list of authentication methods and connection strings for YDB is provided in the [JDBC driver](https://github.com/ydb-platform/ydb-jdbc-driver) description.

   ![connection](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/datagrip-ydb-connection.png)

6. Click **Test Connection** to verify the settings.

   If all the settings are correct, a message appears indicating a successful connection test.

7. Click **OK** to save the connection.

## Working with YDB {#datagrip_ydb_connection1}

With DataGrip you can view the list and structure of tables.

![tables](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/datagrip-list-tables.png)

You can also execute queries on the data.

![run SQL](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/datagrip-run-sql.png)
