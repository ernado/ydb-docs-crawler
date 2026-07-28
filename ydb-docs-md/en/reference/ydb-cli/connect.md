---
title: "Connecting the CLI to and authenticating with a database"
url: "https://ydb.tech/docs/en/reference/ydb-cli/connect?version=v26.1"
doc_path: "en/reference/ydb-cli/connect"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/connect.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/connect.md"
description: "Connecting the CLI to and authenticating with a database."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Connecting the CLI to and authenticating with a database

Most of the YDB CLI commands relate to operations on a YDB database and require establishing a connection to it to be executed.

The YDB CLI uses the following sources to determine the database to connect to and the [authentication mode](../../security/authentication.md) to use with it (listed in descending priority):

1. The command line.
2. The profile set in the `--profile` command-line option.
3. Environment variables.
4. The activated profile.

For the YDB CLI to try connecting to the database, these steps must result in the [endpoint](../../concepts/connect.md#endpoint) and [database path](../../concepts/connect.md#database).

If all the steps are completed, but the YDB CLI did not determine the authentication mode, requests will be sent to the YDB server without adding authentication data. This may let you successfully work with locally deployed YDB clusters that require no authentication. For all databases available over the network, such requests will be rejected by the server with an authentication error returned.

To learn about potential situations where the YDB CLI won't try to connect to the database, see the [Error messages](connect.md#errors) below.

## Command line parameters {#command-line-pars}

DB connection options in the command line are specified before defining the command and its parameters:

```bash
ydb <connection_options> <command> <command_options>
```

- `-e, --endpoint <endpoint>` is the [endpoint](../../concepts/connect.md#endpoint), that is, the main connection parameter that allows finding a YDB server on the network. If no port is specified, port 2135 is used. If no protocol is specified, gRPCs (with encryption) is used in YDB CLI public builds.
- `-d, --database <database>` is the [database path](../../concepts/connect.md#database).
- `--no-discovery` means do not perform discovery (client balancing) for ydb cluster connection. If this option is set the user provided endpoint (by `-e` option) will be used to setup a connections.

The authentication mode and parameters are selected by setting one of the following options:

- `--token-file <filepath>`: Enables the **Access Token** authentication mode using the contents of the file specified in this option.
- `--yc-token-file <filepath>`: Enables the **Refresh Token** authentication mode using the contents of the file specified in this option.
- `--use-metadata-credentials` : The **Metadata** authentication mode is used.
- `--sa-key-file <filepath>`: Enables the **Service Account Key** authentication mode, where the key and other parameters are taken from the JSON file specified in this option.

- `--user <username>` : The username and password based authentication mode is used with the username set in this option value. Additionally , you can specify:

  - `--password-file <filename>` : The password is read from the specified file.
  - `--no-password` : Defines an empty password. The password will be requested interactively if none of the password identification options listed above are specified in the command line parameters.

- `--oauth2-key-file <filepath>`: Enables the [**OAuth 2.0 token exchange**](https://www.rfc-editor.org/rfc/rfc8693) authentication mode, where the key and other parameters are taken from the [JSON file](../ydb-sdk/auth.md#oauth2-key-file-format) specified in this option. The `--iam-endpoint` option sets the token exchange endpoint in the `<schema>://<host>:<port>/<path>` format (via the YDB CLI option, profile, or environment variable).

If several of the above options are set simultaneously in the command line, the CLI returns an error asking you to specify only one:

```bash
$ ydb --use-metadata-credentials --iam-token-file ~/.ydb/token scheme ls
More than one auth method were provided via options. Choose exactly one of them
Try "--help" option for more info.
```

When using authentication modes that involve token rotation along with regularly re-requesting them from IAM (**Refresh Token**, **Service Account Key**, or **OAuth 2.0 token exchange**), a special parameter can be set to indicate where the IAM service is located:

- `--iam-endpoint <URL>` : Sets the URL of the IAM service to request new tokens in authentication modes with token rotation. The default value is `"iam.api.cloud.yandex.net"`.

## Parameters from the profile set by the command-line option {#profile}

If a certain connection parameter is not specified in the command line when calling the YDB CLI, it tries to determine it by the [profile](profile/index.md) set in the `--profile` command-line option.

In the profile, you can define most of the variables that have counterparts in the [Command line parameters](connect.md#command-line-pars) section. Their values are processed in the same way as command line parameters.

## Parameters from environment variables {#env}

If you did not explicitly specify a profile or authentication parameters at the command line, the YDB CLI attempts to determine the authentication mode and parameters from the YDB CLI environment as follows:

- If the value of the `IAM_TOKEN` environment variable is set, the **Access Token** authentication mode is used, where this variable value is passed.
- Otherwise, if the value of the `YC_TOKEN` environment variable is set, the **Refresh Token** authentication mode is used and the token to transfer to the IAM endpoint is taken from this variable value when repeating the request.
- Otherwise, if the value of the `USE_METADATA_CREDENTIALS` environment variable is set to 1, the **Metadata** authentication mode is used.
- Otherwise, if the value of the `SA_KEY_FILE` environment variable is set, the **Service Account Key** authentication mode is used and the key is taken from the file whose name is specified in this variable.

- If the value of the `YDB_USER` or `YDB_PASSWORD` environment variable is set, the username and password based authentication mode is used. The username is read from the `YDB_USER` variable. If it is not set, an error saying `User password was provided without user name` is returned. The password is read from the `YDB_PASSWORD` variable. If it is not set, then, depending on whether the `--no-password` command-line option is specified, either an empty password is used or a password is requested interactively.

- Otherwise, if the `YDB_OAUTH2_KEY_FILE` environment variable value is set, the [**OAuth 2.0 token exchange**](https://www.rfc-editor.org/rfc/rfc8693) authentication mode is used, and the token exchange parameters are taken from a [JSON file](../ydb-sdk/auth.md#oauth2-key-file-format) specified in this variable. The `--iam-endpoint` option is used to set the token exchange endpoint in the `<schema>://<host>:<port>/<path>` format (via a YDB CLI option, profile, or environment variable).

## Parameters from the activated profile {#activated-profile}

If some connection parameter could not be determined in the previous steps, and you did not explicitly specify a profile at the command line with the `--profile` option, the YDB CLI attempts to use the connection parameters from the [activated profile](profile/activate.md).

## Error messages {#errors}

### Errors before attempting to establish a DB connection

If the CLI completed all the steps listed at the beginning of this article but failed to determine the [endpoint](../../concepts/connect.md#endpoint), the command terminates with the error `Missing required option 'endpoint'`.

If the CLI completed all the steps listed at the beginning of this article but failed to determine the [database path](../../concepts/connect.md#database), the command terminates with the error message `Missing required option 'database'`.

If the authentication mode is known, but the necessary additional parameters are not, the command is aborted and an error message describing the issue is returned:

- `(No such file or directory) util/system/file.cpp:857: can't open "<filepath>" with mode RdOnly|Seq (0x00000028)`: Couldn't open and read the file `<filepath>` specified in a parameter passing the file name and path.

## Additional parameters {#additional}

When using gRPCs (with encryption), you may need to [select a root certificate](../../concepts/connect.md#tls-cert).

- `--ca-file <filepath>`: Root certificate PEM file for a TLS connection.

## Authentication {#whoami}

The YDB CLI [`discovery whoami`](commands/discovery-whoami.md) auxiliary command lets you check the account that you actually used to authenticate with the server.
