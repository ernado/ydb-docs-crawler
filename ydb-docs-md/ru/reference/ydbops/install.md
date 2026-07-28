---
title: "Установка ydbops"
url: "https://ydb.tech/docs/ru/reference/ydbops/install?version=v26.1"
doc_path: "ru/reference/ydbops/install"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydbops/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydbops/install.md"
description: "Примечание. Утилита ydbops находится в активной разработке. В редких случаях обратная совместимость может быть нарушена."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Установка ydbops

> [!NOTE]
> Утилита `ydbops` находится в активной разработке. В редких случаях обратная совместимость может быть нарушена.

## Загрузка бинарного файла со страницы релизов {#zagruzka-binarnogo-fajla-so-stranicy-relizov}

Скомпилированные исполняемые файлы можно скачать с [YDBOps Releases](../../downloads/index.md#ydbops).

## Сборка из исходного кода {#sborka-iz-ishodnogo-koda}

1. Склонируйте репозиторий `ydbops` с GitHub:

   ```bash
   git clone https://github.com/ydb-platform/ydbops.git
   ```

2. Сборка исполняемого файла может быть выполнена одним из двух вариантов:

   1. [Сборка с использованием компилятора Go](install.md#go)
   2. [Сборка внутри docker-контейнера](install.md#docker)

Для сборки с помощью [Docker](<https://en.wikipedia.org/wiki/Docker_(software)>) используется официальный docker image для [Golang](<https://en.wikipedia.org/wiki/Go_(programming_language)>) [v1.22](https://hub.docker.com/_/golang/tags?name=1.22), это гарантирует то, что сборка будет проведена успешно. Описание работы docker-контейнера в `Dockerfile` репозитория. Так же сборка в Docker проводит дополнительные манипуляции: выполняет проверки линтером, подставляет версию для сборки ydbops, чтобы она прописалась в исполняемом файле ydbops.

### Сборка с использованием компилятора Go {#go}

#### Требования {#trebovaniya}

[Установите Go](https://go.dev/doc/install). Рекомендуемая версия Go — 1.22.

#### Компиляция {#kompilyaciya}

Вызовите `go build` в корневой папке репозитория:

```bash
go build
```

Исполняемый файл `ydbops` будет доступен в корневой папке репозитория.

#### Установка {#ustanovka}

Вручную переместите исполняемый файл в требуемый каталог или используйте утилиту `make` для установки в каталог `install_folder` из текущего каталога:

```bash
make install INSTALL_DIR=install_folder BUILD_DIR=.
```

### Сборка внутри docker-контейнера {#docker}

#### Требования {#trebovaniya1}

- make;
- [docker engine](https://docs.docker.com/engine/install/).

#### Компиляция {#kompilyaciya1}

Выполните в папке репозитория команду:

```bash
make build-in-docker
```

Исполняемый файл `ydbops` будет доступен в корневой папке `bin`. Автоматически собираются исполняемые файлы для Linux и MacOS (arm64, amd64).

| Исполняемый файл | Платформа |
| --- | --- |
| ydbops | Linux(amd64) |
| ydbops_darwin_amd64 | MacOS(amd64) |
| ydbops_darwin_arm64 | MacOS(arm64) |

#### Установка {#ustanovka1}

Для установки исполняемого файла выполните команду `make`.

Дополнительные параметры:

- `INSTALL_DIR`: каталог, в который будет установлен исполняемый файл. По умолчанию: `~/ydb/bin`.
- `BUILD_DIR`: каталог, содержащий скомпилированный исполняемый файл. Этот параметр используется, если файл собран самостоятельно. Например, если файл находится в текущем каталоге, используйте `BUILD_DIR=.`.

```bash
make install [INSTALL_DIR=<путь_к_каталогу>] [BUILD_DIR=<путь_к_каталогу>]
```

Пример команды для установки в каталог `install_folder` из текущего каталога:

```bash
make install INSTALL_DIR=install_folder BUILD_DIR=.
```
