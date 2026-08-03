---
title: "DataLens"
url: "https://ydb.tech/docs/ru/integrations/visualization/datalens?version=v26.1"
doc_path: "ru/integrations/visualization/datalens"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/visualization/datalens.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/visualization/datalens.md"
description: "DataLens — инструмент бизнес-аналитики (BI) и визуализации данных с открытым исходным кодом, который позволяет анализировать и отображать данные из различных ис"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DataLens

[DataLens](https://datalens.tech) — инструмент бизнес-аналитики (BI) и визуализации данных с открытым исходным кодом, который позволяет анализировать и отображать данные из различных источников, включая YDB. DataLens позволяет описывать модели данных, строить графики и визуализации, собирать дашборды и обеспечивать коллективный доступ к аналитике.

## Предварительные требования {#predvaritelnye-trebovaniya}

DataLens должен быть [развёрнут и настроен](https://datalens.tech/docs/ru/quickstart.html).

> [!NOTE]
> В этой статье рассматривается интеграция YDB и DataLens, развёрнутых самостоятельно. Документацию по интеграции соответствующих управляемых сервисов см. в [документации Yandex Cloud](https://yandex.cloud/ru/docs/datalens/operations/connection/create-ydb).

## Добавление подключения к базе данных YDB {#add-database-connection}

Чтобы создать подключение к YDB:

1. Перейдите на страницу [воркбука](https://datalens.tech/docs/ru/workbooks-collections/index.html) или создайте новый.

2. В правом верхнем углу нажмите **Создать** → **Подключение**.

3. Выберите тип подключения **YDB**.

4. Укажите тип аутентификации:

   {% list tabs %}

   - Анонимный

     - **Имя хоста** — хостнейм для подключения к YDB.
     - **Порт** — порт подключения к YDB. По умолчанию — 2135.
     - **Путь к базе данных** — имя базы данных для подключения.

   - Пароль

     - **Имя хоста** — хостнейм для подключения к YDB.
     - **Порт** — порт подключения к YDB. По умолчанию — 2135.
     - **Путь к базе данных** — имя базы данных для подключения.
     - **Имя пользователя** — имя пользователя для подключения к YDB.
     - **Пароль** — пароль пользователя.

   - OAuth

     - **OAuth-токен** — OAuth-токен для доступа к YDB.
     - **Имя хоста** — хостнейм для подключения к YDB.
     - **Порт** — порт подключения к YDB. По умолчанию — 2135.
     - **Путь к базе данных** — имя базы данных для подключения.

   {% endlist %}

   - **Время жизни кэша в секундах** — установите время жизни кэша или оставьте значение по умолчанию. Рекомендуемое значение — 300 секунд (5 минут).
   - **Уровень доступа к SQL-запросам** — позволяет использовать собственные SQL-запросы для создания датасета.

5. Нажмите **Создать подключение**.

6. Укажите имя подключения и нажмите **Создать**.

7. Перейдите к [созданию датасета](https://datalens.tech/docs/ru/dataset/index.html).

## Пример {#primer}

![DataLens YDB connection](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/integrations/visualization/_assets/datalens.jpeg)
