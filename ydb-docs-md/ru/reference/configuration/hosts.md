---
title: "hosts"
url: "https://ydb.tech/docs/ru/reference/configuration/hosts?version=v26.1"
doc_path: "ru/reference/configuration/hosts"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/hosts.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/hosts.md"
description: "В данной группе перечисляются статические узлы кластера, на которых запускаются процессы работы со Storage, и задаются их основные характеристики:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# hosts

В данной группе перечисляются статические узлы кластера, на которых запускаются процессы работы со Storage, и задаются их основные характеристики:

- Числовой идентификатор узла
- DNS-имя хоста и порт, по которым может быть установлено соединение с узлом в IP network
- Идентификатор [типовой конфигурации хоста](host_configs.md)
- Размещение в определенной зоне доступности, стойке
- Инвентарный номер сервера (опционально)

## Синтаксис {#sintaksis}

```yaml
hosts:
- host: <DNS-имя хоста>
  host_config_id: <числовой идентификатор типовой конфигурации хоста>
  port: <порт> # 19001 по умолчанию
  location:
    unit: <строка с инвентарным номером сервера>
    data_center: <строка с идентификатором зоны доступности>
    rack: <строка с идентификатором стойки>
- host: <DNS-имя хоста>
  # ...
```

## Примеры {#primery}

```yaml
hosts:
- host: hostname1
  host_config_id: 1
  node_id: 1
  port: 19001
  location:
    unit: '1'
    data_center: '1'
    rack: '1'
- host: hostname2
  host_config_id: 1
  node_id: 2
  port: 19001
  location:
    unit: '1'
    data_center: '1'
    rack: '1'
```

### Особенности режима bridge {#hosts-bridge}

В [режиме bridge](../../concepts/bridge.md) каждый хост должен быть привязан к одному из pile, объявленных в [`bridge_config`](bridge_config.md). Для этого в разделе `location` укажите поле `bridge_pile_name` с именем pile. Пример:

```yaml
hosts:
- host: hostname1
  host_config_id: 1
  location:
    ...
    bridge_pile_name: 'pile_1'
```

## Особенности Kubernetes {#hosts-k8s}

При развертывании YDB с помощью оператора Kubernetes секция `hosts` полностью генерируется автоматически, заменяя любой указанный пользователем контент в передаваемой оператору конфигурации. Все Storage узлы используют `host_config_id` = `1`, для которого должна быть задана [корректная конфигурация](host_configs.md#host-configs-k8s).
