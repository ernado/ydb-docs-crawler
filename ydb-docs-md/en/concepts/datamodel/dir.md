---
title: "Directory"
url: "https://ydb.tech/docs/en/concepts/datamodel/dir?version=v26.1"
doc_path: "en/concepts/datamodel/dir"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/datamodel/dir.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/datamodel/dir.md"
description: "Directory."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Directory

For convenience, YDB supports creating [directories](../glossary.md#folder) similar to a filesystem, meaning the entire database consists of a directory tree, and [scheme objects](../glossary.md#scheme-object), such as tables, are located in the leaves of this tree. A directory can host multiple subdirectories and several scheme objects. The names of scheme objects within a single directory are unique.
