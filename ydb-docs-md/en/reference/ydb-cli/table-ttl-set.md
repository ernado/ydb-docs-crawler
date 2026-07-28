---
title: "Setting TTL parameters"
url: "https://ydb.tech/docs/en/reference/ydb-cli/table-ttl-set?version=v26.1"
doc_path: "en/reference/ydb-cli/table-ttl-set"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/table-ttl-set.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/table-ttl-set.md"
description: "Use the table ttl set subcommand to set TTL for the specified table. General format of the command:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Setting TTL parameters

Use the `table ttl set` subcommand to set [TTL](../../concepts/ttl.md) for the specified table.

General format of the command:

```bash
ydb [global options...] table ttl set [options...] <table path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](table-ttl-set.md#options).
- `table path`: The table path.

View a description of the TTL set command:

```bash
ydb table ttl set --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--column` | The name of the column that will be used to calculate the lifetime of the rows. The column must have the [numeric](../../yql/reference/types/primitive.md#numeric) or [date and time](../../yql/reference/types/primitive.md#datetime) type.  <br>In case of the numeric type, the value will be interpreted as the time elapsed since the beginning of the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time). Measurement units must be specified in the `--unit` parameter. |
| `--expire-after` | Additional time before deleting that must elapse after the lifetime of the row has expired. Specified in seconds.  <br>The default value is `0`. |
| `--unit` | The value measurement units of the column specified in the `--column` parameter. It is mandatory if the column has the [numeric](../../yql/reference/types/primitive.md#numeric) type.  <br>Possible values:<br>- `seconds (s, sec)`: Seconds.<br>- `milliseconds (ms, msec)`: Milliseconds.<br>- `microseconds (us, usec)`: Microseconds.<br>- `nanoseconds (ns, nsec)`: Nanoseconds. |
| `--run-interval` | The interval for running the operation to delete rows with expired TTL. Specified in seconds. The default database settings do not allow an interval of less than 15 minutes (900 seconds).  <br>The default value is `3600`. |

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Set TTL for the `series` table

```bash
ydb -p quickstart table ttl set \
  --column createtime \
  --expire-after 3600 \
  --run-interval 1200 \
  series
```
