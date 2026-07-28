---
title: "Статусы завершения gRPC"
url: "https://ydb.tech/docs/ru/reference/ydb-sdk/grpc-status-codes?version=v26.1"
doc_path: "ru/reference/ydb-sdk/grpc-status-codes"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-sdk/grpc-status-codes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-sdk/grpc-status-codes.md"
description: "YDB предоставляет gRPC API, с помощью которого вы можете управлять ресурсами и данными БД. В следующей таблице описаны статусы завершения запросов gRPC: Код."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Статусы завершения gRPC

YDB предоставляет gRPC API, с помощью которого вы можете управлять ресурсами и данными БД. В следующей таблице описаны статусы завершения запросов gRPC:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Код | Статус | Возможность повтора | Стратегия задержек | Пересоздать сессию |
| [0](grpc-status-codes.md#ok) | [OK](grpc-status-codes.md#ok) | – | – | – |
| [1](grpc-status-codes.md#cancelled) | [CANCELLED](grpc-status-codes.md#cancelled) | *условно повторяемый* | *короткая* | да |
| [2](grpc-status-codes.md#unknown) | [UNKNOWN](grpc-status-codes.md#unknown) | *неповторяемый* | – | да |
| [3](grpc-status-codes.md#invalid-argument) | [INVALID_ARGUMENT](grpc-status-codes.md#invalid-argument) | *неповторяемый* | – | да |
| [4](grpc-status-codes.md#deadline-exceeded) | [DEADLINE_EXCEEDED](grpc-status-codes.md#deadline-exceeded) | *условно повторяемый* | *короткая* | да |
| [5](grpc-status-codes.md#not-found) | [NOT_FOUND](grpc-status-codes.md#not-found) | *неповторяемый* | – | да |
| [6](grpc-status-codes.md#already-exists) | [ALREADY_EXISTS](grpc-status-codes.md#already-exists) | *неповторяемый* | – | да |
| [7](grpc-status-codes.md#permission-denied) | [PERMISSION_DENIED](grpc-status-codes.md#permission-denied) | *неповторяемый* | – | да |
| [8](grpc-status-codes.md#resource-exhausted) | [RESOURCE_EXHAUSTED](grpc-status-codes.md#resource-exhausted) | *повторяемый* | *большая* | нет |
| [9](grpc-status-codes.md#failed-precondition) | [FAILED_PRECONDITION](grpc-status-codes.md#failed-precondition) | *неповторяемый* | – | да |
| [10](grpc-status-codes.md#aborted) | [ABORTED](grpc-status-codes.md#aborted) | *повторяемый* | *моментально* | да |
| [11](grpc-status-codes.md#out-of-range) | [OUT_OF_RANGE](grpc-status-codes.md#out-of-range) | *неповторяемый* | – | нет |
| [12](grpc-status-codes.md#unimplemented) | [UNIMPLEMENTED](grpc-status-codes.md#unimplemented) | *неповторяемый* | – | да |
| [13](grpc-status-codes.md#internal) | [INTERNAL](grpc-status-codes.md#internal) | *условно повторяемый* | *короткая* | да |
| [14](grpc-status-codes.md#unavailable) | [UNAVAILABLE](grpc-status-codes.md#unavailable) | *условно повторяемый* | *короткая* | да |
| [15](grpc-status-codes.md#data-loss) | [DATA_LOSS](grpc-status-codes.md#data-loss) | *неповторяемый* | – | да |
| [16](grpc-status-codes.md#unauthenticated) | [UNAUTHENTICATED](grpc-status-codes.md#unauthenticated) | *неповторяемый* | – | да |

## 0: OK {#ok}

Не является ошибкой. Возвращается при успешном выполнении.

## 1: CANCELLED {#cancelled}

[Условно повторяемый](error_handling.md) | Короткая задержка

Операция была отменена, как правило, вызывающей стороной.

## 2: UNKNOWN {#unknown}

[Неповторяемый](error_handling.md)

Неизвестная ошибка. Например, эта ошибка может возникнуть, когда значение `Status`, полученное из другого адресного пространства, относится к неизвестному пространству ошибок. Также эта ошибка может быть преобразована из ошибок, вызванных API, которые не предоставляют достаточно информации об ошибке.

## 3: INVALID_ARGUMENT {#invalid-argument}

[Неповторяемый](error_handling.md)

Клиент указал недопустимый аргумент. В отличие от `FAILED_PRECONDITION`, `INVALID_ARGUMENT` указывает на аргументы, которые являются проблемными независимо от состояния системы (например, неправильное имя файла).

## 4: DEADLINE_EXCEEDED {#deadline-exceeded}

[Условно повторяемый](error_handling.md) | Короткая задержка

Запрос не был обработан за заданный клиентский таймаут или произошла иная сетевая проблема.

Проверьте корректность заданного таймаута, наличие сетевого доступа, правильность endpoint'а и других сетевых настроек. Также рекомендуется снизить интенсивность потока запросов и оптимизировать их.

## 5: NOT_FOUND {#not-found}

[Неповторяемый](error_handling.md)

Запрашиваемый схемный объект (например, таблица или папка) не найден.

## 6: ALREADY_EXISTS {#already-exists}

[Неповторяемый](error_handling.md)

Схемный объект, который пытается создать клиент (например, таблица или папка), уже существует.

## 7: PERMISSION_DENIED {#permission-denied}

[Неповторяемый](error_handling.md)

У вызывающего нет разрешения на выполнение указанной операции.

## 8: RESOURCE_EXHAUSTED {#resource-exhausted}

[Повторяемый](error_handling.md) | Большая задержка

Недостаточно свободных ресурсов для обслуживания запроса.

Снизьте интенсивность потока запросов, проверьте клиентскую балансировку.

## 9: FAILED_PRECONDITION {#failed-precondition}

[Неповторяемый](error_handling.md)

Запрос не может быть выполнен в текущем состоянии (например, вставка в таблицу с существующим ключом).

Исправьте состояние или запрос и повторите попытку.

## 10: ABORTED {#aborted}

[Повторяемый](error_handling.md) | Моментально

Операция не выполнена (например, из-за инвалидации локов, `TRANSACTION_LOCKS_INVALIDATE` в подробных сообщениях об ошибке).

Повторите всю транзакцию.

## 11: OUT_OF_RANGE {#out-of-range}

[Неповторяемый](error_handling.md)

Была предпринята попытка выполнить операцию за пределами допустимого диапазона. В отличие от `INVALID_ARGUMENT`, эта ошибка указывает на проблему, которая может быть исправлена при изменении состояния системы.

## 12: UNIMPLEMENTED {#unimplemented}

[Неповторяемый](error_handling.md)

Операция не реализована или не поддерживается (не активирована) в YDB.

## 13: INTERNAL {#internal}

[Условно повторяемый](error_handling.md) | Короткая задержка

Внутренние ошибки. Это означает, что некоторые инварианты, ожидаемые базовой системой, были нарушены. Данный код ошибки предназначен для серьёзных ошибок.

## 14: UNAVAILABLE {#unavailable}

[Условно повторяемый](error_handling.md) | Короткая задержка

Сервис в данный момент недоступен. Скорее всего, это временное состояние, которое можно обойти, повторив запрос после некоторой задержки. Обратите внимание, что повторение неидемпотентных операций не всегда безопасно.

## 15: DATA_LOSS {#data-loss}

[Неповторяемый](error_handling.md)

Неустранимая потеря или повреждение данных.

## 16: UNAUTHENTICATED {#unauthenticated}

[Неповторяемый](error_handling.md)

Запрос не содержит действительных учётных данных для аутентификации.

Повторите запрос с актуальными данными для аутентификации.

***Немедленный повтор** – одна из стратегий задержек, применяемых в SDK при повторе запросов, завершившихся ошибкой.  
  
 Повторные попытки при такой стратегии совершаются немедленно.  
  
 См. подробнее в статье [Обработка временных сбоев (retryable errors)](error_handling.md#handling-retryable-errors).****Короткая экспоненциальная задержка** – одна из стратегий задержек, применяемых в SDK при повторе запросов, завершившихся ошибкой.  
  
 Первоначальный интервал при такой задержке составляет несколько **миллисекунд**. Для каждой последующей попытки интервал увеличивается экспоненциально.  
  
 См. подробнее в статье [Обработка временных сбоев (retryable errors)](error_handling.md#handling-retryable-errors).****Большая экспоненциальная задержка** – одна из стратегий задержек, применяемых в SDK при повторе запросов, завершившихся ошибкой.  
  
 Первоначальный интервал при такой задержке составляет несколько **секунд**. Для каждой последующей попытки интервал увеличивается по экспоненциальному закону.  
  
 См. подробнее в статье [Обработка временных сбоев (retryable errors)](error_handling.md#handling-retryable-errors).****Временные сбои** (retryable). Включают кратковременную потерю сетевого соединения, временную недоступность или перегруженность одной из подсистем YDB, а также неспособность YDB ответить на запрос в течение установленного времени ожидания. В случае возникновения таких ошибок повторный запрос через некоторый промежуток времени с высокой вероятностью будет выполнен успешно.****Ошибки, которые не могут быть исправлены с помощью повтора** (non-retryable). Включают некорректно сформированные запросы, внутренние ошибки YDB, а также запросы, не соответствующие схеме данных. В такой ситуации нет необходимости повторять запрос, требуется дополнительное вмешательство разработчика.****Ошибки, которые, предположительно, могут быть исправлены с помощью повтора после реакции клиентского приложения** (conditionally retryable). Возникают при идемпотентных операциях, таких как отсутствие ответа в течение отведённого времени или запрос аутентификации.*
