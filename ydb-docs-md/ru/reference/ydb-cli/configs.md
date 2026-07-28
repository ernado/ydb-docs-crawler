---
title: "ru/reference/ydb-cli/configs"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/configs?version=v26.1"
doc_path: "ru/reference/ydb-cli/configs"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/configs.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/configs.md"
description: "Работа с конфигурацией. Примечание. До версии YDB CLI 2.20.0 команды ydb admin cluster config имели формат ydb admin config."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ru/reference/ydb-cli/configs

## Работа с конфигурацией {#rabota-s-konfiguraciej}

> [!NOTE]
> До версии YDB CLI 2.20.0 команды `ydb admin cluster config` имели формат `ydb admin config`.

В этом разделе приведены команды для работы с [конфигурацией кластера](../configuration/index.md) YDB.

- Применение конфигурации `dynconfig.yaml` на кластер:

  ```bash
  ydb admin cluster config replace -f dynconfig.yaml
  ```

- Проверка возможности применения конфигурации `dynconfig.yaml` на кластер (проверить все валидаторы, версия конфигурации в yaml-файле должна быть выше на 1, чем версия конфигурации кластера, имя кластера должно совпадать):

  ```bash
  ydb admin cluster config replace -f dynconfig.yaml --dry-run
  ```

- Применение конфигурации `dynconfig.yaml` на кластер игнорируя проверку версий и кластера (версия и кластер всё равно будут перезаписаны на корректные):

  ```bash
  ydb admin cluster config replace -f dynconfig.yaml --force
  ```

- Получение основной конфигурации кластера:

  ```bash
  ydb admin cluster config fetch
  ```

- Генерация всех возможных конечных конфигураций для `dynconfig.yaml`:

  ```bash
  ydb admin cluster config resolve --all -f dynconfig.yaml
  ```

- Генерация конечной конфигурации для `dynconfig.yaml` при лейблах `tenant=/Root/test` и `canary=true`:

  ```bash
  ydb admin cluster config resolve -f dynconfig.yaml --label tenant=/Root/test --label canary=true
  ```

- Генерация конечной конфигурации для `dynconfig.yaml` для лейблов с узла 1003:

  ```bash
  ydb admin cluster config resolve -f dynconfig.yaml --node-id 100
  ```

- Генерация файла динамической конфигурации на основе статической конфигурации на кластере:

  ```bash
  ydb admin cluster config genereate
  ```

- Инициализация директории с конфигурацией, используя путь до конфигурационного файла:

  ```bash
  ydb admin node config init --config-dir <путь до директории> --from-config <путь до файла конфигурации>
  ```

- Инициализация директории с конфигурацией, используя конфигурацию на кластере:

  ```bash
  ydb admin node config init --config-dir <путь до директории> --seed-node <эндпоинт узла кластера>
  ```

## Работа с временной конфигурацией {#rabota-s-vremennoj-konfiguraciej}

В этом разделе перечислены команды, которые используются для работы с [временной конфигурацией](../../devops/configuration-management/configuration-v1/dynamic-config-volatile-config.md).

- Получение всех временных конфигураций кластера:

  ```bash
  ydb admin volatile-config fetch --all --output-directory <dir>
  ```

- Получение временной конфигурации с id 1 с кластера:

  ```bash
  ydb admin volatile-config fetch --id 1
  ```

- Применение временной конфигурации `volatile.yaml` на кластер:

  ```bash
  ydb admin volatile-config add -f volatile.yaml
  ```

- Удаление временной конфигурации с id 1 и 3 на кластере:

  ```bash
  ydb admin volatile-config drop --id 1 --id 3
  ```

- Удаление всех временных конфигурации на кластере:

  ```bash
  ydb admin volatile-config drop --all
  ```

## Параметры {#parametry}

- `-f, --filename <filename.yaml>` — считать input из файла, `-` для STDIN. Для команд принимающих n файлов (прим. resolve) можно указать несколько раз, тип файла будет определён по полю metadata
- `--output-directory <dir>` — сдампить/порезолвить файлы в директорию
- `--strip-metadata` — выкинуть поле metadata из вывода
- `--all` — расширяет вывод команд до всей конфигурации (см. продвинутое конфигурирование)
- `--allow-unknown-fields` — позволяет игнорировать неизвестные поля в конфигурации

## Сценарии {#scenarii}

### Обновить основную конфигурацию кластера {#obnovit-osnovnuyu-konfiguraciyu-klastera}

```bash
# Получить конфигурацию кластера
ydb admin cluster config fetch > dynconfig.yaml
# Отредактировать конфигурацию вашим любимым редактором
vim dynconfig.yaml
# Применить конфигурацию dynconfig.yaml на кластер
ydb admin cluster config replace -f dynconfig.yaml
```

аналогично в одну строчку:

```bash
ydb admin cluster config fetch | yq '.config.actor_system_config.scheduler.resolution = 128' | ydb admin cluster config replace -f -
```

вывод команды:

```text
OK
```

### Посмотреть конфигурацию для определённого набора лейблов {#posmotret-konfiguraciyu-dlya-opredelyonnogo-nabora-lejblov}

```bash
ydb admin cluster config resolve --remote --label tenant=/Root/db1 --label canary=true
```

вывод команды:

```yaml
---
label_sets:
- dynamic:
    type: COMMON
    value: true
config:
  actor_system_config:
    use_auto_config: true
    node_type: COMPUTE
    cpu_count: 4
```

### Посмотреть конфигурацию для определённого узла {#posmotret-konfiguraciyu-dlya-opredelyonnogo-uzla}

```bash
ydb admin cluster config resolve --remote --node-id <node_id>
```

вывод команды:

```yaml
---
label_sets:
- dynamic:
    type: COMMON
    value: true
config:
  actor_system_config:
    use_auto_config: true
    node_type: COMPUTE
    cpu_count: 4
```

### Сохранить все конфигурации локально {#sohranit-vse-konfiguracii-lokalno}

```bash
ydb admin cluster config fetch --all --output-directory <configs_dir>
ls <configs_dir>
```

вывод команды:

```text
dynconfig.yaml volatile_1.yaml volatile_3.yaml
```

### Посмотреть все конфигурации локально {#posmotret-vse-konfiguracii-lokalno}

```bash
ydb admin cluster config fetch --all
```

вывод команды:

```yaml
---
metadata:
  kind: main
  cluster: unknown
  version: 1
config:
  actor_system_config:
    use_auto_config: true
    node_type: COMPUTE
    cpu_count: 4
allowed_labels: {}
selector_config: []
---
metadata:
  kind: volatile
  cluster: unknown
  version: 1
  id: 1
# some comment example
selectors:
- description: test
  selector:
    tenant: /Root/db1
  config:
    actor_system_config: !inherit
      use_auto_config: true
      cpu_count: 12
```

### Посмотреть конечную конфигурацию для определённого узла из сохраненной локально исходной конфигурации {#posmotret-konechnuyu-konfiguraciyu-dlya-opredelyonnogo-uzla-iz-sohranennoj-lokalno-ishodnoj-konfiguracii}

```bash
ydb admin cluster config resolve -k <configs_dir> --node-id <node_id>
```

вывод команды:

```yaml
---
label_sets:
- dynamic:
    type: COMMON
    value: true
config:
  actor_system_config:
    use_auto_config: true
    node_type: COMPUTE
    cpu_count: 4
```
