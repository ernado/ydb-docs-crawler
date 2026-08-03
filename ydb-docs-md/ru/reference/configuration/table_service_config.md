---
title: "table_service_config"
url: "https://ydb.tech/docs/ru/reference/configuration/table_service_config?version=v26.1"
doc_path: "ru/reference/configuration/table_service_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/table_service_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/table_service_config.md"
description: "Секция table_service_config содержит параметры конфигурации для сервиса таблиц, включая настройки спиллинга. spilling_service_config."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# table_service_config

Секция `table_service_config` содержит параметры конфигурации для сервиса таблиц, включая настройки спиллинга.

## spilling_service_config {#spilling_service_config}

[Спиллинг](../../concepts/query_execution/spilling.md) — это механизм управления памятью в YDB, который временно сохраняет данные на диск при нехватке оперативной памяти.

### Основные параметры конфигурации {#osnovnye-parametry-konfiguracii}

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      root: ""
      max_total_size: 21474836480
      io_thread_pool:
        workers_count: 2
        queue_size: 1000
```

### Конфигурация директории {#konfiguraciya-direktorii}

#### local_file_config.root {#local_file_configroot}

**Тип:** `string`  
 **По умолчанию:** `""` (временная директория)  
 **Описание:** Файловая директория для сохранения файлов спиллинга.

Для каждого процесса `ydbd` создается отдельная директория с уникальным именем. Директории спиллинга имеют следующий формат имени:

`node_<node_id>_<spilling_service_id>`

Где:

- `node_id` — идентификатор [узла](../../concepts/glossary.md#node)
- `spilling_service_id` — уникальный идентификатор экземпляра, который создается при инициализации [Spilling Service](../../contributor/spilling-service.md) один раз при запуске процесса ydbd

Файлы спиллинга хранятся внутри каждой такой директории.

Пример полного пути к директории спиллинга:

```bash
/tmp/spilling-tmp-<username>/node_1_32860791-037c-42b4-b201-82a0a337ac80
```

Где:

- `/tmp` — значение параметра `root`
- `<username>` — имя пользователя, под которым запускается процесс `ydbd`

**Важные замечания:**

- При запуске процесса все существующие директории спиллинга в указанной директории автоматически удаляются. Директории спиллинга имеют специальный формат имени, который включает идентификатор экземпляра, генерируемый один раз при запуске процесса ydbd. При запуске нового процесса все директории в директории спиллинга, которые соответствуют формату имени, но имеют другой `spilling_service_id` от текущего, удаляются.
- Директория должна иметь достаточные права на запись и чтение для пользователя, под которым запускается ydbd

> [!NOTE]
> Спиллинг выполняется только на [узлах базы данных](../../concepts/glossary.md#database-node).

##### Возможные ошибки {#vozmozhnye-oshibki}

- `Permission denied` — недостаточные права доступа к директории. См. [Permission denied](../../troubleshooting/spilling/permission-denied.md)

#### local_file_config.max_total_size {#local_file_configmax_total_size}

**Тип:** `uint64`  
 **По умолчанию:** `21474836480` (20 GiB)  
 **Описание:** Максимальный суммарный размер всех файлов спиллинга на каждом [узле](../../concepts/glossary.md#node). При превышении лимита операции спиллинга завершаются ошибкой. Общий лимит спиллинга во всем кластере равен сумме значений `max_total_size` со всех узлов.

##### Рекомендации {#rekomendacii}

- Устанавливайте значение исходя из доступного дискового пространства

##### Возможные ошибки {#vozmozhnye-oshibki1}

- `Total size limit exceeded: X/YMb` — превышен максимальный суммарный размер файлов спиллинга. См. [Total size limit exceeded](../../troubleshooting/spilling/total-size-limit-exceeded.md)

### Конфигурация пула потоков {#konfiguraciya-pula-potokov}

> [!NOTE]
> Потоки пула I/O для спиллинга создаются дополнительно к потокам, выделяемым для [акторной системы](../../concepts/glossary.md#actor-system). При планировании количества потоков учитывайте общую нагрузку на систему.
>
> **Важно:** Пул потоков спиллинга отделен от пулов потоков акторной системы.
>
> Для получения информации о настройке пулов потоков акторной системы и их влиянии на производительность системы см. [Конфигурация акторной системы](index.md#actor-system) и [Изменение конфигурации акторной системы](../../devops/configuration-management/configuration-v1/change_actorsystem_configs.md). Для Configuration V2 настройки акторной системы описаны в [настройках Configuration V2](../../devops/configuration-management/configuration-v2/config-settings.md).

#### local_file_config.io_thread_pool.workers_count {#local_file_configio_thread_poolworkers_count}

**Тип:** `uint32`  
 **По умолчанию:** `2`  
 **Описание:** Количество рабочих потоков для обработки операций ввода-вывода спиллинга.

##### Рекомендации {#rekomendacii1}

- Увеличивайте для высоконагруженных систем

##### Возможные ошибки {#vozmozhnye-oshibki2}

- `Can not run operation` — переполнение очереди операций в пуле потоков I/O. См. [Can not run operation](../../troubleshooting/spilling/can-not-run-operation.md)

#### local_file_config.io_thread_pool.queue_size {#local_file_configio_thread_poolqueue_size}

**Тип:** `uint32`  
 **По умолчанию:** `1000`  
 **Описание:** Размер очереди операций спиллинга. Каждая задача отправляет только один блок данных на спиллинг одновременно, поэтому большие значения обычно не требуются.

##### Возможные ошибки {#vozmozhnye-oshibki3}

- `Can not run operation` — переполнение очереди операций в пуле потоков I/O. См. [Can not run operation](../../troubleshooting/spilling/can-not-run-operation.md)

### Управление памятью {#memory-management}

#### Связь с memory_controller_config {#svyaz-s-memory_controller_config}

Активация спиллинга тесно связана с настройками контроллера памяти. Подробная конфигурация `memory_controller_config` описана в [отдельной статье](memory_controller_config.md).

Ключевым параметром для спиллинга является **`activities_limit_percent`**, который определяет объем памяти, выделяемый для активностей по обработке запросов. От этого параметра зависит доступная память для пользовательских запросов и, соответственно, частота активации спиллинга.

#### Влияние на спиллинг {#vliyanie-na-spilling}

- При увеличении `activities_limit_percent` больше памяти доступно для запросов → спиллинг активируется реже
- При уменьшении `activities_limit_percent` меньше памяти доступно для запросов → спиллинг активируется чаще

> [!WARNING]
> Однако важно учитывать, что сам спиллинг также требует память. Если установить `activities_limit_percent` слишком высоким, память может все равно закончиться несмотря на спиллинг, поскольку механизм спиллинга сам потребляет ресурсы памяти.

### Требования к файловой системе {#trebovaniya-k-fajlovoj-sisteme}

#### Файловые дескрипторы {#fajlovye-deskriptory}

> [!NOTE]
> Для получения информации о настройке лимитов файловых дескрипторов при первоначальном развертывании см. раздел [Лимиты файловых дескрипторов](../../devops/deployment-options/manual/initial-deployment/index.md#file-descriptors).

### Примеры конфигурации {#primery-konfiguracii}

#### Высоконагруженная система {#vysokonagruzhennaya-sistema}

Для максимальной производительности в высоконагруженных системах рекомендуется увеличить размер спиллинга и количество рабочих потоков:

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      root: ""
      max_total_size: 107374182400   # 100 GiB
      io_thread_pool:
        workers_count: 8
        queue_size: 2000
```

