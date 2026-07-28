---
title: "Running YDB in Docker"
url: "https://ydb.tech/docs/en/reference/docker/start?version=v26.1"
doc_path: "en/reference/docker/start"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/docker/start.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/docker/start.md"
description: "Before start. Create a folder for testing YDB and use it as the current working directory: mkdir ~/ydbd && cd ~/ydbd mkdir ydb_data mkdir ydb_certs."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Running YDB in Docker

## Before start

Create a folder for testing YDB and use it as the current working directory:

```bash
mkdir ~/ydbd && cd ~/ydbd
mkdir ydb_data
mkdir ydb_certs
```

## Launching a container with YDB in Docker

Example of the YDB startup command in Docker with detailed comments:

```bash
docker_args=(
    -d                              # run container in background and print container ID
    --rm                            # automatically remove the container
    --name ydb-local                # assign a name to the container
    --hostname localhost            # hostname
    --platform linux/amd64          # platform
    -p 2135:2135                    # publish a container grpcs port to the host
    -p 2136:2136                    # publish a container grpc port to the host
    -p 8765:8765                    # publish a container http port to the host
    -p 9092:9092                    # publish a container port to the host that provides Kafka compatibility
    -v $(pwd)/ydb_certs:/ydb_certs  # mount directory with TLS certificates
    -v $(pwd)/ydb_data:/ydb_data    # mount working directory
    -e GRPC_TLS_PORT=2135           # grpcs port, needs to match what's published above
    -e GRPC_PORT=2136               # grpc port, needs to match what's published above
    -e MON_PORT=8765                # http port, needs to match what's published above
    -e YDB_KAFKA_PROXY_PORT=9092    # port, needs to match what's published above
    ydbplatform/local-ydb:latest
)

docker run "${docker_args[@]}"
```

> [!NOTE]
> If you are using a Mac with an Apple Silicon processor, emulate the x86_64 CPU instruction set with [Rosetta](https://support.apple.com/en-us/102527):
>
> - [colima](https://github.com/abiosoft/colima) with the `colima start --arch aarch64 --vm-type=vz --vz-rosetta` options.
> - [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/) with installed and enabled Rosetta 2.
>
> If Rosetta 2 is not enabled, add the `-e YDB_USE_IN_MEMORY_PDISKS=true` parameter to the command for running the Docker container. For more information, see [Configuring the YDB Docker container](configuration.md).

For more information about environment variables available when running a Docker container with YDB, see [Configuring the YDB Docker container](configuration.md).

With the parameters specified in the example above and running Docker locally, [Embedded UI](../embedded-ui/index.md) YDB will be available at [http://localhost:8765](http://localhost:8765).

For more information about stopping and deleting a Docker container with YDB, see [Docker stop](cleanup.md).

### Overriding the configuration file

By default, when starting a Docker container for YDB, a built-in [configuration file](../configuration/index.md) is used, which provides standard operating parameters. To use your own config, mount it at `/ydb_data/cluster/kikimr_configs/config.yaml`:

```bash
docker run "${docker_args[@]}" \
  -v $(pwd)/ydb_config/my-ydb-config.yaml:/ydb_data/cluster/kikimr_configs/config.yaml
```

For users who are not experienced with Docker, it's important to understand how to properly mount a configuration file into the container. Below is a step-by-step example:

1. Run the container without specifying a configuration file and without mounting the data directory, so that it generates a default configuration:

   ```bash
   docker run -d \
     --rm \
     --name ydb-local \
     --hostname localhost \
     --platform linux/amd64 \
     -v $(pwd)/ydb_certs:/ydb_certs \
     -e GRPC_TLS_PORT=2135 \
     -e GRPC_PORT=2136 \
     -e MON_PORT=8765 \
     ydbplatform/local-ydb:latest
   ```

2. Create a directory for your configuration files and copy the generated configuration file from the container directly to it:

   ```bash
   mkdir ydb_config
   docker cp ydb-local:/ydb_data/cluster/kikimr_configs/config.yaml ydb_config/my-ydb-config.yaml
   ```

3. Stop the container if it's still running, and remove the created data directory:

   ```bash
   docker stop ydb-local
   rm -rf ydb_data
   ```

4. Edit the copied configuration file `ydb_config/my-ydb-config.yaml` as needed.

5. When running the container, mount the edited configuration file at `/ydb_data/cluster/kikimr_configs/config.yaml`:

   ```bash
   docker_args=(
       -d
       --rm
       --name ydb-local
       --hostname localhost
       --platform linux/amd64
       -p 2135:2135
       -p 2136:2136
       -p 8765:8765
       -v $(pwd)/ydb_data:/ydb_data
       -v $(pwd)/ydb_certs:/ydb_certs
       -v $(pwd)/ydb_config/my-ydb-config.yaml:/ydb_data/cluster/kikimr_configs/config.yaml
       -e GRPC_TLS_PORT=2135
       -e GRPC_PORT=2136
       -e MON_PORT=8765
       ydbplatform/local-ydb:latest
   )

   docker run "${docker_args[@]}"
   ```

In this example, the local file `ydb_config/my-ydb-config.yaml` replaces the default configuration inside the container.
