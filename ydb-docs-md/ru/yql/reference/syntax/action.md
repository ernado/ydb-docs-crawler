---
title: "ACTION"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/action?version=v26.1"
doc_path: "ru/yql/reference/syntax/action"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/action.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/action.md"
description: "DEFINE ACTION. Задает именованное действие, которое представляют собой параметризуемый блок из нескольких выражений верхнего уровня. Синтаксис."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ACTION

## DEFINE ACTION

Задает именованное действие, которое представляют собой параметризуемый блок из нескольких выражений верхнего уровня.

### Синтаксис {#sintaksis}

1. `DEFINE ACTION` — объявление действия.
2. [Имя действия](expressions.md#named-nodes), по которому объявляемое действие доступно далее для вызова.
3. В круглых скобках — список имен параметров.
4. Ключевое слово `AS`.
5. Список выражений верхнего уровня.
6. `END DEFINE` — маркер последнего выражения внутри действия.

Один или более последних параметров могут быть помечены знаком вопроса `?` как необязательные. Если они не будут указаны при вызове, то им будет присвоено значение `NULL`.

## DO

Выполняет `ACTION` с указанными параметрами.

### Синтаксис {#sintaksis1}

1. `DO` — выполнение действия.
2. Именованное выражение, по которому объявлено действие.
3. В круглых скобках — список значений для использования в роли параметров.

`EMPTY_ACTION` — действие, которое ничего не выполняет.

### Пример {#primer}

```yql
DEFINE ACTION $hello_world($name, $suffix?) AS
    $name = $name ?? ($suffix ?? "world");
    SELECT "Hello, " || $name || "!";
END DEFINE;

DO EMPTY_ACTION();
DO $hello_world(NULL);
DO $hello_world("John");
DO $hello_world(NULL, "Earth");
```

## BEGIN .. END DO {#begin}

Выполнение действия без его объявления (анонимное действие).

### Синтаксис {#sintaksis2}

1. `BEGIN`;
2. Список выражений верхнего уровня;
3. `END DO`.

Анонимное действие не может содержать параметров.

### Пример {#primer1}

```yql
DO BEGIN
    SELECT 1;
    SELECT 2  -- здесь и в предыдущем примере ';' перед END можно не ставить
END DO
```
