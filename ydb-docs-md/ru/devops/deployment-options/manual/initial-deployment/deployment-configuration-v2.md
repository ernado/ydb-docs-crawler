---
title: "Развёртывание кластера с использованием конфигурации V2"
url: "https://ydb.tech/docs/ru/devops/deployment-options/manual/initial-deployment/deployment-configuration-v2?version=v26.1"
doc_path: "ru/devops/deployment-options/manual/initial-deployment/deployment-configuration-v2"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/manual/initial-deployment/deployment-configuration-v2.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/manual/initial-deployment/deployment-configuration-v2.md"
description: "Внимание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Развёртывание кластера с использованием конфигурации V2

> [!CAUTION]
> Эта статья посвящена кластерам YDB, в которых используется **конфигурация V2**. Данный способ конфигурирования пока является экспериментальным и доступен только для версий YDB начиная с v25.1. Для использования в продакшене мы рекомендуем выбирать [конфигурацию V1](deployment-configuration-v1.md) — она является основной и официально поддерживаемой для всех кластеров YDB.

## Подготовьте окружение {#deployment-preparation}

Перед развёртыванием системы обязательно выполните подготовительные действия. Ознакомьтесь с документом [Подготовка к развертыванию](deployment-preparation.md).

## Подготовьте конфигурационные файлы {#config}

Подготовьте конфигурационный файл YDB:

