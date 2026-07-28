---
title: "Обзор управления кластером YDB вручную"
url: "https://ydb.tech/docs/ru/devops/deployment-options/manual/?version=v26.1"
doc_path: "ru/devops/deployment-options/manual/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/manual/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/manual/index.md"
description: "В данном разделе описано развёртывание, конфигурирование, обслуживание, мониторинг и диагностика многоузловых кластеров YDB без использования систем оркестрации"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Обзор управления кластером YDB вручную

В данном разделе описано развёртывание, конфигурирование, обслуживание, мониторинг и диагностика многоузловых [кластеров YDB](../../../concepts/topology.md) без использования систем оркестрации и автоматизации (таких как Kubernetes или специализированных инструментов управления). При таком подходе администратор самостоятельно выполняет все операции по установке компонентов, настройке конфигурации и обслуживанию кластера, используя командную строку и напрямую взаимодействуя с узлами кластера.

Основные материалы:

- [Развёртывание YDB кластера вручную](initial-deployment/index.md)
- [Обзор управления дисковой подсистемой кластера](../../../maintenance/manual/index.md)
- [Использование встроенного web-интерфейса](../../../reference/embedded-ui/index.md)
