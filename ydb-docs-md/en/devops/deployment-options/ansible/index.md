---
title: "Working With YDB Using Ansible"
url: "https://ydb.tech/docs/en/devops/deployment-options/ansible/?version=v26.1"
doc_path: "en/devops/deployment-options/ansible/"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/ansible/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/ansible/index.md"
description: "This section of YDB documentation contains a collection of articles intended for DevOps engineers managing YDB clusters using Ansible. This is the recommended a"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Working With YDB Using Ansible

This section of YDB documentation contains a collection of articles intended for DevOps engineers managing YDB clusters using [Ansible](https://www.ansible.com/). This is the recommended approach to running production YDB clusters directly on virtual machines or bare metal. It is recommended to use [Kubernetes](../kubernetes/index.md) instead of Ansible for containerized environments.

The key articles to get started with this section:

- [Deploying a YDB cluster with Ansible](initial-deployment/index.md)

- [Deploy Infrastructure for YDB Cluster using Terraform](preparing-vms-with-terraform.md)

- [Restarting YDB Clusters deployed with Ansible](restart.md)

- Observability:

  - [Logging on Clusters Deployed with Ansible](observability/logging.md)
