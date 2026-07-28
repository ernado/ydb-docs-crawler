---
title: "monitoring_config"
url: "https://ydb.tech/docs/ru/reference/configuration/monitoring_config?version=v26.1"
doc_path: "ru/reference/configuration/monitoring_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/monitoring_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/monitoring_config.md"
description: "Секция monitoring_config файла конфигурации YDB задаёт параметры YDB Monitoring. Ниже описаны настройки, связанные с аутентификацией на отдельных страницах встр"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# monitoring_config

Секция `monitoring_config` файла конфигурации YDB задаёт параметры [YDB Monitoring](../embedded-ui/ydb-monitoring.md). Ниже описаны настройки, связанные с [аутентификацией](../../security/authentication.md) на отдельных страницах встроенного мониторинга.

```yaml
monitoring_config:
  # аутентификация на страницах /counters и /healthcheck
  require_counters_authentication: false
  require_healthcheck_authentication: false
```

## Аутентификация на страницах мониторинга {#authentication}

|  |  |
| --- | --- |
| Параметр | Описание |
| `require_counters_authentication` | Режим обязательной [аутентификации](../../security/authentication.md) на страницах `/counters` и `/counters/hosts`.<br>Возможные значения:<br>- `true` — доступ к `/counters` и `/counters/hosts` только с [аутентификационным токеном](../../concepts/glossary.md#auth-token); запросы проходят аутентификацию и проверку прав.<br><br>  Значение `true` допустимо только при включенном режиме обязательной [аутентификации](../../security/authentication.md) в секции [security_config](security_config.md) файла конфигурации YDB.<br><br>- `false` — запросы к `/counters` и `/counters/hosts` могут выполняться без [аутентификационного токена](../../concepts/glossary.md#auth-token).<br>Значение по умолчанию: `false`. |
| `require_healthcheck_authentication` | Дополнительное требование [аутентификации](../../security/authentication.md) для эндпоинта `/healthcheck` поверх общих правил кластера.<br>Возможные значения:<br>- `true` — любой ответ `/healthcheck`, включая [формат Prometheus](https://prometheus.io/docs/instrumenting/exposition_formats/) (параметр `format=prometheus`), выдаётся только при запросе с [аутентификационным токеном](../../concepts/glossary.md#auth-token); запросы проходят аутентификацию и проверку прав.<br><br>  Значение `true` допустимо только при включенном режиме обязательной [аутентификации](../../security/authentication.md) в секции [security_config](security_config.md) файла конфигурации YDB.<br><br>- `false` — при обязательной аутентификации в кластере запросы к `/healthcheck` без токена по-прежнему допускаются, если запрошен вывод в [формате Prometheus](https://prometheus.io/docs/instrumenting/exposition_formats/) (`format=prometheus`). Для остальных форматов ответа `/healthcheck` действуют общие правила (см. примечание ниже).<br>Значение по умолчанию: `false`.<br>> [!NOTE]<br>> Если в [security_config](security_config.md) включена обязательная [аутентификация](../../security/authentication.md), то для ответов `/healthcheck` в любом формате, кроме Prometheus, токен обязателен независимо от значения `require_healthcheck_authentication`. |
