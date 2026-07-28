---
title: "Перемещение статической группы"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/static-group-move?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/static-group-move"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/static-group-move.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/static-group-move.md"
description: "Если нужно вывести из эксплуатации хост кластера YDB, на котором располагается часть статической группы, необходимо переместить её на другой хост. Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Перемещение статической группы

Если нужно вывести из эксплуатации хост кластера YDB, на котором располагается часть [статической группы](../../../reference/configuration/index.md#blob_storage_config), необходимо переместить её на другой хост.

> [!WARNING]
> Неправильная последовательность действий или ошибка в конфигурации могут привести к недоступности кластера YDB.

В качестве примера рассмотрим кластер YDB, в котором на хосте с `node_id:1` сконфигурирован и запущен [статический узел](../../../reference/configuration/index.md#hosts). Этот узел обслуживает часть статической группы.

Фрагмент конфигурации статической группы:

```yaml
...
blob_storage_config:
  ...
  service_set:
    ...
    groups:
      ...
      rings:
        ...
        fail_domains:
        - vdisk_locations:
          - node_id: 1
            path: /dev/vda
            pdisk_category: SSD
        ...
      ...
    ...
  ...
...
```

Для замены `node_id:1` мы [добавили](cluster-expansion.md#add-static-node) в кластер новый хост с `node_id:10` и [развернули](cluster-expansion.md#add-static-node) на нём статический узел.

Чтобы переместить часть статической группы с хоста `node_id:1` на `node_id:10`:

1. Остановите статический узел кластера на хосте с `node_id:1`.

   > [!NOTE]
   > Кластер YDB является отказоустойчивым. Временное выключение узла не приводит к недоступности кластера. Подробнее см. [Топология кластера YDB](../../../concepts/topology.md).

2. В конфигурационном файле `config.yaml` измените значение `node_id`, заменив идентификатор удаляемого хоста на идентификатор добавляемого:

   ```yaml
   ...
   blob_storage_config:
     ...
     service_set:
       ...
       groups:
         ...
         rings:
           ...
           fail_domains:
           - vdisk_locations:
             - node_id: 10
               path: /dev/vda
               pdisk_category: SSD
           ...
         ...
       ...
     ...
   ...
   ```

   Измените путь `path` и категорию `pdisk_category` диска, если на хосте с `node_id: 10` они отличаются.

3. Обновите конфигурационные файлы `config.yaml` для всех узлов кластера, в том числе и динамических.

4. С помощью процедуры [rolling-restart](../../../maintenance/manual/node_restarting.md) перезапустите все статические узлы кластера.

5. Перейдите на страницу мониторинга Embedded UI и убедитесь, что VDisk статической группы появился на целевом физическом диске и реплицируется. Подробнее см. [Мониторинг статической группы](../../../reference/embedded-ui/ydb-monitoring.md#static-group).

6. С помощью процедуры [rolling-restart](../../../maintenance/manual/node_restarting.md) перезапустите все динамические узлы кластера.
