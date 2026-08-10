---
title: "Директория"
url: "https://ydb.tech/docs/ru/concepts/datamodel/dir?version=v26.1"
doc_path: "ru/concepts/datamodel/dir"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/datamodel/dir.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/datamodel/dir.md"
description: "Директория."
revision: "a6ee1837f90009a183281888dccad12a7b30d774"
---

# Директория

Для удобства организации поддерживается создание [директорий](../glossary.md#folder) по аналогии с файловой системой, то есть вся база состоит из дерева директорий, а [схемные объекты](../glossary.md#scheme-object), например, таблицы, находятся в листах этого дерева. В одной директории могут быть несколько поддиректорий и несколько схемных объектов. Имена схемных объектов внутри одной директории уникальны.
