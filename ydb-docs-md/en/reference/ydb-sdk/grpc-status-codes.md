---
title: "gRPC status codes"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/grpc-status-codes?version=v26.1"
doc_path: "en/reference/ydb-sdk/grpc-status-codes"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/grpc-status-codes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/grpc-status-codes.md"
description: "YDB provides the gRPC API, which you can use to manage your database resources and data. The following table describes the gRPC status codes: Code. Status."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# gRPC status codes

YDB provides the gRPC API, which you can use to manage your database resources and data. The following table describes the gRPC status codes:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Code | Status | Retryability | Backoff strategy | Recreate session |
| [0](grpc-status-codes.md#ok) | [OK](grpc-status-codes.md#ok) | – | – | – |
| [1](grpc-status-codes.md#cancelled) | [CANCELLED](grpc-status-codes.md#cancelled) | *conditionally-retryable* | *fast* | yes |
| [2](grpc-status-codes.md#unknown) | [UNKNOWN](grpc-status-codes.md#unknown) | *non-retryable* | – | yes |
| [3](grpc-status-codes.md#invalid-argument) | [INVALID_ARGUMENT](grpc-status-codes.md#invalid-argument) | *non-retryable* | – | yes |
| [4](grpc-status-codes.md#deadline-exceeded) | [DEADLINE_EXCEEDED](grpc-status-codes.md#deadline-exceeded) | *conditionally-retryable* | *fast* | yes |
| [5](grpc-status-codes.md#not-found) | [NOT_FOUND](grpc-status-codes.md#not-found) | *non-retryable* | – | yes |
| [6](grpc-status-codes.md#already-exists) | [ALREADY_EXISTS](grpc-status-codes.md#already-exists) | *non-retryable* | – | yes |
| [7](grpc-status-codes.md#permission-denied) | [PERMISSION_DENIED](grpc-status-codes.md#permission-denied) | *non-retryable* | – | yes |
| [8](grpc-status-codes.md#resource-exhausted) | [RESOURCE_EXHAUSTED](grpc-status-codes.md#resource-exhausted) | *retryable* | *slow* | no |
| [9](grpc-status-codes.md#failed-precondition) | [FAILED_PRECONDITION](grpc-status-codes.md#failed-precondition) | *non-retryable* | – | yes |
| [10](grpc-status-codes.md#aborted) | [ABORTED](grpc-status-codes.md#aborted) | *retryable* | *instant* | yes |
| [11](grpc-status-codes.md#out-of-range) | [OUT_OF_RANGE](grpc-status-codes.md#out-of-range) | *non-retryable* | – | no |
| [12](grpc-status-codes.md#unimplemented) | [UNIMPLEMENTED](grpc-status-codes.md#unimplemented) | *non-retryable* | – | yes |
| [13](grpc-status-codes.md#internal) | [INTERNAL](grpc-status-codes.md#internal) | *conditionally-retryable* | *fast* | yes |
| [14](grpc-status-codes.md#unavailable) | [UNAVAILABLE](grpc-status-codes.md#unavailable) | *conditionally-retryable* | *fast* | yes |
| [15](grpc-status-codes.md#data-loss) | [DATA_LOSS](grpc-status-codes.md#data-loss) | *non-retryable* | – | yes |
| [16](grpc-status-codes.md#unauthenticated) | [UNAUTHENTICATED](grpc-status-codes.md#unauthenticated) | *non-retryable* | – | yes |

## 0: OK {#ok}

Not an error; returned on success.

## 1: CANCELLED {#cancelled}

[Conditionally retryable](error_handling.md) | Fast Backoff

The operation was cancelled, typically by the caller.

## 2: UNKNOWN {#unknown}

[Non-retryable](error_handling.md)

Unknown error. For example, this error may be returned when a `Status` value received from another address space belongs to an error space that is not known in this address space. Errors raised by APIs that do not return enough error information may also be converted to this error.

## 3: INVALID_ARGUMENT {#invalid-argument}

[Non-retryable](error_handling.md)

The client specified an invalid argument. Unlike `FAILED_PRECONDITION`, `INVALID_ARGUMENT` indicates arguments that are problematic regardless of the system state (e.g., a malformed file name).

## 4: DEADLINE_EXCEEDED {#deadline-exceeded}

[Conditionally retryable](error_handling.md) | Fast Backoff

The query was not processed within the specified client timeout, or a network issue occurred.

Check the specified timeout, network access, endpoint, and other network settings. Reduce the query rate and optimize queries.

## 5: NOT_FOUND {#not-found}

[Non-retryable](error_handling.md)

A requested scheme object (for example, a table or directory) was not found.

## 6: ALREADY_EXISTS {#already-exists}

[Non-retryable](error_handling.md)

The scheme object that a client attempted to create (e.g., file or directory) already exists.

## 7: PERMISSION_DENIED {#permission-denied}

[Non-retryable](error_handling.md)

The caller does not have permission to execute the specified operation.

## 8: RESOURCE_EXHAUSTED {#resource-exhausted}

[Retryable](error_handling.md) | Slow Backoff

There are not enough resources available to fulfill the query.

Reduce the query rate and check client balancing.

## 9: FAILED_PRECONDITION {#failed-precondition}

[Non-retryable](error_handling.md)

The query cannot be executed in the current state (for example, inserting data into a table with an existing key).

Fix the state or query, then retry.

## 10: ABORTED {#aborted}

[Retryable](error_handling.md) | Instant

The operation was aborted, typically due to a concurrency issue, such as a transaction abort.

## 11: OUT_OF_RANGE {#out-of-range}

[Non-retryable](error_handling.md)

The operation was attempted past the valid range. Unlike `INVALID_ARGUMENT`, this error indicates a problem that may be fixed if the system state changes.

## 12: UNIMPLEMENTED {#unimplemented}

[Non-retryable](error_handling.md)

The operation is not implemented, supported, or enabled in this service.

## 13: INTERNAL {#internal}

[Conditionally retryable](error_handling.md) | Fast Backoff

Internal errors. This means that some invariants expected by the underlying system have been broken. This error code is reserved for significant problems.

## 14: UNAVAILABLE {#unavailable}

[Conditionally retryable](error_handling.md) | Fast Backoff

The service is currently unavailable. This is most likely a transient condition that can be corrected by retrying with a backoff. Note that it is not always safe to retry non-idempotent operations.

## 15: DATA_LOSS {#data-loss}

[Non-retryable](error_handling.md)

Unrecoverable data loss or corruption.

## 16: UNAUTHENTICATED {#unauthenticated}

[Non-retryable](error_handling.md)

The request did not have valid authentication credentials.

Retry the request with valid authentication credentials.

***Instant retry** is one of the backoff strategies used in YDB SDK when retrying queries that return an error.  
  
 This strategy retries queries immediately after receiving an error.  
  
 For more information, see [Handling retryable errors](error_handling.md#handling-retryable-errors).****Fast exponential backoff** is one of the backoff strategies used in YDB SDK when retrying queries that return an error.  
  
 The initial interval for this strategy is several **milliseconds**. For each subsequent attempt, the interval increases exponentially.  
  
 For more information, see [Handling retryable errors](error_handling.md#handling-retryable-errors).****Slow exponential backoff** is one of the backoff strategies used by YDB SDK when retrying queries that return an error.  
  
 The initial interval for this strategy is several **seconds**. For each subsequent attempt, the interval increases exponentially.  
  
 For more information, see [Handling retryable errors](error_handling.md#handling-retryable-errors).****Temporary failures** (retryable). Such errors include a short-term loss of network connectivity, temporary unavailability, overload of a YDB subsystem, or a failure of YDB to respond to a query within the set timeout. If one of these errors occurs, retrying the failed query is likely to be successful after some time.****Errors that cannot be fixed with a retry** (non-retryable). Such errors are caused by incorrectly written queries, YDB internal errors, or queries that mismatch the data schema. Retrying such queries will not resolve the issue. This situation requires developer attention.****Errors that can presumably be fixed with a retry after the client application response** (conditionally retryable). Such errors include no response within the set timeout or an authentication request. Only idempotent operations can be fixed with a retry.*
