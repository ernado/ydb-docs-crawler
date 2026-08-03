---
title: "Logging in YDB"
url: "https://ydb.tech/docs/en/devops/observability/logging?version=v26.1"
doc_path: "en/devops/observability/logging"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/observability/logging.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/observability/logging.md"
description: "Each YDB component writes messages of different levels to logs. These can be used to detect critical problems or understand the causes of issues. Logging Setup."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Logging in YDB

Each YDB component writes messages of different levels to logs. These can be used to detect critical problems or understand the causes of issues.

## Logging Setup {#log_setup}

Logging configuration for individual components can be done in the [embedded interface](../../reference/embedded-ui/logs.md#change_log_level) of YDB.

Currently, there are two options for starting YDB logging: manually and using systemd.

### Manually {#log_setup_manually}

For convenience, YDB provides standard mechanisms for collecting logs and metrics.  
 Logging is performed to standard `stdout` and `stderr` channels and can be redirected using popular solutions.

### Using Systemd {#log_setup_systemd}

By default, logs are written to `journald` and can be retrieved using `journalctl -u ydbd-storage`. For database nodes, change the systemd unit name appropriately.
