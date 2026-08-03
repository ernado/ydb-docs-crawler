---
title: "Приложение на JavaScript"
url: "https://ydb.tech/docs/ru/dev/example-app/example-js?version=v26.1"
doc_path: "ru/dev/example-app/example-js"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/example-app/example-js.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/example-app/example-js.md"
description: "Приложение на JavaScript. На этой странице представлено подробное описание кода тестового приложения, использующего YDB JavaScript SDK."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Приложение на JavaScript

На этой странице представлено подробное описание кода тестового приложения, использующего [YDB JavaScript SDK](https://github.com/ydb-platform/ydb-js-sdk).

Примеры использования SDK доступны в репозитории [ydb-js-sdk](https://github.com/ydb-platform/ydb-js-sdk/tree/main/examples), а дополнительные примеры реальных сценариев использования — в репозитории [ydb-js-examples](https://github.com/ydb-platform/ydb-js-examples).

## Инициализация соединения с базой данных {#init}

Для взаимодействия с YDB создается экземпляр драйвера, клиента и сессии:

- Драйвер YDB отвечает за взаимодействие приложения и YDB на транспортном уровне. Драйвер должен существовать на всем протяжении жизненного цикла работы с YDB и должен быть инициализирован перед созданием клиента и сессии.
- Клиент YDB работает поверх драйвера YDB и отвечает за работу с сущностями и транзакциями.
- Сессия YDB содержит информацию о выполняемых транзакциях и подготовленных запросах и содержится в контексте клиента YDB.

Для работы с YDB необходимо создать экземпляр драйвера и клиента для выполнения запросов.

Установка необходимых пакетов:

```bash
npm install @ydbjs/core @ydbjs/query
```

Фрагмент кода приложения для инициализации драйвера:

{% list tabs %}

- Используя connectionString

  ```ts
  import { Driver } from '@ydbjs/core'
  import { query } from '@ydbjs/query'

  const connectionString = 'grpc://localhost:2136/local'
  const driver = new Driver(connectionString)
  await driver.ready()

  const sql = query(driver)
  ```

- Используя аутентификацию

  ```ts
  import { Driver } from '@ydbjs/core'
  import { query } from '@ydbjs/query'
  import { AnonymousCredentialsProvider } from '@ydbjs/auth'

  const connectionString = 'grpc://localhost:2136/local'
  const driver = new Driver(connectionString, {
    credentialsProvider: new AnonymousCredentialsProvider(),
  })
  await driver.ready()

  const sql = query(driver)
  ```

{% endlist %}

## Создание строковых таблиц {#create-table}

Выполняется создание строковых таблиц, которые используются в дальнейших операциях тестового приложения. В результате исполнения шага в базе данных будут созданы строковые таблицы модели данных справочника сериалов:

- `series` - Сериалы
- `seasons` - Сезоны
- `episodes` - Эпизоды

После создания вызывается метод получения информации об объекте схемы данных, и выводится результат его выполнения.

```ts
await sql`
    CREATE TABLE series (
        series_id Uint64,
        title Text,
        series_info Text,
        release_date Date,
        PRIMARY KEY (series_id)
    )
`

await sql`
    CREATE TABLE seasons (
        series_id Uint64,
        season_id Uint64,
        title Text,
        first_aired Date,
        last_aired Date,
        PRIMARY KEY (series_id, season_id)
    )
`

await sql`
    CREATE TABLE episodes (
        series_id Uint64,
        season_id Uint64,
        episode_id Uint64,
        title Text,
        air_date Date,
        PRIMARY KEY (series_id, season_id, episode_id)
    )
`
```

## Запись данных {#write-queries}

Выполняется запись данных в созданные строковые таблицы с использованием команды [`UPSERT`](../../yql/reference/syntax/upsert_into.md) языка запросов [YQL](../../yql/reference/index.md). Применяется режим передачи запроса на изменение данных с автоматическим подтверждением транзакции в одном запросе к серверу.

Фрагмент кода, демонстрирующий выполнение запроса на запись/изменение данных:

```ts
await sql`
    UPSERT INTO episodes (series_id, season_id, episode_id, title)
    VALUES (2, 6, 1, "TBD")
`
```

Для вставки данных с использованием параметров:

```ts
import { Uint64, Text, Date as YdbDate } from '@ydbjs/value/primitive'

const data = [
  {
    series_id: new Uint64(1n),
    title: new Text('IT Crowd'),
    series_info: new Text('British sitcom'),
    release_date: new YdbDate(new Date('2006-02-03')),
  },
]

await sql`INSERT INTO series SELECT * FROM AS_TABLE(${data})`
```

## Получение выборки данных {#query-processing}

Выполняется запрос на получение выборки данных с использованием команды [`SELECT`](../../yql/reference/syntax/select/index.md) языка запросов [YQL](../../yql/reference/index.md). Демонстрируется обработка полученной выборки в приложении.

Для выполнения YQL-запросов используется tagged template синтаксис. Результатом выполнения является массив наборов данных (YDB поддерживает несколько наборов результатов в одном запросе).

```ts
const resultSets = await sql`
    SELECT series_id, title, release_date
    FROM series
    WHERE series_id = 1
`

// resultSets[0] содержит первый набор результатов
const [firstResultSet] = resultSets
console.log(firstResultSet)
// [ { series_id: 1n, title: 'IT Crowd', release_date: 2006-02-03T00:00:00.000Z } ]
```

Для запросов с несколькими наборами результатов:

```ts
type Result = [[{ id: bigint }], [{ count: bigint }]]
const [rows, [{ count }]] = await sql<Result>`
    SELECT series_id as id FROM series;
    SELECT COUNT(*) as count FROM series;
`
```

## Параметризованные запросы {#param-queries}

Выполняется запрос к данным с использованием параметров. Этот вариант выполнения запросов является предпочтительным, так как позволяет серверу переиспользовать план исполнения запроса при последующих его вызовах, а также спасает от уязвимостей вида [SQL Injection](https://ru.wikipedia.org/wiki/%D0%92%D0%BD%D0%B5%D0%B4%D1%80%D0%B5%D0%BD%D0%B8%D0%B5_SQL-%D0%BA%D0%BE%D0%B4%D0%B0).

SDK автоматически привязывает параметры через интерполяцию в шаблонных строках. Поддерживаются нативные типы JavaScript, классы значений YDB, массивы и объекты.

```ts
const seriesId = 1n
const title = 'IT Crowd'

const resultSets = await sql`
    SELECT series_id, title, release_date
    FROM series
    WHERE series_id = ${seriesId} AND title = ${title}
`
```

Для именованных параметров и пользовательских типов:

```ts
import { Uint64 } from '@ydbjs/value/primitive'

const id = new Uint64(1n)
const resultSets = await sql`SELECT * FROM series WHERE series_id = $id`.parameter('id', id)
```

Запросы выполняются с потоковой передачей данных по умолчанию. Для работы с большими объёмами данных используйте стандартные запросы:

```ts
const resultSets = await sql`
    SELECT series_id, season_id, title, first_aired
    FROM seasons
    WHERE series_id IN (1, 2)
    ORDER BY season_id
`

for (const row of resultSets[0]) {
  console.log(`Season ${row.season_id}: ${row.title}`)
}
```

## Управление транзакциями {#tcl}

Выполняются вызовы операторов управления транзакциями [TCL](../../concepts/transactions.md) - Begin и Commit.

В большинстве случаев вместо явного использования вызовов Begin и Commit лучше использовать параметры контроля транзакций в вызовах execute. Это позволит избежать лишних обращений к YDB и эффективней выполнять запросы.

Для выполнения запросов в рамках транзакции используются методы `sql.begin()` или `sql.transaction()`:

{% list tabs %}

- begin() — serializable read-write

  ```ts
  const result = await sql.begin(async (tx) => {
    await tx`
        UPDATE episodes
        SET air_date = CurrentUtcDate()
        WHERE series_id = 2 AND season_id = 6 AND episode_id = 1
    `
    return await tx`SELECT * FROM episodes WHERE series_id = 2`
  })
  ```

- begin() с настройками изоляции

  ```ts
  await sql.begin({ isolation: 'snapshotReadOnly', idempotent: true }, async (tx) => {
    return await tx`SELECT COUNT(*) FROM series`
  })
  ```

{% endlist %}

## Обработка ошибок {#error-handling}

Подробно об обработке ошибок написано в разделе [Обработка ошибок в API](../../reference/ydb-sdk/error_handling.md).

Для обработки ошибок используется класс `YDBError`:

```ts
import { YDBError } from '@ydbjs/error'

try {
  await sql`SELECT * FROM non_existent_table`
} catch (error) {
  if (error instanceof YDBError) {
    console.error('YDB Error:', error.message)
  }
}
```

## Дополнительные возможности {#dopolnitelnye-vozmozhnosti}

### Настройки запроса {#nastrojki-zaprosa}

```ts
import { StatsMode } from '@ydbjs/api/query'

await sql`SELECT * FROM series`
  .isolation('onlineReadOnly', { allowInconsistentReads: true })
  .idempotent(true)
  .timeout(5000)
  .withStats(StatsMode.FULL)
```

### Динамические идентификаторы {#dinamicheskie-identifikatory}

Для динамических имён таблиц и колонок используйте метод `identifier`:

```ts
const tableName = 'series'
await sql`SELECT * FROM ${sql.identifier(tableName)}`
```

### Закрытие драйвера {#zakrytie-drajvera}

Всегда закрывайте драйвер по завершении работы:

```ts
driver.close()
```
