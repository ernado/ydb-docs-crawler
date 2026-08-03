---
title: "domains_config"
url: "https://ydb.tech/docs/ru/reference/configuration/domains_config?version=v26.1"
doc_path: "ru/reference/configuration/domains_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/domains_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/domains_config.md"
description: "Данный раздел содержит конфигурацию кластера YDB, включая конфигурации Blob Storage (хранилища бинарных объектов) и State Storage (хранилища состояний)."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# domains_config

Данный раздел содержит конфигурацию кластера YDB, включая [конфигурации Blob Storage](domains_config.md#domains-blob) (хранилища бинарных объектов) и [State Storage](domains_config.md#domains-state) (хранилища состояний).

> [!NOTE]
> Не требуется для работы кластера с [автоматической конфигурацией](../../devops/configuration-management/index.md) State Storage и статической группы.

## Синтаксис {#sintaksis}

```yaml
domains_config:
  domain:
  - name: <имя корня кластера>
    storage_pool_types: <конфигурация Blob Storage>
  state_storage: <конфигурация State Storage>
  security_config: <конфигурация безопасности>
```

> [!NOTE]
> Формально, поле `domain` может содержать много элементов, так как это список. Но имеет значение только первый элемент, остальные будут проигнорированы (в кластере может быть только один «домен»).

## Конфигурация Blob Storage {#domains-blob}

> [!NOTE]
> Не требуется для работы кластера с [автоматической конфигурацией](../../devops/configuration-management/index.md) State Storage и статической группы.

Данный раздел определяет один или более типов пулов хранения, доступных в кластере для данных в базах данных, со следующими возможностями конфигурации:

- имя пула хранения;
- свойства устройств (например, тип дисков);
- шифрование данных (вкл/выкл);
- [режим отказоустойчивости](../../concepts/topology.md).

### Синтаксис {#sintaksis1}

```yaml
domains_config:
  domain:
    ...
    storage_pool_types:
    - kind: <имя пула хранения>
      pool_config:
        box_id: 1
        encryption_mode: <опциональный, укажите 1 для шифрования данных на диске>
        erasure_species: <имя режима отказоустойчивости - none, block-4-2, or mirror-3-dc>
        kind: <имя пула хранения - укажите то же значение, что выше>
        pdisk_filter:
        - property:
          - type: <тип устройства для сопоставления с указанным в host_configs.drive.type>
        vdisk_kind: Default
    - kind: <имя пула хранения>
```

Каждой базе данных в кластере назначается как минимум один из доступных пулов хранения, выбираемый в операции создания базы данных. Имена пулов хранения среди назначенных могут быть использованы в атрибуте `DATA` при определении групп колонок в операторах YQL [`CREATE TABLE`](../../yql/reference/syntax/create_table/family.md)/[`ALTER TABLE`](../../yql/reference/syntax/alter_table/family.md).

## Конфигурация State Storage {#domains-state}

> [!NOTE]
> Не требуется для работы кластера с [автоматической конфигурацией](../../devops/configuration-management/index.md) State Storage и статической группы.

State Storage (хранилище состояний) — это независимое хранилище в памяти для изменяемых данных, поддерживающее внутренние процессы YDB. Оно хранит реплики данных на множестве назначенных узлов.

Обычно State Storage не требует масштабирования в целях повышения производительности, поэтому количество узлов в нём следует делать как можно меньшим с учётом необходимого уровня отказоустойчивости.

Доступность State Storage является ключевой для кластера YDB, так как влияет на все базы данных, независимо от того какие пулы хранения в них используются. Для обеспечения отказоустойчивости State Storate его узлы должны быть выбраны таким образом, чтобы гарантировать рабочее большинство в случае ожидаемых отказов.

Для выбора узлов State Storage можно воспользоваться следующими рекомендациями:

| Тип кластера | Мин количество  <br>узлов | Рекомендации по выбору |
| --- | --- | --- |
| Без отказоустойчивости | 1 | Выберите один произвольный узел. |
| В пределах одной зоны доступности | 5 | Выберите пять узлов в разных доменах отказа пула хранения block-4-2, для гарантии, что большинство в трёх работающих узлах (из пяти) остаётся при сбое двух доменов. |
| Геораспределенный | 9 | Выберите три узла в разных доменах отказа внутри каждой из трёх зон доступности пула хранения mirror-3-dc для гарантии, что большинство в пяти работающих узлов (из девяти) остаётся при сбое зоны доступности + домена отказа. |

При развёртывании State Storage на кластерах, в которых применяется несколько пулов хранения с возможным сочетанием режимов отказоустойчивости, рассмотрите возможность увеличения количества узлов с распространением их на разные пулы хранения, так как недоступность State Storage приводит к недоступности всего кластера.

```yaml
domains_config:
  ...
  state_storage:
  - ring:
      node: <массив узлов StateStorage>
      nto_select: <количество реплик данных в StateStorage>
    ssid: 1
```

Каждый клиент State Storage (например, таблетка DataShard) использует `nto_select` узлов для записи копий его данных в State Storage. Если State Storage состоит из большего количества узлов чем `nto_select`, то разные узлы могут быть использованы для разных клиентов. Поэтому необходимо обеспечить, чтобы любое подмножество из `nto_select` узлов в пределах State Storage отвечало критериям отказоустойчивости.

Для `nto_select` должны использоваться нечётные числа, так как использование чётных чисел не улучшает отказоустойчивость по сравнению с ближайшим меньшим нечётным числом.

## Полные примеры конфигурации {#polnye-primery-konfiguracii}

### Один дата-центр с `block-4-2` erasure {#erasure}

```yaml
domains_config:
  domain:
  - name: Root
    storage_pool_types:
    - kind: ssd
      pool_config:
        box_id: 1
        erasure_species: block-4-2
        kind: ssd
        pdisk_filter:
        - property:
          - type: SSD
        vdisk_kind: Default
  state_storage:
  - ring:
      node: [1, 2, 3, 4, 5, 6, 7, 8]
      nto_select: 5
    ssid: 1
```

### Несколько дата-центров с `mirror-3-dc` erasure {#erasure1}

```yaml
domains_config:
  domain:
  - name: Root
    storage_pool_types:
    - kind: ssd
      pool_config:
        box_id: 1
        erasure_species: mirror-3-dc
        kind: ssd
        pdisk_filter:
        - property:
          - type: SSD
        vdisk_kind: Default
  state_storage:
  - ring:
      node: [1, 2, 3, 4, 5, 6, 7, 8, 9]
      nto_select: 9
    ssid: 1
```

### Без отказоустойчивости (`none`) - для тестирования {#dlya-testirovaniya}

```yaml
domains_config:
  domain:
  - name: Root
    storage_pool_types:
    - kind: ssd
      pool_config:
        box_id: 1
        erasure_species: none
        kind: ssd
        pdisk_filter:
        - property:
          - type: SSD
        vdisk_kind: Default
  state_storage:
  - ring:
      node: [1]
      nto_select: 1
    ssid: 1
```

### Несколько типов пулов хранения {#neskolko-tipov-pulov-hraneniya}

```yaml
domains_config:
  domain:
  - name: Root
    storage_pool_types:
    - kind: ssd
      pool_config:
        box_id: '1'
        erasure_species: block-4-2
        kind: ssd
        pdisk_filter:
        - property:
          - {type: SSD}
        vdisk_kind: Default
    - kind: rot
      pool_config:
        box_id: '1'
        erasure_species: block-4-2
        kind: rot
        pdisk_filter:
        - property:
          - {type: ROT}
        vdisk_kind: Default
    - kind: rotencrypted
      pool_config:
        box_id: '1'
        encryption_mode: 1
        erasure_species: block-4-2
        kind: rotencrypted
        pdisk_filter:
        - property:
          - {type: ROT}
        vdisk_kind: Default
    - kind: ssdencrypted
      pool_config:
        box_id: '1'
        encryption_mode: 1
        erasure_species: block-4-2
        kind: ssdencrypted
        pdisk_filter:
        - property:
          - {type: SSD}
        vdisk_kind: Default
  state_storage:
  - ring:
      node: [1, 16, 31, 46, 61, 76, 91, 106]
      nto_select: 5
    ssid: 1
```
