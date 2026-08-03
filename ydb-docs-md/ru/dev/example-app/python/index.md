---
title: "Приложение на Python"
url: "https://ydb.tech/docs/ru/dev/example-app/python/?version=v26.1"
doc_path: "ru/dev/example-app/python/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/example-app/python/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/example-app/python/index.md"
description: "На этой странице подробно разбирается код тестового приложения, доступного в составе Python SDK YDB. Скачивание и запуск."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Приложение на Python

На этой странице подробно разбирается код [тестового приложения](https://github.com/ydb-platform/ydb-python-sdk/tree/master/examples/basic_example_v2), доступного в составе [Python SDK](https://github.com/ydb-platform/ydb-python-sdk) YDB.

## Скачивание и запуск {#download}

Приведенный ниже сценарий запуска использует [git](https://git-scm.com/downloads) и [Python3](https://www.python.org/downloads/). Предварительно должен быть установлен [YDB Python SDK](../../../reference/ydb-sdk/install.md).

Создайте рабочую директорию и выполните в ней из командной строки команды клонирования репозитория с GitHub и установки необходимых пакетов Python:

```bash
git clone https://github.com/ydb-platform/ydb-python-sdk.git
python3 -m pip install iso8601
```

Далее из этой же рабочей директории выполните команду запуска тестового приложения, которая будет отличаться в зависимости от того, к какой базе данных необходимо подключиться.

{% list tabs %}

- Local Docker

  Для соединения с развернутой локальной базой данных YDB по сценарию [Docker](../../../quickstart.md) в конфигурации по умолчанию выполните следующую команду:

  ```bash
  YDB_ANONYMOUS_CREDENTIALS=1 \
  python3 ydb-python-sdk/examples/basic_example_v1/ -e grpc://localhost:2136 -d /local
  ```

- Любая база данных

  Для выполнения примера с использованием любой доступной базы данных YDB вам потребуется знать [эндпоинт](../../../concepts/connect.md#endpoint) и [путь базы данных](../../../concepts/connect.md#database).

  Если в базе данных включена аутентификация, то вам также понадобится выбрать [режим аутентификации](../../../security/authentication.md) и получить секреты - токен или логин/пароль.

  Выполните команду по следующему образцу:

  ```bash
  <auth_mode_var>="<auth_mode_value>" \
  python3 ydb-python-sdk/examples/basic_example_v1/ -e <endpoint> -d <database>
  ```

  , где

  - `<endpoint>` - [эндпоинт](../../../concepts/connect.md#endpoint).
  - `<database>` - [путь базы данных](../../../concepts/connect.md#database).
  - `<auth_mode_var`> - [переменная окружения](../../../reference/ydb-sdk/auth.md#env), определяющая режим аутентификации.
  - `<auth_mode_value>` - значение параметра аутентификации для выбранного режима.

  Например:

  ```bash
  YDB_ACCESS_TOKEN_CREDENTIALS="t1.9euelZqOnJuJlc..." \
  python3 ydb-python-sdk/examples/basic_example_v1/ -e grpcs://ydb.example.com:2135 -d /path/db )
  ```

{% endlist %}

## Инициализация соединения с базой данных {#init}

Для взаимодействия с YDB создается экземпляр драйвера, клиента и сессии:

- Драйвер YDB отвечает за взаимодействие приложения и YDB на транспортном уровне. Драйвер должен существовать на всем протяжении жизненного цикла работы с YDB и должен быть инициализирован перед созданием клиента и сессии.
- Клиент YDB работает поверх драйвера YDB и отвечает за работу с сущностями и транзакциями.
- Сессия YDB содержит информацию о выполняемых транзакциях и подготовленных запросах и содержится в контексте клиента YDB.

Фрагмент кода приложения для инициализации драйвера:

{% list tabs %}

- Синхронный

  ```python
  def run(endpoint, database):
      driver_config = ydb.DriverConfig(
          endpoint, database, credentials=ydb.credentials_from_env_variables(),
          root_certificates=ydb.load_ydb_root_certificate(),
      )
      with ydb.Driver(driver_config) as driver:
          try:
              driver.wait(timeout=5)
          except TimeoutError:
              print("Connect failed to YDB")
              print("Last reported errors by discovery:")
              print(driver.discovery_debug_details())
              exit(1)
  ```

- Асинхронный

  ```python
  async def run(endpoint, database):
      driver_config = ydb.DriverConfig(
          endpoint, database, credentials=ydb.credentials_from_env_variables(),
          root_certificates=ydb.load_ydb_root_certificate(),
      )
      async with ydb.aio.Driver(driver_config) as driver:
          try:
              await driver.wait(timeout=5)
          except TimeoutError:
              print("Connect failed to YDB")
              print("Last reported errors by discovery:")
              print(driver.discovery_debug_details())
              exit(1)
  ```

{% endlist %}

Фрагмент кода приложения для создания пула сессий:

{% list tabs %}

- Синхронный

  ```python
  with ydb.QuerySessionPool(driver) as pool:
      pass  # operations with pool here
  ```

- Асинхронный

  ```python
  async with ydb.aio.QuerySessionPool(driver) as pool:
      pass  # operations with pool here
  ```

{% endlist %}

## Выполнение запросов {#vypolnenie-zaprosov}

YDB Python SDK поддерживает выполнение запросов с использованием синтаксиса YQL.  
 Существует два основных метода для выполнения запросов, которые имеют различные свойства и области применения:

- `pool.execute_with_retries`:

  - Буферизует весь результат в памяти клиента.
  - Автоматически перезапускает выполнение в случае ошибок, которые можно устранить перезапуском.
  - Не позволяет указать режим выполнения транзакции.
  - Рекомендуется для разовых запросов, которые возвращают небольшой по размеру результат.

- `tx.execute`:

  - Возвращает итератор над результатом запроса, что позволяет обработать результат, который может не поместиться в памяти клиента.
  - Перезапуски в случае ошибок должны обрабатываться вручную с помощью `pool.retry_operation_sync`.
  - Позволяет указать режим выполнения транзакции.
  - Рекомендуется для сценариев, где `pool.execute_with_retries` неэффективен.

## Создание строковых таблиц {#create-table}

Выполняется создание строковых таблиц, которые используются в дальнейших операциях тестового приложения. В результате исполнения шага в базе данных будут созданы строковые таблицы модели данных справочника сериалов:

- `series` - Сериалы
- `seasons` - Сезоны
- `episodes` - Эпизоды

После создания вызывается метод получения информации об объекте схемы данных, и выводится результат его выполнения.

Для выполнения запросов `CREATE TABLE` стоит использовать метод `pool.execute_with_retries()`:

{% list tabs %}

- Синхронный

  ```python
  def create_tables(pool: ydb.QuerySessionPool):
      print("\nCreating table series...")
      pool.execute_with_retries(
          """
          CREATE TABLE `series` (
              `series_id` Int64,
              `title` Utf8,
              `series_info` Utf8,
              `release_date` Date,
              PRIMARY KEY (`series_id`)
          )
          """
      )

      print("\nCreating table seasons...")
      pool.execute_with_retries(
          """
          CREATE TABLE `seasons` (
              `series_id` Int64,
              `season_id` Int64,
              `title` Utf8,
              `first_aired` Date,
              `last_aired` Date,
              PRIMARY KEY (`series_id`, `season_id`)
          )
          """
      )

      print("\nCreating table episodes...")
      pool.execute_with_retries(
          """
          CREATE TABLE `episodes` (
              `series_id` Int64,
              `season_id` Int64,
              `episode_id` Int64,
              `title` Utf8,
              `air_date` Date,
              PRIMARY KEY (`series_id`, `season_id`, `episode_id`)
          )
          """
      )
  ```

- Асинхронный

  ```python
  async def create_tables(pool: ydb.aio.QuerySessionPool):
      print("\nCreating table series...")
      await pool.execute_with_retries(
          """
          CREATE TABLE `series` (
              `series_id` Int64,
              `title` Utf8,
              `series_info` Utf8,
              `release_date` Date,
              PRIMARY KEY (`series_id`)
          )
          """
      )

      print("\nCreating table seasons...")
      await pool.execute_with_retries(
          """
          CREATE TABLE `seasons` (
              `series_id` Int64,
              `season_id` Int64,
              `title` Utf8,
              `first_aired` Date,
              `last_aired` Date,
              PRIMARY KEY (`series_id`, `season_id`)
          )
          """
      )

      print("\nCreating table episodes...")
      await pool.execute_with_retries(
          """
          CREATE TABLE `episodes` (
              `series_id` Int64,
              `season_id` Int64,
              `episode_id` Int64,
              `title` Utf8,
              `air_date` Date,
              PRIMARY KEY (`series_id`, `season_id`, `episode_id`)
          )
          """
      )
  ```

{% endlist %}

## Запись данных {#write-queries}

Выполняется запись данных в созданные строковые таблицы с использованием команды [`UPSERT`](../../../yql/reference/syntax/upsert_into.md) языка запросов [YQL](../../../yql/reference/index.md). Применяется режим передачи запроса на изменение данных с автоматическим подтверждением транзакции в одном запросе к серверу.

Фрагмент кода, демонстрирующий выполнение запроса на запись/изменение данных:

{% list tabs %}

- Синхронный

  ```python
  def upsert_simple(pool: ydb.QuerySessionPool):
      print("\nPerforming UPSERT into episodes...")
      pool.execute_with_retries(
          """
          UPSERT INTO episodes (series_id, season_id, episode_id, title) VALUES (2, 6, 1, "TBD");
          """
      )
  ```

- Асинхронный

  ```python
  async def upsert_simple(pool: ydb.aio.QuerySessionPool):
      print("\nPerforming UPSERT into episodes...")
      await pool.execute_with_retries(
          """
          UPSERT INTO episodes (series_id, season_id, episode_id, title) VALUES (2, 6, 1, "TBD");
          """
      )
  ```

{% endlist %}

## Получение выборки данных {#query-processing}

Выполняется запрос на получение выборки данных с использованием команды [`SELECT`](../../../yql/reference/syntax/select/index.md) языка запросов [YQL](../../../yql/reference/index.md). Демонстрируется обработка полученной выборки в приложении.

Для выполнения YQL-запросов метод часто эффективен метод `pool.execute_with_retries()`.

{% list tabs %}

- Синхронный

  ```python
  def select_simple(pool: ydb.QuerySessionPool):
      print("\nCheck series table...")
      result_sets = pool.execute_with_retries(
          """
          SELECT
              series_id,
              title,
              release_date
          FROM series
          WHERE series_id = 1;
          """,
      )
      first_set = result_sets[0]
      for row in first_set.rows:
          print(
              "series, id: ",
              row.series_id,
              ", title: ",
              row.title,
              ", release date: ",
              row.release_date,
          )
      return first_set
  ```

- Асинхронный

  ```python
  async def select_simple(pool: ydb.aio.QuerySessionPool):
      print("\nCheck series table...")
      result_sets = await pool.execute_with_retries(
          """
          SELECT
              series_id,
              title,
              release_date
          FROM series
          WHERE series_id = 1;
          """,
      )
      first_set = result_sets[0]
      for row in first_set.rows:
          print(
              "series, id: ",
              row.series_id,
              ", title: ",
              row.title,
              ", release date: ",
              row.release_date,
          )
      return first_set
  ```

{% endlist %}

В качестве результата выполнения запроса возвращается список из `result_set`, итерирование по которым выводит на консоль текст:

```bash
> SelectSimple:
series, Id: 1, title: IT Crowd, Release date: 2006-02-03
```

## Параметризованные запросы {#param-queries}

Для выполнения параметризованных запросов методы `pool.execute_with_retries()` и `tx.execute()` работают схожим образом - необходимо передать словарь с параметрами специального вида, где ключом служит имя параметра, а значение может быть одним из следующих:

1. Обычное значение
2. Кортеж со значением и типом
3. Специальный тип `ydb.TypedValue(value=value, value_type=value_type)`

В случае указания значения без типа, конвертация происходит по следующим правилам:

| Python type | YDB type |
| --- | --- |
| `int` | `ydb.PrimitiveType.Int64` |
| `float` | `ydb.PrimitiveType.Double` |
| `str` | `ydb.PrimitiveType.Utf8` |
| `bytes` | `ydb.PrimitiveType.String` |
| `bool` | `ydb.PrimitiveType.Bool` |
| `list` | `ydb.ListType` |
| `dict` | `ydb.DictType` |

> [!WARNING]
> Автоматическая конвертация списков и словарей возможна только в случае однородных структур. Тип вложенного значения будет вычисляться рекурсивно по вышеупомянутым правилам. В случае использования неоднородной структуры запросы будут падать с ошибкой типа `TypeError`.

Фрагмент кода, демонстрирующий возможность использования параметризованных запросов:

{% list tabs %}

- Синхронный

  ```python
  def select_with_parameters(pool: ydb.QuerySessionPool, series_id, season_id, episode_id):
      result_sets = pool.execute_with_retries(
          """
          DECLARE $seriesId AS Int64;
          DECLARE $seasonId AS Int64;
          DECLARE $episodeId AS Int64;

          SELECT
              title,
              air_date
          FROM episodes
          WHERE series_id = $seriesId AND season_id = $seasonId AND episode_id = $episodeId;
          """,
          {
              "$seriesId": series_id,  # data type could be defined implicitly
              "$seasonId": (season_id, ydb.PrimitiveType.Int64),  # could be defined via a tuple
              "$episodeId": ydb.TypedValue(episode_id, ydb.PrimitiveType.Int64),  # could be defined via a special class
          },
      )

      print("\n> select_with_parameters:")
      first_set = result_sets[0]
      for row in first_set.rows:
          print("episode title:", row.title, ", air date:", row.air_date)

      return first_set
  ```

- Асинхронный

  ```python
  async def select_with_parameters(pool: ydb.aio.QuerySessionPool, series_id, season_id, episode_id):
      result_sets = await pool.execute_with_retries(
          """
          DECLARE $seriesId AS Int64;
          DECLARE $seasonId AS Int64;
          DECLARE $episodeId AS Int64;

          SELECT
              title,
              air_date
          FROM episodes
          WHERE series_id = $seriesId AND season_id = $seasonId AND episode_id = $episodeId;
          """,
          {
              "$seriesId": series_id,  # could be defined implicitly
              "$seasonId": (season_id, ydb.PrimitiveType.Int64),  # could be defined via a tuple
              "$episodeId": ydb.TypedValue(episode_id, ydb.PrimitiveType.Int64),  # could be defined via a special class
          },
      )

      print("\n> select_with_parameters:")
      first_set = result_sets[0]
      for row in first_set.rows:
          print("episode title:", row.title, ", air date:", row.air_date)

      return first_set
  ```

{% endlist %}

Фрагмент кода выше при запуске выводит на консоль текст:

```bash
> select_prepared_transaction:
('episode title:', u'To Build a Better Beta', ', air date:', '2016-06-05')
```

## Управление транзакциями {#tcl}

Выполняются вызовы операторов управления транзакциями [TCL](../../../concepts/transactions.md) - Begin и Commit.

В большинстве случаев вместо явного использования вызовов Begin и Commit лучше использовать параметры контроля транзакций в вызовах execute. Это позволит избежать лишних обращений к YDB и эффективней выполнять запросы.

Метод `session.transaction().execute()` так же может быть использован для выполнения YQL запросов. В отличие от `pool.execute_with_retries`, данный метод позволяет в явном виде контролировать выполнение транзакций и настраивать необходимый режим выполнения транзакций с помощью класса `TxControl`.

Доступные режимы транзакции:

- `ydb.QuerySerializableReadWrite()` (по умолчанию);
- `ydb.QueryOnlineReadOnly(allow_inconsistent_reads=False)`;
- `ydb.QuerySnapshotReadOnly()`;
- `ydb.QueryStaleReadOnly()`.

Подробнее про режимы транзакций описано в [Режимы транзакций](../../../concepts/transactions.md#modes).

Результатом выполнения `tx.execute()` является итератор. Итератор позволяет считать неограниченное количество строк и объем данных, не загружая в память весь результат. Однако, для корректного сохранения состояния транзакции на стороне YDB итератор необходимо прочитывать до конца после каждого запроса. Если этого не сделать, пишущие запросы могут не выполниться на стороне YDB. Для удобства результат функции `tx.execute()` представлен в виде контекстного менеджера, который долистывает итератор до конца после выхода.

{% list tabs %}

- Синхронный

  ```python
  with tx.execute(query) as _:
      pass
  ```

- Асинхронный

  ```python
  async with await tx.execute(query) as _:
      pass
  ```

{% endlist %}

Фрагмент кода, демонстрирующий явное использование вызовов `transaction().begin()` и `tx.commit()`:

{% list tabs %}

- Синхронный

  ```python
  def explicit_transaction_control(pool: ydb.QuerySessionPool, series_id, season_id, episode_id):
      def callee(session: ydb.QuerySession):
          query = """
          DECLARE $seriesId AS Int64;
          DECLARE $seasonId AS Int64;
          DECLARE $episodeId AS Int64;

          UPDATE episodes
          SET air_date = CurrentUtcDate()
          WHERE series_id = $seriesId AND season_id = $seasonId AND episode_id = $episodeId;
          """

          # Get newly created transaction id
          tx = session.transaction().begin()

          # Execute data query.
          # Transaction control settings continues active transaction (tx)
          with tx.execute(
              query,
              {
                  "$seriesId": (series_id, ydb.PrimitiveType.Int64),
                  "$seasonId": (season_id, ydb.PrimitiveType.Int64),
                  "$episodeId": (episode_id, ydb.PrimitiveType.Int64),
              },
          ) as _:
              pass

          print("\n> explicit TCL call")

          # Commit active transaction(tx)
          tx.commit()

      return pool.retry_operation_sync(callee)
  ```

- Асинхронный

  ```python
  async def explicit_transaction_control(
      pool: ydb.aio.QuerySessionPool, series_id, season_id, episode_id
  ):
      async def callee(session: ydb.aio.QuerySession):
          query = """
          DECLARE $seriesId AS Int64;
          DECLARE $seasonId AS Int64;
          DECLARE $episodeId AS Int64;

          UPDATE episodes
          SET air_date = CurrentUtcDate()
          WHERE series_id = $seriesId AND season_id = $seasonId AND episode_id = $episodeId;
          """

          # Get newly created transaction id
          tx = await session.transaction().begin()

          # Execute data query.
          # Transaction control settings continues active transaction (tx)
          async with await tx.execute(
              query,
              {
                  "$seriesId": (series_id, ydb.PrimitiveType.Int64),
                  "$seasonId": (season_id, ydb.PrimitiveType.Int64),
                  "$episodeId": (episode_id, ydb.PrimitiveType.Int64),
              },
          ) as _:
              pass

          print("\n> explicit TCL call")

          # Commit active transaction(tx)
          await tx.commit()

      return await pool.retry_operation_async(callee)
  ```

{% endlist %}

Однако стоит помнить, что транзакция может быть открыта неявно при первом запросе. Завершиться же она может автоматически с явным указанием флага `commit_tx=True`.  
 Неявное управление транзакцией предпочтительно, так как требует меньше обращений к серверу. Пример неявного управления будет продемонстрирован в следующем блоке.

## Итерирование по результатам запроса {#iterating}

Если ожидается, что результат `SELECT` запроса будет иметь потенциально большое количество найденных строк, рекомендуется использовать метод `tx.execute` вместо `pool.execute_with_retries` для избежания чрезмерного потребления памяти на стороне клиента.

Пример `SELECT` с неограниченным количеством данных и неявным контролем транзакции:

{% list tabs %}

- Синхронный

  ```python
  def huge_select(pool: ydb.QuerySessionPool):
      def callee(session: ydb.QuerySession):
          query = """SELECT * from episodes;"""

          with session.transaction(ydb.QuerySnapshotReadOnly()).execute(
              query,
              commit_tx=True,
          ) as result_sets:
              print("\n> Huge SELECT call")
              for result_set in result_sets:
                  for row in result_set.rows:
                      print("episode title:", row.title, ", air date:", row.air_date)

      return pool.retry_operation_sync(callee)
  ```

- Асинхронный

  ```python
  async def huge_select(pool: ydb.aio.QuerySessionPool):
      async def callee(session: ydb.aio.QuerySession):
          query = """SELECT * from episodes;"""

          async with await session.transaction(ydb.QuerySnapshotReadOnly()).execute(
              query,
              commit_tx=True,
          ) as result_sets:
              print("\n> Huge SELECT call")
              async for result_set in result_sets:
                  for row in result_set.rows:
                      print("episode title:", row.title, ", air date:", row.air_date)

      return await pool.retry_operation_async(callee)
  ```

{% endlist %}
