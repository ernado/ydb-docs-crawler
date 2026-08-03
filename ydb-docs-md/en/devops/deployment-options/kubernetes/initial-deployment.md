---
title: "Getting Started with YDB in Kubernetes"
url: "https://ydb.tech/docs/en/devops/deployment-options/kubernetes/initial-deployment?version=v26.1"
doc_path: "en/devops/deployment-options/kubernetes/initial-deployment"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/kubernetes/initial-deployment.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/kubernetes/initial-deployment.md"
description: "Deploying YDB in Kubernetes is a simple way to set up and run a YDB cluster. Kubernetes allows to use an universal approach to managing your application in any"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Getting Started with YDB in Kubernetes

Deploying YDB in Kubernetes is a simple way to set up and run a YDB cluster. Kubernetes allows to use an universal approach to managing your application in any cloud service provider. This guide provides instructions on how to deploy YDB in [AWS EKS](https://aws.amazon.com/eks/) or [Yandex Managed Service for Kubernetes](https://yandex.cloud/services/managed-kubernetes).

## Prerequisites

YDB is delivered as a [Helm](https://helm.sh/) chart that is a package with templates of Kubernetes structures. For more information about Helm, see the [documentation](https://helm.sh/docs/). The YDB chart can be deployed in the following environment:

1. A Kubernetes cluster with version 1.20 or higher. It needs to support [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/). Follow the instructions below if you don't have a suitable cluster yet.
2. The `kubectl` command line tool is [installed](https://kubernetes.io/docs/tasks/tools/install-kubectl) and Kubernetes cluster access is configured.
3. The Helm package manager with a version higher than 3.1.0 is [installed](https://helm.sh/docs/intro/install/).

For YDB to work efficiently, we recommend using physical (not virtual) disks larger than 800 GB as block devices.

The minimum disk size is 80 GB, otherwise the YDB node won't be able to use the device. Correct and uninterrupted operation with minimum-size disks is not guaranteed. We recommend using such disks exclusively for informational purposes.

> [!WARNING]
> Configurations with disks less than 800 GB or any types of storage system virtualization cannot be used for production services or system performance testing.
>
> We don't recommend storing YDB data on disks shared with other processes (for example, the operating system).

## Creating a Kubernetes Cluster

Skip this section if you have already configured a suitable Kubernetes cluster.

{% list tabs %}

- AWS EKS

  1. Configure `awscli` and `eksctl` to work with AWS resources according to the [documentation](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html).
  2. Configure `kubectl` to work with a Kubernetes cluster.
  3. Run the following command:

  ```bash
    eksctl create cluster \
      --name ydb \
      --nodegroup-name standard-workers \
      --node-type c5a.2xlarge \
      --nodes 3 \
      --nodes-min 1 \
      --nodes-max 4
  ```

  This command will create a Kubernetes cluster named `ydb`. The `--node-type` flag indicates that the cluster is deployed using `c5a.2xlarge` (8vCPUs, 16 GiB RAM) instances. This meets minimal guidelines for running YDB.

  It takes 10 to 15 minutes on average to create a Kubernetes cluster. Wait for the process to complete before proceeding to the next step of YDB deployment. The `kubectl` configuration will be automatically updated to work with the cluster after it is created.

- Yandex Managed Service for Kubernetes

  Follow the instructions in the [Yandex Managed Service for Kubernetes quick start guide](https://yandex.cloud/en/docs/managed-kubernetes/quickstart).

{% endlist %}

## Overview of YDB Helm chart

The Helm chart installs [YDB Kubernetes Operator](https://github.com/ydb-platform/ydb-kubernetes-operator) to the Kubernetes cluster. It is a controller that follows the [Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) design pattern. It implements the logic required for deploying and managing YDB components.

A YDB cluster consists of two kinds of nodes:

- **Storage nodes** ([Storage](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/samples/storage-block-4-2.yaml) resource) provide the data persistence layer.
- **Dynamic nodes** ([Database](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/samples/database.yaml) resource) implement data access and processing.

Create both resources with the desired parameters to deploy a YDB cluster in Kubernetes. The schema for these resources is [hosted on GitHub](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/deploy/ydb-operator/crds).

After the chart data is processed by the controller, the following resources are created:

- [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/): A workload controller that assigns stable network IDs and disk resources to each container.
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/): An object that is used to access the created databases from applications.
- [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/): An object that is used to store the cluster configuration.

See the operator's source code [on GitHub](https://github.com/ydb-platform/ydb-kubernetes-operator). The Helm chart is in the [deploy](https://github.com/ydb-platform/ydb-kubernetes-operator/tree/master/deploy) folder.  
 YDB containers are deployed using `cr.yandex/yc/ydb` images. Currently, they are only available as prebuilt artifacts.

## Environment Preparation

1. Add the YDB repository to Helm:

Run the command:

```bash
helm repo add ydb https://charts.ydb.tech/
```

`ydb`: The repository alias.  
 `https://charts.ydb.tech/`: The YDB repository URL.

Output:

```text
"ydb" has been added to your repositories
```

2. Update the Helm chart index:

Run the command:

```bash
helm repo update
```

Output:

```text
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "ydb" chart repository
Update Complete. ⎈Happy Helming!⎈
```

## Deploying a YDB Cluster

### Install the YDB Kubernetes operator

Use `helm` to deploy the YDB Kubernetes operator to the cluster:

```bash
helm install ydb-operator ydb/ydb-operator
```

- `ydb-operator`: The installation name.
- `ydb/ydb-operator`: The name of the chart in the repository you have added earlier.

Result:

```text
NAME: ydb-operator
LAST DEPLOYED: Thu Aug 12 19:32:28 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

### Deploy Storage Nodes

YDB supports a number of [storage topologies](../../../concepts/topology.md). YDB Kubernetes operator comes with a few sample configuration files for the most common topologies. This guide uses them as-is, but feel free to adjust them as needed or implement a new configuration file from scratch.

Apply the manifest for creating storage nodes:

{% list tabs %}

- block-4-2

  ```bash
  kubectl apply -f https://raw.githubusercontent.com/ydb-platform/ydb-kubernetes-operator/master/samples/storage-block-4-2.yaml
  ```

  This will create 8 YDB storage nodes that persist data using erasure coding. This takes only 50% of additional storage space to provide fault-tolerance.

- mirror-3-dc

  ```bash
  kubectl apply -f https://raw.githubusercontent.com/ydb-platform/ydb-kubernetes-operator/master/samples/storage-mirror-3dc.yaml
  ```

  This will create 9 YDB storage nodes that store data with replication factor 3.

{% endlist %}

This command creates a `StatefulSet` object that describes a set of YDB containers with stable network IDs and disks assigned to them, as well as `Service` and `ConfigMap` objects that are required for the cluster to work.

YDB storage nodes take a while to initialize. You can check the initialization progress with `kubectl get storages.ydb.tech` or `kubectl describe storages.ydb.tech`. Wait until the status of the Storage resource changes to `Ready`.

> [!WARNING]
> The cluster configuration is static. The controller won't process any changes when the manifest is reapplied. You can only update cluster parameters such as version or disk size by creating a new cluster.

### Create a database and dynamic nodes

YDB database is a logical entity that is served by a set of dynamic nodes. A sample manifest that comes with YDB Kubernetes operator creates a database named `database-sample` with 3 dynamic nodes. As with storage nodes, feel free to adjust the configuration as needed.

Apply the manifest for creating a database and dynamic nodes:

```bash
kubectl apply -f https://raw.githubusercontent.com/ydb-platform/ydb-kubernetes-operator/master/samples/database.yaml
```

> [!NOTE]
> The value referenced by `.spec.storageClusterRef.name` key must match the name of the `Storage` resource with storage nodes.

A `StatefulSet` object that describes a set of dynamic nodes is created after processing the manifest. The created database will be accessible from inside the Kubernetes cluster by the `database-sample` hostname or the `database-sample.<namespace>.svc.cluster.local` FQDN, where `namespace` indicates the namespace that was used for the installation. You can connect the database via port 2135.

View the status of the created resource:

```bash
kubectl describe database.ydb.tech
```

Result:

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

`State: Ready` means that the database is ready to be used.

### Test Cluster Operation

Check how YDB works:

1. Check that all nodes are in the `Running` status:

   ```bash
   kubectl get pods
   ```

   Result:

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

2. Start a new pod with [YDB CLI](../../../reference/ydb-cli/index.md):

   ```bash
   kubectl run -it --image=cr.yandex/crptqonuodf51kdj7a7d/ydb:24.4.4.2 --rm ydb-cli bash
   ```

3. Query the YDB database (you can get the endpoint from the output of `kubectl describe database.ydb.tech`):

   ```bash
   /opt/ydb/bin/ydb \
     --endpoint grpc://database-sample-grpc:2135 \
     --database /Root/database-sample \
     sql -s 'SELECT 2 + 2;'
   ```

   - `--endpoint`: The database endpoint.
   - `--database`: The name of the created database.
   - `--query`: The query text.

   Result:

   ```text
   ┌─────────┐
   | column0 |
   ├─────────┤
   | 4       |
   └─────────┘
   ```

## Further Steps

After you have tested that the created YDB cluster operates fine you can continue using it as you see fit. For example, if you just want to continue experimenting, you can use it to follow the [YQL tutorial](../../../dev/yql-tutorial/index.md).

Below are a few more things to consider.

### Monitoring

YDB provides standard mechanisms for collecting logs and metrics. Logging is done to standard `stdout` and `stderr` streams and can be redirected using popular solutions. For example, you can use a combination of [Fluentd](https://www.fluentd.org/) and [Elastic Stack](https://www.elastic.co/elastic-stack/).

To collect metrics, `ydb-controller` provides resources like `ServiceMonitor`. They can be handled using [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack).

### Tuning Allocated Resources {#resource-allocation}

You can limit resource consumption for each YDB pod. If you leave the limit values empty, a pod can use the entire CPU time and VM RAM. This may cause undesirable effects. We recommend that you always specify the resource limits explicitly.

To learn more about resource allocation and limits, see the [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

### Release the Unused Resources {#cleanup}

If you no longer need the created YDB cluster, delete it by following these steps:

1. To delete a YDB database and its dynamic nodes, just delete the respective `Database` resource:

   ```bash
   kubectl delete database.ydb.tech database-sample
   ```

2. To delete YDB storage nodes, run the following commands:

   ```bash
   kubectl delete storage.ydb.tech storage-sample
   kubectl delete pvc -l app.kubernetes.io/name=ydb
   ```

3. To remove the YDB Kubernetes operator, delete it with Helm:

   ```bash
   helm delete ydb-operator
   ```

   - `ydb-operator`: The name of the release that the controller was installed under.
