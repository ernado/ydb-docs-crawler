---
title: "Статусы завершения сервера YDB"
url: "https://ydb.tech/docs/ru/reference/ydb-sdk/ydb-status-codes?version=v26.1"
doc_path: "ru/reference/ydb-sdk/ydb-status-codes"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-sdk/ydb-status-codes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-sdk/ydb-status-codes.md"
description: "Код. Статус. Возможность повтора. Стратегия задержек. Пересоздать сессию. 400000. SUCCESS. –. –. –. 400010. BAD_REQUEST. неповторяемый. –. нет. 400020."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Статусы завершения сервера YDB

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Код | Статус | Возможность повтора | Стратегия задержек | Пересоздать сессию |
| [400000](ydb-status-codes.md#success) | [SUCCESS](ydb-status-codes.md#success) | – | – | – |
| [400010](ydb-status-codes.md#bad-request) | [BAD_REQUEST](ydb-status-codes.md#bad-request) | *неповторяемый* | – | нет |
| [400020](ydb-status-codes.md#unauthorized) | [UNAUTHORIZED](ydb-status-codes.md#unauthorized) | *неповторяемый* | – | нет |
| [400030](ydb-status-codes.md#internal-error) | [INTERNAL_ERROR](ydb-status-codes.md#internal-error) | *неповторяемый* | – | нет |
| [400040](ydb-status-codes.md#aborted) | [ABORTED](ydb-status-codes.md#aborted) | *повторяемый* | *короткая* | нет |
| [400050](ydb-status-codes.md#unavailable) | [UNAVAILABLE](ydb-status-codes.md#unavailable) | *повторяемый* | *короткая* | нет |
| [400060](ydb-status-codes.md#overloaded) | [OVERLOADED](ydb-status-codes.md#overloaded) | *повторяемый* | *большая* | нет |
| [400070](ydb-status-codes.md#scheme-error) | [SCHEME_ERROR](ydb-status-codes.md#scheme-error) | *неповторяемый* | – | нет |
| [400080](ydb-status-codes.md#generic-error) | [GENERIC_ERROR](ydb-status-codes.md#generic-error) | *неповторяемый* | – | нет |
| [400090](ydb-status-codes.md#timeout) | [TIMEOUT](ydb-status-codes.md#timeout) | *неповторяемый* | – | нет |
| [400100](ydb-status-codes.md#bad-session) | [BAD_SESSION](ydb-status-codes.md#bad-session) | *повторяемый* | *моментально* | да |
| [400120](ydb-status-codes.md#precondition-failed) | [PRECONDITION_FAILED](ydb-status-codes.md#precondition-failed) | *неповторяемый* | – | нет |
| [400130](ydb-status-codes.md#already-exists) | [ALREADY_EXISTS](ydb-status-codes.md#already-exists) | *неповторяемый* | – | нет |
| [400140](ydb-status-codes.md#not-found) | [NOT_FOUND](ydb-status-codes.md#not-found) | *неповторяемый* | – | нет |
| [400150](ydb-status-codes.md#session-expired) | [SESSION_EXPIRED](ydb-status-codes.md#session-expired) | *повторяемый* | *моментально* | да |
| [400160](ydb-status-codes.md#cancelled) | [CANCELLED](ydb-status-codes.md#cancelled) | *неповторяемый* | – | нет |
| [400170](ydb-status-codes.md#undetermined) | [UNDETERMINED](ydb-status-codes.md#undetermined) | *условно повторяемый* | *короткая* | нет |
| [400180](ydb-status-codes.md#unsupported) | [UNSUPPORTED](ydb-status-codes.md#unsupported) | *неповторяемый* | – | нет |
| [400190](ydb-status-codes.md#session-busy) | [SESSION_BUSY](ydb-status-codes.md#session-busy) | *повторяемый* | *короткая* | да |
| [400200](ydb-status-codes.md#external-error) | [EXTERNAL_ERROR](ydb-status-codes.md#external-error) | *неповторяемый* | – | нет |

## 400000: SUCCESS {#success}

Не является ошибкой — запрос успешно обработан.

## 400010: BAD_REQUEST {#bad-request}

[Неповторяемый](error_handling.md)

Ошибка в синтаксисе запроса, пропущены обязательные поля.

Проверьте запрос.

## 400020: UNAUTHORIZED {#unauthorized}

[Неповторяемый](error_handling.md)

Отсутствует доступ к запрашиваемому схемному объекту (таблица, директория).

Запросите доступ у администратора базы данных.

## 400030: INTERNAL_ERROR {#internal-error}

[Неповторяемый](error_handling.md)

Неизвестная внутренняя ошибка.

Зарегистрируйте проблему на [GitHub](https://github.com/ydb-platform/ydb/issues/new) или обратитесь к технической поддержке YDB.

## 400040: ABORTED {#aborted}

[Повторяемый](error_handling.md) | Короткая задержка

Операция не выполнена (например, по причине инвалидации локов, `TRANSACTION_LOCKS_INVALIDATED` в подробных сообщениях об ошибке).

Повторите всю транзакцию.

## 400050: UNAVAILABLE {#unavailable}

[Повторяемый](error_handling.md) | Короткая задержка

Часть системы недоступна.

Повторите последнее действие (запрос).

## 400060: OVERLOADED {#overloaded}

[Повторяемый](error_handling.md) | Большая задержка

Часть системы перегружена.

Повторите последнее действие (запрос), снизьте интенсивность потока запросов.

## 400070: SCHEME_ERROR {#scheme-error}

[Неповторяемый](error_handling.md)

Запрос не соответствует схеме.

Исправьте запрос или схему.

## 400080: GENERIC_ERROR {#generic-error}

[Неповторяемый](error_handling.md)

Неклассифицируемая ошибка, возможно, связанная с запросом.

Ознакомьтесь с подробным сообщением об ошибке. При необходимости зарегистрируйте проблему на [GitHub](https://github.com/ydb-platform/ydb/issues/new) или обратитесь к технической поддержке YDB.

## 400090: TIMEOUT {#timeout}

[Условно повторяемый](error_handling.md) | Моментально

Запрос не выполнен за отведённое время.

Можно повторить для идемпотентных запросов.

## 400100: BAD_SESSION {#bad-session}

[Повторяемый](error_handling.md) | Моментально

Данная сессия больше недоступна.

Пересоздайте сессию.

## 400120: PRECONDITION_FAILED {#precondition-failed}

[Неповторяемый](error_handling.md)

Запрос не может быть выполнен в текущем состоянии (например, вставка в таблицу с существующим ключом).

Исправьте состояние или запрос и повторите попытку.

## 400130: ALREADY_EXISTS {#already-exists}

[Неповторяемый](error_handling.md)

Объект базы данных, который создаётся, уже существует в кластере YDB.

Ответ зависит от логики приложения.

## 400140: NOT_FOUND {#not-found}

[Неповторяемый](error_handling.md)

Объект базы данных не найден в YDB.

Ответ зависит от логики приложения.

## 400150: SESSION_EXPIRED {#session-expired}

[Условно повторяемый](error_handling.md) | Моментально

Срок действия сессии уже истёк.

Пересоздать сессию.

## 400160: CANCELLED {#cancelled}

[Неповторяемый](error_handling.md)

Запрос был отменён на сервере. Например, пользователь отменил запрос во [встроенном UI](../embedded-ui/index.md), который выполнялся слишком долго, или запрос был сделан с опцией таймаута [cancel_after](../../dev/timeouts.md#cancel).

Если выполнение запроса заняло слишком много времени, попробуйте оптимизировать запрос. Если использовалась опция таймаута `cancel_after`, увеличьте её значение.

## 400170: UNDETERMINED {#undetermined}

[Условно повторяемый](error_handling.md) | Короткая задержка

Состояние транзакции неизвестно. В результате выполнения запроса произошёл сбой, из-за которого невозможно определить состояние транзакции. На запросы, завершившиеся с таким статусом, распространяются гарантии целостности и атомарности транзакции. То есть либо все изменения зафиксированы, либо вся транзакция отменена.

Для идемпотентных транзакций можно повторить всю транзакцию с небольшой задержкой. В противном случае реакция зависит от логики приложения.

## 400180: UNSUPPORTED {#unsupported}

[Неповторяемый](error_handling.md)

Запрос не поддерживается YDB, либо потому, что обработка таких запросов ещё не реализована в данной версии YDB, либо потому, что поддержка таких запросов не включена в конфигурации YDB.

Исправьте запрос или включите поддержку подобных запросов в конфигурации YDB.

## 400190: SESSION_BUSY {#session-busy}

[Повторяемый](error_handling.md) | Короткая задержка

Сессия занята.

Пересоздайте сессию.

## 400200: EXTERNAL_ERROR {#external-error}

[Неповторяемый](error_handling.md)

Произошла ошибка во внешней системе, например, при обработке федеративного запроса или при импорте данных из внешнего источника.

Проанализируйте подробное сообщение об ошибке. При необходимости зарегистрируйте проблему на [GitHub](https://github.com/ydb-platform/ydb/issues/new) или обратитесь к технической поддержке YDB.

## Смотрите также {#smotrite-takzhe}

[Ошибки](../../faq/errors.md)

***Немедленный повтор** – одна из стратегий задержек, применяемых в SDK при повторе запросов, завершившихся ошибкой.  
  
 Повторные попытки при такой стратегии совершаются немедленно.  
  
 См. подробнее в статье [Обработка временных сбоев (retryable errors)](error_handling.md#handling-retryable-errors).****Короткая экспоненциальная задержка** – одна из стратегий задержек, применяемых в SDK при повторе запросов, завершившихся ошибкой.  
  
 Первоначальный интервал при такой задержке составляет несколько **миллисекунд**. Для каждой последующей попытки интервал увеличивается экспоненциально.  
  
 См. подробнее в статье [Обработка временных сбоев (retryable errors)](error_handling.md#handling-retryable-errors).****Большая экспоненциальная задержка** – одна из стратегий задержек, применяемых в SDK при повторе запросов, завершившихся ошибкой.  
  
 Первоначальный интервал при такой задержке составляет несколько **секунд**. Для каждой последующей попытки интервал увеличивается по экспоненциальному закону.  
  
 См. подробнее в статье [Обработка временных сбоев (retryable errors)](error_handling.md#handling-retryable-errors).****Временные сбои** (retryable). Включают кратковременную потерю сетевого соединения, временную недоступность или перегруженность одной из подсистем YDB, а также неспособность YDB ответить на запрос в течение установленного времени ожидания. В случае возникновения таких ошибок повторный запрос через некоторый промежуток времени с высокой вероятностью будет выполнен успешно.****Ошибки, которые не могут быть исправлены с помощью повтора** (non-retryable). Включают некорректно сформированные запросы, внутренние ошибки YDB, а также запросы, не соответствующие схеме данных. В такой ситуации нет необходимости повторять запрос, требуется дополнительное вмешательство разработчика.****Ошибки, которые, предположительно, могут быть исправлены с помощью повтора после реакции клиентского приложения** (conditionally retryable). Возникают при идемпотентных операциях, таких как отсутствие ответа в течение отведённого времени или запрос аутентификации.*
