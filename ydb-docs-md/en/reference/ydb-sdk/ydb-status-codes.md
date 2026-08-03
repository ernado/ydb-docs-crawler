---
title: "Status codes from the YDB server"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/ydb-status-codes?version=v26.1"
doc_path: "en/reference/ydb-sdk/ydb-status-codes"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/ydb-status-codes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/ydb-status-codes.md"
description: "Code. Status. Retryability. Backoff strategy. Recreate session. 400000. SUCCESS. –. –. –. 400010. BAD_REQUEST. non-retryable. –. no. 400020. UNAUTHORIZED."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Status codes from the YDB server

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Code | Status | Retryability | Backoff strategy | Recreate session |
| [400000](ydb-status-codes.md#success) | [SUCCESS](ydb-status-codes.md#success) | – | – | – |
| [400010](ydb-status-codes.md#bad-request) | [BAD_REQUEST](ydb-status-codes.md#bad-request) | *non-retryable* | – | no |
| [400020](ydb-status-codes.md#unauthorized) | [UNAUTHORIZED](ydb-status-codes.md#unauthorized) | *non-retryable* | – | no |
| [400030](ydb-status-codes.md#internal-error) | [INTERNAL_ERROR](ydb-status-codes.md#internal-error) | *non-retryable* | – | no |
| [400040](ydb-status-codes.md#aborted) | [ABORTED](ydb-status-codes.md#aborted) | *retryable* | *fast* | no |
| [400050](ydb-status-codes.md#unavailable) | [UNAVAILABLE](ydb-status-codes.md#unavailable) | *retryable* | *fast* | no |
| [400060](ydb-status-codes.md#overloaded) | [OVERLOADED](ydb-status-codes.md#overloaded) | *retryable* | *slow* | no |
| [400070](ydb-status-codes.md#scheme-error) | [SCHEME_ERROR](ydb-status-codes.md#scheme-error) | *non-retryable* | – | no |
| [400080](ydb-status-codes.md#generic-error) | [GENERIC_ERROR](ydb-status-codes.md#generic-error) | *non-retryable* | – | no |
| [400090](ydb-status-codes.md#timeout) | [TIMEOUT](ydb-status-codes.md#timeout) | *non-retryable* | – | no |
| [400100](ydb-status-codes.md#bad-session) | [BAD_SESSION](ydb-status-codes.md#bad-session) | *retryable* | *instant* | yes |
| [400120](ydb-status-codes.md#precondition-failed) | [PRECONDITION_FAILED](ydb-status-codes.md#precondition-failed) | *non-retryable* | – | no |
| [400130](ydb-status-codes.md#already-exists) | [ALREADY_EXISTS](ydb-status-codes.md#already-exists) | *non-retryable* | – | no |
| [400140](ydb-status-codes.md#not-found) | [NOT_FOUND](ydb-status-codes.md#not-found) | *non-retryable* | – | no |
| [400150](ydb-status-codes.md#session-expired) | [SESSION_EXPIRED](ydb-status-codes.md#session-expired) | *retryable* | *instant* | yes |
| [400160](ydb-status-codes.md#cancelled) | [CANCELLED](ydb-status-codes.md#cancelled) | *non-retryable* | – | no |
| [400170](ydb-status-codes.md#undetermined) | [UNDETERMINED](ydb-status-codes.md#undetermined) | *conditionally-retryable* | *fast* | no |
| [400180](ydb-status-codes.md#unsupported) | [UNSUPPORTED](ydb-status-codes.md#unsupported) | *non-retryable* | – | no |
| [400190](ydb-status-codes.md#session-busy) | [SESSION_BUSY](ydb-status-codes.md#session-busy) | *retryable* | *fast* | yes |
| [400200](ydb-status-codes.md#external-error) | [EXTERNAL_ERROR](ydb-status-codes.md#external-error) | *non-retryable* | – | no |

## 400000: SUCCESS {#success}

The query was processed successfully.

No response is required. Continue application execution.

## 400010: BAD_REQUEST {#bad-request}

[Non-retryable](error_handling.md)

Invalid query syntax or missing required fields.

Correct the query.

## 400020: UNAUTHORIZED {#unauthorized}

[Non-retryable](error_handling.md)

Access to the requested schema object (for example, a table or directory) is denied.

Request access from its owner.

## 400030: INTERNAL_ERROR {#internal-error}

[Non-retryable](error_handling.md)

An unknown internal error occurred.

File a [GitHub issue](https://github.com/ydb-platform/ydb/issues/new) or contact YDB technical support.

## 400040: ABORTED {#aborted}

[Retryable](error_handling.md) | Fast Backoff

The operation was aborted. Possible reasons might include lock invalidation with `TRANSACTION_LOCKS_INVALIDATED` in detailed error messages.

Retry the entire transaction.

## 400050: UNAVAILABLE {#unavailable}

[Retryable](error_handling.md) | Fast Backoff

A part of the system is not available.

Retry the last action (query).

## 400060: OVERLOADED {#overloaded}

[Retryable](error_handling.md) | Slow Backoff

A part of the system is overloaded.

Retry the last action (query) and reduce the query rate.

## 400070: SCHEME_ERROR {#scheme-error}

[Non-retryable](error_handling.md)

The query does not match the schema.

Correct the query or schema.

## 400080: GENERIC_ERROR {#generic-error}

[Non-retryable](error_handling.md)

An unclassified error occurred, possibly related to the query.

See the detailed error message. If necessary, file a [GitHub issue](https://github.com/ydb-platform/ydb/issues/new) or contact YDB technical support.

## 400090: TIMEOUT {#timeout}

[Conditionally retryable](error_handling.md) | Instant

The query timeout expired.

If the query is idempotent, retry it.

## 400100: BAD_SESSION {#bad-session}

[Retryable](error_handling.md) | Instant

This session is no longer available.

Create a new session.

## 400120: PRECONDITION_FAILED {#precondition-failed}

[Non-retryable](error_handling.md)

The query cannot be executed in the current state. For example, inserting data into a table with an existing key.

Correct the state or query, then retry.

## 400130: ALREADY_EXISTS {#already-exists}

[Non-retryable](error_handling.md)

The database object being created already exists in the YDB cluster.

The response depends on the application logic.

## 400140: NOT_FOUND {#not-found}

[Non-retryable](error_handling.md)

The database object was not found in the YDB database.

The response depends on the application logic.

## 400150: SESSION_EXPIRED {#session-expired}

[Conditionally retryable](error_handling.md) | Instant

The session has already expired.

Create a new session.

## 400160: CANCELLED {#cancelled}

[Non-retryable](error_handling.md)

The request was canceled on the server. For example, a user canceled a long-running query in the [Embedded UI](../embedded-ui/index.md), or the query included the [cancel_after](../../dev/timeouts.md#cancel) timeout option.

If the query took too long to complete, try optimizing it. If you used the `cancel_after` timeout option, increase the timeout value.

## 400170: UNDETERMINED {#undetermined}

[Conditionally retryable](error_handling.md) | Fast Backoff

An unknown transaction status. The query ended with a failure, making it impossible to determine the transaction status. Queries that terminate with this status are subject to transaction integrity and atomicity guarantees. That is, either all changes are registered, or the entire transaction is canceled.

For idempotent transactions, retry the entire transaction after a short delay. Otherwise, the response depends on the application logic.

## 400180: UNSUPPORTED {#unsupported}

[Non-retryable](error_handling.md)

The query is not supported by YDB either because support for such queries is not yet implemented or is not enabled in the YDB configuration.

Correct the query or enable support for such queries in YDB.

## 400190: SESSION_BUSY {#session-busy}

[Retryable](error_handling.md) | Fast Backoff

The session is busy.

Create a new session.

## 400200: EXTERNAL_ERROR {#external-error}

[Non-retryable](error_handling.md)

An error occurred in an external system, for example, when processing a federated query or importing data from an external data source.

See the detailed error message. If necessary, file a [GitHub issue](https://github.com/ydb-platform/ydb/issues/new) or contact YDB technical support.

## See also

[Questions and answers: Errors](../../faq/errors.md)

***Instant retry** is one of the backoff strategies used in YDB SDK when retrying queries that return an error.  
  
 This strategy retries queries immediately after receiving an error.  
  
 For more information, see [Handling retryable errors](error_handling.md#handling-retryable-errors).****Fast exponential backoff** is one of the backoff strategies used in YDB SDK when retrying queries that return an error.  
  
 The initial interval for this strategy is several **milliseconds**. For each subsequent attempt, the interval increases exponentially.  
  
 For more information, see [Handling retryable errors](error_handling.md#handling-retryable-errors).****Slow exponential backoff** is one of the backoff strategies used by YDB SDK when retrying queries that return an error.  
  
 The initial interval for this strategy is several **seconds**. For each subsequent attempt, the interval increases exponentially.  
  
 For more information, see [Handling retryable errors](error_handling.md#handling-retryable-errors).****Temporary failures** (retryable). Such errors include a short-term loss of network connectivity, temporary unavailability, overload of a YDB subsystem, or a failure of YDB to respond to a query within the set timeout. If one of these errors occurs, retrying the failed query is likely to be successful after some time.****Errors that cannot be fixed with a retry** (non-retryable). Such errors are caused by incorrectly written queries, YDB internal errors, or queries that mismatch the data schema. Retrying such queries will not resolve the issue. This situation requires developer attention.****Errors that can presumably be fixed with a retry after the client application response** (conditionally retryable). Such errors include no response within the set timeout or an authentication request. Only idempotent operations can be fixed with a retry.*
