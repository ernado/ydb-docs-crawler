---
title: "ydbops utility overview"
url: "https://ydb.tech/docs/en/reference/ydbops/?version=v26.1"
doc_path: "en/reference/ydbops/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydbops/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydbops/index.md"
description: "Note. The ydbops utility is under active development. Although backward-incompatible changes are unlikely, they may still occur."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ydbops utility overview

> [!NOTE]
> The `ydbops` utility is under active development. Although backward-incompatible changes are unlikely, they may still occur.

`ydbops` utility automates some operational tasks on YDB clusters. It supports clusters deployed using [Ansible](../../devops/deployment-options/ansible/index.md), [Kubernetes](../../devops/deployment-options/kubernetes/index.md), or [manually](../../devops/deployment-options/manual/index.md).

## See also

- To install the utility, follow the [instructions](install.md).
- See [configuration reference](configuration.md) for available configuration options.
- The source code of `ydbops` can be found [on GitHub](https://github.com/ydb-platform/ydbops).

## Currently supported scenarios

See the list of currently supported scenarios [here](rolling-restart-scenario.md).

## Scenarios in development

- Requesting permission to take out a set of YDB nodes for maintenance without breaking YDB fault model invariants.
