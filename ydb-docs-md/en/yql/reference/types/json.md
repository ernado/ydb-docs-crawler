---
title: "Data representation in JSON format"
url: "https://ydb.tech/docs/en/yql/reference/types/json?version=v26.1"
doc_path: "en/yql/reference/types/json"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/types/json.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/types/json.md"
description: "Bool. Boolean value. Type in JSON: bool. Sample YDB value: true. Sample JSON value: true. Int8, Int16, Int32, Int64. Signed integer types. Type in JSON: number."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Data representation in JSON format

## Bool

Boolean value.

- Type in JSON: `bool`.
- Sample YDB value: `true`.
- Sample JSON value: `true`.

## Int8, Int16, Int32, Int64 {#int}

Signed integer types.

- Type in JSON: `number`.
- Sample YDB value: `123456`, `-123456`.
- Sample JSON value: `123456`, `-123456`.

## Uint8, Uint16, Uint32, Uint64 {#uint}

Unsigned integer types.

- Type in JSON: `number`.
- Sample YDB value: `123456`.
- Sample JSON value: `123456`.

## Float

Real 4-byte number.

- Type in JSON: `number`.
- Sample YDB value: `0.12345679`.
- Sample JSON value: `0.12345679`.

## Double

Real 8-byte number.

- Type in JSON: `number`.
- Sample YDB value: `0.12345678901234568`.
- Sample JSON value: `0.12345678901234568`.

## Decimal

Fixed-precision number.

- Type in JSON: `string`.
- Sample YDB value: `-320.789`.
- Sample JSON value: `"-320.789"`.

## String, Yson {#string}

Binary strings. Encoding algorithm depending on the byte value:

- \[0-31\] — `\u00XX` (6 characters denoting the Unicode character code).
- \[32-126\] — as is. These are readable single-byte characters that don't need to be escaped.
- \[127-255\] — `\u00XX`.

Decoding is a reverse process. Character codes in `\u00XX`, maximum 255.

- Type in JSON: `string`.

- Sample YDB value: A sequence of 4 bytes:

  - 5 `0x05`: A control character.
  - 10 `0x0a`: The `\n` newline character.
  - 107 `0x6b`: The `k` character.
  - 255 `0xff`: The `ÿ` character in Unicode.

- Sample JSON value: `"\u0005\nk\u00FF"`.

## Utf8, Json, Uuid {#utf}

String types in UTF-8. Such strings are represented in JSON as strings with JSON characters escaped: `\\`, `\"`, `\n`, `\r`, `\t`, `\f`.

- Type in JSON: `string`.

- Sample YDB value: C++ code:

  ```c++
  "Escaped characters: "
  "\\ \" \f \b \t \r\n"
  "Non-escaped characters: "
  "/ ' < > & []() ".
  ```

- Sample JSON value: `"Escaped characters: \\ \" \f \b \t \r\nNon-escaped characters: / ' < > & []() "`.

## Date

Date. Uint64, unix time days.

- Type in JSON: `string`.
- Sample YDB value: `18367`.
- Sample JSON value: `"2020-04-15"`.

## Datetime

Date and time. Uint64, unix time seconds.

- Type in JSON: `string`.
- Sample YDB value: `1586966302`.
- Sample JSON value: `"2020-04-15T15:58:22Z"`.

## Timestamp

Date and time. Uint64, unix time microseconds.

- Type in JSON: `string`.
- Sample YDB value: `1586966302504185`.
- Sample JSON value: `"2020-04-15T15:58:22.504185Z"`.

## Interval

Time interval. Int64, precision to the microsecond, the interval values must not exceed 24 hours.

- Type in JSON: `number`.
- Sample YDB value: `123456`, `-123456`.
- Sample JSON value: `123456`, `-123456`.

## Optional

Means that the value can be `null`. If the value is `null`, then in JSON it's also `null`. If the value is not `null`, then the JSON value is expressed as if the type isn't `Optional`.

- Type in JSON is missing.
- Sample YDB value: `null`.
- Sample JSON value: `null`.

## List

List. An ordered set of values of a given type.

- Type in JSON: `array`.

- Sample YDB value:

  - Type: `List<Int32>`.
  - Value: `1, 10, 100`.

- Sample JSON value: `[1,10,100]`.

## Stream

Stream. Single-pass iterator by same-type values,

- Type in JSON: `array`.

- Sample YDB value:

  - Type: `Stream<Int32>`.
  - Value: `1, 10, 100`.

- Sample JSON value: `[1,10,100]`.

## Struct

Structure. An unordered set of values with the specified names and type.

- Type in JSON: `object`.

- Sample YDB value:

  - Type: `Struct<'Id':Uint32,'Name':String,'Value':Int32,'Description':Utf8?>`;
  - Value: `"Id":1,"Name":"Anna","Value":-100,"Description":null`.

- Sample JSON value: `{"Id":1,"Name":"Anna","Value":-100,"Description":null}`.

## Tuple

Tuple. An ordered set of values of the set types.

- Type in JSON: `array`.

- Sample YDB value:

  - Type: `Tuple<Int32??,Int64???,String??,Utf8???>`;
  - Value: `10,-1,null,"Some string"`.

- Sample JSON value: `[10,-1,null,"Some string"]`.

## Dict

Dictionary. An unordered set of key-value pairs. The type is set both for the key and the value. It's written in JSON to an array of arrays including two items.

- Type in JSON: `array`.

- Sample YDB value:

  - Type: `Dict<Int64,String>`.
  - Value: `1:"Value1",2:"Value2"`.

- Sample JSON value: `[[1,"Value1"],[2,"Value2"]]`.
