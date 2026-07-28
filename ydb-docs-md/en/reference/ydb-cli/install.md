---
title: "Installing the YDB CLI"
url: "https://ydb.tech/docs/en/reference/ydb-cli/install?version=v26.1"
doc_path: "en/reference/ydb-cli/install"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/install.md"
description: "Installing the YDB CLI. Linux. macOS. Windows. To install the YDB CLI, run the command: curl -sSL https://install.ydb.tech/cli | bash."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Installing the YDB CLI

{% list tabs %}

- Linux

  To install the YDB CLI, run the command:

  ```bash
  curl -sSL https://install.ydb.tech/cli | bash
  ```

  The script will install the YDB CLI and add the executable file path to the `PATH` environment variable. It will also generate shell completion files and print instructions on how to enable tab completion for commands and options.

  > [!NOTE]
  > The script will update the `PATH` variable only if you run it in the bash or zsh command shell. If you run the script in a different shell, add the path to the CLI to the `PATH` variable yourself.
  >
  > Shell completion for bash requires the `bash-completion` package to be installed.

  > [!TIP]
  > If you use a non-standard shell configuration, you can source the generated completion files from any rc file. The files are located at `~/.local/share/ydb/completion.bash.inc` and `~/.local/share/ydb/completion.zsh.inc`, and are kept up to date automatically by `ydb update`.

  To update the environment variables, restart the command shell.

- macOS

  To install the YDB CLI, run the command:

  ```bash
  curl -sSL https://install.ydb.tech/cli | bash
  ```

  The script will install the YDB CLI and add the executable file path to the `PATH` environment variable. It will also generate shell completion files and print instructions on how to enable tab completion for commands and options.

  To update the environment variables, restart the command shell.

- Windows

  You can install the YDB CLI using:

  **PowerShell.** To do this, run the command:

  ```powershell
  iex (New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/cli-windows')
  ```

  Specify whether to add the executable file path to the `PATH` environment variable:

  ```text
  Add ydb installation dir to your PATH? [Y/n]
  ```

  **cmd.** To do this, run the command:

  ```cmd
  @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/cli-windows'))"
  ```

  Specify whether to add the executable file path to the `PATH` environment variable:

  ```text
  Add ydb installation dir to your PATH? [Y/n]
  ```

  To update the environment variables, restart the command shell.

  > [!NOTE]
  > The YDB CLI uses Unicode characters in the output of some commands. If these characters aren't displayed correctly in the Windows console, switch the encoding to UTF-8:
  >
  > ```cmd
  > chcp 65001
  > ```

{% endlist %}
