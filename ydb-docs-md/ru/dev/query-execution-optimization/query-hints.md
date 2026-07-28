---
title: "Optimizer Hints (Подсказки Оптимизатора)"
url: "https://ydb.tech/docs/ru/dev/query-execution-optimization/query-hints?version=v26.1"
doc_path: "ru/dev/query-execution-optimization/query-hints"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/query-execution-optimization/query-hints.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/query-execution-optimization/query-hints.md"
description: "Подсказки оптимизатора позволяют влиять на поведение стоимостного оптимизатора при планировании выполнения SQL-запросов. YDB поддерживает четыре типа подсказок"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Optimizer Hints (Подсказки Оптимизатора)

Подсказки оптимизатора позволяют влиять на поведение стоимостного оптимизатора при планировании выполнения SQL-запросов. YDB поддерживает четыре типа подсказок для управления соединениями (joins) и статистикой.

## Использование {#ispolzovanie}

Подсказки задаются через прагму `PRAGMA ydb.OptimizerHints` в начале SQL-запроса.  
 Если оптимизатор не смог применить хотя бы одну из указанных подсказок к запросу, пользователь будет оповещен через warning.

## Синтаксис {#sintaksis}

Подсказки задаются в виде строки, содержащей массив выражений одного из четырех типов:

```text
JoinType(TableList JoinType) 
Rows(TableList Op Value) 
Bytes(TableList Op Value) 
JoinOrder(JoinTree)

где:
TableList - перечисление названий таблиц или элиасов из запроса
Op - операция:
  - `#` - задать абсолютное значение
  - `*` - умножить на значение
  - `/` - разделить на значение
  - `+` - прибавить значение
  - `-` - вычесть значение
  - `Number` - числовое значение
