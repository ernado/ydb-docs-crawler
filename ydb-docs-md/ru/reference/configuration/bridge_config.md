---
title: "bridge_config"
url: "https://ydb.tech/docs/ru/reference/configuration/bridge_config?version=v26.1"
doc_path: "ru/reference/configuration/bridge_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/bridge_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/bridge_config.md"
description: "Секция описывает pile кластера для режима bridge. Укажите список имён pile, которые используются для привязки хостов и других сущностей. В режиме bridge для каж"
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# bridge_config

Секция описывает pile кластера для [режима bridge](../../concepts/bridge.md). Укажите список имён pile, которые используются для привязки хостов и других сущностей. В режиме bridge для каждого хоста также необходимо указать имя соответствующего pile в секции `hosts` (поле `bridge_pile_name`), см. [hosts](hosts.md#hosts-bridge).

## Синтаксис {#sintaksis}

```yaml
bridge_config:
  piles:
  - name: <pile_name_1>
  - name: <pile_name_2>
  ...
  - name: <pile_name_n>
```
