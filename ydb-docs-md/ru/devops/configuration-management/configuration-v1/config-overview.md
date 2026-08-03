---
title: "Обзор конфигурации V1"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/config-overview?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/config-overview"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/config-overview.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/config-overview.md"
description: "Для запуска узла YDB требуется конфигурация. Существуют два типа конфигурации: Статическая — файл в формате YAML, хранящийся на локальном диске узла."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обзор конфигурации V1

Для запуска узла YDB требуется конфигурация. Существуют два типа конфигурации:

- **Статическая** — файл в формате YAML, хранящийся на локальном диске узла.
- **Динамическая** — документ в формате YAML, хранящийся в хранилище конфигурации YDB .

Статические узлы кластера используют статическую конфигурацию. Динамические узлы могут использовать статическую конфигурацию, динамическую конфигурацию или их комбинацию.

## Статическая конфигурация {#static-config}

Статическая конфигурация представляет собой YAML файл, хранимый на узлах кластера. В этом файле перечислены все настройки системы. Путь к файлу передается на вход процессу `ydbd` при запуске через параметр командной строки. Распространение статической конфигурации по кластеру и поддержка её в консистентном состоянии на всех узлах — ответственность администратора кластера. Подробности по использованию статической конфигурации можно найти в разделе [Параметры конфигурации кластера](static-config.md). Эта конфигурация **необходима** для запуска статических узлов.

![data tab](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/_assets/config-chart-1.png "static configs")

### Базовый сценарий использования {#bazovyj-scenarij-ispolzovaniya}

1. Скопировать [стандартную конфигурацию](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/) из GitHub.
2. Изменить конфигурацию в соответствии с вашими требованиями.
3. Разместить идентичные файлы конфигурации на всех узлах кластера.
4. Запустить все узлы кластера, указав путь к файлу конфигурации явно, используя аргумент командной строки `--yaml-config`.

## Динамическая конфигурация {#dynamic-config}

Динамическая конфигурация является YAML-документом, надёжно сохранённом в кластере в [таблетке Console](../../../concepts/glossary.md#console). В отличие от статической её достаточно загрузить в кластер, так как за её распространение и поддержание в консистентном состоянии будет отвечать YDB. При этом динамическая конфигурация при помощи селекторов позволяет обрабатывать, в том числе, сложные сценарии, оставаясь при этом в рамках одного файла конфигурации. Описание динамической конфигурации представлено в разделе [Динамическая конфигурация кластера](dynamic-config.md).

![data tab](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/_assets/config-chart-2.png "static and dynamic configs")

### Базовый сценарий использования {#bazovyj-scenarij-ispolzovaniya1}

1. Скопировать [стандартную конфигурацию](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/) из GitHub.
2. Изменить конфигурацию в соответствии с вашими требованиями.
3. Разместить идентичные файлы конфигурации на всех статических узлах кластера.
4. Запустить все статические узлы кластера, указав путь к файлу конфигурации явно, используя аргумент командной строки `--yaml-config`.
5. Дополнить файл конфигурации до [формата динамической конфигурации](dynamic-config.md#example).
6. Загрузить на кластер полученную конфигурацию при помощи `ydb admin config replace -f dynconfig.yaml`.
