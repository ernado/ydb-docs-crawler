---
title: "Остановка Docker"
url: "https://ydb.tech/docs/ru/reference/docker/cleanup?version=v26.1"
doc_path: "ru/reference/docker/cleanup"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/docker/cleanup.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/docker/cleanup.md"
description: "Для остановки YDB в Docker необходимо выполнить следующую команду: docker stop ydb-local."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
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
