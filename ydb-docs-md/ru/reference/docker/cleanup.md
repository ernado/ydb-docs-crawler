---
title: "Остановка Docker"
url: "https://ydb.tech/docs/ru/reference/docker/cleanup?version=v26.1"
doc_path: "ru/reference/docker/cleanup"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/docker/cleanup.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/docker/cleanup.md"
description: "Для остановки YDB в Docker необходимо выполнить следующую команду: docker stop ydb-local."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Остановка Docker

Для остановки YDB в Docker необходимо выполнить следующую команду:

```bash
docker stop ydb-local
```

Если при запуске был указан флаг `--rm`, то контейнер будет удалён после остановки.

## Удаление Docker-контейнера YDB {#udalenie-docker-kontejnera-ydb}

Для удаления Docker-контейнера, содержащего YDB, необходимо выполнить следующую команду:

```bash
docker kill ydb-local
```

Для очистки файловую систему удалите рабочую директорию с помощью команды `rm -rf ~/ydbd`, при этом все данные внутри локального кластера YDB будут потеряны.
