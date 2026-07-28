---
title: "Развёртывание кластера с использованием конфигурации V2"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2.md"
description: "Внимание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Развёртывание кластера с использованием конфигурации V2

> [!CAUTION]
> Эта статья посвящена кластерам YDB, в которых используется **конфигурация V2**. Данный способ конфигурирования пока является экспериментальным и доступен только для версий YDB начиная с v25.1. Для использования в продакшене мы рекомендуем выбирать [конфигурацию V1](deployment-configuration-v1.md) — она является основной и официально поддерживаемой для всех кластеров YDB.

## Подготовьте окружение

Перед развёртыванием системы обязательно выполните подготовительные действия. Ознакомьтесь с документом [Подготовка к развертыванию](deployment-preparation.md).

## Создайте директорию для работы {#prepare-directory}

```bash
mkdir deployment
cd deployment
mkdir -p inventory/group_vars/ydb
mkdir files
```

## Создайте конфигурационный файл Ansible

Создайте `ansible.cfg` с конфигурацией Ansible, подходящей для целевой среды развёртывания. Подробности в [справочнике по конфигурации Ansible](https://docs.ansible.com/ansible/latest/reference_appendices/config.html). Дальнейшее руководство предполагает, что поддиректория `./inventory` рабочей директории настроена для использования файлов инвентаризации.

<details>
<summary>Пример стартового ansible.cfg</summary>

> [!NOTE]
> Использование параметра `StrictHostKeyChecking=no` в `ssh_args` повышает удобство автоматизации, но снижает уровень безопасности SSH-соединения (отключает проверку подлинности хоста). Для production-окружений рекомендуется не указывать этот аргумент и настроить доверенные ключи вручную. Используйте этот параметр только для тестовых и временных установок.

```ini
[defaults]
conditional_bare_variables = False
force_handlers = True
forks = 300
gathering = explicit
host_key_checking = False
interpreter_python = /usr/bin/python3
inventory = ./inventory
module_name = shell
pipelining = True
private_role_vars = True
retry_files_enabled = False
timeout = 5
vault_password_file = ./ansible_vault_password_file
verbosity = 1
log_path = ./ydb.log

[ssh_connection]
retries = 5
ssh_args = -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ControlMaster=auto -o ControlPersist=60s -o ControlPath=/tmp/ssh-%h-%p-%r -o ServerAliveCountMax=3 -o ServerAliveInterval=10 
```

</details>

## Создайте основной файл инвентаризации {#inventory-create}

Создайте файл `inventory/group_vars/ydb/all.yaml` и заполните его.

{% list tabs %}

- mirror-3-dc-3nodes

  ```yaml
  # Ansible
  ansible_user: имя_пользователя
  ansible_ssh_private_key_file: "/путь/к/вашему/id_rsa"

  # Система
  system_timezone: UTC
  system_ntp_servers: [time.cloudflare.com, time.google.com, ntp.ripe.net, pool.ntp.org]

  # База данных
  ydb_user: root
  ydb_dbname: db

  # Хранилище
  ydb_disks:
    - name: /dev/vdb
      label: ydb_disk_1
    - name: /dev/vdc
      label: ydb_disk_2
    - name: /dev/vdd
      label: ydb_disk_3
  ydb_pool_kind: ssd
  ydbops_local: true
  ydb_cores_dynamic: 2
  ydb_dynnodes:
    - {"instance": "a", offset: 1}
  ydb_cores_static:  2

  # YDB
  ydb_version: "версия_системы"
  ydb_archive: "{{ ansible_config_file | dirname }}/files/ydbd.tar.gz"

  # Дополнительные параметры
  ydb_allow_format_drives: true
  ydb_skip_data_loss_confirmation_prompt: false
  ```

{% endlist %}

Обязательные настройки, которые нужно адаптировать под окружение в выбранном шаблоне:

1. **Настройка SSH доступа.** Укажите пользователя `ansible_user` и путь к приватному ключу `ansible_ssh_private_key_file`, которые Ansible будет использовать для подключения к вашим серверам.
2. **Пути к блочным устройствам в файловой системе.** В секции `ydb_disks` шаблон предполагает, что `/dev/vda` предназначен для операционной системы, а следующие диски, такие как `/dev/vdb`, — для слоя хранения YDB. Метки дисков создаются плейбуками автоматически, и их имена могут быть произвольными.
3. **Версия системы.** В параметре `ydb_version` укажите номер версии YDB, которую нужно установить. Список доступных версий вы найдёте на странице [загрузок](../../../../downloads/ydb-open-source-database.md).

Рекомендуемые настройки для адаптации:

- `ydb_domain`. Это будет первый компонент пути для всех [объектов схемы](../../../../concepts/glossary.md#scheme-object) в кластере. Например, можно поместить туда название своей компании, регион кластера и т.д.
- `ydb_dbname`. Это будет второй компонент пути для всех [объектов схемы](../../../../concepts/glossary.md#scheme-object) в базе данных. Например, можно поместить туда название сценария использования или проекта.

<details>
<summary>Дополнительные настройки</summary>

Существует несколько вариантов указания того, какие именно исполняемые файлы YDB вы хотите использовать для кластера:

- `ydb_version`: автоматически загрузить один из [официальных релизов YDB](../../../../downloads/index.md#ydb-server) по номеру версии. Например, `23.4.11`.
- `ydb_archive`: локальный путь файловой системы к архиву дистрибутива YDB, [загруженному](../../../../downloads/index.md#ydb-server) или иным образом подготовленному заранее.

Для использования [федеративных запросов](../../../../concepts/query_execution/federated_query/index.md) может потребоваться установка [коннектора](../../../../concepts/query_execution/federated_query/architecture.md#connectors). Плейбук может развернуть [fq-connector-go](../../manual/federated-queries/connector-deployment.md#fq-connector-go) на хостах с динамическими узлами. Используйте следующие настройки:

- `ydb_install_fq_connector` — установите в `true` для установки коннектора.

- Выберите один из доступных вариантов развёртывания исполняемых файлов fq-connector-go:

  - `ydb_fq_connector_version`: автоматически загрузить один из [официальных релизов fq-connector-go](https://github.com/ydb-platform/fq-connector-go/releases) по номеру версии. Например, `v0.7.1`.
  - `ydb_fq_connector_git_version`: автоматически скомпилировать исполняемый файл fq-connector-go из исходного кода, загруженного из [официального репозитория GitHub](https://github.com/ydb-platform/fq-connector-go). Значение настройки — это имя ветки, тега или коммита. Например, `main`.
  - `ydb_fq_connector_archive`: локальный путь файловой системы к архиву дистрибутива fq-connector-go, [загруженному](https://github.com/ydb-platform/fq-connector-go/releases) или иным образом подготовленному заранее.
  - `ydb_fq_connector_binary`: локальные пути файловой системы к исполняемому файлу fq-connector-go, [загруженному](https://github.com/ydb-platform/fq-connector-go/releases) или иным образом подготовленному заранее.

- `ydb_tls_dir` — укажите локальный путь к папке с TLS-сертификатами, подготовленными заранее. Она должна содержать файл `ca.crt` и подкаталоги с именами, соответствующими именам хостов узлов, содержащие сертификаты для данного узла. Если не указано, самоподписанные TLS-сертификаты будут сгенерированы автоматически для всего кластера YDB.

- `ydb_brokers` — перечислите FQDN узлов брокеров. Например:

  ```yaml
  ydb_brokers:
      - static-node-1.ydb-cluster.com
      - static-node-2.ydb-cluster.com
      - static-node-3.ydb-cluster.com
  ```

Оптимальное значение настройки `ydb_database_groups` в разделе `vars` зависит от доступных дисков. Предполагая только одну базу данных в кластере, используйте следующую логику:

- Для промышленных развёртываний используйте диски ёмкостью более 800 ГБ с высокой производительностью IOPS, затем выберите значение для этой настройки на основе топологии кластера:

  - Для `block-4-2` установите `ydb_database_groups` на 95% от общего количества дисков, округляя вниз.
  - Для `mirror-3-dc` установите `ydb_database_groups` на 84% от общего количества дисков, округляя вниз.

- Для тестирования YDB на небольших дисках установите `ydb_database_groups` в 1 независимо от топологии кластера.

Значения переменных `system_timezone` и `system_ntp_servers` зависят от свойств инфраструктуры, на которой развёртывается кластер YDB. По умолчанию `system_ntp_servers` включает набор NTP-серверов без учёта географического расположения инфраструктуры, на которой будет развёрнут кластер YDB. Мы настоятельно рекомендуем использовать локальный NTP-сервер для on-premise инфраструктуры и следующие NTP-серверы для облачных провайдеров:

{% list tabs %}

- AWS

  - `system_timezone`: USA/\<region_name>
  - `system_ntp_servers`: \[169.254.169.123, time.aws.com\] [Подробнее](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html#configure-time-sync) о настройках NTP-серверов AWS.

- Azure

  - О том, как настраивается синхронизация времени на виртуальных машинах Azure, можно прочитать в [этой](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync) статье.

- Alibaba

  - Специфика подключения к NTP-серверам в Alibaba описана в [этой статье](https://www.alibabacloud.com/help/en/ecs/user-guide/alibaba-cloud-ntp-server).

- Yandex Cloud

  - `system_timezone`: Europe/Moscow
  - `system_ntp_servers`: \[0.ru.pool.ntp.org, 1.ru.pool.ntp.org, ntp0.NL.net, ntp2.vniiftri.ru, ntp.ix.ru, ntps1-1.cs.tu-berlin.de\] [Подробнее](https://yandex.cloud/ru/docs/tutorials/infrastructure-management/ntp) о настройках NTP-серверов Yandex Cloud.

{% endlist %}

</details>

## Измените пароль пользователя root {#change-password}

Создайте файл `ansible_vault_password_file` с содержимым:

```bash
password
```

Этот файл содержит пароль, который Ansible будет использовать для автоматического шифрования и расшифровки конфиденциальных данных, например, файлов с паролями пользователей. Благодаря этому пароли не хранятся в открытом виде в репозитории. Подробнее о работе механизма Ansible Vault можно прочитать в [официальной документации](https://docs.ansible.com/ansible/latest/vault_guide/index.html).

Далее необходимо установить пароль для начального пользователя, указанного в настройке `ydb_user` (по умолчанию `root`). Этот пользователь изначально будет иметь полные права доступа в кластере, но при необходимости это можно изменить позже. Создайте `inventory/group_vars/ydb/vault.yaml` со следующим содержимым (замените `<password>` на фактический пароль):

```yaml
ydb_password: <password>
```

Зашифруйте этот файл с помощью команды `ansible-vault encrypt inventory/group_vars/ydb/vault.yaml`.

## Подготовка конфигурационного файла YDB {#ydb-config-prepare}

Создайте файл `files/config.yaml` и заполните его.

{% list tabs %}

- mirror-3-dc-3nodes

  ```yaml
  metadata:
    kind: MainConfig
    cluster: ""
    version: 0
  config:
    yaml_config_enabled: true
    erasure: mirror-3-dc
    fail_domain_type: disk
    self_management_config:
      enabled: true
    default_disk_type: SSD
    host_configs:
    - host_config_id: 1
      drive:
      - path: /dev/disk/by-partlabel/ydb_disk_1
        type: SSD
      - path: /dev/disk/by-partlabel/ydb_disk_2
        type: SSD
      - path: /dev/disk/by-partlabel/ydb_disk_3
        type: SSD
    hosts:
    - host: ydb-node-zone-a.local
      host_config_id: 1
      location:
        body: 1
        data_center: 'zone-a'
        rack: '1'
    - host: ydb-node-zone-b.local
      host_config_id: 1
      location:
        body: 2
        data_center: 'zone-b'
        rack: '1'
    - host: ydb-node-zone-c.local
      host_config_id: 1
      location:
        body: 3
        data_center: 'zone-c'
        rack: '1'
    actor_system_config:
      use_auto_config: true
      cpu_count: 1
    interconnect_config:
      start_tcp: true
      encryption_mode: OPTIONAL
      path_to_certificate_file: "/opt/ydb/certs/node.crt"
      path_to_private_key_file: "/opt/ydb/certs/node.key"
      path_to_ca_file: "/opt/ydb/certs/ca.crt"
    grpc_config:
      cert: "/opt/ydb/certs/node.crt"
      key: "/opt/ydb/certs/node.key"
      ca: "/opt/ydb/certs/ca.crt"
      services_enabled:
      - legacy
    security_config:
      enforce_user_token_requirement: true
    client_certificate_authorization:
      request_client_certificate: true
      client_certificate_definitions:
      - member_groups: ["databaseNodes@cert"]
        subject_terms:
        - short_name: "O"
          values: ["YDB"]
    domains_config:
      security_config:
        monitoring_allowed_sids:
        - "root"
        - "ADMINS"
        - "DATABASE-ADMINS"
        administration_allowed_sids:
        - "root"
        - "ADMINS"
        - "DATABASE-ADMINS"
        viewer_allowed_sids:
        - "root"
        - "ADMINS"
        - "DATABASE-ADMINS"
        register_dynamic_node_allowed_sids:
        - databaseNodes@cert
        - root@builtin
  ```

{% endlist %}

Для ускорения и упрощения первичного развёртывания YDB конфигурационный файл уже содержит большинство настроек для установки кластера. Достаточно заменить стандартные хосты FQDN в разделе `hosts` и пути к дискам на актуальные в разделе `hosts_configs`.

- Раздел `hosts`:

  ```yaml
  ...
  hosts:
    - host: ydb-node-zone-a.local
    host_config_id: 1
    location:
      body: 1
      data_center: 'zone-a'
      rack: '1'
  ...
  ```

- Раздел `hosts_configs`:

  ```yaml
  ...
  host_configs:
  - host_config_id: 1
    drive:
    - path: /dev/disk/by-partlabel/ydb_disk_1
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_2
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_3
      type: SSD
  ...
  ```

Остальные секции и настройки конфигурационного файла остаются без изменений.

Создайте файл `inventory/ydb_inventory.yaml` с содержимым:

```yaml
plugin: ydb_platform.ydb.ydb_inventory
ydb_config: "files/config.yaml"
```

## Разверните кластер YDB

После завершения всех описанных выше подготовительных действий фактическое первоначальное развёртывание кластера сводится к выполнению следующей команды из рабочей директории:

```bash
ansible-playbook ydb_platform.ydb.initial_setup
```

Вскоре после начала будет необходимо подтвердить полную очистку настроенных дисков. Затем завершение развёртывания может занять десятки минут в зависимости от окружения и настроек. Этот плейбук выполняет примерно те же шаги, которые описаны в инструкциях для [ручного развёртывания кластера YDB](../../manual/initial-deployment/index.md).

### Проверьте состояние кластера {#cluster-state}

На последнем этапе плейбук выполнит несколько тестовых запросов с использованием настоящих временных таблиц для проверки корректной работы. При успешном выполнении для каждого сервера будут отображены статус ok, failed=0 и результаты тестовых запросов (3 и 6) при достаточно подробном выводе плейбука.

<details>
<summary>Пример вывода</summary>

```txt
...

TASK [ydb_platform.ydb.ydbd_dynamic : run test queries] *******************************************************************************************************************************************************
ok: [static-node-1.ydb-cluster.com] => (item={'instance': 'a'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "a"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-1.ydb-cluster.com] => (item={'instance': 'b'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "b"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-2.ydb-cluster.com] => (item={'instance': 'a'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "a"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-2.ydb-cluster.com] => (item={'instance': 'b'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "b"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-3.ydb-cluster.com] => (item={'instance': 'a'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "a"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-3.ydb-cluster.com] => (item={'instance': 'b'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "b"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
PLAY RECAP ****************************************************************************************************************************************************************************************************
static-node-1.ydb-cluster.com : ok=167  changed=80   unreachable=0    failed=0    skipped=167  rescued=0    ignored=0
static-node-2.ydb-cluster.com : ok=136  changed=69   unreachable=0    failed=0    skipped=113  rescued=0    ignored=0
static-node-3.ydb-cluster.com : ok=136  changed=69   unreachable=0    failed=0    skipped=113  rescued=0    ignored=0
```

</details>

В результате выполнения плейбука `ydb_platform.ydb.initial_setup` будет создан кластер YDB. Он будет содержать [домен](../../../../concepts/glossary.md#domain) с именем из настройки `ydb_domain` (по умолчанию `Root`), [базу данных](../../../../concepts/glossary.md#database) с именем из настройки `ydb_dbname` (по умолчанию `db`) и начального [пользователя](../../../../concepts/glossary.md#access-user) с именем из настройки `ydb_user` (по умолчанию `root`).

## Дополнительные шаги

Самый простой способ исследовать только что развёрнутый кластер — использовать [Embedded UI](../../../../reference/embedded-ui/index.md), работающий на порту 8765 каждого сервера. Если нет прямого доступа к порту из браузера, можно настроить SSH-туннелирование. Для этого выполните команду `ssh -L 8765:localhost:8765 -i <private-key> <user>@<any-ydb-server-hostname>` на локальной машине (при необходимости добавьте дополнительные опции). После успешного установления соединения можно перейти по URL [localhost:8765](http://localhost:8765) через браузер. Браузер может попросить принять исключение безопасности. Пример того, как это может выглядеть:

![ydb-web-ui](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/_assets/ydb-web-console.png)

После успешного создания кластера YDB проверьте его состояние, используя следующую страницу Embedded UI: [http://localhost:8765/monitoring/cluster/tenants](http://localhost:8765/monitoring/cluster/tenants). Это может выглядеть так:

![ydb-cluster-check](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/_assets/ydb-cluster-check.png)

В этом разделе отображаются следующие параметры кластера YDB, отражающие его состояние:

- `Tablets` — список запущенных [таблеток](../../../../concepts/glossary.md#tablet). Все индикаторы состояния таблеток должны быть зелёными.
- `Nodes` — количество и состояние узлов хранения и узлов базы данных, запущенных в кластере. Индикатор состояния узлов должен быть зелёным, а количество созданных и запущенных узлов должно быть равным. Например, 18/18 для кластера из девяти узлов с одним узлом базы данных на сервер.

Индикаторы `Load` (количество используемой RAM) и `Storage` (количество используемого дискового пространства) также должны быть зелёными.

Проверить состояние группы хранения можно в разделе `storage` — [http://localhost:8765/monitoring/cluster/storage](http://localhost:8765/monitoring/cluster/storage):

![ydb-storage-gr-check](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/_assets/ydb-storage-gr-check.png)

Индикаторы `VDisks` должны быть зелёными, а статус `state` (находится в подсказке при наведении на индикатор Vdisk) должен быть `Ok`. Больше об индикаторах состояния кластера и мониторинге можно прочитать в статье [YDB Monitoring](../../../../reference/embedded-ui/ydb-monitoring.md).

### Тестирование кластера {#testing}

Протестировать кластер можно с помощью встроенных нагрузочных тестов в YDB CLI. Для этого [установите YDB CLI](../../../../reference/ydb-cli/install.md) и создайте профиль с параметрами подключения, заменив заполнители:

```shell
ydb \
  config profile create <profile-name> \
  -d /<ydb-domain>/<ydb-database> \
  -e grpcs://<any-ydb-cluster-hostname>:2135 \
  --ca-file $(pwd)/files/TLS/certs/ca.crt \
  --user root \
  --password-file <path-to-a-file-with-password>
```

Параметры команды и их значения:

- `config profile create` — эта команда используется для создания профиля подключения. Укажите имя профиля. Более подробную информацию о том, как создавать и изменять профили, можно найти в статье [Создание и изменение профиля](../../../../reference/ydb-cli/profile/create.md).
- `-d` — [путь базы данных](../../../../concepts/connect.md#database) в виде `/<домен>/<имя_базы>`. Вместо `<ydb-domain>` укажите значение параметра `ydb_domain`, вместо `<ydb-database>` — `ydb_dbname` из `inventory/group_vars/ydb/all.yaml` (секция «База данных»). Для примера из этого руководства путь будет `/Root/db`.
- `-e` — конечная точка, строка в формате `protocol://host:port`. Допускается указать FQDN любого узла кластера и опустить порт. По умолчанию используется порт 2135.
- `--ca-file` — путь к корневому сертификату для подключений к базе данных по `grpcs`.
- `--user` — пользователь для подключения к базе данных.
- `--password-file` — путь к файлу с паролем. Опустите это, чтобы ввести пароль вручную.

Проверить, создался ли профиль, можно с помощью команды `ydb config profile list`, которая отобразит список профилей. После создания профиля его нужно активировать командой `ydb config profile activate <profile-name>`. Чтобы убедиться, что профиль активирован, можно повторно выполнить команду `ydb config profile list` — активный профиль будет иметь отметку `(active)`.

Для выполнения [YQL](../../../../yql/reference/index.md) запроса можно использовать команду `ydb sql -s 'SELECT 1;'`, которая вернёт результат запроса `SELECT 1` в табличной форме в терминал. После проверки соединения можно создать тестовую таблицу командой:  
 `ydb workload kv init --init-upserts 1000 --cols 4`. Это создаст тестовую таблицу `kv_test`, состоящую из 4 столбцов и 1000 строк. Проверить, что таблица `kv_test` создалась и заполнилась тестовыми данными, можно с помощью команды `ydb sql -s 'select * from kv_test limit 10;'`.

В терминал будет выведена таблица из 10 строк. Теперь можно выполнять тестирование производительности кластера. В статье [Key-Value нагрузка](../../../../reference/ydb-cli/workload-kv.md) описаны несколько типов рабочих нагрузок (`upsert`, `insert`, `select`, `read-rows`, `mixed`) и параметры их выполнения. Пример выполнения тестовой рабочей нагрузки `upsert` с параметром для вывода времени выполнения `--print-timestamp` и стандартными параметрами выполнения: `ydb workload kv run upsert --print-timestamp`:

```text
Window Txs/Sec Retries Errors  p50(ms) p95(ms) p99(ms) pMax(ms)        Timestamp
1          727 0       0       11      27      71      116     2024-02-14T12:56:39Z
2          882 0       0       10      21      29      38      2024-02-14T12:56:40Z
3          848 0       0       10      22      30      105     2024-02-14T12:56:41Z
4          901 0       0       9       20      27      42      2024-02-14T12:56:42Z
5          879 0       0       10      22      31      59      2024-02-14T12:56:43Z
...
```

После завершения тестов таблицу `kv_test` можно удалить командой: `ydb workload kv clean`. Подробнее о параметрах создания тестовой таблицы и тестах можно прочитать в статье [Key-Value нагрузка](../../../../reference/ydb-cli/workload-kv.md).

## См. также {#sm-takzhe}

- [Дополнительные примеры конфигурации Ansible](https://github.com/ydb-platform/ydb-ansible-examples)
- [Перезапуск кластеров YDB, развёрнутых с помощью Ansible](../restart.md)
- [Обновление конфигурации кластеров YDB, развёрнутых с Ansible](../update-config.md)
- [Обновление версии YDB на кластерах, развёрнутых с помощью Ansible](../update-executable.md)
