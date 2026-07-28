---
title: "Balancing"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/balancing?version=v26.1"
doc_path: "en/recipes/ydb-sdk/balancing"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/balancing.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/balancing.md"
description: "YDB uses client load balancing because it is more efficient when a lot of traffic from multiple client applications comes to a database."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Balancing

YDB uses client load balancing because it is more efficient when a lot of traffic from multiple client applications comes to a database.  
 In most cases, it just works in the YDB SDK. However, sometimes specific settings for client load balancing are required, for example, to reduce server hops and request time or to distribute the load across availability zones.

Note that custom balancing is limited when it comes to YDB sessions. Custom balancing in the YDB SDKs is performed only when creating a new YDB session on a specific node. Once the session is created, all queries in this session are passed to the node where the session was created. Queries in the same YDB session are not balanced between different YDB nodes.

This section contains code recipes with client load balancing settings in different YDB SDKs.

Table of contents:

- [Random choice](balancing-random-choice.md)
- [Prefer the nearest data center](balancing-prefer-local.md)
- [Prefer the specific availability zone](balancing-prefer-location.md)
- [Prefer a pile with a specific state](balancing-prefer-pile.md)
