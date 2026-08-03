---
title: "CREATE GROUP"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-group?version=v26.1"
doc_path: "en/yql/reference/syntax/create-group"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-group.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-group.md"
description: "Creates a group with the specified name. Optionally, you can specify a list of users to add to the group. Syntax."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE GROUP

Creates a [group](../../../concepts/glossary.md#access-group) with the specified name. Optionally, you can specify a list of [users](../../../concepts/glossary.md#access-user) to add to the group.

## Syntax

```yql
CREATE GROUP group_name [ WITH USER user_name [ , user_name [ ... ]] [ , ] ]
```

### Parameters

- `group_name`: The name of the group. It may contain lowercase Latin letters and digits.
- `user_name`: The name of the user who will become a member of the group after its creation. It may contain lowercase Latin letters and digits.

## Examples

```yql
CREATE GROUP group1;
```

```yql
CREATE GROUP group2 WITH USER user1;
```

```yql
CREATE GROUP group3 WITH USER user1, user2,;
```

```yql
CREATE GROUP group4 WITH USER user1, user3, user2;
```
