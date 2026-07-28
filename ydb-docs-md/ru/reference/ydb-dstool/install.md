---
title: "Установка YDB DSTool"
url: "https://ydb.tech/docs/ru/reference/ydb-dstool/install?version=v26.1"
doc_path: "ru/reference/ydb-dstool/install"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-dstool/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-dstool/install.md"
description: "Linux. macOS. Windows. Чтобы установить YDB DSTool: Выполните команду: curl -sSL 'https://install.ydb.tech/dstool' | bash."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Установка YDB DSTool

{% list tabs %}

- Linux

  Чтобы установить YDB DSTool:

  1. Выполните команду:

     ```bash
     curl -sSL 'https://install.ydb.tech/dstool' | bash
     ```

     Скрипт установит YDB DSTool. Если скрипт запускается из оболочки `bash` или `zsh`, он также добавит исполняемый файл `ydb-dstool` в переменную окружения `PATH`. В противном случае вы можете запускать его из папки `~/ydb/bin` или добавить в `PATH` вручную.

  2. Чтобы обновить переменные окружения, перезапустите командную оболочку.

  3. Проверьте работу, выполнив команду вывода информации о кластере:

     ```bash
     ydb-dstool -e <bs_endpoint> cluster list
     ```

     - `bs_endpoint` — URI HTTP-эндпоинта кластера — это тот же самый эндпоинт, который обслуживает [Embedded UI](../embedded-ui/index.md). Пример: `http://localhost:8765`.

     Результат:

     ```text
     ┌───────┬───────┬───────┬────────┬────────┬───────┬────────┐
     │ Hosts │ Nodes │ Pools │ Groups │ VDisks │ Boxes │ PDisks │
     ├───────┼───────┼───────┼────────┼────────┼───────┼────────┤
     │ 8     │ 16    │ 1     │ 5      │ 40     │ 1     │ 32     │
     └───────┴───────┴───────┴────────┴────────┴───────┴────────┘
     ```

- macOS

  Чтобы установить YDB DSTool:

  1. Выполните команду:

     ```bash
     curl -sSL 'https://install.ydb.tech/dstool' | bash
     ```

     Скрипт установит YDB DSTool. Если скрипт запускается из оболочки `bash` или `zsh`, он также добавит исполняемый файл `ydb-dstool` в переменную окружения `PATH`. В противном случае вы можете запускать его из папки `~/ydb/bin` или добавить в `PATH` вручную.

  2. Чтобы обновить переменные окружения, перезапустите командную оболочку.

  3. Проверьте работу, выполнив команду вывода информации о кластере:

     ```bash
     ydb-dstool -e <bs_endpoint> cluster list
     ```

     - `bs_endpoint` — URI HTTP-эндпоинта кластера — это тот же самый эндпоинт, который обслуживает [Embedded UI](../embedded-ui/index.md). Пример: `http://localhost:8765`.

     Результат:

     ```text
     ┌───────┬───────┬───────┬────────┬────────┬───────┬────────┐
     │ Hosts │ Nodes │ Pools │ Groups │ VDisks │ Boxes │ PDisks │
     ├───────┼───────┼───────┼────────┼────────┼───────┼────────┤
     │ 8     │ 16    │ 1     │ 5      │ 40     │ 1     │ 32     │
     └───────┴───────┴───────┴────────┴────────┴───────┴────────┘
     ```

- Windows

  Чтобы установить YDB DSTool:

  1. Выполните команду:

     - **PowerShell**:

       ```powershell
       iex (New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/dstool-windows')
       ```

     - **CMD**:

       ```cmd
       @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/dstool-windows'))"
       ```

  2. Укажите, нужно ли добавить путь к `ydb-dstool` в переменную окружения `PATH`:

     ```text
     Add ydb-dstool installation dir to your PATH? [Y/n]
     ```

  3. Чтобы обновить переменные окружения, перезапустите командную оболочку.

     > [!NOTE]
     > YDB DSTool использует символы Юникода в выводе некоторых команд. При некорректном отображении таких символов в консоли Windows, переключите кодировку на UTF-8:
     >
     > ```cmd
     > chcp 65001
     > ```

  4. Проверьте работу, выполнив команду вывода информации о кластере:

     ```bash
     ydb-dstool -e <bs_endpoint> cluster list
     ```

     - `bs_endpoint` — URI HTTP-эндпоинта кластера — это тот же самый эндпоинт, который обслуживает [Embedded UI](../embedded-ui/index.md). Пример: `http://localhost:8765`.

     Результат:

     ```text
     ┌───────┬───────┬───────┬────────┬────────┬───────┬────────┐
     │ Hosts │ Nodes │ Pools │ Groups │ VDisks │ Boxes │ PDisks │
     ├───────┼───────┼───────┼────────┼────────┼───────┼────────┤
     │ 8     │ 16    │ 1     │ 5      │ 40     │ 1     │ 32     │
     └───────┴───────┴───────┴────────┴────────┴───────┴────────┘
     ```

{% endlist %}
