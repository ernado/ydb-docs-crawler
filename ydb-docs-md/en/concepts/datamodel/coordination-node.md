---
title: "Coordination Node"
url: "https://ydb.tech/docs/en/concepts/datamodel/coordination-node?version=v26.1"
doc_path: "en/concepts/datamodel/coordination-node"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/datamodel/coordination-node.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/datamodel/coordination-node.md"
description: "A coordination node is an object in YDB that allows client applications to coordinate their actions in a distributed manner. Typical use cases for coordination"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Coordination Node

A coordination node is an object in YDB that allows client applications to coordinate their actions in a distributed manner. Typical use cases for coordination nodes include:

- Distributed [semaphores](<https://en.wikipedia.org/wiki/Semaphore_(programming)>) and [mutexes](https://en.wikipedia.org/wiki/Mutual_exclusion).
- Service discovery.
- Leader election.
- Task queues.
- Publishing small amounts of data with the ability to receive change notifications.
- Ephemeral locking of arbitrary entities not known in advance.

## Semaphores {#semaphore}

Coordination nodes allow you to create and manage semaphores within them. Typical operations with semaphores include:

- Create.
- Acquire.
- Release.
- Describe.
- Subscribe.
- Delete.

A semaphore can have a counter that limits the number of simultaneous acquisitions, as well as a small amount of arbitrary data attached to it.

YDB supports two types of semaphores: persistent and ephemeral. A persistent semaphore must be created before acquisition and will exist either until it is explicitly deleted or until the coordination node in which it was created is deleted. Ephemeral semaphores are automatically created at the moment of their first acquisition and deleted at the last release, which is convenient to use, for example, in distributed locking scenarios.

> [!NOTE]
> Semaphores in YDB are **not** recursive. Thus, semaphore acquisition and release are idempotent operations.

## Usage

Working with coordination nodes and semaphores is done through [dedicated methods in YDB SDK](../../reference/ydb-sdk/coordination.md).

## Similar Systems

YDB coordination nodes can solve tasks that are traditionally performed using systems such as [Apache Zookeeper](https://zookeeper.apache.org/), [etcd](https://etcd.io/), [Consul](https://www.consul.io/), and others. If a project uses YDB for data storage along with one of these third-party systems for coordination, switching to YDB coordination nodes can reduce the number of systems that need to be operated and maintained.
