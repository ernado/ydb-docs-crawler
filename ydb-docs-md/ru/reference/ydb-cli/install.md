---
title: "Установка YDB CLI"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/install?version=v26.1"
doc_path: "ru/reference/ydb-cli/install"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/install.md"
description: "Установка YDB CLI. Linux. macOS. Windows. Чтобы установить YDB CLI, выполните команду: curl -sSL https://install.ydb.tech/cli | bash."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Установка YDB CLI

{% list tabs %}

- Linux

  Чтобы установить YDB CLI, выполните команду:

  ```bash
  curl -sSL https://install.ydb.tech/cli | bash
  ```

  Скрипт установит YDB CLI и добавит путь к исполняемому файлу в переменную окружения `PATH`. Также скрипт сгенерирует файлы автодополнения и выведет инструкцию по включению автодополнения команд и опций в вашей оболочке.

  > [!NOTE]
  > Скрипт дополнит переменную `PATH`, только если его запустить в командной оболочке bash или zsh. Если вы запустили скрипт в другой оболочке, добавьте путь до CLI в переменную `PATH` самостоятельно.
  >
  > Для работы автодополнения в bash необходим установленный пакет `bash-completion`.

  > [!TIP]
  > При нестандартной конфигурации оболочки можно подключить сгенерированные файлы автодополнения из любого rc-файла. Файлы расположены в `~/.local/share/ydb/completion.bash.inc` и `~/.local/share/ydb/completion.zsh.inc` и автоматически обновляются при `ydb update`.

  Чтобы обновить переменные окружения, перезапустите командную оболочку.

- macOS

  Чтобы установить YDB CLI, выполните команду:

  ```bash
  curl -sSL https://install.ydb.tech/cli | bash
  ```

  Скрипт установит YDB CLI и добавит путь до исполняемого файла в переменную окружения `PATH`. Также скрипт сгенерирует файлы автодополнения и выведет инструкцию по включению автодополнения команд и опций в вашей оболочке.

  Чтобы обновить переменные окружения, перезапустите командную оболочку.

- Windows

  YDB CLI можно установить с помощью:

  - PowerShell. Для этого выполните команду:

    ```powershell
    iex (New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/cli-windows')
    ```

    Укажите, нужно ли добавить путь к исполняемому файлу в переменную окружения `PATH`:

    ```text
    Add ydb installation dir to your PATH? [Y/n]
    ```

  - cmd. Для этого выполните команду:

    ```cmd
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/cli-windows'))"
    ```

    Укажите, нужно ли добавить путь к исполняемому в переменную окружения `PATH`:

    ```text
    Add ydb installation dir to your PATH? [Y/n]
    ```

    Чтобы обновить переменные окружения, перезапустите командную оболочку.

  > [!NOTE]
  > YDB CLI использует символы Юникода в выводе некоторых команд. При некорректном отображении таких символов в консоли Windows, переключите кодировку на UTF-8:
  >
  > ```cmd
  > chcp 65001
  > ```

{% endlist %}
