---
title: "Миграция на конфигурацию V2"
url: "https://ydb.tech/docs/ru/devops/configuration-management/migration/migration-to-v2?version=v26.1"
doc_path: "ru/devops/configuration-management/migration/migration-to-v2"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/migration/migration-to-v2.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/migration/migration-to-v2.md"
description: "Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Миграция на конфигурацию V2

> [!WARNING]
> Эта статья посвящена кластерам YDB, в которых используется [конфигурация V2](../configuration-v2/index.md). Данный способ конфигурирования пока является экспериментальным и доступен только для версий YDB начиная с v25.1. Для использования в продакшене мы рекомендуем выбирать [конфигурацию V1](../index.md) — она является основной и официально поддерживаемой для всех кластеров YDB.

Данный документ содержит инструкцию по миграции с [конфигурации V1](../configuration-v1/config-overview.md) на [конфигурацию V2](../configuration-v2/config-overview.md).

В конфигурации V1 существует два различных механизма применения конфигурационных файлов:

- [статическая конфигурация](../configuration-v2/config-overview.md#static-config) управляет [узлами хранения](../../../concepts/glossary.md#storage-node) кластера YDB и требует ручного размещения файлов на каждом узле кластера;
- [динамическая конфигурация](../configuration-v2/config-overview.md#dynamic-config) управляет [узлами базы данных](../../../concepts/glossary.md#database-node) кластера YDB и загружается в кластер централизованно с помощью команд YDB CLI.

В конфигурации V2 этот процесс унифицирован: единый конфигурационный файл загружается в систему через команды YDB CLI, автоматически доставляясь на все узлы кластера.

Компоненты [State Storage](../../../concepts/glossary.md#state-storage) и [статической группы](../../../concepts/glossary.md#static-group) кластера YDB являются ключевыми для корректной работы кластера. При работе с конфигурацией V1 данные компоненты настраиваются вручную через задание секций `domains_config` и `blob_storage_config` в конфигурационном файле.  
 В конфигурации V2 возможна [автоматическая конфигурация](../configuration-v2/config-overview.md) этих компонентов без указания соответствующих секций в конфигурационном файле.

## Исходное состояние {#ishodnoe-sostoyanie}

Миграция на конфигурацию V2 может быть осуществлена в случае выполнения следующих условий:

1. Кластер YDB [обновлён](../../deployment-options/manual/update-executable.md) до версии 25.1 и выше.
2. Кластер YDB сконфигурирован с файлом [конфигурации V1](../configuration-v2/config-overview.md#static-config) `config.yaml`, расположенным в файловой системе узлов и подключённым через аргумент `ydbd --yaml-config`.
3. В конфигурационном файле кластера заданы разделы `domains_config` и `blob_storage_config` для настройки State Storage и статической группы соответственно.

## Проверка текущей версии конфигурации {#proverka-tekushej-versii-konfiguracii}

Перед началом миграции убедитесь, что ваш кластер работает на конфигурации V1. Узнать текущую версию конфигурации на узлах можно несколькими способами, описанными в статье [Проверка версии конфигурации](../check-config-version.md).

Продолжать выполнение данной инструкции следует только в том случае, если узлы работают на версии конфигурации V1. Если на всех узлах уже включена версия V2, миграция не требуется.

## Инструкция по миграции на конфигурацию V2 {#instrukciya-po-migracii-na-konfiguraciyu-v2}

Для того чтобы перевести кластер YDB на конфигурацию V2, необходимо проделать следующие шаги:

1. Проверить наличие файла [динамической конфигурации](../configuration-v2/config-overview.md#dynamic-config) в кластере. Для этого необходимо выполнить команду [ydb admin cluster config fetch](../../../reference/ydb-cli/commands/configuration/cluster/fetch.md):

   ```bash
   ydb -e grpc://<node.ydb.tech>:2135 admin cluster config fetch > config.yaml
   ```

   В случае отсутствия такой конфигурации в кластере команда выдаст сообщение:

   ```bash
   No config returned.
   ```

   Если файл найден, следует использовать его и пропустить следующий шаг данной инструкции.

2. В случае отсутствия файла динамической конфигурации в кластере выполнить команду генерации файла динамической конфигурации [ydb admin cluster config generate](../../../reference/ydb-cli/commands/configuration/cluster/generate.md). Файл будет сгенерирован на основе файла статической конфигурации, расположенного на узлах кластера.

   ```bash
   ydb -e grpc://<node.ydb.tech>:2135 admin cluster config generate > config.yaml
   ```

3. Добавить в полученный на шаге 1 или 2 файл `config.yaml` следующее поле:

   ```yaml
   feature_flags:
       ...
       switch_to_config_v2: true
   ```

   <details>
   <summary>Подробнее</summary>

   Включение данного флага означает, что за хранение конфигурации и операции над ней теперь отвечает таблетка [DS Controller](../../../concepts/glossary.md#ds-controller), а не таблетка [Console](../../../concepts/glossary.md#console). Это переключает основной механизм управления конфигурацией кластера.

   </details>

4. Разместить файл `config.yaml` на всех узлах кластера, заменив им предыдущий файл конфигурации.

5. Создать директорию для работы узла YDB с конфигурацией на каждом из узлов. В случае запуска нескольких узлов кластера на одном хосте создайте отдельные директории под каждый узел. Инициализируйте директорию, выполнив команду [ydb admin node config init](../../../reference/ydb-cli/commands/configuration/node/init.md) на каждом из узлов. В параметре `--from-config` укажите путь к файлу `config.yaml`, размещённому на узлах ранее.

   ```bash
   sudo mkdir -p /opt/ydb/config-dir
   sudo chown -R ydb:ydb /opt/ydb/config-dir
   ydb admin node config init --config-dir /opt/ydb/config-dir --from-config /opt/ydb/cfg/config.yaml
   ```

   <details>
   <summary>Подробнее</summary>

   В дальнейшем система самостоятельно будет сохранять актуальную конфигурацию в указанные директории.

   </details>

6. Перезапустить все узлы кластера с помощью процедуры [rolling-restart](../../../maintenance/manual/node_restarting.md), добавив опцию `ydbd --config-dir` при запуске узла с указанием пути до директории, а также убрав опцию `ydbd --yaml-config`.

   {% list tabs %}

   - Вручную

     При ручном запуске добавьте опцию `--config-dir` к команде `ydbd server`, не указывая опцию `--yaml-config`:

     ```bash
     ydbd server --config-dir /opt/ydb/config-dir
     ```

   - С использованием systemd

     При использовании systemd добавьте опцию `--config-dir` к команде `ydbd server` в конфигурационный файл systemd, а также удалите опцию `--yaml-config`:

     ```ini
     ExecStart=/opt/ydb/bin/ydbd server --config-dir /opt/ydb/config-dir
     ```

     После обновления файла systemd выполните следующую команду, чтобы применить изменения:

     ```bash
     sudo systemctl daemon-reload
     ```

   {% endlist %}

7. Загрузить полученный ранее конфигурационный файл `config.yaml` в систему с помощью команды [ydb admin cluster config replace](../../../reference/ydb-cli/commands/configuration/cluster/replace.md):

   ```bash
   ydb -e grpc://<node.ydb.tech>:2135 cluster config replace -f config.yaml
   ```

   Команда запросит подтверждение на выполнение операции `This command may damage your cluster, do you want to continue? [y/N]`, в ответ на этот запрос необходимо согласиться и ввести `y`.

   <details>
   <summary>Подробнее</summary>

   После выполнения команды конфигурационный файл загрузится во внутреннее хранилище таблетки [DS Controller](../../../concepts/glossary.md#ds-controller) и сохранится в директориях, указанных в опции `--config-dir` на каждом узле. С этого момента любое изменение конфигурации на существующих узлах выполняется с помощью [специальных команд](../configuration-v2/update-config.md) YDB CLI. Также при запуске узла актуальная конфигурация будет автоматически загружаться из конфигурационной директории.

   </details>

8. Получить текущую конфигурацию кластера с помощью [ydb admin cluster config fetch](../../../reference/ydb-cli/commands/configuration/cluster/fetch.md):

   ```bash
   ydb -e grpc://<node.ydb.tech>:2135 admin cluster config fetch > config.yaml
   ```

   Файл `config.yaml` должен совпадать с конфигурационными файлами, разложенными по узлам кластера, за исключением поля `metadata.version`, которое должно быть больше на единицу по сравнению с версией на узлах кластера.

9. Добавить в `config.yaml` в разделе `config` следующий блок:

   ```yaml
   self_management_config:
     enabled: true
   ```

   <details>
   <summary>Подробнее</summary>

   Данная секция отвечает за включение механизма [распределённой конфигурации](../../../concepts/glossary.md#distributed-configuration) в кластере. Хранение конфигурации и любые операции над ней будут осуществляться через данный механизм.

   </details>

10. Загрузить обновлённый конфигурационный файл в кластер с помощью [ydb admin cluster config replace](../../../reference/ydb-cli/commands/configuration/cluster/replace.md):

    ```bash
    ydb -e grpc://<node.ydb.tech>:2135 cluster config replace -f config.yaml
    ```

11. Перезапустить все [узлы хранения](../../../concepts/glossary.md#storage-node) кластера с помощью процедуры [rolling restart](../../../reference/ydbops/rolling-restart-scenario.md).

12. При наличии секции `config.domains_config.security_config` в файле `config.yaml` вынести её на уровень выше — в секцию `config`.

13. Удалить из файла `config.yaml` секции `config.blob_storage_config` и `config.domains_config`.

14. Загрузить обновлённый конфигурационный файл в кластер:

    ```bash
    ydb -e grpc://<node.ydb.tech>:2135 cluster config replace -f config.yaml
    ```

    <details>
    <summary>Подробнее</summary>

    После загрузки конфигурации кластер YDB будет переведён в режим автоматического управления конфигурацией [State Storage](../../../reference/configuration/index.md#domains-state) и [статической группой](../../../reference/configuration/index.md#blob_storage_config) с помощью механизма распределённой конфигурации.

    </details>

Убедиться в успешном завершении миграции можно, проверив версию конфигурации на узлах кластера одним из способов, описанных в статье [Проверка версии конфигурации](../check-config-version.md). На всех узлах кластера версия `Configuration version` должна быть равна `v2`.

## Результат {#rezultat}

В результате проделанных действий кластер будет переведён на режим конфигурации V2. Управление единой конфигурацией осуществляется с помощью [специальных команд](../configuration-v2/update-config.md) YDB CLI, статическая группа и State Storage управляются системой автоматически.
