---
title: "Безопасный рестарт и выключение узлов"
url: "https://ydb.tech/docs/ru/maintenance/manual/node_restarting?version=v26.1"
doc_path: "ru/maintenance/manual/node_restarting"
version: "v26.1"
lang: "ru"
source_path: "ru/core/maintenance/manual/node_restarting.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/maintenance/manual/node_restarting.md"
description: "Остановка/рестарт процесса YDB на узле. Чтобы убедиться, что процесс можно остановить, надо выполнить следующие шаги. Перейти в узел по ssh. Выполнить команду."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Безопасный рестарт и выключение узлов

## Остановка/рестарт процесса YDB на узле {#restart_process}

Чтобы убедиться, что процесс можно остановить, надо выполнить следующие шаги.

1. Перейти в узел по ssh.

2. Выполнить команду

   ```bash
   ydbd cms request restart host {node_id} --user {user} --duration 60 --dry --reason 'some-reason'
   ```

   При разрешение выведет `ALLOW`.

3. Остановить процесс

   ```bash
   sudo service ydbd stop
   ```

4. Если потребуется, запустить процесс

   ```bash
    sudo service ydbd start
   ```

## Замена оборудования {#replace-hardware}

Перед заменой нужно убедиться, что процесс YDB можно [остановить](node_restarting.md#restart_process).  
 При длительном отсутствии стоит перед этим перевезти все VDisk'и с данного узла и дождаться окончания репликации.  
 После окончания репликации узел можно безопасно выключать.

Чтобы отключение динамического узла не оказало влияние на обработку запросов, необходимо перед отключением выполнить мягкий перенос (drain) таблеток с этого узла.

Стоит перейти на страницу [Hive web-viewer](../../reference/embedded-ui/hive.md).  
 После нажатия на кнопку "View Nodes" отобразится список всех узлов.

Перед отключением узла, сначала требуется отключить перевоз таблеток через кнопку Active, после чего нажать Drain и дождаться увоза всех таблеток.
