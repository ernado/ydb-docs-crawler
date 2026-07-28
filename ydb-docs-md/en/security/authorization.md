---
title: "Authorization"
url: "https://ydb.tech/docs/en/security/authorization?version=v26.1"
doc_path: "en/security/authorization"
version: "v26.1"
lang: "en"
source_path: "en/core/security/authorization.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/security/authorization.md"
description: "Basic concepts. Authorization in YDB is based on the concepts of: Access object. Access subject. Access right. Access control list. Owner. User. Group."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Authorization

## Basic concepts

Authorization in YDB is based on the concepts of:

- [Access object](../concepts/glossary.md#access-object)
- [Access subject](../concepts/glossary.md#access-subject)
- [Access right](../concepts/glossary.md#access-right)
- [Access control list](../concepts/glossary.md#access-acl)
- [Owner](../concepts/glossary.md#access-owner)
- [User](../concepts/glossary.md#access-user)
- [Group](../concepts/glossary.md#access-group)

Regardless of the [authentication](https://en.wikipedia.org/wiki/Authentication) method, [authorization](https://en.wikipedia.org/wiki/Authorization) is always performed on the server side of YDB based on the stored information about access objects and rights. Access rights determine the set of operations available to perform.

Authorization is performed for each user action: the rights are not cached, as they can be revoked or granted at any time.

## User

To create, alter, and delete users in YDB, the following commands are available:

- [CREATE USER](../yql/reference/syntax/create-user.md)
- [ALTER USER](../yql/reference/syntax/alter-user.md)
- [DROP USER](../yql/reference/syntax/drop-user.md)

> [!NOTE]
> The scope of the commands `CREATE USER`, `ALTER USER`, and `DROP USER` does not extend to external user directories. Keep this in mind if users with third-party authentication (e.g., LDAP) are connecting to YDB. For example, the `CREATE USER` command does not create a user in the LDAP directory. Learn more about [YDB's interaction with the LDAP directory](authentication.md#ldap-auth-provider).

> [!NOTE]
> There is a separate user `root` with maximum rights. It is created during the initial deployment of the cluster, during which a password must be set immediately. It is not recommended to use this account long-term; instead, users with limited rights should be created.
>
> More about initial deployment:
>
> - [Ansible](../devops/deployment-options/ansible/initial-deployment/index.md)
> - [Kubernetes](../devops/deployment-options/kubernetes/initial-deployment.md)
> - [Manually](../devops/deployment-options/manual/initial-deployment/index.md)

YDB allows working with [users](../concepts/glossary.md#access-user) from different directories and systems, and they differ by [SID](../concepts/glossary.md#access-sid) using a suffix.

The suffix `@<subsystem>` identifies the "user source" or "auth domain", within which the uniqueness of all `login` is guaranteed. For example, in the case of [LDAP authentication](authentication.md#ldap-auth-provider), user names will be `user1@ldap` and `user2@ldap`.  
 If a `login` without a suffix is specified, it implies users directly created in the YDB cluster.

## Group

Any [user](../concepts/glossary.md#access-user) can be included in or excluded from a certain [access group](../concepts/glossary.md#access-group). Once a user is included in a group, they receive all the rights to [database objects](../concepts/glossary.md#access-object) that were provided to the access group.  
 With access groups in YDB, business roles for user applications can be implemented by pre-configuring the required access rights to the necessary objects.

> [!NOTE]
> An access group can be empty when it does not include any users.
>
> Access groups can be nested.

To create, alter, and delete [groups](../concepts/glossary.md#access-group), the following types of YQL queries are available:

- [CREATE GROUP](../yql/reference/syntax/create-group.md)
- [ALTER GROUP](../yql/reference/syntax/alter-group.md)
- [DROP GROUP](../yql/reference/syntax/drop-group.md)

## Right

[Rights](../concepts/glossary.md#access-right) in YDB are tied not to the [subject](../concepts/glossary.md#access-subject), but to the [access object](../concepts/glossary.md#access-object).

Each access object has a list of permissions — [ACL](../concepts/glossary.md#access-acl) (Access Control List) — it stores all the rights provided to [access subjects](../concepts/glossary.md#subject) (users and groups) for the object.

By default, rights are inherited from parents to descendants in the access objects tree.

The following types of YQL queries are used for managing rights:

- [GRANT](../yql/reference/syntax/grant.md).
- [REVOKE](../yql/reference/syntax/revoke.md).

The following CLI commands are used for managing rights:

- [chown](../reference/ydb-cli/commands/scheme-permissions.md#chown)
- [grant](../reference/ydb-cli/commands/scheme-permissions.md#grant-revoke)
- [revoke](../reference/ydb-cli/commands/scheme-permissions.md#grant-revoke)
- [set](../reference/ydb-cli/commands/scheme-permissions.md#set)
- [clear](../reference/ydb-cli/commands/scheme-permissions.md#clear)
- [clear-inheritance](../reference/ydb-cli/commands/scheme-permissions.md#clear-inheritance)
- [set-inheritance](../reference/ydb-cli/commands/scheme-permissions.md#set-inheritance)

The following CLI commands are used to view the ACL of an access object:

- [describe](../reference/ydb-cli/commands/scheme-describe.md)
- [list](../reference/ydb-cli/commands/scheme-permissions.md#list)

## Object Owner {#owner}

Each access object has an [owner](../concepts/glossary.md#access-owner). By default, it becomes the [access subject](../concepts/glossary.md#access-subject) who created the [access object](../concepts/glossary.md#access-object).

> [!NOTE]
> For the owner, [permission lists](../concepts/glossary.md#access-control-list) on this [access object](../concepts/glossary.md#access-object) are not checked.
>
> They have a full set of rights on the object.

An object owner exists for the entire cluster and each database.

The owner can be changed using the CLI command [`chown`](../reference/ydb-cli/commands/scheme-permissions.md#chown).

The owner of an object can be viewed using the CLI command [`describe`](../reference/ydb-cli/commands/scheme-describe.md).
