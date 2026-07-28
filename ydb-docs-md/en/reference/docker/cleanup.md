---
title: "Docker stop"
url: "https://ydb.tech/docs/en/reference/docker/cleanup?version=v26.1"
doc_path: "en/reference/docker/cleanup"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/docker/cleanup.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/docker/cleanup.md"
description: "To stop YDB in Docker, run the following command: docker stop ydb-local."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Docker stop

To stop YDB in Docker, run the following command:

```bash
docker stop ydb-local
```

If the `--rm` flag was specified at startup, the container will be deleted after stopping.

## Kill Docker container with YDB

To delete a Docker container with YDB, run the following command:

```bash
docker kill ydb-local
```

If you want to clean up the file system, delete your work directory using the `rm -rf ~/ydbd` command. This will permanently remove all data inside the local YDB cluster.