```yaml
metadata:
  kind: MainConfig
  cluster: ""
  version: 0
config:
  erasure: mirror-3-dc
  fail_domain_type: disk
  self_management_config:
    enabled: true
  default_disk_type: SSD
  host_configs:
  - host_config_id: 1
    drive:
    - path: /dev/disk/by-partlabel/ydb_disk_ssd_01
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_ssd_02
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_ssd_03
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
      rack: '2'
  - host: ydb-node-zone-c.local
    host_config_id: 1
    location:
      body: 3
      data_center: 'zone-c'
      rack: '3'
  actor_system_config:
    use_auto_config: true
    cpu_count: 8
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
    bootstrap_allowed_sids:
    - "root"
    - "ADMINS"
    - "DATABASE-ADMINS"
  client_certificate_authorization:
    request_client_certificate: true
    client_certificate_definitions:
        - member_groups: ["ADMINS"]
          subject_terms:
          - short_name: "O"
            values: ["YDB"]
```

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
    - path: /dev/disk/by-partlabel/ydb_disk_ssd_01
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_ssd_02
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_ssd_03
      type: SSD
  ...
  ```

Остальные секции и настройки конфигурационного файла остаются без изменений.

Сохраните конфигурационный файл YDB под именем `/tmp/config.yaml` на каждом сервере кластера.

Более подробная информация по созданию файла конфигурации приведена в разделе [Параметры конфигурации кластера](../../../../reference/configuration/index.md).

## Скопируйте ключи и сертификаты TLS на каждый сервер {#tls-copy-cert}

Подготовленные ключи и сертификаты TLS необходимо скопировать в защищённый каталог на каждом из узлов кластера YDB.

Подробности подготовки — в разделе [Подготовка ключей и сертификатов TLS](deployment-preparation.md#tls-certificates). Если сертификаты сгенерированы скриптом `tls_cert_gen`, возьмите `ca.crt` из каталога `CA/certs/YYYY-MM-DD_hh-mi-ss` (подставьте метку времени из вывода скрипта или выберите нужный каталог в `CA/certs/`), а `node.crt`, `node.key` и `web.pem` — из подкаталога с именем FQDN этого сервера в `ydb-ca-nodes.txt`. Перенесите эти четыре файла на соответствующий сервер кластера (например, через `scp`) в один локальный каталог.

Для административных команд в разделах [Инициализируйте кластер](deployment-configuration-v2.md#initialize-cluster), [Создайте базу данных](deployment-configuration-v2.md#create-db), [Настройка учётных записей](deployment-configuration-v2.md#security-setup) и [Протестируйте работу с созданной базой](deployment-configuration-v2.md#try-first-db) в примерах используется путь `~/CA/certs/`. Чтобы не менять пути в командах, на каждом сервере создайте каталог `~/CA/certs/` в домашнем каталоге того пользователя, от имени которого вы выполняете эти команды, и поместите в него четыре файла: `ca.crt`, `node.crt`, `node.key` и `web.pem`.

Каталог `/opt/ydb/certs/` (см. ниже) нужен для запуска `ydbd` от пользователя `ydb`; `~/CA/certs/` — для административных команд из последующих разделов.

На каждом сервере выполните команды ниже: сначала разместите файлы в `~/CA/certs/`, затем скопируйте их в `/opt/ydb/certs/`.

```bash
mkdir -p ~/CA/certs
cp -v ca.crt ~/CA/certs/
cp -v node.crt ~/CA/certs/
cp -v node.key ~/CA/certs/
cp -v web.pem ~/CA/certs/
sudo mkdir -p /opt/ydb/certs
sudo cp -v ~/CA/certs/ca.crt /opt/ydb/certs/
sudo cp -v ~/CA/certs/node.crt /opt/ydb/certs/
sudo cp -v ~/CA/certs/node.key /opt/ydb/certs/
sudo cp -v ~/CA/certs/web.pem /opt/ydb/certs/
sudo chown -R ydb:ydb /opt/ydb/certs
sudo chmod 700 /opt/ydb/certs
```

Перед запуском `ydbd` убедитесь, что процессы от пользователя `ydb` смогут прочитать сертификат мониторинга (иначе при `--mon-cert /opt/ydb/certs/web.pem` будет ошибка `Permission denied`):

```bash
sudo -u ydb test -r /opt/ydb/certs/web.pem
```

При успешной проверке команда завершается без вывода, код возврата `0` (проверить: `echo $?` → `0`). Если файл отсутствует или права настроены неверно — код `1`; повторите `chown`/`chmod` из блока выше и убедитесь, что на этот узел скопирован `web.pem` этого хоста.

## Подготовьте конфигурацию на статических узлах кластера {#podgotovte-konfiguraciyu-na-staticheskih-uzlah-klastera}

Создайте на каждой машине пустую директорию `opt/ydb/cfg` для работы кластера с конфигурацией. В случае запуска нескольких узлов кластера на одной машине создайте отдельные директории под каждый узел.

```bash
sudo mkdir -p /opt/ydb/cfg
sudo chown -R ydb:ydb /opt/ydb/cfg
```

Выполнив специальную команду на каждой машине, инициализируйте эту директорию файлом конфигурации.

```bash
sudo /opt/ydb/bin/ydb admin node config init --config-dir /opt/ydb/cfg --from-config /tmp/config.yaml
```

Исходный файл `/tmp/config.yaml` после выполнения этой команды больше не используется, его можно удалить.

## Запустите статические узлы {#start-storage}

{% list tabs %}

- Вручную

  Запустите сервис хранения данных YDB на каждом статическом узле кластера. Поочередно выполните команды ниже. Не вставляйте все строки разом вместе с `sudo su - ydb` — иначе следующие команды могут выполниться не от пользователя `ydb`.

  После шага 1 дождитесь приглашения `ydb@...$`.

  На шаге 4 дождитесь вывода `ydbd` в этом же терминале.

  1. Переключитесь на пользователя `ydb`:

     ```bash
     sudo su - ydb
     ```

  2. Перейдите в каталог установки:

     ```bash
     cd /opt/ydb
     ```

  3. Укажите путь к библиотекам:

     ```bash
     export LD_LIBRARY_PATH=/opt/ydb/lib
     ```

  4. Запустите статический узел:

     ```bash
     /opt/ydb/bin/ydbd server --log-level 3 --syslog --tcp --yaml-config /opt/ydb/cfg/config.yaml --grpcs-port 2135 --ic-port 19001 --mon-port 8765 --mon-cert /opt/ydb/certs/web.pem --node static
     ```

     При успешном старте в выводе появится, в частности, `Determined node ID: ...`. Если [проверка `web.pem`](deployment-configuration-v2.md#tls-copy-cert) не пройдена, здесь будет ошибка `Permission denied` для `/opt/ydb/certs/web.pem`.

- С использованием systemd

  Создайте на каждом сервере, где будет размещен статический узел кластера, конфигурационный файл systemd `/etc/systemd/system/ydbd-storage.service` по приведенному ниже образцу. Образец файла также можно [скачать из репозитория](https://github.com/ydb-platform/ydb/blob/main/ydb/deploy/systemd_services/ydbd-storage.service).

  ```ini
  [Unit]
  Description=YDB storage node
  After=network-online.target rc-local.service
  Wants=network-online.target
  StartLimitInterval=10
  StartLimitBurst=15

  [Service]
  Restart=always
  RestartSec=1
  User=ydb
  PermissionsStartOnly=true
  StandardOutput=syslog
  StandardError=syslog
  SyslogIdentifier=ydbd
  SyslogFacility=daemon
  SyslogLevel=err
  Environment=LD_LIBRARY_PATH=/opt/ydb/lib
  ExecStart=/opt/ydb/bin/ydbd server --log-level 3 --syslog --tcp \
      --yaml-config  /opt/ydb/cfg/config.yaml \
      --grpcs-port 2135 --ic-port 19001 --mon-port 8765 \
      --mon-cert /opt/ydb/certs/web.pem --node static
  LimitNOFILE=65536
  LimitCORE=0
  LimitMEMLOCK=3221225472

  [Install]
  WantedBy=multi-user.target
  ```

  Запустите сервис на каждом статическом узле YDB:

  ```bash
  sudo systemctl start ydbd-storage
  ```

{% endlist %}

В конфигурации V2 встроенный web-интерфейс (Embedded UI) доступен для входа только **после** инициализации кластера. Сразу после запуска статических узлов попытка входа на экране логина завершится ошибкой — это нормально. Проверку UI выполните после раздела [Инициализируйте кластер](deployment-configuration-v2.md#initialize-cluster).

## Инициализируйте кластер {#initialize-cluster}

Операция инициализации кластера осуществляет настройку набора статических узлов, перечисленных в конфигурационном файле кластера, для хранения данных YDB.

Для инициализации кластера потребуются файлы `ca.crt`, `node.crt` и `node.key` из каталога `~/CA/certs/` (см. раздел [Скопируйте ключи и сертификаты TLS на каждый сервер](deployment-configuration-v2.md#tls-copy-cert)). Пути к ним указываются в командах ниже (для bootstrap — все три, для получения токена — `ca.crt`).

На одном из серверов хранения в составе кластера выполните команды:

Инициализируйте кластер:

```bash
export LD_LIBRARY_PATH=/opt/ydb/lib
/opt/ydb/bin/ydb --ca-file ~/CA/certs/ca.crt \
    --client-cert-file ~/CA/certs/node.crt \
    --client-cert-key-file ~/CA/certs/node.key \
    -e grpcs://`hostname -f`:2135 \
    admin cluster bootstrap --uuid <строка>
