---
title: "DataLens"
url: "https://ydb.tech/docs/en/integrations/visualization/datalens?version=v26.1"
doc_path: "en/integrations/visualization/datalens"
version: "v26.1"
lang: "en"
source_path: "en/core/integrations/visualization/datalens.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/integrations/visualization/datalens.md"
description: "DataLens is an open-source business intelligence (BI) and data visualization tool that enables users to analyze and display data from various sources, including"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DataLens

[DataLens](https://datalens.tech) is an open-source business intelligence (BI) and data visualization tool that enables users to analyze and display data from various sources, including YDB. DataLens allows you to describe data models, create charts and other visualizations, build dashboards, and provide collaborative access to analytics.

## Prerequisites

DataLens must be [deployed and configured](https://datalens.tech/docs/en/quickstart.html).

> [!NOTE]
> This article covers the integration of self-managed YDB and DataLens. For documentation on integrating the respective managed services, refer to the [Yandex Cloud documentation](https://yandex.cloud/en/docs/datalens/operations/connection/create-ydb).

## Adding a database connection to YDB {#add-database-connection}

To create a connection to YDB:

1. Go to the [workbook](https://datalens.tech/docs/en/workbooks-collections/index.html) page or create a new one.

2. In the top right corner, click **Create** → **Connection**.

3. Select the **YDB** connection.

4. Choose an authentication type:

   {% list tabs %}

   - Anonymous

     - **Host name**. Specify the hostname for YDB connection.
     - **Port**. Specify the connection port for YDB. The default port is 2135.
     - **Database path**. Specify the name of the database to connect to.

   - Password

     - **Host name**. Specify the hostname for YDB connection.
     - **Port**. Specify the connection port for YDB. The default port is 2135.
     - **Database path**. Specify the name of the database to connect to.
     - **Username**. Enter the username to connect to YDB.
     - **Password**. Enter the user password.

   - OAuth

     - **OAuth token**. Provide the OAuth token to access YDB.
     - **Host name**. Specify the hostname for YDB connection.
     - **Port**. Specify the connection port for YDB. The default port is 2135.
     - **Database path**. Specify the name of the database to connect to.

   {% endlist %}

   - **Cache lifetime in seconds**. Set the cache lifetime or leave the default value. The recommended value is 300 seconds (5 minutes).
   - **SQL query access level**. Allows the use of custom SQL queries to create a dataset.

5. Click **Create connection**.

6. Specify a connection name and click **Create**.

7. Proceed to [creating a dataset](https://datalens.tech/docs/en/dataset/index.html).

## Example

![DataLens YDB connection](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/integrations/visualization/_assets/datalens.jpeg)
