---
title: "Domain-specific language (DSL) конфигурации кластера"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v1/dynamic-config-selectors?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v1/dynamic-config-selectors"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v1/dynamic-config-selectors.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v1/dynamic-config-selectors.md"
description: "YDB предоставляет DSL конфигурации кластера для более гибкого управления применением настроек к узлам кластера. Селекторы."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Domain-specific language (DSL) конфигурации кластера

YDB предоставляет [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) конфигурации кластера для более гибкого управления применением настроек к узлам кластера.

## Селекторы {#selectors-intro}

Основной сущностью DSL являются **селекторы**. Они позволяют переопределять часть конфигурации или конфигурацию целиком для определённых узлов или групп узлов. Например, они могут быть использованы для включения экспериментальной функциональности узлов определённой базы данных.  
 Каждый селектор представляет собой массив переопределений и расширений основной конфигурации. У каждого селектора есть поле `description`, которое может использоваться для хранения произвольной строки описания. Поле `selector` представляет собой набор правил, по которым определяется, должен ли данный селектор применяться для определённого узла, то есть для какого-либо набора лейблов. Поле `config` описывает правила переопределения.  
 Селекторы применяются в порядке их описания.

> [!NOTE]
> Механизм селекторов поддерживается только для [узлов баз данных](../../../concepts/glossary.md#database-node).

## Лейблы {#labels}

Лейблы — это особые метки, с помощью которых можно пометить узлы или группы узлов. Каждый узел имеет набор автоматически задаваемых лейблов:

- `node_id` — внутренний идентификатор узла в системе;
- `node_host` — `hostname` узла, получаемый при старте;
- `tenant` — база данных, обслуживаемая данным узлом;
- `dynamic` — является ли данный узел динамическим (true/false).

И, опционально, какие-либо дополнительные лейблы, явно определённые пользователем при запуске процесса `ydbd` на узле при помощи аргументов командной строки. Например: `--label example=test`.

## Пример использования селекторов {#selectors-example}

В примере ниже определяется общая конфигурация актор-системы и конфигурация для тенанта `large_tenant`. По умолчанию при такой конфигурации актор-система считает, что на узле 4 ядра, а на узлах тенанта `large_tenant` — по 16 ядер, при этом также переопределяется тип узлов для актор-системы на `COMPUTE`.

```yaml
metadata:
  cluster: ""
  version: 8
config:
  actor_system_config:
    use_auto_config: true
    node_type: STORAGE
    cpu_count: 4

# Раздел используется как хинт при генерации возможных конфигураций при помощи команды resolve
allowed_labels:
  dynamic:
    type: string

selector_config:
- description: large_tenant has bigger nodes with 16 cpu # произвольная строка с описанием
  selector: # селектор для всех узлов тенанта large_tenant
    tenant: large_tenant
  config:
    actor_system_config: !inherit # переиспользуем исходный actor_system_config, семантика !inherit описана в разделе ниже
      # в данном случае !inherit позволяет управлять параметром actor_system_config.use_auto_config одновременно для всего кластера изменяя лишь базовую настройку
      cpu_count: 16
      node_type: COMPUTE
```

## Допустимые лейблы {#dopustimye-lejbly}

Отображение, в котором можно задать допустимые значения для лейблов. Раздел используется как хинт при генерации возможных конфигураций при помощи команды `resolve`. При запуске узлов значения не валидируются.

Доступны два типа лейблов:

- `string`;
- `enum`.

### string

Может принимать любые значения или быть не задан.

Пример:

```yaml
dynamic:
  type: string
host_name:
  type: string
```

### enum

Может принимать значения из списка `values` или быть не задан.

Пример:

```yaml
flavour:
  type: enum
  values:
    ? small
    ? medium
    ? big
```

## Поведение селекторов {#povedenie-selektorov}

Селекторы представляют собой простой язык предикатов. Селекторы по каждому лейблу объединяются через условие **И**.

### Простой селектор {#prostoj-selektor}

Следующий селектор выберет узлы, на которых значение лейбла `label1` равно `value1` **и** лейбла `label2` — `value2`:

```yaml
selector:
  label1: value1
  label2: value2
```

Следующий селектор выберет **ВСЕ** узлы в кластере, т.к. никаких условий не задано:

```yaml
selector: {}
```

### In

Данный оператор позволяет выбирать узлы с значением лейблов из списка.

Следующий селектор выберет все узлы, где лейбл `label1` равен `value1` **или** `value2`:

```yaml
selector:
  label1:
    in:
    - value1
    - value2
```

### NotIn

Данный оператор позволяет выбирать узлы, у которых выбранный лейбл не равен значению из списка.

Следующий селектор выберет все узлы, где лейбл `label1` равен `value1` **и** `label2` не равен `value2` **и** `value3`:

```yaml
selector:
  label1: value1
  label2:
    not_in:
    - value2
    - value3
```

## Дополнительные теги в YAML {#dopolnitelnye-tegi-v-yaml}

Теги необходимы для частичного или полного переиспользования конфигураций предыдущих селекторов. С помощью них можно объеденить, расширить, удалить и полностью переопределить параметры, заданные в предыдущих селекторах и основной конфигурации.

### !inherit

**Область применения:** [YAML mapping](https://yaml.org/spec/1.2.2/#mapping)  
 **Действие:** аналогично [merge-тегу](https://yaml.org/type/merge.html) в YAML, скопировать все дочерние элементы из родительского отображения и объеденить с текущими с перезаписью  
 **Пример:**

|  |  |  |
| --- | --- | --- |
| Изначальная конфигурация | Переопределение | Результирующая конфигурация |
| ```yaml<br>config:<br>  some_config:<br>    first_entry: 1<br>    second_entry: 2<br>    third_entry: 3<br>``` | ```yaml<br>config:<br>  some_config: !inherit<br>    second_entry: 100<br>``` | ```yaml<br>config:<br>  some_config:<br>    first_entry: 1<br>    second_entry: 100<br>    third_entry: 3<br>``` |

### !inherit:\<key> {#key}

**Область применения:** [YAML sequence](https://yaml.org/spec/1.2.2/#sequence)  
 **Действие:** скопировать элементы родительского массива и переписать, трактуя объект key в элементах как ключ, дописывая новые ключи в конец  
 **Пример:**

|  |  |  |
| --- | --- | --- |
| Изначальная конфигурация | Переопределение | Результирующая конфигурация |
| ```yaml<br>config:<br>  some_config:<br>    array:<br>    - abc: 2<br>      value: 10<br>    - abc: 1<br>      value: 20<br>      another_value: test<br>``` | ```yaml<br>config:<br>  some_config: !inherit<br>    array: !inherit:abc<br>    - abc: 1<br>      value: 30<br>    - abc: 3<br>      value: 40<br>``` | ```yaml<br>config:<br>  some_config:<br>    array:<br>    - abc: 2<br>      value: 10<br>    - abc: 1<br>      value: 30<br>    - abc: 3<br>      value: 40<br>``` |

### !remove

**Область применения:** YAML sequence element под `!inherit:<key>`  
 **Действие:** удалить элемент с соотвествующим ключом.  
 **Пример:**

|  |  |  |
| --- | --- | --- |
| Изначальная конфигурация | Переопределение | Результирующая конфигурация |
| ```yaml<br>config:<br>  some_config:<br>    array:<br>    - abc: 2<br>      value: 10<br>    - abc: 1<br>      value: 20<br>      another_value: test<br>``` | ```yaml<br>config:<br>  some_config: !inherit<br>    array: !inherit:abc<br>    - !remove<br>      abc: 1<br>``` | ```yaml<br>config:<br>  some_config:<br>    array:<br>    - abc: 2<br>      value: 10<br>``` |

### !append

**Область применения:** [YAML sequence](https://yaml.org/spec/1.2.2/#sequence)  
 **Действие:** скопировать элементы родительского массива и дописать новые в конец  
 **Пример:**

|  |  |  |
| --- | --- | --- |
| Изначальная конфигурация | Переопределение | Результирующая конфигурация |
| ```yaml<br>config:<br>  some_config:<br>    array:<br>    - abc: 2<br>      value: 10<br>    - abc: 1<br>      value: 20<br>      another_value: test<br>``` | ```yaml<br>config:<br>  some_config: !inherit<br>    array: !append<br>    - abc: 1<br>      value: 30<br>    - abc: 3<br>      value: 40<br>``` | ```yaml<br>config:<br>  some_config:<br>    array:<br>    - abc: 2<br>      value: 10<br>    - abc: 1<br>      value: 20<br>      another_value: test<br>    - abc: 1<br>      value: 30<br>    - abc: 3<br>      value: 40<br>``` |

## Генерация конечных конфигураций {#selectors-resolve}

Конфигурации могут содержать сложные наборы переопределений. С помощью [YDB CLI](../../../reference/ydb-cli/index.md) существует возможность посмотреть конечные конфигурации для:

- конкретных узлов;
- наборов лейблов;
- все возможные комбинации для текущей конфигурации.

```bash
# Сгенерировать все возможные конечные конфигурации для cluster.yaml
ydb admin config resolve --all -f cluster.yaml
# Сгенерировать конфигурацию для cluster.yaml при лейблах tenant=/Root/test и canary=true
ydb admin config resolve -f cluster.yaml --label tenant=/Root/test --label canary=true
# Сгенерировать конфигурацию для cluster.yaml при лейблах аналогичных текущим на узле 1001
ydb admin config resolve -f cluster.yaml --node_id 1001
# Взять текущую конфигурацию кластера и сгенерировать для него финальную конфигурацию при лейблах аналогичных текущим на узле 1001
ydb admin config resolve --from-cluster --node_id 1001
```

Более подробно команда преобразования конфигурации описана в разделе [Получить конфигурацию кластера](../../../reference/ydb-cli/configs.md).

Пример вывода `ydb admin config resolve --all -f cluster.yaml` для следующего файла конфигурации:

```yaml
metadata:
  cluster: ""
  version: 8
config:
  actor_system_config:
    use_auto_config: true
    node_type: STORAGE
    cpu_count: 4
allowed_labels:
  dynamic:
    type: string
selector_config:
- description: Actorsystem for dynnodes # произвольная строка с описанием
  selector: # селектор для всех узлов с лейблом dynamic = true
    dynamic: true
  config:
    actor_system_config: !inherit # переиспользуем исходный actor_system_config, семантика !inherit описана в разделе ниже
      node_type: COMPUTE
      cpu_count: 8
```

Вывод:

```yaml
---
label_sets: # наборы лейблов, для которых сгенерирована конфигурация
- dynamic:
    type: NOT_SET # один из трех типов лейбла: NOT_SET | COMMON | EMPTY
config: # сгенерированная конфигурация
  invalid: 1
  actor_system_config:
    use_auto_config: true
    node_type: STORAGE
    cpu_count: 4
---
label_sets:
- dynamic:
    type: COMMON
    value: true # значение лейбла
config:
  invalid: 1
  actor_system_config:
    use_auto_config: true
    node_type: COMPUTE
    cpu_count: 8
```
