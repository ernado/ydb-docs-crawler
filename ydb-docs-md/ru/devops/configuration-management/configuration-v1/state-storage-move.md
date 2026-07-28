---
title: "Перемещение State Storage"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/state-storage-move?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/state-storage-move"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/state-storage-move.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/state-storage-move.md"
description: "Если нужно вывести из эксплуатации хост кластера YDB, на котором располагается часть State Storage, необходимо переместить её на другой хост. Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Перемещение State Storage

Если нужно вывести из эксплуатации хост кластера YDB, на котором располагается часть [State Storage](../../../reference/configuration/index.md#domains-state), необходимо переместить её на другой хост.

> [!WARNING]
> Неправильная последовательность действий или ошибка в конфигурации могут привести к недоступности кластера YDB.

В качестве примера рассмотрим кластер YDB со следующей конфигурацией State Storage:

```yaml
...
domains_config:
  ...
  state_storage:
  - ring:
      node: [1, 2, 3, 4, 5, 6, 7, 8, 9]
      nto_select: 9
    ssid: 1
  ...
...
```

На хосте с `node_id:1` сконфигурирован и запущен [статический узел](../../../reference/configuration/index.md#hosts) кластера, который обслуживает часть State Storage. Предположим, нам нужно вывести из эксплуатации этот хост.

Для замены `node_id:1` мы [добавили](cluster-expansion.md#add-host) в кластер новый хост с `node_id:10` и [развернули](cluster-expansion.md#add-static-node) на нём статический узел.

Чтобы переместить State Storage с хоста `node_id:1` на `node_id:10`:

1. Остановите статические узлы кластера на хостах с `node_id:1` и `node_id:10`.

   > [!NOTE]
   > Кластер YDB является отказоустойчивым. Временное выключение узла не приводит к недоступности кластера. Подробнее см. [Топология кластера YDB](../../../concepts/topology.md).

2. В конфигурационном файле `config.yaml` измените список хостов `node`, заменив идентификатор удаляемого хоста на идентификатор добавляемого:

   ```yaml
   domains_config:
   ...
     state_storage:
     - ring:
         node: [2, 3, 4, 5, 6, 7, 8, 9, 10]
         nto_select: 9
       ssid: 1
   ...
   ```

3. Обновите конфигурационные файлы `config.yaml` для всех узлов кластера, в том числе и динамических.

4. С помощью процедуры [rolling-restart](../../../maintenance/manual/node_restarting.md) перезапустите все узлы кластера, включая динамические, кроме статических узлов на хостах с `node_id:1` и `node_id:10`. Обратите внимание, что между рестартом хостов необходима задержка как минимум в 15 секунд.

5. Запустите статические узлы кластера на хостах `node_id:1` и `node_id:10`.
