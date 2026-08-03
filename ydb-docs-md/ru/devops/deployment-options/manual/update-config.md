---
title: "Обновление конфигурации кластеров YDB, развёрнутых вручную"
url: "https://ydb.tech/docs/ru/devops/deployment-options/manual/update-config?version=v26.1"
doc_path: "ru/devops/deployment-options/manual/update-config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/manual/update-config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/manual/update-config.md"
description: "При ручном развертывании кластера YDB управление конфигурацией осуществляется через YDB CLI. В этой статье рассматриваются способы изменения конфигурации класте"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обновление конфигурации кластеров YDB, развёрнутых вручную

При ручном развертывании кластера YDB управление конфигурацией осуществляется через [YDB CLI](../../../reference/ydb-cli/index.md). В этой статье рассматриваются способы изменения конфигурации кластера после первоначального развертывания.

## Базовые операции с конфигурацией {#bazovye-operacii-s-konfiguraciej}

### Получение текущей конфигурации {#poluchenie-tekushej-konfiguracii}

Для получения текущей конфигурации кластера используется команда:

```bash
ydb -e grpcs://<endpoint>:2135 admin cluster config fetch > config.yaml
```

В качестве `<endpoint>` указывается адрес любого из узлов кластера.

### Применение новой конфигурации {#primenenie-novoj-konfiguracii}

Для загрузки обновленной конфигурации на кластер используется следующая команда:

```bash
ydb -e grpcs://<endpoint>:2135 admin cluster config replace -f config.yaml
```

Некоторые параметры конфигурации применяются на ходу после выполнения команды, однако для некоторых требуется выполнение процедуры [перезапуска кластера](../../../maintenance/manual/node_restarting.md).
