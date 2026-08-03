---
title: "Deleting a profile"
url: "https://ydb.tech/docs/en/reference/ydb-cli/profile/delete?version=v26.1"
doc_path: "en/reference/ydb-cli/profile/delete"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/profile/delete.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/profile/delete.md"
description: "Deleting a profile. Currently, you can only delete profiles interactively with the following command: ydb config profile delete <profile_name>."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Deleting a profile

Currently, you can only delete profiles interactively with the following command:

```bash
ydb config profile delete <profile_name>
```

where `<profile_name>` is the profile name.

The YDB CLI will request confirmation to delete the profile:

```text
Profile "<profile_name>" will be permanently removed. Continue? (y/n):
```

Choose `y` (Yes) to delete the profile.

## Example

Deleting the `mydb1` profile:

```bash
$ ydb config profile delete mydb1
Profile "mydb1" will be permanently removed. Continue? (y/n): y
Profile "mydb1" was removed.
```

## Deleting a profile without interactive input {#non-interactive}

Although this mode is not supported by the YDB CLI, if necessary, you can use input redirection in your OS to automatically respond `y` to the request to confirm the deletion:

```bash
echo y | ydb config profile delete my_profile
```

The efficiency of this method is not guaranteed in any way.
