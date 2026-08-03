---
title: "Включение и выключение Scrubbing"
url: "https://ydb.tech/docs/ru/maintenance/manual/scrubbing?version=v26.1"
doc_path: "ru/maintenance/manual/scrubbing"
version: "v26.1"
lang: "ru"
source_path: "ru/core/maintenance/manual/scrubbing.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/maintenance/manual/scrubbing.md"
description: "Scrubbing — процесс читает данные, проверяет их на целостность и, если нужно, восстанавливает ее. Процесс запущен по умолчанию, интервал между окончанием провер"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Включение и выключение Scrubbing

Scrubbing — процесс читает данные, проверяет их на целостность и, если нужно, восстанавливает ее. Процесс запущен по умолчанию, интервал между окончанием проверки и запуском следующей — 1 месяц. Вы можете изменить интервал с помощью утилиты [YDB DSTool](../../reference/ydb-dstool/index.md). Проверяются данные, последний доступ к которым был раньше времени предыдущей проверки. Scrubbing-процесс запускается или останавливается для всего кластера YDB. Проверка выполняется в фоне и не перегружает систему.

Чтобы задать интервал в 48 часов, выполните команду:

```bash
ydb-dstool -e <bs_endpoint> cluster set --scrub-periodicity 48h
```

`<bs_endpoint>` - эндпоинт произвольного [узла хранения](../../concepts/glossary.md#storage-node) кластера.

Так же можно указать максимальное число дисков кластера, которые будут проверяться одновременно. Например, чтобы проверять одновременно не более одного диска, выполните команду:

```bash
ydb-dstool -e <bs_endpoint> cluster set --max-scrubbed-disks-at-once
```

Чтобы остановить scrubbing-процесс на кластере, выполните команду:

```bash
ydb-dstool -e <bs_endpoint> cluster set --scrub-periodicity disable
```