#### Ограниченные ресурсы {#ogranichennye-resursy}

Для систем с ограниченными ресурсами рекомендуется использовать консервативные настройки:

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      root: ""
      max_total_size: 5368709120     # 5 GiB
      io_thread_pool:
        workers_count: 1
        queue_size: 500
```

### Расширенная конфигурация {#rasshirennaya-konfiguraciya}

#### Включение и отключение спиллинга {#vklyuchenie-i-otklyuchenie-spillinga}

Следующие параметры управляют включением и отключением различных типов спиллинга. Их следует изменять только при наличии специфических требований системы.

##### local_file_config.enable {#local_file_configenable}

**Расположение:** `table_service_config.spilling_service_config.local_file_config.enable`  
 **Тип:** `boolean`  
 **По умолчанию:** `true`  
 **Описание:** Включает или отключает сервис спиллинга. При отключении (`false`) [спиллинг](../../concepts/query_execution/spilling.md) не функционирует, что может привести к ошибкам при обработке больших объемов данных.

##### Возможные ошибки {#vozmozhnye-oshibki4}

- `Spilling Service not started` / `Service not started` — попытка использования спиллинга при выключенном Spilling Service. См. [Spilling Service not started](../../troubleshooting/spilling/service-not-started.md)

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      enable: true
```

##### enable_spilling_nodes {#enable_spilling_nodes}

**Расположение:** `table_service_config.enable_spilling_nodes`  
 **Тип:** `bool`  
 **По умолчанию:** `true`  
 **Описание:** Включает спиллинг на узлах базы данных. При отключении (`false`) спиллинг не функционирует на узлах базы данных.

```yaml
table_service_config:
  enable_spilling_nodes: true
```

##### enable_query_service_spilling {#enable_query_service_spilling}

**Расположение:** `table_service_config.enable_query_service_spilling`  
 **Тип:** `boolean`  
 **По умолчанию:** `true`  
 **Описание:** Глобальная опция, которая включает транспортный спиллинг при передаче данных между задачами.

```yaml
table_service_config:
  enable_query_service_spilling: true
```

> [!NOTE]
> Эта настройка работает совместно с локальной конфигурацией сервиса спиллинга. При отключении (`false`) транспортный спиллинг не функционирует даже при включенном `spilling_service_config`.

### Полный пример {#polnyj-primer}

```yaml
table_service_config:
  enable_spilling_nodes: true
  enable_query_service_spilling: true
  spilling_service_config:
    local_file_config:
      enable: true
      root: "/var/spilling"
      max_total_size: 53687091200    # 50 GiB
      io_thread_pool:
        workers_count: 4
        queue_size: 1500
```

## См. также {#sm-takzhe}

- [Концепция спиллинга](../../concepts/query_execution/spilling.md)
- [Архитектура Spilling Service](../../contributor/spilling-service.md)
- [Устранение неполадок спиллинга](../../troubleshooting/spilling/index.md)
- [Конфигурация контроллера памяти](memory_controller_config.md)
- [Мониторинг YDB](../../devops/observability/monitoring.md)
- [Диагностика производительности](../../troubleshooting/performance/index.md)
