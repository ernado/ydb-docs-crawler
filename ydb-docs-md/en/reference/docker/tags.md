---
title: "Docker image `ydbplatform/local-ydb` tags naming"
url: "https://ydb.tech/docs/en/reference/docker/tags?version=v26.1"
doc_path: "en/reference/docker/tags"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/docker/tags.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/docker/tags.md"
description: "For the ydbplatform/local-ydb Docker image, the following naming rules apply for tags: Tag Name Description. latest."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Docker image `ydbplatform/local-ydb` tags naming

For the [ydbplatform/local-ydb](https://hub.docker.com/r/ydbplatform/local-ydb) Docker image, the following naming rules apply for tags:

| Tag Name | Description |
| --- | --- |
| `latest` | Corresponds to the most recent *stable* version of YDB tested on production clusters. Rebuilt for each new YDB release. |
| `edge` | A candidate for the next *stable* version, currently undergoing testing. Includes new features but may not be stable and thus unsuitable for production environments. |
| `trunk`, `main`, `nightly` | The latest version of YDB from the main development branch. Includes all recent changes and is rebuilt nightly. Similarly to `edge`, it is not suitable for production environments. |
| `XX.Y` | Corresponds to the latest minor version of YDB in a major release `XX.Y`, including all patches. |
| `XX.Y.ZZ` | Corresponds to the YDB release version `XX.Y.ZZ`. |
| `XX.Y-slim`, `XX.Y.ZZ-slim` | Compressed binaries of YDB (`ydbd` and `ydb`) with smaller image size but a slower startup. Uses [UPX](https://github.com/upx/upx). |
