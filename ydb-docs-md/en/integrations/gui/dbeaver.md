---
title: "Connecting to YDB with DBeaver"
url: "https://ydb.tech/docs/en/integrations/gui/dbeaver?version=v26.1"
doc_path: "en/integrations/gui/dbeaver"
version: "v26.1"
lang: "en"
source_path: "en/core/integrations/gui/dbeaver.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/integrations/gui/dbeaver.md"
description: "DBeaver is a free, cross-platform, open-source database management tool that provides a visual interface for connecting to various databases and executing SQL q"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Connecting to YDB with DBeaver

[DBeaver](https://dbeaver.com) is a free, cross-platform, open-source database management tool that provides a visual interface for connecting to various databases and executing SQL queries. It supports many database management systems, including MySQL, PostgreSQL, Oracle, and SQLite.

DBeaver allows you to work with YDB using the Java DataBase Connectivity ([JDBC](https://en.wikipedia.org/wiki/Java_Database_Connectivity)) protocol. This article demonstrates how to set up this integration.

## Connecting the YDB JDBC Driver to DBeaver {#dbeaver_ydb}

To connect to YDB from DBeaver, you will need the JDBC driver. Follow these steps to download the JDBC driver:

1. Go to the [ydb-jdbc-driver repository](https://github.com/ydb-platform/ydb-jdbc-driver/releases).
2. Select the latest release (tagged as `Latest`) and save the `ydb-jdbc-driver-shaded-<driver-version>.jar` file.

Follow these steps to connect the downloaded JDBC driver:

1. In the top menu of DBeaver, select the **Database** option, then select **Driver Manager**:

   ![driver management](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-driver-management.png)

2. To create a new driver, click the **New** button in the **Driver Manager** window that opens

   ![create new driver](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-driver-create-new-driver.png)

3. In the **Create Driver** window that opens, specify `YDB` in the **Driver Name** field:

   ![set name](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-driver-create-new-driver-set-name.png)

4. Go to the **Libraries** section, click **Add File**, specify the path to the previously downloaded YDB JDBC driver (the `ydb-jdbc-driver-shaded-<driver-version>.jar` file), and click **OK**:

   ![driver management](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-driver-management-driver.png)

5. The **YDB** item will appear in the list of drivers. Double-click the new driver and go to the **Libraries** tab, click **Find Class**, and select `tech.ydb.jdbc.YdbDriver` from the dropdown list.

   > [!WARNING]
   > Be sure to explicitly select the `tech.ydb.jdbc.YdbDriver` item from the dropdown list by clicking on it. Otherwise, DBeaver will consider that the driver has not been selected.

   ![driver management set](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-driver-management-driver_set.png)

## Creating a Connection to YDB {#dbeaver_ydb_connection}

Perform the following steps to establish a connection:

1. In DBeaver, create a new connection, specifying the `YDB` connection type.

2. In the window that opens, go to the **Main** section.

3. In the **General** subsection, in the **JDBC URL** input field, specify the following connection string:

   ```text
   jdbc:ydb:<ydb_endpoint>/<ydb_database>?useQueryService=true
   ```

   Where:

   - `ydb_endpoint` — the [endpoint](../../concepts/connect.md#endpoint) of the YDB cluster to which the connection will be made.
   - `ydb_database` — the path to the [database](../../concepts/glossary.md#database) in the YDB cluster to which queries will be made.

   ![connection](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-ydb-connection.png)

4. In the **User** and **Password** fields, enter the login and password for connecting to the database. A complete list of authentication methods and connection strings for YDB is provided in the [JDBC driver](https://github.com/ydb-platform/ydb-jdbc-driver) description.

> [!NOTE]
> In Managed installations of YDB login and password authentication is not available.

1. Click **Test Connection...** to verify the settings.

   If all settings are correct, a message indicating successful connection testing will appear:

   ![connection test](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-connection-test.png)

2. Click **Finish** to save the connection.

## Working with YDB {#dbeaver_ydb_connection1}

With DBeaver, you can view the list and structure of tables:

![structure](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-table-structure.png)

As well as execute queries on the data:

![query](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/gui/_assets/dbeaver-query.png)