echo $?
```

После инициализации кластера для выполнения дальнейших административных команд необходимо предварительно получить аутентификационный токен.

```bash
/opt/ydb/bin/ydb -e grpcs://`hostname -f`:2135 -d /Root --ca-file ~/CA/certs/ca.crt \
--user root --no-password auth get-token --force > auth_token
```

При успешном выполнении инициализации кластера выведенный на экран код завершения команды инициализации кластера должен быть нулевым.

После успешной инициализации кластера проверьте работоспособность статических узлов через встроенный web-интерфейс YDB (Embedded UI):

1. Откройте в браузере адрес `https://<static-node.ydb.tech>:8765`, где `<static-node.ydb.tech>` — FQDN сервера с запущенным статическим узлом;
2. Войдите под учётной записью `root` с пустым паролем (пароль задаётся позже, в разделе [Настройка учётных записей](deployment-configuration-v2.md#security-setup));
3. Перейдите на вкладку **Nodes**;
4. Убедитесь, что в списке отображаются все статические узлы кластера.

![Ручная установка, запущенные статические узлы](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/deployment-options/_assets/manual_installation_1.png)

## Создайте базу данных {#create-db}

Для работы со строковыми или колоночными таблицами необходимо создать как минимум одну базу данных и запустить процесс или процессы, обслуживающие эту базу данных (динамические узлы).

Для выполнения административной команды создания базы данных потребуется файл `ca.crt` из каталога `~/CA/certs/` (см. раздел [Скопируйте ключи и сертификаты TLS на каждый сервер](deployment-configuration-v2.md#tls-copy-cert)).

При создании базы данных устанавливается первоначальное количество используемых групп хранения, определяющее доступную пропускную способность ввода-вывода и максимальную емкость хранения. Количество групп хранения может быть при необходимости увеличено после создания базы данных.

На одном из серверов хранения в составе кластера выполните команды:

```bash
export LD_LIBRARY_PATH=/opt/ydb/lib
/opt/ydb/bin/ydbd --ca-file ~/CA/certs/ca.crt -s grpcs://`hostname -f`:2135 -f auth_token \
    admin database /Root/testdb create ssd:8
echo $?
```

При успешном создании базы данных, выведенный на экран код завершения команды должен быть нулевым.

В приведенном выше примере команд используются следующие параметры:

- `/Root` - имя корневого домена, сгенерированного автоматически при инициализации кластера;
- `testdb` - имя создаваемой базы данных;
- `ssd:8` - задает пул хранения для базы данных и количество групп в нем. Имя пула (`ssd`) должно соответствовать типу диска, указанному в конфигурации кластера (например, в `default_disk_type`), и является регистронезависимым. Число после двоеточия — это количество выделяемых групп хранения.

## Запустите динамические узлы {#start-dynnode}

Первый динамический узел запустите на одном из серверов кластера, где уже подготовлены каталоги `/opt/ydb/certs` и `/opt/ydb/cfg` и работает статический узел. Совмещение статического и динамического узла на одном сервере допустимо (см. [Требования](deployment-preparation.md#requirements)).

Для топологий из примера (`mirror-3-dc-3nodes` — три сервера, `mirror-3-dc-9nodes` — девять) для отказоустойчивости и масштабирования запустите дополнительные динамические узлы на тех же серверах, что и статические — по одному на каждом из оставшихся хостов.

{% list tabs %}

- Вручную

  Запустите динамический узел YDB для базы `/Root/testdb`. Поочередно выполните команды ниже. Не вставляйте все строки разом вместе с `sudo su - ydb` — иначе следующие команды могут выполниться не от пользователя `ydb`.

  После шага 1 дождитесь приглашения `ydb@...$`.

  На шаге 4 дождитесь вывода `ydbd` в этом же терминале. В команде ниже замените `<ydb-static-node1>`, `<ydb-static-node2>`, `<ydb-static-node3>` на FQDN трёх любых серверов со статическими узлами.

  1. Переключитесь на пользователя `ydb`:

     ```bash
     sudo su - ydb
     ```

  2. Перейдите в каталог установки:

     ```bash
     cd /opt/ydb
     ```

  3. Укажите путь к библиотекам:

     ```bash
     export LD_LIBRARY_PATH=/opt/ydb/lib
     ```

  4. Запустите динамический узел:

     ```bash
     /opt/ydb/bin/ydbd server --grpcs-port 2136 --grpc-ca /opt/ydb/certs/ca.crt --ic-port 19002 --ca /opt/ydb/certs/ca.crt --mon-port 8766 --mon-cert /opt/ydb/certs/web.pem --yaml-config /opt/ydb/cfg/config.yaml --tenant /Root/testdb --grpc-cert /opt/ydb/certs/node.crt --grpc-key /opt/ydb/certs/node.key --node-broker grpcs://<ydb-static-node1>:2135 --node-broker grpcs://<ydb-static-node2>:2135 --node-broker grpcs://<ydb-static-node3>:2135
     ```

     Если [проверка `web.pem`](deployment-configuration-v2.md#tls-copy-cert) не пройдена, будет ошибка `Permission denied` для `/opt/ydb/certs/web.pem`.

- С использованием systemd

  Создайте конфигурационный файл systemd `/etc/systemd/system/ydbd-testdb.service` по приведенному ниже образцу. Образец файла также можно [скачать из репозитория](https://github.com/ydb-platform/ydb/blob/main/ydb/deploy/systemd_services/ydbd-testdb.service).

  ```ini
  [Unit]
  Description=YDB testdb dynamic node
  After=network-online.target rc-local.service
  Wants=network-online.target
  StartLimitInterval=10
  StartLimitBurst=15

  [Service]
  Restart=always
  RestartSec=1
  User=ydb
  PermissionsStartOnly=true
  StandardOutput=syslog
  StandardError=syslog
  SyslogIdentifier=ydbd
  SyslogFacility=daemon
  SyslogLevel=err
  Environment=LD_LIBRARY_PATH=/opt/ydb/lib
  ExecStart=/opt/ydb/bin/ydbd server \
      --grpcs-port 2136 --grpc-ca /opt/ydb/certs/ca.crt \
      --ic-port 19002 --ca /opt/ydb/certs/ca.crt \
      --mon-port 8766 --mon-cert /opt/ydb/certs/web.pem \
      --yaml-config  /opt/ydb/cfg/config.yaml \
      --tenant /Root/testdb \
      --grpc-cert /opt/ydb/certs/node.crt \
      --grpc-key /opt/ydb/certs/node.key \
      --node-broker grpcs://<ydb-static-node1>:2135 \
      --node-broker grpcs://<ydb-static-node2>:2135 \
      --node-broker grpcs://<ydb-static-node3>:2135
  LimitNOFILE=65536
  LimitCORE=0
  LimitMEMLOCK=32212254720

  [Install]
  WantedBy=multi-user.target
  ```

  В примере команды выше `<ydb-static-node1>` , `<ydb-static-node2>`, `<ydb-static-node3>` - FQDN трех любых серверов, на которых запущены статические узлы кластера.

  Запустите динамический узел YDB для базы `/Root/testdb`:

  ```bash
  sudo systemctl start ydbd-testdb
  ```

{% endlist %}

## Настройка учетных записей {#security-setup}

В командах ниже `<node.ydb.tech>` — FQDN сервера с запущенным динамическим узлом базы `/Root/testdb` (порт gRPC `2136`). При выполнении команд по SSH на этом сервере можно указать endpoint: `grpcs://$(hostname -f):2136`.

1. Установите пароль для учетной записи `root`, используя полученный ранее токен:

   ```bash
   ydb --ca-file ~/CA/certs/ca.crt -e grpcs://<node.ydb.tech>:2136 -d /Root/testdb --token-file auth_token \
       yql -s 'ALTER USER root PASSWORD "passw0rd"'
   ```

   Вместо значения `passw0rd` подставьте необходимый пароль. Сохраните пароль в отдельный файл. Последующие команды от имени пользователя `root` будут выполняться с использованием пароля, передаваемого с помощью ключа `--password-file <path_to_user_password>`. Также пароль можно сохранить в профиле подключения, как описано в [документации YDB CLI](../../../../reference/ydb-cli/profile/index.md).

2. Создайте дополнительные учетные записи:

   ```bash
   ydb --ca-file ~/CA/certs/ca.crt -e grpcs://<node.ydb.tech>:2136 -d /Root/testdb --user root --password-file <path_to_root_pass_file> \
       yql -s 'CREATE USER user1 PASSWORD "passw0rd"'
   ```

3. Установите права учетных записей, включив их во встроенные группы:

   ```bash
   ydb --ca-file ~/CA/certs/ca.crt -e grpcs://<node.ydb.tech>:2136 -d /Root/testdb --user root --password-file <path_to_root_pass_file> \
       yql -s 'ALTER GROUP `ADMINS` ADD USER user1'
   ```

При выполнении команд создания учётных записей и присвоения групп клиент YDB CLI будет запрашивать ввод пароля пользователя `root`. Избежать многократного ввода пароля можно, создав профиль подключения, как описано в [документации YDB CLI](../../../../reference/ydb-cli/profile/index.md).

## Протестируйте работу с созданной базой {#try-first-db}

1. Установите YDB CLI, как описано в [документации](../../../../reference/ydb-cli/install.md).

В командах ниже `<node.ydb.tech>` — тот же FQDN динамического узла базы `/Root/testdb`, что в разделе [Настройка учетных записей](deployment-configuration-v2.md#security-setup).

1. Создайте тестовую строковую (`test_row_table`) или колоночную таблицу (`test_column_table`):

{% list tabs %}

- Создание строковой таблицы

  ```bash
  ydb --ca-file ~/CA/certs/ca.crt -e grpcs://<node.ydb.tech>:2136 -d /Root/testdb --user root \
      yql -s 'CREATE TABLE `testdir/test_row_table` (id Uint64, title Utf8, PRIMARY KEY (id));'
  ```

- Создание колоночной таблицы

  ```bash
  ydb --ca-file ~/CA/certs/ca.crt -e grpcs://<node.ydb.tech>:2136 -d /Root/testdb --user root \
      yql -s 'CREATE TABLE `testdir/test_column_table` (id Uint64 NOT NULL, title Utf8, PRIMARY KEY (id)) WITH (STORE = COLUMN);'
  ```

{% endlist %}

## Проверка доступа ко встроенному web-интерфейсу {#proverka-dostupa-ko-vstroennomu-web-interfejsu}

Для проверки доступа ко встроенному web-интерфейсу YDB достаточно открыть в Web-браузере страницу с адресом `https://<static-node.ydb.tech>:8765`, где `<static-node.ydb.tech>` - FQDN сервера, на котором запущен любой статический узел YDB.

В Web-браузере должно быть настроено доверие в отношении центра регистрации, выпустившего сертификаты для кластера YDB, в противном случае будет отображено предупреждение об использовании недоверенного сертификата.

Если в кластере включена аутентификация, в Web-браузере должен отобразиться запрос логина и пароля. После ввода верных данных аутентификации должна отобразиться начальная страница встроенного web-интерфейса. Описание доступных функций и пользовательского интерфейса приведено в разделе [Использование встроенного web-интерфейса](../../../../reference/embedded-ui/index.md).

> [!NOTE]
> Обычно для обеспечения доступа ко встроенному web-интерфейсу YDB настраивают отказоустойчивый HTTP-балансировщик на базе программного обеспечения `haproxy`, `nginx` или аналогов. Детали настройки HTTP-балансировщика выходят за рамки стандартной инструкции по установке YDB.

## Особенности установки YDB в незащищенном режиме {#osobennosti-ustanovki-ydb-v-nezashishennom-rezhime}

> [!WARNING]
> Мы не рекомендуем использовать незащищенный режим работы YDB ни при эксплуатации, ни при разработке приложений.

Описанная выше процедура установки предусматривает развёртывание YDB в стандартном защищенном режиме.

Незащищённый режим работы YDB предназначен для решения тестовых задач, преимущественно связанных с разработкой и тестированием программного обеспечения YDB. В незащищенном режиме:

- трафик между узлами кластера, а также между приложениями и кластером использует незашифрованные соединения;
- не используется аутентификация пользователей (включение аутентификации при отсутствии шифрования трафика не имеет смысла, поскольку логин и пароль в такой конфигурации передавались бы через сеть в открытом виде).

Установка YDB для работы в незащищенном режиме производится в порядке, описанном выше, со следующими исключениями:

1. При подготовке к установке не требуется формировать сертификаты и ключи TLS, и не выполняется копирование сертификатов и ключей на узлы кластера.

2. Из конфигурационных файлов кластерных узлов исключаются секции `security_config`, `interconnect_config` и `grpc_config`.

3. Используются упрощенный вариант команд запуска статических и динамических узлов кластера: исключаются опции с именами файлов сертификатов и ключей, используется протокол `grpc` вместо `grpcs` при указании точек подключения.

4. Пропускается ненужный в незащищенном режиме шаг по получению токена аутентификации перед выполнением инициализации кластера и созданием базы данных.

5. Команда инициализации кластера выполняется в следующей форме:

   ```bash
   export LD_LIBRARY_PATH=/opt/ydb/lib
   ydb admin cluster bootstrap --uuid <строка>
   echo $?
   ```

6. Команда создания базы данных выполняется в следующей форме:

   ```bash
   export LD_LIBRARY_PATH=/opt/ydb/lib
   /opt/ydb/bin/ydbd admin database /Root/testdb create ssd:1
   ```

7. При обращении к базе данных из YDB CLI и приложений используется протокол grpc вместо grpcs, и не используется аутентификация.