Value - числовое значение
JoinTree - представление бинарного дерева с помощью скобок, например: (R S) (T U) 
```

Например, в следующем запросе используются 3 подсказки кардинальности (кол-во записей) `Rows`, подсказка полного порядка джоинов `JoinOrder` и подсказка выбора алгоритма джоина `JoinType`:

```sql
PRAGMA ydb.OptimizerHints =
'
    Rows(R # 10e8)
    Rows(T # 1)
    Rows(R T # 1)
    JoinOrder( (R S) (T U) )
    JoinType(T U Broadcast)
';

SELECT * FROM
    R   INNER JOIN  S   on  R.id = S.id
        INNER JOIN  T   on  R.id = T.id
        INNER JOIN  U   on  T.id = U.id;
```

## Требования к CBO (Cost Based Optimizer) {#trebovaniya-k-cbo-cost-based-optimizer}

> [!NOTE]
> Все подсказки (`Rows`, `Bytes`, `JoinOrder`) работают только с **включенным** [стоимостным оптимизатором](../../concepts/query_execution/optimizer.md), кроме `JoinType` - его можно указывать и для выключенного CBO.

## Типы подсказок {#tipy-podskazok}

### JoinType - Алгоритм соединения {#jointype-algoritm-soedineniya}

Позволяет принудительно задать алгоритм соединения для определенных таблиц.

В YDB сейчас поддерживаются три типа алгоритмов соединений:

- BroadcastJoin - это тип соединения, при котором один из наборов данных достаточно мал, чтобы его скопировать (разослать) на все необходимые узлы в кластере. Это позволяет каждому узлу выполнять объединение локально, не передавая данные по сети.

> [!NOTE]
> Если порядок соединений не зафиксирован отдельной подсказкой, оптимизатор построит оба варианта планов: где пересылается левый и правый вход соединения. Если порядок соединенй зафиксирован подсказкой, пересылаться будет правая сторона соединения.

- ShuffleJoin - это тип соединения, при котором данные разделяются (shuffle) по ключу соединения так, чтобы записи с одинаковым ключом обработать на одном узле обработки. После такого перераспределения данных каждый узел выполняет локальное соединение таблиц. Результаты объединяются в один общий набор данных.
- LookupJoin - по каждой строке одного входа делается запрос в таблицу или индекс другого входа, в данный момент поддерживается только для [строковых таблиц](../../concepts/datamodel/table.md#row-oriented-table).

> [!NOTE]
> Если порядок соединений не зафиксирован отдельной подсказкой, оптимизатор построит оба варианта планов: где делаются запросы в левый и правый входы соединения. Если порядок соединенй зафиксирован подсказкой, запросы будут делаться в правую сторону соединения.

#### Синтаксис {#sintaksis1}

```text
JoinType(t1 t2 ... tn Broadcast | Shuffle | Lookup)
```

#### Параметры {#parametry}

- `t1 t2 ... tn` - таблицы, участвующие в соединении

- Алгоритм:

  - `Broadcast` - выбрать алгоритм BroadcastJoin
  - `Shuffle` - выбрать алгоритм ShuffleJoin
  - `Lookup` - выбрать алгоритм LookupJoin

#### Принцип работы {#princip-raboty}

Если в плане запроса присутствует оператор соединения, который соединяет только те таблицы, что перечислены в списке, то оптимизатор выберет указанный алгоритм соединения, если он применим (например, нельзя применить алгоритм LookupJoin к [колоночным таблицам](../../concepts/datamodel/table.md#column-oriented-table)). Если алгоритм не может быть применим, пользователь будет оповещен через warning.

#### Примеры {#primery}

```sql
-- Использовать Broadcast для соединения таблиц nation, region
JoinType(nation region Broadcast)

-- Использовать HashJoin для соединения, в поддереве которого будут только таблицы customers, orders, products
JoinType(customers orders products Shuffle)

JoinType(nation region Lookup)
```

Применим подсказки алгоритмов соединений к следующему запросу:

```sql
PRAGMA ydb.OptimizerHints =
'
    JoinType(R S Shuffle)
    JoinType(R S T Broadcast)
    JoinType(R S T U Shuffle)
    JoinType(R S T U V Broadcast)
';

SELECT * FROM
    R   INNER JOIN  S   on  R.id = S.id
        INNER JOIN  T   on  R.id = T.id
        INNER JOIN  U   on  T.id = U.id
        INNER JOIN  V   on  U.id = V.id;
```

Посмореть план выполнения запроса можно с помощью команды [CLI](../../reference/ydb-cli/commands/explain-plan.md):

```bash
 ydb -p <profile_name> sql --explain -f query.sql
```

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ Operation                                                                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ┌> ResultSet                                                                            │
│ └─┬> InnerJoin (MapJoin) (U.id = V.id)                                                  │
│   ├─┬> InnerJoin (Grace) (T.id = U.id)                                                  │
│   │ ├─┬> HashShuffle (KeyColumns: ["T.id"], HashFunc: "HashV2")                         │
│   │ │ └─┬> InnerJoin (MapJoin) (R.id = T.id)                                            │
│   │ │   ├─┬> InnerJoin (Grace) (R.id = S.id)                                            │
│   │ │   │ ├─┬> HashShuffle (KeyColumns: ["id"], HashFunc: "HashV2")                     │
│   │ │   │ │ └──> TableFullScan (Table: R, ReadColumns: ["id (-∞, +∞)","payload1","ts"]) │
│   │ │   │ └─┬> HashShuffle (KeyColumns: ["id"], HashFunc: "HashV2")                     │
│   │ │   │   └──> TableFullScan (Table: S, ReadColumns: ["id (-∞, +∞)","payload2"])      │
│   │ │   └──> TableFullScan (Table: T, ReadColumns: ["id (-∞, +∞)","payload3"])          │
│   │ └─┬> HashShuffle (KeyColumns: ["id"], HashFunc: "HashV2")                           │
│   │   └──> TableFullScan (Table: U, ReadColumns: ["id (-∞, +∞)","payload4"])            │
│   └──> TableFullScan (Table: V, ReadColumns: ["id (-∞, +∞)","payload5"])                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

Так как в процессе оптимизации запроса оптимизатор может изменить порядок соединений, подсказка должна отражать точный список таблиц, которые соединяются.  
 Например, в этом запросе предполагается, что порядок соединений будет: R с S, затем T и в итоге U. Указание другого алгоритма соединения может изменить порядок соединений в плане, и некоторые подсказки не будут применены. В таком случае можно добавить дополнительную подсказку порядка соединений.

### 2. Rows - Подсказки по кардинальности {#2-rows-podskazki-po-kardinalnosti}

Позволяет изменить ожидаемое количество строк (оценку оптимизатора) для соединения или отдельных таблиц.

#### Принцип работы {#princip-raboty1}

Оптимизатор поменяет свою оценку кардинальности (количества строк) для операции соединения, которая соединяет те и только те таблицы, которые перечислены в списке.

#### Синтаксис {#sintaksis2}

```text
Rows(t1 t2 ... tn (*|/|+|-|#) Number)
```

#### Параметры {#parametry1}

- `t1 t2 ... tn` - таблицы

- Операция:

  - `*` - умножить на значение
  - `/` - разделить на значение
  - `+` - прибавить значение
  - `-` - вычесть значение
  - `#` - заменить значение

- `Number` - числовое значение

#### Примеры {#primery1}

```sql
-- Умножить ожидаемое количество строк на 2 для соединения в поддереве которого есть только таблицы users orders yandex
Rows(users orders yandex * 2.0)

-- Заменить кардинальность таблицы products на 1.3e6
Rows(products # 1.3e6)

-- Уменьшить ожидаемое количество строк в 228 раз
Rows(filtered_table / 228)

-- Добавить 5000 строк к ожидаемому результату
Rows(table1 table2 + 5000)
```

Запустим запрос без подсказок кардинальностей, и затем посмотрим как подсказки меняют план запроса.

```sql
SELECT * FROM
    R   INNER JOIN  S   on  R.id = S.id
        INNER JOIN  T   on  R.id = T.id;
```

Без подсказок оптимизатор строит следующий план:

```text
┌────────┬────────┬────────┬───────────────────────────────────────────────────────────────────────────────┐
│ E-Cost │ E-Rows │ E-Size │ Operation                                                                     │
├────────┼────────┼────────┼───────────────────────────────────────────────────────────────────────────────┤
|        │        │        │ ┌> ResultSet                                                                  │
│ 114    │ 10     │ 300    │ └─┬> InnerJoin (MapJoin) (S.id = R.id)                                        │
│ 57     │ 10     │ 200    │   ├─┬> InnerJoin (MapJoin) (S.id = T.id)                                      │
│ 0      │ 10     │ 100    │   │ ├──> TableFullScan (Table: S, ReadColumns: ["id (-∞, +∞)","payload2"])    │
│ 0      │ 10     │ 100    │   │ └──> TableFullScan (Table: T, ReadColumns: ["id (-∞, +∞)","payload3"])    │
│ 0      │ 10     │ 100    │   └──> TableFullScan (Table: R, ReadColumns: ["id (-∞, +∞)","payload1","ts"]) │
└────────┴────────┴────────┴───────────────────────────────────────────────────────────────────────────────┘
```

Если применить следующие подсказки:

```sql
PRAGMA ydb.OptimizerHints =
'
    Rows(R # 10e8)
    Rows(T # 1)
    Rows(S # 10e8)
    Rows(R T # 1)
    Rows(R S # 10e8)
';
SELECT * FROM
    R   INNER JOIN  S   on  R.id = S.id
        INNER JOIN  T   on  R.id = T.id;
```

То получится следующий план:

```text
┌───────────┬────────┬────────┬─────────────────────────────────────────────────────────────────────────────────┐
│ E-Cost    │ E-Rows │ E-Size │ Operation                                                                       │
├───────────┼────────┼────────┼─────────────────────────────────────────────────────────────────────────────────┤
│           │        │        │ ┌> ResultSet                                                                    │
| 3.000e+09 │ 1      │ 100    │ └─┬> InnerJoin (MapJoin) (S.id = R.id)                                          │
│ 0         │ 1e+09  │ 100    │   ├──> TableFullScan (Table: S, ReadColumns: ["id (-∞, +∞)","payload2"])        │
│ 1.500e+09 │ 1      │ 100    │   └─┬> InnerJoin (MapJoin) (R.id = T.id)                                        │
│ 0         │ 1e+09  │ 100    │     ├──> TableFullScan (Table: R, ReadColumns: ["id (-∞, +∞)","payload1","ts"]) │
│ 0         │ 10     │ 100    │     └──> TableFullScan (Table: T, ReadColumns: ["id (-∞, +∞)","payload3"])      │
└───────────┴────────┴────────┴─────────────────────────────────────────────────────────────────────────────────┘
```

Также вернутся оповещения:

```text
Warning: Unapplied hint: Rows(R S # 10e8)
```

Здесь видно, что после применения подсказок кардинальности базовых таблиц, поменялся порядок соединений, и одна из подсказок не смогла примениться, так как такого соединения в плане нет.

### 3. Bytes - Подсказки по размеру данных {#3-bytes-podskazki-po-razmeru-dannyh}

Позволяет изменить ожидаемый размер данных в байтах для соединения или отдельных таблиц.

#### Синтаксис {#sintaksis3}

```text
Bytes(t1 t2 ... tn (*|/|+|-|#) Number)
```

#### Параметры аналогичны Rows, но применяются к размеру данных в байтах {#parametry-analogichny-rows,-no-primenyayutsya-k-razmeru-dannyh-v-bajtah}

#### Примеры {#primery2}

```sql
-- Умножить ожидаемый размер данных на 1.5
Bytes(large_table * 1.5)

-- Заменить размер данных для соединения на 1GB
Bytes(table1 table2 # 1073741824)

-- Уменьшить ожидаемый размер в 2 раза
Bytes(compressed_table / 2)

-- Добавить 100MB к ожидаемому размеру
Bytes(temp_table + 104857600)
```

### 4. JoinOrder - Порядок соединений {#4-joinorder-poryadok-soedinenij}

Позволяет зафиксировать определенное поддерево соединений в общем дереве соединений.

#### Синтаксис {#sintaksis4}

```text
JoinOrder((t1 t2) (t3 (t4 ...)))
```

#### Параметры {#parametry2}

- Вложенная структура скобок определяет порядок соединений
- `(t1 t2)` означает, что t1 и t2 должны быть соединены первыми
- Можно задавать произвольную глубину вложенности

#### Принцип работы {#princip-raboty2}

Оптимизатор будет рассматривать только те планы, в которых присутствует заданный частичный или полный порядок соединений.

#### Примеры {#primery3}

```sql
-- Принудительно соединить сначала users с orders, затем с products
JoinOrder((users orders) products)

-- Более сложный порядок соединений
JoinOrder(((customers orders) products) shipping)

-- Группировка соединений
JoinOrder((table1 table2) (table3 table4))

-- Многоуровневая структура
JoinOrder((users (orders products)) (addresses phones))
```

Применим подсказку порядка соединений к следующему запросу:

```sql
SELECT * FROM
    R   INNER JOIN  S   on  R.id = S.id
        INNER JOIN  T   on  R.id = T.id;
```

План запроса без применения подсказок получается следующий:

```text
┌────────┬────────┬────────┬───────────────────────────────────────────────────────────────────────────────┐
│ E-Cost │ E-Rows │ E-Size │ Operation                                                                     │
├────────┼────────┼────────┼───────────────────────────────────────────────────────────────────────────────┤
│        │        │        │ ┌> ResultSet                                                                  │
│ 114    │ 10     │ 300    │ └─┬> InnerJoin (MapJoin) (S.id = R.id)                                        │
│ 57     │ 10     │ 200    │   ├─┬> InnerJoin (MapJoin) (S.id = T.id)                                      │
│ 0      │ 10     │ 100    │   │ ├──> TableFullScan (Table: S, ReadColumns: ["id (-∞, +∞)","payload2"])    │
│ 0      │ 10     │ 100    │   │ └──> TableFullScan (Table: T, ReadColumns: ["id (-∞, +∞)","payload3"])    │
│ 0      │ 10     │ 100    │   └──> TableFullScan (Table: R, ReadColumns: ["id (-∞, +∞)","payload1","ts"]) │
└────────┴────────┴────────┴───────────────────────────────────────────────────────────────────────────────┘
```

Применив следующую подсказку порядка соединений:

```sql
PRAGMA ydb.OptimizerHints =
'
    JoinOrder(T (R S))
';
SELECT * FROM
    R   INNER JOIN  S   on  R.id = S.id
        INNER JOIN  T   on  R.id = T.id;
```

Получим такой план:

```text
┌────────┬────────┬────────┬─────────────────────────────────────────────────────────────────────────────────┐
│ E-Cost │ E-Rows │ E-Size │ Operation                                                                       │
├────────┼────────┼────────┼─────────────────────────────────────────────────────────────────────────────────┤
│        │        │        │ ┌> ResultSet                                                                    │
│ 114    │ 10     │ 300    │ └─┬> InnerJoin (MapJoin) (T.id = R.id)                                          │
│ 0      │ 10     │ 100    │   ├──> TableFullScan (Table: T, ReadColumns: ["id (-∞, +∞)","payload3"])        │
│ 57     │ 10     │ 200    │   └─┬> InnerJoin (MapJoin) (R.id = S.id)                                        │
│ 0      │ 10     │ 100    │     ├──> TableFullScan (Table: R, ReadColumns: ["id (-∞, +∞)","payload1","ts"]) │
│ 0      │ 10     │ 100    │     └──> TableFullScan (Table: S, ReadColumns: ["id (-∞, +∞)","payload2"])      │
└────────┴────────┴────────┴─────────────────────────────────────────────────────────────────────────────────┘
```

Здесь видно, что изменился порядок соединений на тот, который указан в подсказке.

## Комбинирование подсказок {#kombinirovanie-podskazok}

Можно использовать несколько типов подсказок одновременно в рамках одной прагмы:

```sql
PRAGMA ydb.OptimizerHints =
'
    JoinType(users orders Broadcast)
    Rows(users orders * 0.5)
    JoinOrder((users orders) products)
    Bytes(products # 1073741824)
';
```
