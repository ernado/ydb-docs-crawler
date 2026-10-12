---
title: "Директория"
url: "https://ydb.tech/docs/ru/concepts/datamodel/dir?version=v26.1"
doc_path: "ru/concepts/datamodel/dir"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/datamodel/dir.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/datamodel/dir.md"
description: "Для удобства организации поддерживается создание директорий по аналогии с файловой системой, то есть вся база состоит из дерева директорий, а схемные объекты, н"
revision: "665607947c838b4f199a3b30499a54d29413ee4f"
---

# Директория

Для удобства организации поддерживается создание [директорий](../glossary.md#folder) по аналогии с файловой системой, то есть вся база состоит из дерева директорий, а [схемные объекты](../glossary.md#scheme-object), например, таблицы, находятся в листах этого дерева. В одной директории могут быть несколько поддиректорий и несколько схемных объектов. Имена схемных объектов внутри одной директории уникальны.
