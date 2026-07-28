---
title: "Начало работы с YDB в Kubernetes"
url: "https://ydb.tech/docs/ru/devops/deployment-options/kubernetes/initial-deployment?version=v26.1"
doc_path: "ru/devops/deployment-options/kubernetes/initial-deployment"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/kubernetes/initial-deployment.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/kubernetes/initial-deployment.md"
description: "Развертывание YDB в Kubernetes — это простой способ установки и эксплуатации YDB кластера. С Kubernetes вы можете использовать универсальный подход к управлению"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Начало работы с YDB в Kubernetes

Развертывание YDB в Kubernetes — это простой способ установки и эксплуатации YDB кластера. С Kubernetes вы можете использовать универсальный подход к управлению приложением в любом облачном провайдере. Это руководство содержит инструкции для развертывания YDB в [AWS EKS](https://aws.amazon.com/ru/eks/) или [Yandex Managed Service for Kubernetes](https://cloud.yandex.ru/services/managed-kubernetes).

## Пререквизиты {#prerekvizity}

YDB поставляется в виде [Helm](https://helm.sh/)-чарта — пакета, который содержит шаблоны структур Kubernetes. Подробнее о Helm читайте в [документации](https://helm.sh/docs/). Чарт YDB может быть развернут в следующем окружении:

1. Кластер Kubernetes версии 1.20 и старше. Он должен поддерживать динамическое предоставление томов ([Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)). Следуйте иструкциям ниже, если у вас ещё не настроен подходящий кластер.
2. [Установлена](https://kubernetes.io/docs/tasks/tools/install-kubectl) утилита kubectl и настроен доступ к кластеру.
3. [Установлен](https://helm.sh/docs/intro/install/) менеджер пакетов Helm версии старше 3.1.0.

Для эффективной работы YDB рекомендуется использовать физические (не виртуальные) диски объемом более 800 ГБ как блочные устройства.

Минимальный объем диска должен быть не менее 80 ГБ, при меньшем объеме узел YDB не сможет использовать устройство. Корректная и бесперебойная работа с дисками минимального объема не гарантируется. Использовать такие диски рекомендуется исключительно в ознакомительных целях.

> [!WARNING]
> Конфигурации с дисками объемом меньше 800 ГБ или с любыми видами виртуализации системы хранения нельзя использовать для сервисов, находящихся в промышленной эксплуатации, а также для тестирования производительности системы.
>
> Мы не рекомендуем использовать для хранения данных YDB диски, которые используются другими процессами (в том числе операционной системой).

### Создание Kubernetes кластера {#sozdanie-kubernetes-klastera}

Пропустите этот раздел, если у вас уже имеется подходящий Kubernetes

{% list tabs %}

- AWS EKS

  1. Настройте утилиты `awscli` и `eksctl` для работы с ресурсами AWS по [документации](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html).

  2. Настройте `kubectl` для работы с кластером Kubernetes.

  3. Выполните следующую команду:

     ```bash
       eksctl create cluster \
         --name ydb \
         --nodegroup-name standard-workers \
         --node-type c5a.2xlarge \
         --nodes 3 \
         --nodes-min 1 \
         --nodes-max 4
     ```

     Это команда создаст Kubernetes кластер с именем `ydb`. Флаг `--node-type` указывает, что кластер будет развернут с использованием инстансов `c5a.2xlarge` (8vCPUs, 16 GiB RAM), что соответствует рекомендациям по запуску YDB.

     Создание Kubernetes кластера занимает в среднем от 10 до 15 минут. Дождитесь завершения процесса перед переходом к следующим шагам развертывания YDB. Конфигурация `kubectl` будет автоматически обновлена для работы с кластером после его создания.

- Yandex Managed Service for Kubernetes

  1. Создайте кластер Kubernetes.

     Вы можете использовать уже работающий кластер Kubernetes или создать новый.

     <details>
     <summary>Как создать кластер Kubernetes в Yandex Managed Service for Kubernetes</summary>

     Следуйте инструкциям по [началу работы с Yandex Managed Service for Kubernetes](https://cloud.yandex.ru/docs/managed-kubernetes/quickstart).

     </details>

{% endlist %}

## Обзор YDB Helm-чарта {#obzor-ydb-helm-charta}

Helm-чарт устанавливает [YDB Kubernetes Operator](https://github.com/ydb-platform/ydb-kubernetes-operator) в Kubernetes кластер. Он представляет собой контроллер, построенный по паттерну [Оператор](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/). Он реализует необходимую логику для развертывания и управления компонентами YDB.

Кластер YDB состоит из двух видов узлов:

- **Storage nodes** (ресурс [Storage](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/samples/storage-block-4-2.yaml)) — обеспечивают слой хранения данных;
- **Dynamic nodes** (ресурс [Database](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/samples/database.yaml)) — реализуют доступ к данным и их обработку.

Для развертывания кластера YDB в Kubernetes необходимо создать оба эти ресурса. Этот процесс будет рассмотрен подробнее ниже. Схема этих ресурсов [располагается на GitHub](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/deploy/ydb-operator/crds).

После обработки чарта контроллером будут созданы следующие ресурсы:

- [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) — контроллер рабочей нагрузки, который предоставляет предсказуемые сетевые имена и дисковые ресурсы для каждого контейнера.
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/) для доступа к созданным базам данных из приложений.
- [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) для хранения конфигурации кластера.

Ознакомиться с исходным кодом оператора можно [на GitHub](https://github.com/ydb-platform/ydb-kubernetes-operator), Helm-чарт расположен в папке [deploy](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/deploy).  
 При разворачивании контейнеров YDB используются образы `cr.yandex/yc/ydb`, на данный момент доступные только как предсобранные артефакты.

## Подготовка рабочего окружения {#podgotovka-rabochego-okruzheniya}

1. Добавьте в Helm репозиторий для YDB:

   Выполните команду:

   ```bash
   helm repo add ydb https://charts.ydb.tech/
   ```

   - `ydb` — алиас репозитория;
   - `https://charts.ydb.tech/` — URL репозитория YDB.

   Результат выполнения:

   ```text
   "ydb" has been added to your repositories
   ```

2. Обновите индекс чартов Helm:

   Выполните команду:

   ```bash
   helm repo update
   ```

   Результат выполнения:

   ```text
   Hang tight while we grab the latest from your chart repositories...
   ...Successfully got an update from the "ydb" chart repository
   Update Complete. ⎈Happy Helming!⎈
   ```

## Развертывание кластера YDB {#razvertyvanie-klastera-ydb}

### Установите YDB Kubernetes оператор {#ustanovite-ydb-kubernetes-operator}

Разверните YDB Kubernetes оператор на кластере с помощью `helm`, выполните команду:

```bash
helm install ydb-operator ydb/ydb-operator
```

- `ydb-operator` — имя установки;
- `ydb/ydb-operator` — название чарта в добавленном ранее репозитории.

Результат выполнения:

```text
NAME: ydb-operator
LAST DEPLOYED: Thu Aug 12 19:32:28 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

### Разверните узлы хранения {#razvernite-uzly-hraneniya}

YDB поддерживает различные [топологии хранения данных](../../../concepts/topology.md). YDB Kubernetes оператор имеет несколько примеров конфигураций для типовых топологий. В данной инструкции они используются без изменений, но их можно подстраивать под свои нужды или написать новый конфигурационный файл с нуля.

Примените манифест для создания узлов хранения:

{% list tabs %}

- block-4-2

  ```bash
  kubectl apply -f https://raw.githubusercontent.com/ydb-platform/ydb-kubernetes-operator/master/samples/storage-block-4-2.yaml
  ```

  Это создаст 8 узлов хранения YDB, сохраняющих данные с использованием erasure coding. В этом случае используется лишь +50% дополнительного дискового пространства для обеспечения отказоустойчивости.

- mirror-3-dc

  ```bash
  kubectl apply -f https://raw.githubusercontent.com/ydb-platform/ydb-kubernetes-operator/master/samples/storage-mirror-3dc.yaml
  ```

  Это создаст 9 узлов хранения YDB, которые сохраняют данные с фактором репликации 3.

{% endlist %}

Эта команда создаст объект `StatefulSet`, который описывает набор контейнеров с предсказуемыми сетевыми именами и закрепленными за ними дисками, а также необходимые для работы кластера объекты `Service` и `ConfigMap`.

Узлам хранения YDB требуется время для инициализации. За прогрессом инициализации можно следить с помощью команд `kubectl get storages.ydb.tech` или `kubectl describe storages.ydb.tech`. Дождитесь пока статус ресурса `Storage` станет `Ready`.

> [!WARNING]
> Конфигурация кластера статична, контроллер не будет обрабатывать изменения при повторном применении манифеста. Изменение таких параметров кластера, как версия или размер дисков, возможно только через пересоздание кластера.

### Создайте базу данных и динамические узлы {#create-database}

YDB база данных представляет собой логическую сущность, обслуживаемую динамическими узлами. Пример конфигурационного файла, который поставляется с YDB Kubernetes оператором, создаёт базу данных с именем `database-sample` и 3 динамическими узлами. Как и в случае с узлами хранения, конфигурацию можно изменять под свои нужды.

Примените манифест для создания базы данных и динамических узлов:

```bash
kubectl apply -f https://raw.githubusercontent.com/ydb-platform/ydb-kubernetes-operator/master/samples/database.yaml
```

> [!NOTE]
> Значение по ключу `.spec.storageClusterRef.name` должно совпадать с именем ресурса `Storage` с узлами хранения.

После обработки манифеста будет создан объект `StatefulSet`, который описывает набор динамических нод. Созданная база данных будет доступна изнутри Kubernetes кластера по имени `database-sample`, или по FQDN-имени `database-sample.<namespace>.svc.cluster.local`, где `namespace` — название пространства имен, использовавшегося при установке. Подключиться к базе данных можно по порту 2135.

Посмотрите статус созданного ресурса:

```bash
kubectl describe database.ydb.tech
```

Результат выполнения команды:

```text
Name:         database-sample
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  ydb.tech/v1alpha1
Kind:         Database
...
  Storage Endpoint:  grpc://storage-sample-grpc.default.svc.cluster.local:2135
Status:
  State:  Ready
Events:
  Type     Reason              Age    From          Message
  ----     ------              ----   ----          -------
  Normal   Provisioning        8m10s  ydb-operator  Resource sync is in progress
  Normal   Provisioning        8m9s   ydb-operator  Resource sync complete
  Normal   TenantInitialized   8m9s   ydb-operator  Tenant /root/database-sample created
```

`State: Ready` означает, что база данных готова к работе.

### Проверьте работу кластера {#proverte-rabotu-klastera}

Проверьте работоспособность YDB:

1. Проверьте, что все узлы в состоянии `Running`:

   ```bash
   kubectl get pods
   ```

   Результат:

   ```text
   NAME                READY   STATUS    RESTARTS   AGE
   database-sample-0   1/1     Running   0          1m
   database-sample-1   1/1     Running   0          1m
   database-sample-2   1/1     Running   0          1m
   database-sample-3   1/1     Running   0          1m
   database-sample-4   1/1     Running   0          1m
   database-sample-5   1/1     Running   0          1m
   storage-sample-0    1/1     Running   0          1m
   storage-sample-1    1/1     Running   0          1m
   storage-sample-2    1/1     Running   0          1m
   storage-sample-3    1/1     Running   0          1m
   storage-sample-4    1/1     Running   0          1m
   storage-sample-5    1/1     Running   0          1m
   storage-sample-6    1/1     Running   0          1m
   storage-sample-7    1/1     Running   0          1m
   storage-sample-8    1/1     Running   0          1m
   ```

2. Запустите новый под с [YDB CLI](../../../reference/ydb-cli/index.md):

   ```bash
   kubectl run -it --image=cr.yandex/crptqonuodf51kdj7a7d/ydb:24.4.4.2 --rm ydb-cli bash
   ```

3. Выполните запрос к базе данных YDB (endpoint можно получить из вывода `kubectl describe database.ydb.tech`):

   ```bash
   /opt/ydb/bin/ydb \
     --endpoint grpc://database-sample-grpc:2135 \
     --database /Root/database-sample \
     sql -s 'SELECT 2 + 2;'
   ```

   - `--endpoint` — эндпоинт базы данных;
   - `--database` — имя созданной базы данных;
   - `--query` — текст запроса.

   Результат:

   ```text
   ┌─────────┐
   | column0 |
   ├─────────┤
   | 4       |
   └─────────┘
   ```

## Дальнейшие шаги {#dalnejshie-shagi}

После проверки, что созданный кластер YDB работает нормально, его можно использовать в соответствии с вашими задачами. Например, если вы хотите просто продолжить экспериментировать, можете использовать этот кластер, чтобы пройти [YQL туториал](../../../dev/yql-tutorial/index.md).

Также, ниже описаны ещё несколько аспектов, которые можно учесть далее.

### Мониторинг {#monitoring}

YDB предоставляет стандартные механизмы сбора логов и метрик. Логирование осуществляется в стандартные каналы `stdout` и `stderr` и может быть перенаправлено при помощи популярных решений. Например, можно использовать комбинацию из [Fluentd](https://www.fluentd.org/) и [Elastic Stack](https://www.elastic.co/elastic-stack/).

Для сбора метрик `ydb-controller` предоставляет ресурсы типа `ServiceMonitor`, которые могут быть обработаны с помощью [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack).

### Выделение ресурсов {#resource-allocation}

Каждый под YDB может быть ограничен в потреблении ресурсов. Если оставить значения ограничений пустыми, поду будет доступно все процессорное время и вся память виртуальной машины, что может привести к нежелательным последствиям. Мы рекомендуем всегда явно указывать лимиты ресурсов.

Более детально ознакомиться с принципами распределения и ограничения ресурсов можно в [документации Kubernetes](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

### Освобождение неиспользуемых ресурсов {#cleanup}

Если созданный кластер YDB больше не нужен, удалите его с помощью следующих шагов:

1. Чтобы удалить базу данных YDB и её динамические узлы, достаточно удалить сопоставленный с ней ресурс `Database`:

   ```bash
   kubectl delete database.ydb.tech database-sample
   ```

2. Чтобы удалить узлы хранения YDB, выполните следующие команды:

   ```bash
   kubectl delete storage.ydb.tech storage-sample
   kubectl delete pvc -l app.kubernetes.io/name=ydb
   ```

3. Чтобы удалить YDB Kubernetes оператор с кластера, используйте Helm:

   ```bash
   helm delete ydb-operator
   ```
