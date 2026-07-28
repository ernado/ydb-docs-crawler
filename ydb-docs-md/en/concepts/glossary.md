---
title: "YDB glossary"
url: "https://ydb.tech/docs/en/concepts/glossary?version=v26.1"
doc_path: "en/concepts/glossary"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/glossary.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/glossary.md"
description: "This article is an overview of terms and definitions used in YDB and its documentation. It starts with key terms that will be useful to get acquainted with earl"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# YDB glossary

This article is an overview of terms and definitions used in YDB and its documentation. It [starts with key terms](glossary.md#key-terminology) that will be useful to get acquainted with early when you start working with YDB, while the rest of it is more [advanced](glossary.md#advanced-terminology) and might be helpful later on.

## Key terminology

This section explains terms that are useful to any person working with YDB regardless of their role and use case.

### Cluster

A YDB **cluster** is a set of interconnected YDB [nodes](glossary.md#node) that communicate with each other to serve user queries and reliably store user data. These nodes form one of the supported [cluster topologies](glossary.md#topology), which directly affects the cluster's reliability and performance characteristics.

YDB clusters are multitenant and can contain multiple isolated [databases](glossary.md#database).

### Database

Like in most database management systems, a **database** in YDB is a logical container for other entities like [tables](glossary.md#table). However, in YDB, the namespace inside databases is hierarchical like in [virtual file systems](https://en.wikipedia.org/wiki/Virtual_file_system), and thus [folders](glossary.md#folder) allow for further organization of entities.

Another essential characteristic of YDB databases is that they typically have dedicated compute resources allocated to them. Hence, creating a database requires additional operations from [DevOps engineers](../devops/index.md).

### Node

A YDB **node** is a server process running an executable called `ydbd`. A physical server or virtual machine can run multiple YDB nodes, which is common. Thus, in the context of YDB, nodes are **not** synonymous with hosts.

Given YDB follows the approach of separated storage and compute layers, `ydbd` has multiple operation modes that determine the node type. The available node types are explained below.

#### Database node

**Database nodes** (also known as **tenant nodes** or **compute nodes**) serve user queries addressed to a specific logical [database](glossary.md#database). Their state is only in memory and can be recovered from the [Distributed Storage](glossary.md#distributed-storage). All database nodes of a given [YDB cluster](topology.md) can be considered its compute layer. Thus, adding database nodes and allocating extra CPU and RAM to them are the main ways to increase the database's compute resources.

The main role of database nodes is to run various [tablets](glossary.md#tablet) and [actors](glossary.md#actor), as well as accept incoming requests via various endpoints.

#### Storage node

**Storage nodes** are stateful and responsible for long-term persisting pieces of data. All storage nodes of a given [YDB cluster](glossary.md#cluster) are called [Distributed Storage](glossary.md#distributed-storage) and can be considered the cluster's storage layer. Thus, adding extra storage nodes and their disks are the main ways to increase the cluster's storage capacity and input/output throughput.

#### Hybrid node {#hybrid-mode}

A **hybrid node** is a process that simultaneously serves both roles of a [database](glossary.md#database-node) and [storage](glossary.md#storage-node) node. Hybrid nodes are often used for development purposes. For instance, you can run a container with a full-featured YDB containing only one process, `ydbd`, in hybrid mode. They are rarely used in production environments.

#### Static node

**Static nodes** are manually configured during the initial cluster initialization or re-configuration. Typically, they play the role of [storage nodes](glossary.md#storage-node), but technically, it is possible to configure them to be [database nodes](glossary.md#database-node) as well.

#### Dynamic node

**Dynamic nodes** are added and removed from the cluster on the fly. They can only play the role of [database nodes](glossary.md#database-node).

### Distributed storage

**Distributed storage**, **Blob storage**, or **BlobStorage** is a distributed fault-tolerant data persistence layer of YDB. It has a specialized API designed for storing immutable pieces of [tablet's](glossary.md#tablet) data.

Multiple terms related to the [distributed storage implementation](glossary.md#distributed-storage-implementation) are covered below.

### Storage group

A **storage group**, **Distributed storage group**, or **Blob storage group** is a location for reliable data storage similar to [RAID](https://en.wikipedia.org/wiki/RAID), but using disks of multiple servers. Depending on the chosen [cluster topology](glossary.md#topology), storage groups use different algorithms to ensure high availability, similar to [standard RAID levels](https://en.wikipedia.org/wiki/Standard_RAID_levels).

[Distributed storage](glossary.md#distributed-storage) typically manages a large number of relatively small storage groups. Each group can be assigned to a specific [database](glossary.md#database) to increase disk capacity and input/output throughput available to this database.

#### Static group

A **static group** is a special [storage group](glossary.md#storage-group) created during the initial cluster deployment. Its primary role is to store system [tablet's](glossary.md#tablet) data, which can be considered cluster-wide metadata.

A static group might require special attention during major maintenance, such as decommissioning an [availability zone](glossary.md#regions-az).

#### Dynamic group

Regular storage groups that are not [static](glossary.md#static-group) are called **dynamic groups**. They are called dynamic because they can be created and decommissioned on the fly during [cluster](glossary.md#cluster) operation.

### Storage pool

**Storage pool** is a collection of data storage devices with similar characteristics. Each storage pool is assigned a unique name within a YDB cluster. Technically, each storage pool consists of multiple [PDisks](glossary.md#pdisk). Each [storage group](glossary.md#storage-group) is created in a particular storage pool, which determines the performance characteristics of the storage group through the selection of appropriate storage devices. It is typical to have separate storage pools for NVMe, SSD, and HDD devices or particular models of those devices with different capacities and speeds.

### Actor

The [actor model](https://en.wikipedia.org/wiki/Actor_model) is one of the main approaches for concurrent programming, which is employed by YDB. In this model, **actors** are lightweight user-space processes that may have and modify their private state but can only affect each other indirectly through message passing. YDB has its own implementation of this model, which is covered [below](glossary.md#actor-implementation).

In YDB, actors with the reliably persisted state are called [tablets](glossary.md#tablet).

### Tablet

A **tablet** is one of YDB's primary building blocks and abstractions. It is an entity responsible for a relatively small segment of user or system data. Typically, a tablet manages up to single-digit gigabytes of data, but some kinds of tablets can handle more.

For example, a [row-oriented user table](glossary.md#row-oriented-table) is managed by one or more [DataShard](glossary.md#data-shard) tablets, with each tablet responsible for a continuous range of [primary keys](glossary.md#primary-key) and the corresponding data.

End users sending queries to a YDB cluster aren't expected to know much about tablets, their kinds, or how they work, but it might still be helpful, for example, for performance optimizations.

Technically, tablets are [actors](glossary.md#actor) with a persistent state reliably saved in [Distributed Storage](glossary.md#distributed-storage). This state allows the tablet to continue operating on a different [database node](glossary.md#database-node) if the previous one is down or overloaded.

[Tablet implementation details](glossary.md#tablet-implementation) and related terms, as well as [main tablet types](glossary.md#tablet-types), are covered below in the advanced section.

### Transactions

YDB implements **transactions** on two main levels:

- [Local database](glossary.md#local-database) and the rest of [tablet infrastructure](glossary.md#tablet-implementation) allow [tablets](glossary.md#tablet) to manipulate their state using **local transactions** with [serializable isolation level](https://en.wikipedia.org/wiki/Isolation_%28database_systems%29#Serializable). Technically, they aren't really local to a single node as such a state persists remotely in [Distributed Storage](glossary.md#distributed-storage).
- In the context of YDB, the term **distributed transactions** usually refers to transactions involving multiple tablets. For example, cross-table or even cross-row transactions are often distributed.
- **Single-shard** transactions span a single tablet and are faster to complete. For example, transactions between rows in the same table partition are often single-shard.

Together, these mechanisms allow YDB to provide [strict consistency](https://en.wikipedia.org/wiki/Consistency_model#Strict_consistency).

The implementation of distributed transactions is covered in a separate article [DataShard: distributed transactions](../contributor/datashard-distributed-txs.md), while below there's a list of several [related terms](glossary.md#deterministic-transactions).

### Implicit Transactions

An **implicit transaction** is the query execution mode used when the [transaction mode](transactions.md#modes) is not specified. YDB automatically determines the behavior for each statement — whether to wrap it in a transaction or execute it outside one. This mode is described in more detail in [Implicit Transactions](transactions.md#implicit).

### Interactive transactions {#interactive-transaction}

The term **interactive transactions** refers to transactions that are split into multiple queries and involve data processing by an application between these queries. For example:

1. Select some data.
2. Process the selected data in the application.
3. Update some data in the database.
4. Commit the transaction in a separate query.

### Sessions

Logical "connections" to the database that maintains the context needed to execute queries and manage transactions. They are explained in more detail in [Sessions](query_execution/index.md#sessions).

### Multi-version concurrency control {#mvcc}

[**Multi-version concurrency control**](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) or **MVCC** is a method YDB used to allow multiple concurrent transactions to access the database simultaneously without interfering with each other. It is described in more detail in a separate article [Multi-Version Concurrency Control (MVCC)](query_execution/mvcc.md).

### Streaming queries {#streaming-query}

A query type designed for [stream processing](https://en.wikipedia.org/wiki/Stream_processing) of unbounded data. Unlike regular queries, streaming queries have no execution time limit, restart automatically on failures, and periodically persist their state as [checkpoints](glossary.md#streaming-queries-checkpoints) for fault tolerance.

Streaming queries are described in more detail in [Streaming queries](streaming-query.md).

### Streaming query checkpoints {#streaming-queries-checkpoints}

Periodically persisted state of a [streaming query](glossary.md#streaming-query), required to automatically recover execution after failures in a distributed system. For more information about checkpoints, see [Checkpoints](../dev/streaming-query/checkpoints.md).

### Topology

YDB supports several [cluster](glossary.md#cluster) topologies, described in more detail in a separate article [YDB Cluster Topology](topology.md). A few related terms are explained below.

#### Availability zones and regions {#regions-az}

An **availability zone** is a data center or an isolated segment thereof with minimal physical distance between nodes and minimal risk of failure at the same time as other availability zones. Thus, availability zones are expected not to share any infrastructure like power, cooling, or external network connections.

A **region** is a large geographic area containing multiple availability zones. The distance between availability zones in the same region is expected to be around 500 km or less. YDB performs synchronous data writes to each availability zone in a region, ensuring reasonable latencies and uninterrupted performance if an availability zone fails.

#### Rack

A **rack** or **server rack** is a piece of equipment used to mount multiple servers in an organized manner. Servers in the same rack are more likely to become unavailable simultaneously due to rack-wide issues related to electricity, cooling, etc. Thus, YDB can consider information about which server is located in which rack when placing each piece of data in bare-metal environments.

#### Pile

A **pile** is a set of nodes that can fail or be disconnected simultaneously while other cluster parts (pile) remain operational. A pile can remain operational when other cluster nodes are disconnected. Pile are used in [bridge mode](glossary.md#bridge) to divide the cluster into several parts with synchronous replication between them. A pile can consist of nodes from one or more regions.

#### Bridge mode {#bridge}

**Bridge mode** is a special cluster topology in which data is stored with synchronous replication between multiple [pile](glossary.md#pile). Mode details are described in [Bridge mode](topology.md#bridge) and in [Bridge cluster operation mode](bridge.md).

### Table

A **table** is a structured piece of information arranged in rows and columns. Each row represents a single record or entry, while each column represents a specific attribute or field with a particular data type.

There are two main approaches to representing tabular data in RAM or on disk drives: [row-oriented (row-by-row)](glossary.md#row-oriented-table) and [column-oriented (column-by-column)](glossary.md#column-oriented-table). The chosen approach greatly impacts the performance characteristics of operations with this data, with the former more suitable for transaction workloads (OLTP) and the latter for analytical (OLAP). YDB supports both.

#### Row-oriented table

**Row-oriented tables** store data for all or most columns of a given row physically close to each other. They are explained in more detail in [Row-Oriented Tables](datamodel/table.md#row-oriented-tables).

#### Column-oriented table

**Column-oriented tables** or **columnar tables** store data for each column independently. They are optimized for building aggregates over a small number of columns but are less suitable for accessing particular rows, as rows need to be reconstructed from their cells on the fly. They are explained in more detail in [Column-Oriented Tables](datamodel/table.md#column-oriented-tables).

#### Primary key

A **primary key** is an ordered list of columns, the values of which uniquely identify rows. It is used to build the [table's primary index](glossary.md#primary-index). It is provided by the YDB user during [table creation](../yql/reference/syntax/create_table/index.md) and dramatically impacts the performance of workloads interacting with that table.

The guidelines on choosing primary keys are provided in [Choosing a primary key](../dev/primary-key/index.md).

#### Primary index

A **primary index** or **primary key index** is the main data structure used to locate rows in a table. It is built based on the chosen [primary key](glossary.md#primary-key) and determines the physical order of rows in a table; thus, each table can have only one primary index. The primary index is unique.

#### Secondary index

A **secondary index** is an additional data structure used to locate rows in a table, typically when it can't be done efficiently using the [primary index](glossary.md#primary-index). Unlike the primary index, secondary indexes are managed independently from the main table data. Thus, a table might have multiple secondary indexes for different use cases. YDB's capabilities in terms of secondary indexes are covered in a separate article [Secondary indexes](query_execution/secondary_indexes.md). Secondary indexes can be either unique or non-unique.

A special type of **secondary index** is singled out separately - [vector index](glossary.md#vector-index).

#### Vector Index

**Vector index** is an additional data structure used to speed up the [vector search](query_execution/vector_search.md) when there is a large amount of data, and the [exact vector search without an index](../yql/reference/udf/list/knn.md) does not perform satisfactorily.  
 The capabilities of YDB regarding **ANN search** (approximate nearest neighbor search) with vector indexes are described in a separate article [Vector Indexes](../dev/vector-indexes.md).

**Vector index** is distinct from a [secondary index](glossary.md#secondary-index) as it solves other tasks.

#### Column family

A **column family** or **column group** is a feature that allows storing a subset of [row-oriented table](glossary.md#row-oriented-table) columns separately in a distinct family or group. The primary use case is to store some columns on different kinds of disk drives (offload less important columns to HDD) or with various compression settings. If the workload requires many column families, consider using [column-oriented tables](glossary.md#column-oriented-table) instead.

#### Time to live {#ttl}

**Time to live** or **TTL** is a mechanism for automatically removing old rows from a table asynchronously in the background. It is explained in a separate article [Time to Live (TTL) and Eviction to External Storage](ttl.md).

### View

A **view** logically represents a table formed by a given query. The view itself contains no data. The content of a view is generated every time you SELECT from it. Thus, any changes in the underlying tables are reflected immediately in the view.

There are user-defined and system-defined views.

#### User-defined view {#user-view}

A **user-defined view** is created by a user with the [CREATE VIEW](../yql/reference/syntax/create-view.md) statement. For more information, see [View](datamodel/view.md).

#### System view

**System views** are special views automatically created by the system for monitoring the state of the database and cluster. They are located in a special directory `.sys` in the root folder of each database. System views for databases are described in [Database system views](../dev/system-views.md); system views for the cluster, as well as access control issues for them, are described in [Cluster System Views](../devops/observability/system-views.md).

### Topic

A **topic** is a persistent queue that can be used for reliable asynchronous communications between various systems via message passing. YDB provides the infrastructure to ensure "exactly once" semantics in such communications, which ensures that there are both no lost messages and no accidental duplicates.

Several terms related to topics are listed below. How YDB topics work is explained in more detail in a separate article [Topic](datamodel/topic.md).

#### Partition

For horizontal scaling purposes, topics are divided into separate elements called **partitions**. Thus, a partition is a unit of parallelism within a topic. Messages inside each partition are ordered.

However, subsets of data managed by a single [data shard](glossary.md#data-shard) or [column shards](glossary.md#column-shard) can also be called partitions.

#### Offset

An **offset** is a sequence number that identifies a message inside a [partition](glossary.md#partition).

#### Producer

A **producer** is an entity that writes new messages to a topic.

#### Consumer

A **consumer** is an entity that reads messages from a topic.

### Change data capture {#cdc}

**Change data capture** or **CDC** is a mechanism that allows subscribing to a **stream of changes** to a given [table](glossary.md#table). Technically, it is implemented on top of [topics](glossary.md#topic). It is described in more detail in a separate article [Change Data Capture (CDC)](cdc.md).

#### Changefeed

**Changefeed** or **stream of changes** is an ordered list of changes in a given [table](glossary.md#table) published via a [topic](glossary.md#topic).

### Backup collection

A **backup collection** is a [schema object](glossary.md#scheme-object) that organizes full and incremental [backups](glossary.md#backup) for selected [row-oriented tables](glossary.md#row-oriented-table). Collections enable recovery to any saved backup point in the chain by maintaining [backup chains](glossary.md#backup-chain) and ensuring consistent restoration across multiple tables. A table can only belong to one backup collection at a time.

For more information, see [Backup Collection](datamodel/backup-collection.md).

#### Backup

A **backup** is a copy of data at a specific point in time that can be used to restore the data. In the context of [backup collections](glossary.md#backup-collection), there are two types:

- **Full backup**: A complete snapshot of all data in the collection. Serves as the foundation for [backup chains](glossary.md#backup-chain) and can be restored independently.
- **Incremental backup**: Captures only changes (inserts, updates, deletes) since the previous backup. Requires the entire backup chain for restoration.

#### Backup chain

A **backup chain** is an ordered sequence of [backups](glossary.md#backup) starting with a full backup followed by zero or more incremental backups. Each incremental backup depends on all previous backups in the chain. Deleting any backup in the chain makes subsequent incremental backups unrestorable.

### Asynchronous replication instance {#async-replication-instance}

**Asynchronous replication instance** is a named entity that stores [asynchronous replication](async-replication.md) settings (connection properties, a list of replicated objects, etc.) It can also be used to retrieve the status of asynchronous replication, such as the [initial synchronization process](async-replication.md#initial-scan), [replication lag](async-replication.md#replication-of-changes), [errors](async-replication.md#error-handling), and more.

#### Replicated object

**Replicated object** is an object, for example, a table, that is asynchronously replicated to the target database.

#### Replica object

**Replica object** is a mirror copy of the replicated object, automatically created by an [asynchronous replication instance](glossary.md#async-replication-instance). Replica objects are typically read-only.

### Coordination node

A **coordination node** is a schema object that allows client applications to create semaphores for coordinating their actions. Learn more about [coordination nodes](datamodel/coordination-node.md).

#### Semaphore

A **semaphore** is an object within a [coordination node](glossary.md#coordination-node) that provides a synchronization mechanism for distributed applications. Semaphores can be persistent or ephemeral and support operations like creation, acquisition, release, and monitoring. Learn more about [semaphores in YDB](datamodel/coordination-node.md#semaphore).

### Resource pool

A **resource pool** is a schema object that describes the restrictions placed on the resources (CPU, RAM, etc.) available for executing queries in that pool. A query is always executed in some resource pool. By default, all queries run in a resource pool named `default`, which does not impose any restrictions. For more on using resource pools, see [Workload Manager — resource consumption management](../dev/resource-consumption-management.md).

### Resource pool classifier

A **resource pool classifier** is an object used to control how queries are distributed across [resource pools](glossary.md#resource-pool). It defines the rules by which a resource pool is chosen for each query. These classifiers are global to the entire [database](glossary.md#database) and apply to all queries submitted to it. For more on how they are used, see [Workload Manager — resource consumption management](../dev/resource-consumption-management.md).

### YQL

**YQL (YDB Query Language)** is a high-level language for working with the system. It is a dialect of [ANSI SQL](https://en.wikipedia.org/wiki/SQL). There's a lot of content covering YQL, including a [tutorial](../dev/yql-tutorial/index.md), [reference](../yql/reference/syntax/index.md), and [recipes](../yql/reference/recipes/index.md).

### Federated queries

**Federated queries** is a feature that allows querying data stored in systems external to the YDB cluster.

A few terms related to federated queries are listed below. How YDB federated queries work is explained in more detail in a separate article [Federated query](query_execution/federated_query/index.md).

#### External data source

An **external data source** or **external connection** is a piece of metadata that describes how to connect to a supported external system for [federated query execution](glossary.md#federated-queries).

#### External table

An **external table** is a piece of metadata that describes a particular dataset that can be retrieved from an [external data source](glossary.md#external-data-source).

#### Secret

A **secret** is a sensitive piece of metadata that requires special handling. For example, secrets can be used in [external data source](glossary.md#external-data-source) definitions and represent things like passwords and tokens.

### Authentication token {#auth-token}

An **authentication token** or **auth token** is a token that YDB uses for [authentication](../security/authentication.md).

YDB supports various [authentication modes](../security/authentication.md) and token types.

### Cluster scheme {#scheme}

A **YDB cluster scheme** is a hierarchical namespace of a YDB cluster. The top-level element of the namespace is the [cluster scheme root](glossary.md#scheme-root) that contains [databases](glossary.md#database) as its children. Scheme objects inside databases can use nested directories to form a hierarchy.

### Database scheme {#scheme-database}

A **database scheme** is a subset of the hierarchical namespace of a YDB cluster that belongs to a database.

### Database root {#scheme-database-root}

A **database root** is a path to a database in a YDB cluster scheme.

### Scheme root

A **scheme root** is a root element of a [YDB cluster scheme](datamodel/index.md#cluster-scheme). Children elements of the cluster scheme root can be [databases](glossary.md#database) or other [scheme objects](glossary.md#scheme-object).

### Scheme object

A database schema consists of **scheme objects**, which can be databases, [tables](glossary.md#table) (including [external tables](glossary.md#external-table)), [topics](glossary.md#topic), [folders](glossary.md#folder), and so on.

For organizational convenience, scheme objects form a hierarchy using [folders](glossary.md#folder).

### Folder

As in file systems, a **folder** or **directory** is a container for [scheme objects](glossary.md#scheme-object).

Folders can contain subfolders, and this nesting can have arbitrary depth.

### Access object

An **access object** in the context of [authorization](../security/authorization.md) is an entity for which access rights and restrictions are configured. In YDB, access objects are [scheme objects](glossary.md#scheme-object).  
 Each access object has an [owner](glossary.md#access-owner) and an [access control list](glossary.md#access-control-list).

### Access subject

An **access subject** is an entity that can interact with [access objects](glossary.md#access-object) or perform specific actions within the system. Access to these interactions and actions depends on configured [access control lists](glossary.md#access-control-list).

An access subject can be a [user](glossary.md#access-user) or a [group](glossary.md#access-group).

### Access right

An **[access right](../security/authorization.md#right)** is an entity that represents permission for an [access subject](glossary.md#access-subject) to perform a specific set of operations in a cluster or database on a specific [access object](glossary.md#access-object).

### Access right inheritance

**Access rights inheritance** is a mechanism by which [access rights](glossary.md#access-right) granted on parent [access objects](glossary.md#access-object) are inherited by child objects in the hierarchical structure of the database. This ensures that permissions granted at a higher level in the hierarchy are applied to all sublevels beneath it, unless [explicitly overridden](../reference/ydb-cli/commands/scheme-permissions.md#clear-inheritance).

### Access control list

An **access control list** or **ACL** is a list of all [rights](glossary.md#access-right) granted to [access subjects](glossary.md#access-subject) (users and groups) for a specific [access object](glossary.md#access-object).

### Access level

An **access level** determines additional privileges of an [access subject](glossary.md#access-subject) for [scheme objects](glossary.md#scheme-object) as well as privileges that are not related to [scheme objects](glossary.md#scheme-object).

YDB uses three access levels:

- viewer
- operator
- administrator

An access level is granted by adding an access subject to an [access level list](glossary.md#access-level-list).

### Access level list

An **access level list** is a list of [SIDs](glossary.md#access-sid) that grants a certain [access level](glossary.md#access-level) to the associated [access subjects](glossary.md#access-subject).

YDB provides several [access level lists](../reference/configuration/security_config.md#security-access-levels) that collectively determine [access levels](glossary.md#access-level) in the system.

### Owner {#access-owner}

An **[owner](../security/authorization.md#owner)** is an [access subject](glossary.md#access-subject) ([user](glossary.md#access-user) or [group](glossary.md#access-group)) having full rights over a specific [access object](glossary.md#access-object).

### User {#access-user}

A **[user](../security/authorization.md#user)** is an individual utilizing YDB to perform a specific function.

YDB has the following types of users depending on their source:

- local users in YDB databases
- external users from third-party directory services

YDB users are identified by their [SIDs](glossary.md#access-sid).

#### Local user

A **local user** is an individual whose YDB account is created directly in YDB using the `CREATE USER` command or during the [initial security configuration](../security/builtin-security.md).

#### External user

An **external user** is an individual whose YDB account is created in a third-party directory service, for example, in LDAP or IAM.

### Group {#access-group}

A **[group](../security/authorization.md#group)** or **access group** is a named collection of [users](glossary.md#access-user) with identical [access rights](glossary.md#access-right) to certain [access objects](glossary.md#access-object).

### Role {#access-role}

A **role** is a named collection of [access rights](glossary.md#access-right) that can be granted to [users](glossary.md#access-user) or [groups](glossary.md#access-group).

Roles in YDB are implemented as [groups](glossary.md#access-group) that are created during the initial cluster deployment and granted a set of [access rights](glossary.md#access-right) on the root of the cluster scheme.

### SID {#access-sid}

**SID** (**Security Identifier**) is a string in the format `<login>[@<subsystem>]`, identifying an [access subject](glossary.md#access-subject) in [access control lists](glossary.md#access-control-list).

### Query optimizer {#optimizer}

[**Query optimizer**](https://en.wikipedia.org/wiki/Query_optimization) is a YDB component that takes a logical plan as input and produces the most efficient physical plan with the lowest estimated resource consumption among the alternatives. The YDB query optimizer is described in the [Query Optimization in YDB](query_execution/optimizer.md) section.

## Advanced terminology

This section explains terms that are useful to [YDB contributors](../contributor/index.md) and users who want to get a deeper understanding of what's going on inside the system.

### Actors implementation {#actor-implementation}

#### Actor system

An **actor system** is a C++ library with YDB's [implementation](https://github.com/ydb-platform/ydb/tree/main/ydb/library/actors) of the [Actor model](https://en.wikipedia.org/wiki/Actor_model).

#### Actor service

An **actor service** is an [actor](glossary.md#actor) that has a well-known name and is usually run in a single instance on a [node](glossary.md#node).

#### ActorId

An **ActorId** is a unique identifier of the actor or [tablet](glossary.md#tablet) in the [cluster](glossary.md#cluster).

#### Actor system interconnect

The **actor system interconnect** or **interconnect** is the [cluster's](glossary.md#cluster) internal network layer. All [actors](glossary.md#actor) interact with each other within the system via the interconnect.

#### Local

A **Local** is an [actor service](glossary.md#actor-service) running on each [node](glossary.md#node). It directly manages the [tablets](glossary.md#tablet) on its node and interacts with [Hive](glossary.md#hive). It registers with Hive and receives commands to launch tablets.

#### Actor system pool

The **actor system pool** is a [thread pool](https://en.wikipedia.org/wiki/Thread_pool) used to run [actors](glossary.md#actor). Each [node](glossary.md#node) operates multiple pools to coarsely separate resources between different types of activities. A typical set of pools includes:

- **System**: A pool that handles internal operations within YDB node. It serves system [tablets](glossary.md#tablet), [state storage](glossary.md#state-storage), [distributed storage](glossary.md#distributed-storage) I/O, and so on.
- **User**: A pool dedicated to user-generated load, such as running non-system tablets or queries executed by the [QP](glossary.md#kqp).
- **Batch**: A pool for tasks without strict execution deadlines, including heavy queries handled by the [QP](glossary.md#kqp) background operations like backups, data compaction, and garbage collection.
- **IO**: A pool for tasks involving blocking operations, such as authentication or writing logs to files.
- **IC**: A pool for [interconnect](glossary.md#actor-system-interconnect), responsible for system calls related to data transfers across the network, data serialization, message splitting and merging.

### Tablet implementation

A [**tablet**](glossary.md#tablet) is an [actor](glossary.md#actor) with a persistent state. It includes a set of data for which this tablet is responsible and a finite state machine through which the tablet's data (or state) changes. The tablet is a fault-tolerant entity because tablet data is stored in a [Distributed storage](glossary.md#distributed-storage) that survives disk and node failures. The tablet is automatically restarted on another [node](glossary.md#node) if the previous one is down or overloaded. The data in the tablet changes in a consistent manner because the system infrastructure ensures that there is no more than one [tablet leader](glossary.md#tablet-leader) through which changes to the tablet data are carried out.

The tablet solves the same problem as the [Paxos](<https://en.wikipedia.org/wiki/Paxos_(computer_science)>) and [Raft](<https://en.wikipedia.org/wiki/Raft_(algorithm)>) algorithms in other systems, namely the [distributed consensus](<https://en.wikipedia.org/wiki/Consensus_(computer_science)>) task. From a technical point of view, the tablet implementation can be described as a Replicated State Machine (RSM) over a shared log, as the tablet state is completely described by an ordered command log stored in a distributed and fault-tolerant storage.

During execution, the tablet state machine is managed by three components:

1. The generic tabular part ensures the log's consistency and recovery in case of failures.
2. **Executor** is an abstraction of a local database, namely data structures and code that arrange work with the data stored by the tablet.
3. An [actor](glossary.md#actor) with a custom code that implements the specific logic of a specific tablet type.

In YDB, there are multiple kinds of specialized tablets storing all kinds of data for all sorts of tasks. Many YDB features like [tables](glossary.md#table) and [topics](glossary.md#topic) are implemented as specific tablets. Thus, reusing tablet infrastructure is one of the key means of YDB extensibility as a platform.

Usually, there are orders of magnitude more tablets running in a YDB cluster compared to processes or threads that other systems would use for a similarly sized cluster. There can easily be hundreds of thousands to millions of tablets working simultaneously in a YDB cluster.

Since the tablet stores its state in [Distributed storage](glossary.md#distributed-storage), it can be (re)started on any node of the cluster. Tablets are identified using [TabletID](glossary.md#tabletid), a 64-bit number assigned when creating a tablet.

### Tablet leader

A **tablet leader** is the current active leader of a given tablet. The tablet leader accepts commands, assigns them an order, and confirms them to the outside world. It is guaranteed that there is no more than one leader for a given tablet at any moment.

### Tablet candidate

A **tablet candidate** is one of the election participants who wants to become a [leader](glossary.md#tablet-leader) for a given tablet. If a candidate wins the election, it assumes the tablet leader role.

### Tablet follower

A **tablet follower** or **hot standby** is a copy of a [tablet leader](glossary.md#tablet-leader) that applies the log of commands accepted by the leader (with some lag). A tablet can have zero or more followers. Followers serve two primary purposes:

- In case of the leader's termination or failure, followers are the preferred [candidates](glossary.md#tablet-candidate) to become the new leader because they can become the leader much faster than other candidates since they have applied most of the log.
- Followers can respond to read-only queries if a client explicitly chooses the optional relaxed transaction mode that allows for stale reads.

### Tablet generation

A **tablet generation** is a number identifying the reincarnation of the tablet leader. It changes only when a new leader is chosen and always grows.

### Tablet local database {#local-database}

A **tablet local database** or **local database** is a set of data structures and related code that manages the tablet's state and the data it stores. Logically, the local database state is represented by a set of tables very similar to relational tables. Modification of the state of the local database is performed by local tablet transactions generated by the tablet's user actor.

Each local database table is stored using the [LSM tree](glossary.md#lsm-tree) data structure.

#### Log-structured merge-tree {#lsm-tree}

A **[log-structured merge-tree](https://en.wikipedia.org/wiki/Log-structured_merge-tree)** or **LSM tree**, is a data structure designed to optimize write and read performance in storage systems. It is used in YDB for storing [local database](glossary.md#local-database) tables and [VDisks](glossary.md#vdisk) data.

#### MemTable

All data written to a [local database](glossary.md#local-database) tables is initially stored in an in-memory data structure called a **MemTable**. When the MemTable reaches a predefined size, it is flushed to disk as an immutable [SST](glossary.md#sst).

#### Sorted string table {#sst}

A **sorted string table** or **SST** is an immutable data structure that stores table rows sorted by key, facilitating efficient key lookups and range queries. Each SST is composed of a contiguous series of small data pages, typically around 7 KiB in size each, which further optimizes the process of reading data from disk. An SST typically represents a part of [LSM tree](glossary.md#lsm-tree).

#### Tablet pipe

A **Tablet pipe** or **TabletPipe** is a virtual connection that can be established with a tablet. It includes resolving the [tablet leader](glossary.md#tablet-leader) by [TabletID](glossary.md#tabletid). It is the recommended way to work with the tablet. The term **open a pipe to a tablet** describes the process of resolving (searching) a tablet in a cluster and establishing a virtual communication channel with it.

#### TabletID

A **TabletID** is a cluster-wide unique [tablet](glossary.md#tablet) identifier.

#### Bootstrapper

The **bootstrapper** is the primary mechanism for launching tablets, used for service tablets (for example, for [Hive](glossary.md#hive), [DS controller](glossary.md#ds-controller), root [SchemeShard](glossary.md#scheme-shard)). The [Hive](glossary.md#hive) tablet initializes the rest of the tablets.

### Shared cache

A **shared cache** is an [actor](glossary.md#actor) that stores data pages recently accessed and read from [distributed storage](glossary.md#distributed-storage). Caching these pages reduces disk I/O operations and accelerates data retrieval, enhancing overall system performance.

### Memory controller

A **memory controller** is an [actor](glossary.md#actor) that manages YDB [memory limits](../reference/configuration/memory_controller_config.md).

### Spilling

**Spilling** is a memory management mechanism in YDB that temporarily offloads intermediate query data to external storage when such data exceeds the available node RAM capacity. In YDB, disk storage is currently used for spilling.

For more details on spilling, see [Spilling](query_execution/spilling.md).

### Tablet types

[Tablets](glossary.md#tablet) can be considered a framework for building reliable components operating in a distributed system. YDB has multiple components implemented using this framework, listed below.

#### Scheme shard

A **Scheme shard** or **SchemeShard** is a tablet that stores a database schema, including metadata of user [tables](glossary.md#table), [topics](glossary.md#topic), etc.

Additionally, there is a **root scheme shard**, which stores information about databases created in a cluster.

#### Data shard

A **data shard** or **DataShard** is a tablet that manages a segment of a [row-oriented user table](datamodel/table.md#row-oriented-tables). The logical user table is divided into segments by continuous ranges of the primary key of the table. Each such range is managed by a separate DataShard tablet instance. Such ranges are also called [partitions](glossary.md#partition). DataShard tablets store data row by row, which is efficient for OLTP workloads.

#### Column shard

A **column shard** or **ColumnShard** is a tablet that stores a data segment of a [column-oriented user table](datamodel/table.md#column-oriented-tables).

#### KV Tablet

A **KV Tablet** or **key-value tablet** is a tablet that implements a simple key->value mapping, where keys and values are strings. It also has a number of specific features, like locks.

#### PQ Tablet

A **PQ Tablet** or **persistent queue tablet** is a tablet that implements the concept of a [topic](glossary.md#topic). Each topic consists of one or more partitions, and each partition is managed by a separate PQ tablet instance.

#### TxAllocator

A **TxAllocator** or **transaction allocator** is a system tablet that allocates unique transaction identifiers ([TxID](glossary.md#txid)) within the cluster. Typically, a cluster has several such tablets, from which [transaction proxy](glossary.md#transaction-proxy) pre-allocates and caches ranges for local issuance within a single process.

#### Coordinator

The **Coordinator** is a system tablet that ensures the global ordering of transactions. The coordinator's task is to assign a logical [PlanStep](glossary.md#planstep) time to each transaction planned through this coordinator. Each transaction is assigned exactly one coordinator, chosen by hashing its [TxId](glossary.md#txid).

#### Mediator

The **Mediator** is a system tablet that distributes the transactions planned by [coordinators](glossary.md#coordinator) to the transaction participants (usually, [DataShards](glossary.md#data-shard)). Mediators ensure the advancement of global time. Each transaction participant is associated with exactly one mediator. Mediators allow to avoid the need for a full mesh of connections between all coordinators and all participants in all transactions.

#### Hive

A **Hive** is a system tablet responsible for launching and managing other tablets. It also moves tablets between nodes in case of [node](glossary.md#node) failures or overload. You can learn more about Hive in a [dedicated article](../contributor/hive.md).

#### Cluster management system {#cms}

The **cluster management system** or **CMS** is a system tablet responsible for managing the information about the current [YDB cluster](glossary.md#cluster) state. This information is used to perform cluster rolling restarts without affecting user workloads, maintenance, cluster re-configuration, etc.

#### Node Broker

The **Node Broker** is a system tablet that registers [dynamic nodes](glossary.md#dynamic-node) in the cluster.

### Slot

A **slot** in YDB can be used in two contexts:

- **Slot** is a portion of a server's resources allocated to running a single YDB [node](glossary.md#node). A common slot size is 10 CPU cores and 50 GB of RAM. Slots are used if a YDB cluster is deployed on servers or virtual machines with sufficient resources to host multiple slots.
- [VDisk](glossary.md#slot) **slot** or **VSlot** is a fraction of [PDisk](glossary.md#pdisk) that can be allocated to one of the [VDisks](glossary.md#vdisk).

### State storage

A **State storage** or **StateStorage** is a distributed service that stores information about tablets, namely:

- The current leader of the tablet or its absence.
- Tablet followers.
- Generation and step of the tablet `(generation:step)`.

State storage is used as a name service for resolving tablets, i.e., getting [ActorId](glossary.md#actorid) by [TabletID](glossary.md#tabletid). StateStorage is also used in the process of electing the [tablet leader](glossary.md#tablet-leader).

Information in state storage is volatile. Thus, it is lost when the power is turned off, or the process is restarted. Despite the name, this service is not persistent storage. It contains only information that is easily recoverable and does not have to be durable. However, state storage keeps information on several nodes to minimize the impact of node failures. Through this service, it is possible to gather a quorum, which is used to elect tablet leaders.

Due to its nature, the state storage service operates in a best-effort manner. For example, the absence of several tablet leaders is guaranteed through the leader election protocol on [distributed storage](glossary.md#distributed-storage), not state storage.

### Board

**Board** is a distributed service for storing metadata as key-value pairs. It is used, among other things, to store information about [endpoints](connect.md#endpoint).

### Scheme board

**SchemeBoard** is a distributed service for storing metadata as key-value pairs. It is used, among other things, to store information about [schemes](glossary.md#global-schema).

#### Compaction

**Compaction** is the internal background process of rebuilding [LSM tree](glossary.md#lsm-tree) data. The data in [VDisks](glossary.md#vdisk) and [local databases](glossary.md#local-database) are organized in the form of an LSM tree. Therefore, there is a distinction between **VDisk compaction** and **Tablet compaction**. The compaction process is usually quite resource-intensive, so efforts are made to minimize the overhead associated with it, for example, by limiting the number of concurrent compactions.

#### gRPC proxy

A **gRPC Proxy** is the client proxy system for external user requests. Client requests enter the system via the [gRPC](https://grpc.io) protocol, then the proxy component translates them into internal calls for executing these requests, passed around via [Interconnect](glossary.md#actor-system-interconnect). This proxy provides an interface for both request-response and bidirectional streaming.

### Distributed configuration

**Distributed configuration** or **DistConf** is an internal cluster [configuration](../devops/configuration-management/configuration-v2/config-overview.md) mechanism that handles startup and configuration of [static nodes](glossary.md#static-node), automatic management of [static storage groups](glossary.md#static-group), and [State storage](glossary.md#state-storage). Distributed configuration starts before any [tablets](glossary.md#tablet), [storage groups](glossary.md#storage-group), or [State storage](glossary.md#state-storage).

For more on how distributed configuration works, see [Internals of the V2 configuration mechanism](../contributor/configuration-v2.md).

### Distributed storage implementation

**Distributed storage** is a distributed fault-tolerant data storage layer that persists binary records called [LogoBlob](glossary.md#logoblob), addressed by a particular type of identifier called [LogoBlobID](glossary.md#logoblobid). Thus, distributed storage is a key-value store that maps LogoBlobID to a string up to 10MB in size. Distributed storage consists of many [storage groups](glossary.md#storage-group), each being an independent data repository.

Distributed storage persists immutable data, with each immutable blob identified by a specific `LogoBlobID` key. The distributed storage API is very specific, designed only for use by [tablets](glossary.md#tablet) to store their data and log changes, not for general-purpose data storage. Data in distributed storage is deleted using special barrier commands. Due to the lack of mutations in its interface, distributed storage can be implemented without implementing [distributed consensus](<https://en.wikipedia.org/wiki/Consensus_(computer_science)>). Moreover, distributed storage is just a building block tablets use to implement distributed consensus.

#### LogoBlob

A **LogoBlob** is a piece of binary immutable data identified by [LogoBlobID](glossary.md#logoblobid) and stored in [Distributed storage](glossary.md#distributed-storage). The blob size is limited at the [VDisk](glossary.md#vdisk) level and higher on the stack. Currently, the maximum blob size VDisks are ready to process is 10 MB.

#### LogoBlobID

A **LogoBlobID** is the [LogoBlob](glossary.md#logoblob) identifier in the [Distributed storage](glossary.md#distributed-storage). It has a structure of the form `[TabletID, Generation, Step, Channel, Cookie, BlobSize, PartID]`. The key elements of LogoBlobID are:

- `TabletID` is an [ID](glossary.md#tabletid) of the tablet that the LogoBlob belongs to.
- `Generation` is the generation of the tablet in which the blob was recorded.
- `Channel` is the tablet [channel](glossary.md#channel) where the LogoBlob is recorded.
- `Step` is an incremental counter, usually within the tablet generation.
- `Cookie` is a unique blob identifier within a single `Step`. A cookie is usually used when writing several blobs within a single `Step`.
- `BlobSize` is the LogoBlob size.
- `PartID` is the identifier of the blob part. It is crucial when the original LogoBlob is broken into parts using [erasure coding](glossary.md#erasure-coding), and the parts are written to the corresponding [VDisks](glossary.md#vdisk) and [storage groups](glossary.md#storage-group).

#### Replication

**Replication** is a process that ensures there are always enough copies (replicas) of data to maintain the desired availability characteristics of a YDB cluster. Typically, it is used in geo-distributed YDB clusters.

#### Erasure Coding

[**Erasure coding**](https://en.wikipedia.org/wiki/Erasure_code) is a method of data encoding in which the original data is supplemented with redundancy and divided into several fragments, providing the ability to restore the original data if one or more fragments are lost. It is widely used in [single-AZ](glossary.md#regions-az) YDB clusters as opposed to [replication](glossary.md#replication) with 3 replicas. For example, the most popular 4+2 scheme provides the same reliability as three replicas, with space redundancy of 1.5 versus 3.

#### PDisk

**PDisk** or **Physical disk** is a component that controls a physical disk drive (block device). In other words, PDisk is a subsystem that implements an abstraction similar to a specialized file system on top of block devices (or files simulating a block device for testing purposes). PDisk provides data integrity controls (including [erasure encoding](glossary.md#erasure-coding) of sector groups for data recovery on single bad sectors, integrity control with checksums), transparent data-at-rest encryption of all disk data, and transactional guarantees of disk operations (write confirmation strictly after `fsync`).

PDisk contains a scheduler that provides device bandwidth sharing between several clients ([VDisks](glossary.md#vdisk)). PDisk divides a block device into chunks called [slots](glossary.md#slot) (about 128 megabytes in size; smaller chunks are allowed). No more than 1 VDisk can own each slot at a time. PDisk also supports a recovery log shared between PDisk service records and all VDisks.

#### VDisk

**VDisk** or **Virtual disk** is a component that implements the persistence of [distributed storage](glossary.md#distributed-storage) [LogoBlobs](glossary.md#logoblob) on [PDisks](glossary.md#pdisk). VDisk stores all its data on PDisks. One VDisk corresponds to one PDisk, but usually, several VDisks are linked to one PDisk. Unlike PDisk, which hides chunks and logs behind it, VDisk provides an interface at the LogoBlob and [LogoBlobID](glossary.md#logoblobid) level, like writing LogoBlob, reading LogoBlobID data, and deleting a set of LogoBlob using a special command. VDisk is a member of a [storage group](glossary.md#storage-group). VDisk itself is local, but many VDisks in a given group provide reliable data storage. The VDisks in a group synchronize the data with each other and replicate the data in case of loss. A set of VDisks in a storage group forms a distributed RAID.

#### Yard

**Yard** is the name of the [PDisk](glossary.md#pdisk) API. It allows [VDisk](glossary.md#vdisk) to read and write data to chunks and logs, reserve chunks, delete chunks, and transactionally receive and return ownership of chunks. In some contexts, Yard can be considered to be a synonym for PDisk.

#### Skeleton

A **Skeleton** is an [actor](glossary.md#actor) that provides an interface to a [VDisk](glossary.md#vdisk).

#### SkeletonFront

**SkeletonFront** is a proxy actor for Skeleton that controls the flow of messages coming to Skeleton.

#### Distributed storage controller {#ds-controller}

The **distributed storage controller** or **DS controller** manages the dynamic configuration of distributed storage, including information about [PDisks](glossary.md#pdisk), [VDisks](glossary.md#vdisk), and [storage groups](glossary.md#storage-group). It interacts with [node wardens](glossary.md#node-warden) to launch various distributed storage components. It interacts with [Hive](glossary.md#hive) to allocate [channels](glossary.md#channel) to [tablets](glossary.md#tablet).

#### Proxy {#ds-proxy}

The **distributed storage proxy**, **DS proxy**, or **BS proxy** plays the role of a client library for performing operations with [Distributed storage](glossary.md#distributed-storage). DS Proxy users are [tablets](glossary.md#tablet) that write to and read from Distributed storage. DS Proxy hides the distributed nature of Distributed storage from the user. The task of DS Proxy is to write to the quorum of the [VDisks](glossary.md#vdisk), make retries if necessary, and control the write/read flow to avoid overloading VDisks.

Technically, DS Proxy is implemented as an [actor service](glossary.md#actor-service) launched by the [node warden](glossary.md#node-warden) on each node for each storage group, processing all requests to the group (writing, reading, and deleting [LogoBlobs](glossary.md#logoblob), blocking the group). When writing data, DS proxy performs [erasure encoding](glossary.md#erasure-coding) of data by dividing LogoBlobs into parts, which are then sent to the corresponding VDisks. DS Proxy performs the reverse process when reading, receiving parts from VDisks, and restoring LogoBlobs from them.

#### Node warden

**Node warden** or `BS_NODE` is an [actor service](glossary.md#actor-service) on each node of the cluster, launching [PDisks](glossary.md#pdisk), [VDisks](glossary.md#vdisk), and [DS proxies](glossary.md#ds-proxy) of [static storage groups](glossary.md#static-group) at the node start. Also, it interacts with the [DS controller](glossary.md#ds-controller) to launch PDisk, VDisk, and DS proxies of [dynamic groups](glossary.md#dynamic-group). The DS proxy of dynamic groups is launched on request: node warden processes "undelivered" messages to the DS proxy, launching the corresponding DS proxies and receiving the group configuration from the DS controller.

#### Fail realm

A **fail realm** is a set of [fail domains](glossary.md#fail-domain) that are likely to fail simultaneously. The correlated failure of two [VDisks](glossary.md#vdisk) within the same fail realm is more probable than that of two VDisks from different fail realms.

An example of a fail realm is a set of hardware located in the same [data center or availability zone](glossary.md#regions-az) that can all fail together due to a natural disaster, major power outage, or similar event.

#### Fail domain

A **fail domain** is a set of hardware that may fail simultaneously. The correlated failure of two [VDisks](glossary.md#vdisk) within the same fail domain is more probable than the failure of two VDisks from different fail domains. In the case of different fail domains, this probability is also affected by whether these domains belong to the same [fail realm](glossary.md#fail-realm) or not.

For example, a fail domain includes disks on the same server, as all server disks may become unavailable if the server's PSU or network controller fails. A fail domain also typically includes servers located in the same server rack, as all the hardware in the rack may become unavailable if there is a power outage or an issue with the network hardware in the same rack. Thus, the typical fail domain corresponds to a server rack if the [cluster](glossary.md#cluster) is configured to be rack-aware, or to a server otherwise.

Domain failures are handled automatically by YDB without shutting down the cluster.

#### Distributed storage channel {#channel}

A **channel** is a logical connection between a [tablet](glossary.md#tablet) and [Distributed storage](glossary.md#distributed-storage) group. The tablet can write data to different channels, and each channel is mapped to a specific [storage group](glossary.md#storage-group). Having multiple channels allows the tablet to:

- Record more data than one storage group can contain.
- Store different [LogoBlobs](glossary.md#logoblob) on different storage groups, with different properties like erasure encoding or on different storage media (HDD, SSD, NVMe).

### Distributed transactions implementation {#distributed-transaction-implementation}

Terms related to the implementation of [distributed transactions](glossary.md#transactions) are explained below. The implementation itself is described in a separate article [DataShard: distributed transactions](../contributor/datashard-distributed-txs.md).

#### Deterministic transactions

YDB distributed transactions are inspired by the research paper [Building Deterministic Transaction Processing Systems without Deterministic Thread Scheduling](http://cs-www.cs.yale.edu/homes/dna/papers/transactions-wodet11.pdf) by Alexander Thomson and Daniel J. Abadi from Yale University. The paper introduced the concept of **deterministic transaction** processing, which allows for highly efficient distributed processing of transactions. The original paper imposed limitations on what kinds of operations can be executed in this manner. As these limitations interfered with real-world user scenarios, YDB evolved its algorithms to overcome them by using deterministic transactions as stages of executing user transactions with additional orchestration and locking.

#### Optimistic locking

As in many other database management systems, YDB queries can put locks on certain pieces of data, like table rows, to ensure that concurrent access does not modify them into an inconsistent state. However, YDB checks these locks not at the beginning of transactions but during commit attempts. The former is called **pessimistic locking** (used in PostgreSQL, for example), while the latter is called **optimistic locking** (used in YDB).

#### Transaction lock invalidation {#tli}

**Transaction lock invalidation** (TLI) is the standard behavior of YDB when parallel transactions conflict under [optimistic locking](glossary.md#optimistic-locking). If one transaction (the breaker) writes data and thereby breaks the locks of another transaction (the victim), YDB detects this at the victim's commit time and rolls it back with a `transaction locks invalidated` error. For more information about TLI diagnostics, see [Transaction lock invalidation](../troubleshooting/performance/queries/transaction-lock-invalidation.md).

#### Prepare stage

The **prepare stage** is a phase of distributed transaction execution, during which the transaction body is registered on all participating shards.

#### Execute stage

The **execute stage** is a phase of distributed query execution in which the scheduled transaction is executed and the response is generated.

In some cases, instead of [prepare](glossary.md#prepare-stage) and execute, the transaction is immediately executed, and a response is generated. For example, this happens for transactions involving only one shard or consistent reads from a snapshot.

#### Dirty operations

In the case of read-only transactions, similar to "read uncommitted" in other database management systems, it might be necessary to read data that has not yet been committed to disk. This is called **dirty operations**.

#### Read-write set {#rw-set}

The **read-write set** or **RW set** is a set of data that will participate in executing a [distributed transaction](glossary.md#transactions). It combines the read set, the data that will be read, and the write set, the data modifications to be carried out.

#### Read set

The **read set** or **ReadSet data** is what participating shards forward during the transaction execution. In the case of data transactions, it may contain information about the state of [optimistic locks](glossary.md#optimistic-locking), the readiness of the shard for commit, or the decision to cancel the transaction.

#### Transaction proxy

The **transaction proxy** or `TX_PROXY` is a service that orchestrates the execution of many [distributed transactions](glossary.md#transactions): sequential phases, phase execution, planning, and aggregation of results. In the case of direct orchestration by other actors (for example, QP data transactions), it is used for caching and allocation of unique [TxIDs](glossary.md#txid).

#### Transaction flags {#txflags}

**Transaction flags** or **TxFlags** is a bitmask of flags that modify the execution of a transaction in some way.

#### Transaction ID {#txid}

**Transaction ID** or **TxID** is a unique identifier assigned to each transaction when it is accepted by YDB.

#### Transaction order ID

A **transaction order ID** is a unique identifier assigned to each transaction during planning. It consists of [PlanStep](glossary.md#planstep) and [Transaction ID](glossary.md#txid).

#### PlanStep

**PlanStep** or **step** is the logical time for which a set of transactions is planned to be executed.

#### Mediator time

During the distributed query execution, **mediator time** is the logical time before which (inclusive) the shard participant must know the entire execution plan. It is used to advance the time in the absence of transactions on a particular shard, to determine whether it can read from a snapshot.

#### MiniKQL

**MiniKQL** is a language that allows the expression of a single [deterministic transaction](glossary.md#deterministic-transactions) in the system. It is a functional, strongly typed language. Conceptually, the language describes a graph of reading from the database, performing calculations on the read data, and writing the results to the database and/or to a special document representing the query result (shown to the user). The MiniKQL transaction must explicitly set its read set (readable data) and assume a deterministic selection of execution branches (for example, there is no random).

MiniKQL is a low-level language. The system's end users only see queries in the [YQL](glossary.md#yql) language, which relies on MiniKQL in its implementation.

#### Query Processor {#kqp}

**QP** or **Query Processor** (previously, **KQP**) is a YDB component responsible for the orchestration of user query execution and generating the final response.

### Global schema

**Global Schema**, **Global Scheme**, or **Database Schema** is a schema of all the data stored in a [database](glossary.md#database). It consists of [tables](glossary.md#table) and other entities, such as [topics](glossary.md#topic). The metadata about these entities is called a global schema. The term is used in contrast to **Local Schema**, which refers to the data schema inside a [tablet](glossary.md#tablet). YDB users never see the local schema and only work with the global schema.

### KiKiMR

**KiKiMR** is the legacy name of YDB that was used long before it became an [open-source product](https://github.com/ydb-platform/ydb). It can still be occasionally found in the source code, old articles and videos, etc.
