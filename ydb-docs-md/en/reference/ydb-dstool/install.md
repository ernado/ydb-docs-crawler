---
title: "Installing the YDB DSTool"
url: "https://ydb.tech/docs/en/reference/ydb-dstool/install?version=v26.1"
doc_path: "en/reference/ydb-dstool/install"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-dstool/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-dstool/install.md"
description: "Linux. macOS. Windows. To install the YDB DSTool, follow these steps: Run the command: curl -sSL 'https://install.ydb.tech/dstool' | bash."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Installing the YDB DSTool

{% list tabs %}

- Linux

  To install the YDB DSTool, follow these steps:

  1. Run the command:

     ```bash
     curl -sSL 'https://install.ydb.tech/dstool' | bash
     ```

     The script will install the YDB DSTool. If the script is run from a `bash` or `zsh` shell, it will also add the `ydb-dstool` executable to the `PATH` environment variable. Otherwise, you can run it from the `~/ydb/bin` folder or add it to `PATH` manually.

  2. To update the environment variables, restart the command shell.

  3. Test it by running the command that shows cluster information:

     ```bash
     ydb-dstool -e <bs_endpoint> cluster list
     ```

     - `bs_endpoint`: URI of the cluster's HTTP endpoint, the same endpoint that serves the [Embedded UI](../embedded-ui/index.md). Example: `http://localhost:8765`.

     Result:

     ```text
     ┌───────┬───────┬───────┬────────┬────────┬───────┬────────┐
     │ Hosts │ Nodes │ Pools │ Groups │ VDisks │ Boxes │ PDisks │
     ├───────┼───────┼───────┼────────┼────────┼───────┼────────┤
     │ 8     │ 16    │ 1     │ 5      │ 40     │ 1     │ 32     │
     └───────┴───────┴───────┴────────┴────────┴───────┴────────┘
     ```

- macOS

  To install the YDB DSTool, follow these steps:

  1. Run the command:

     ```bash
     curl -sSL 'https://install.ydb.tech/dstool' | bash
     ```

     The script will install the YDB DSTool. If the script is run from a `bash` or `zsh` shell, it will also add the `ydb-dstool` executable to the `PATH` environment variable. Otherwise, you can run it from the `~/ydb/bin` folder or add it to `PATH` manually.

  2. To update the environment variables, restart the command shell.

  3. Test it by running the command that shows cluster information:

     ```bash
     ydb-dstool -e <bs_endpoint> cluster list
     ```

     - `bs_endpoint`: URI of the cluster's HTTP endpoint, the same endpoint that serves the [Embedded UI](../embedded-ui/index.md). Example: `http://localhost:8765`.

     Result:

     ```text
     ┌───────┬───────┬───────┬────────┬────────┬───────┬────────┐
     │ Hosts │ Nodes │ Pools │ Groups │ VDisks │ Boxes │ PDisks │
     ├───────┼───────┼───────┼────────┼────────┼───────┼────────┤
     │ 8     │ 16    │ 1     │ 5      │ 40     │ 1     │ 32     │
     └───────┴───────┴───────┴────────┴────────┴───────┴────────┘
     ```

- Windows

  To install the YDB DSTool, follow these steps:

  1. Run the command:

     - in **PowerShell**:

       ```powershell
       iex (New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/dstool-windows')
       ```

     - in **CMD**:

       ```cmd
       @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://install.ydb.tech/dstool-windows'))"
       ```

  2. Specify whether to add `ydb-dstool` to the `PATH` environment variable:

     ```text
     Add ydb-dstool installation dir to your PATH? [Y/n]
     ```

  3. To update the environment variables, restart the command shell.

     > [!NOTE]
     > The YDB DSTool uses Unicode characters in the output of some commands. If these characters aren't displayed correctly in the Windows console, switch the encoding to UTF-8:
     >
     > ```cmd
     > chcp 65001
     > ```

  4. Test it by running the command that shows cluster information:

     ```bash
     ydb-dstool -e <bs_endpoint> cluster list
     ```

     - `bs_endpoint`: URI of the cluster's HTTP endpoint, the same endpoint that serves the [Embedded UI](../embedded-ui/index.md). Example: `http://localhost:8765`.

     Result:

     ```text
     ┌───────┬───────┬───────┬────────┬────────┬───────┬────────┐
     │ Hosts │ Nodes │ Pools │ Groups │ VDisks │ Boxes │ PDisks │
     ├───────┼───────┼───────┼────────┼────────┼───────┼────────┤
     │ 8     │ 16    │ 1     │ 5      │ 40     │ 1     │ 32     │
     └───────┴───────┴───────┴────────┴────────┴───────┴────────┘
     ```

{% endlist %}
