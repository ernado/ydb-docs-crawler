---
title: "Initial cluster security configuration"
url: "https://ydb.tech/docs/en/security/builtin-security?version=v26.1"
doc_path: "en/security/builtin-security"
version: "v26.1"
lang: "en"
source_path: "en/core/security/builtin-security.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/security/builtin-security.md"
description: "Initial security is configured automatically when the YDB cluster starts for the first time."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Initial cluster security configuration

Initial security is configured automatically when the YDB cluster starts for the first time.

During this process YDB adds a [superuser](builtin-security.md#superuser) and a set of [roles](builtin-security.md#roles) for user access management.

> [!NOTE]
> For information about overriding and skipping initial security configuration, see the following sections:
>
> - [Skipping initial security configuration](builtin-security.md#skip-initial-security)
> - [Overriding initial security configuration](builtin-security.md#override-initial-security)

## Roles

| Role | Description |
| --- | --- |
| `ADMINS` | Provides unlimited access rights for the entire YDB cluster scheme. |
| `DATABASE-ADMINS` | Provides access rights to manage databases, their scheme, and scheme access rights. No data access. |
| `ACCESS-ADMINS` | Provides access rights to manage scheme access rights. No data access. |
| `DDL-ADMINS` | Provides access rights to manage the scheme. No data access. |
| `DATA-WRITERS` | Provides access rights for scheme objects, including reading and modifying data. |
| `DATA-READERS` | Provides access rights for scheme objects and reading data. |
| `METADATA-READERS` | Provides access rights for scheme objects. No data access. |
| `USERS` | Provides access rights for databases. This is a common group for all users. |

## Groups

Roles in YDB are implemented as a hierarchy of [user](../concepts/glossary.md#access-user) [groups](authorization.md#group) and a set of [access rights](authorization.md#right) for these groups. Access rights for the groups are granted on the cluster scheme root.

Groups can be nested, and a child group inherits the access rights of its parent group:

For example, users in the `DATA-WRITERS` group are allowed to:

- View the scheme — `METADATA-READERS`
- Read data — `DATA-READERS`
- Change data — `DATA-WRITERS`

Users in the `DDL-ADMINS` group are allowed to:

- View the scheme — `METADATA-READERS`
- Change the scheme — `DDL-ADMINS`

Users in the `ADMINS` group are allowed to perform all operations on the scheme and data.

## Superuser

A superuser belongs to the `ADMINS` and `USERS` groups and has full access rights to the cluster scheme.

By default, a superuser is the `root` user with an empty password.

## A group for all users {#all-users-group}

The `USERS` group is a common [group](../concepts/glossary.md#access-group) for all local [users](../concepts/glossary.md#access-user). When you [add new users](authorization.md#user), they are automatically added to the `USERS` group.

For more information about managing groups and users, see [Authorization](authorization.md).

## Overriding initial security configuration {#override-initial-security}

You can override the initial security configuration with a custom set of users, groups, and access rights.

To specify custom users, groups, and access rights to be created during the initial security configuration, define the `default_users`, `default_groups`, or `default_access` parameters in the [`security_config`](../reference/configuration/security_config.md#security-bootstrap) section in the cluster configuration file.

## Skipping initial security configuration {#skip-initial-security}

You can skip initial security configuration by setting the [`security_config.disable_builtin_security`](../reference/configuration/domains_config.md#domains-config) parameter to `true`.
