---
title: "Логирование в YDB"
url: "https://ydb.tech/docs/ru/devops/observability/logging?version=v26.1"
doc_path: "ru/devops/observability/logging"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/observability/logging.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/observability/logging.md"
description: "Каждый компонент YDB пишет сообщения разного уровня в логи (журналы). По ним можно детектировать критические проблемы или разобраться в причинах неполадок."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Логирование в YDB

Каждый компонент YDB пишет сообщения разного уровня в логи (журналы). По ним можно детектировать критические проблемы или разобраться в причинах неполадок.

## Настройка логирования {#log_setup}

Настройку логирования у отдельных компонентов можно произвести во [встроенном интерфейсе](../../reference/embedded-ui/logs.md#change_log_level) YDB.

На данный момент есть два варианта для запуска логирования YDB: вручную и с использованием systemd.

### Вручную {#log_setup_manually}

Для удобства YDB предоставляет стандартные механизмы сбора логов и метрик.  
 Логирование осуществляется в стандартные каналы `stdout` и `stderr` и может быть перенаправлено при помощи популярных решений.

### С использованием systemd {#log_setup_systemd}

По умолчению пишутся в `journald` и достать их можно через `journalctl -u ydbd-storage`. Для доступа к логам узлов баз данных, измените имя systemd юнита соответствующим образом.
