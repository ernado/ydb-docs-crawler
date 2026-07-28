---
title: "List of objects"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/scheme-ls?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/scheme-ls"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/scheme-ls.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/scheme-ls.md"
description: "List of objects. The scheme ls command lets you get a list of scheme objects in the database: ydb [connection options] scheme ls [path] [-lR1]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# List of objects

The `scheme ls` command lets you get a list of [scheme objects](../../../concepts/glossary.md#scheme-object) in the database:

```bash
ydb [connection options] scheme ls [path] [-lR1]
```

where \[connection options\] are [database connection options](../connect.md#command-line-pars)

Executing the command without parameters produces a compressed list of object names in the database's root directory.

In the `path` parameter, you can specify the [directory](dir.md) you want to list objects in.

The following options are available for the command:

- `-l`: Full details about attributes of each object.
- `-R`: Recursive traversal of all subdirectories.
- `-1`: Output a single schema object per row (for example, to be later handled in a script).

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](../profile/create.md#quickstart).

- Getting objects from the root database directory in a compressed format

```bash
ydb --profile quickstart scheme ls
```

- Getting objects in all database directories in a compressed format

```bash
ydb --profile quickstart scheme ls -R
```

- Getting objects from the given database directory in a compressed format

```bash
ydb --profile quickstart scheme ls dir1
ydb --profile quickstart scheme ls dir1/dir2
```

- Getting objects in all subdirectories in the given directory in a compressed format

```bash
ydb --profile quickstart scheme ls dir1 -R
ydb --profile quickstart scheme ls dir1/dir2 -R
```

- Getting complete information on objects in the root database directory

```bash
ydb --profile quickstart scheme ls -l
```

- Getting complete information about objects in a given database directory

```bash
ydb --profile quickstart scheme ls dir1 -l
ydb --profile quickstart scheme ls dir2/dir3 -l
```

- Getting complete information about objects in all database directories

```bash
ydb --profile quickstart scheme ls -lR
```

- Getting complete information on objects in all subdirectories of a given database directory

```bash
ydb --profile quickstart scheme ls dir1 -lR
ydb --profile quickstart scheme ls dir2/dir3 -lR
```
