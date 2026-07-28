---
title: "Deploy Infrastructure for YDB Cluster using Terraform"
url: "https://ydb.tech/docs/en/devops/deployment-options/ansible/preparing-vms-with-terraform?version=v26.1"
doc_path: "en/devops/deployment-options/ansible/preparing-vms-with-terraform"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/ansible/preparing-vms-with-terraform.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/ansible/preparing-vms-with-terraform.md"
description: "You can deploy a YDB cluster for production use in three recommended ways: using Ansible, Kubernetes or manually. While the Kubernetes option is almost self-suf"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Deploy Infrastructure for YDB Cluster using Terraform

You can deploy a YDB cluster for production use in three recommended ways: using [Ansible](initial-deployment/index.md), [Kubernetes](../kubernetes/index.md) or [manually](../manual/index.md). While the Kubernetes option is almost self-sufficient, the Ansible and manual options require SSH access to properly configured servers or virtual machines.

This article describes how to create and configure the necessary set of virtual machines in various cloud providers for a YDB cluster, using Terraform.

**[Terraform](https://www.terraform.io/)** is an open-source infrastructure management software based on the "Infrastructure as Code" model. The same approach is used in Ansible, a configuration management system. Terraform and Ansible work at different levels: Terraform manages the infrastructure, and Ansible configures the environments on virtual machines (VM).

![AiC_scheme](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/devops/deployment-options/ansible/_assets/terraform/AiC_scheme.png)

The configuration for setting up the VM environment is described in YAML format, and the infrastructure code is written in [HCL](https://github.com/hashicorp/hcl) (Terraform configuration language). The basic logical unit of recording in HCL is a "block". A block consists of a keyword identifying its type, name, and the block's body inside curly brackets. For example, this is what a virtual server control block in AWS might look like:

```
resource "aws_instance" "ydb-vm" {
  count                  = var.instance_count
  ami                    = "ami-008fe2fc65df48dac"
  instance_type          = "t2.micro"
  key_name               = var.req_key_pair
  vpc_security_group_ids = [var.input_security_group_id]
  subnet_id              = element(var.input_subnet_ids, count.index % length(var.input_subnet_ids))

  tags = {
    Name                 = "ydb-node-${count.index +1}"
    Username             = "ubuntu"
  }
}
```

Blocks can be independent, refer to each other, and thus be dependent, or they can also be nested inside each other.

Main block types:

- `resource` – a block for initializing an infrastructure resource (VM, network, subnet, disk, DNS zone, etc.).
- `provider` – a block for initializing the provider, API versions, and authentication data.
- `variable` – a variable either with a default value or empty for storing data entered by the user or passed by other blocks.
- `output` – outputs data to the terminal and saves it in a variable.
- `data` – a variable for requesting data from external cloud resources not presented in the created infrastructure.
- `module` – a logical grouping of resources that can be reused several times within the same or different projects.
- `terraform` – a block for configuring the behavior of Terraform itself, including the version of Terraform and used providers, as well as the backend settings, which are used for storing Terraform's state.

Blocks are written in files with the `.tf` extension and are logically grouped in directories, which in Terraform terminology are called modules. A module usually consists of the following files:

- `main.tf` – the main file where the infrastructure code is located. There can be several files containing infrastructure code.
- `variables.tf` – local variables of the module, which receive data from other modules or have default values.
- `outputs.tf` – variables that contain the results of the resource's operation (VM IP addresses, network/subnet IDs, etc.).

Modules are connected to the project in the root file `main.tf` as follows:

```
module "vpc" {
  source                     = "./modules/vpc"
  subnets_count              = var.subnets_count
  subnets_availability_zones = var.availability_zones
}
```

In the example, the `vpc` module is connected (the module name is assigned when connecting). The required parameter is `source`, a path to the directory where the module is located. `subnets_count` and `subnets_availability_zones` are variables inside the `vpc` module that take values from the global level variables `var.subnets_count`, `var.availability_zones`.

Modules, just like blocks, are placed one after another in the root `main.tf` file of the project. The main advantage of the modular approach to project organization is the ability to manage logically related sets of resources easily. Therefore, our [repository](https://github.com/ydb-platform/ydb-terraform) with ready-made Terraform scenarios is organized as follows:

```txt
.
├── README.md
├── README_RU.md
├── aws
│   ├── README.md
│   ├── README_RU.md
│   ├── main.tf
│   ├── modules
│   │   ├── dns
│   │   ├── eip
│   │   ├── instance
│   │   ├── key_pair
│   │   ├── security
│   │   └── vpc
│   └── variables.tf
├── azure
│   ├── README.md
│   ├── README_RU.md
│   ├── main.tf
│   ├── modules
│   │   ├── dns
│   │   ├── resource_group
│   │   ├── security
│   │   ├── vm
│   │   └── vpc
│   └── variables.tf
├── ...
```

The subdirectories contain readme files, a file `variables.td` with local module variables and a central file `main.tf`, which includes modules from the `modules` subdirectory. The set of modules depends on the cloud provider. Basic modules, functionally the same for all providers, have the same names:

- `vpc` – cloud network and subnet management module.
- `dns` – DNS zone and DNS records management module.
- `security` – security group management module.
- `instance` – VM control module.

To use ready-made Terraform scripts from the repository, you need to download the repository with the command `git clone https://github.com/ydb-platform/ydb-terraform.git`, make changes to the Terraform configuration file `~/.terraformrc`, set the current values of global script variables and download the CLI of the cloud provider where the infrastructure will be created.

If you plan to use multiple providers, you can add the following code to `~/.terraformrc`, which will set the download paths for all providers described below:

```
provider_installation {
  network_mirror {
    url     = "https://terraform-mirror.yandexcloud.net/"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
    exclude = ["terraform.storage.ydb.tech/*/*"]
  }
```

If you already use Terraform providers provided in the [official repository](https://registry.terraform.io/browse/providers), they will continue to work.

## Deployment Overview

The following are step-by-step instructions for creating infrastructure in [AWS](preparing-vms-with-terraform.md#aws-cluster), [Azure](preparing-vms-with-terraform.md#aws-cluster), [GCP](preparing-vms-with-terraform.md#gcp-cluster), or [Yandex Cloud](preparing-vms-with-terraform.md#gcp-cluster). By default, example Terraform scenarios deploy the same type of infrastructure:

- VMs in three availability zones.
- Cloud network, public and private subnets (per subnet per availability zone).
- Private DNS zone.
- Security groups allowing ICMP and traffic on ports: 22, 65535, 19001, 8765, and 2135.

Most cluster parameters are adjustable (number of VMs, size and type of connected disks, number of networks, DNS zone domain name, etc.), but please note that the defaults are minimum recommended values, so changing them downwards may cause issues.

## Create Infrastructure in AWS to Deploy a YDB Cluster {#aws-cluster}

Create an [account](https://console.aws.amazon.com) in AWS and add enough balance to run 9 VMs. Using the [calculator](https://calculator.aws/#/createCalculator/ec2-enhancement), you can estimate the approximate cost of maintaining infrastructure depending on the region and other circumstances.

Create a user and connection key in AWS Cloud to run the AWS CLI:

1. The user is created in the Security credentials → Access management → [Users](https://console.aws.amazon.com/iam/home#/users) → Create User section.
2. The next step is to assign rights to the user. Select `AmazonEC2FullAccess`.
3. After creating a user, go to its page, open the `Security credentials` tab, and click the **Create access key** button in the **Access keys** section.
4. Select `Command Line Interface` from the proposed options.
5. Next, create a tag for the key and click the **Create access key** button.
6. Copy the values of the `Access key` and `Secret access key` fields.

Install [AWS CLI](https://aws.amazon.com/cli/) and run the `aws configure` command. Enter the values of the `Access key` and `Secret access key` fields saved earlier. Edit the `~/.aws/credentials` and `~/.aws/config` files as follows:

1. Add `[AWS_def_reg]` to `~/.aws/config` before `region = ...`.
2. Add `[AWS]` before the connection key secret information.

Go to the `aws` directory in the downloaded repository and edit the following variables in the `variable.tf` file:

1. `aws_region` – the region in which the infrastructure will be deployed.
2. `aws_profile` – security profile name from the file `~/.aws/credentials`.
3. `availability_zones` – list of region availability zones. It is formed from the name of the region and the serial letter. For example, for the `us-west-2` region, the list of availability zones will look like this: `["us-west-2a", "us-west-2b", "us-west-2c"]`.

Now, being in the `aws` subdirectory, you can run the following sequence of commands to install the provider, initialize modules, and create the infrastructure:

1. `terraform init` – installing the provider and initializing modules.
2. `terraform plan` – creating a plan for future infrastructure.
3. `terraform apply` – create resources in the cloud.

Next, use the commands `terraform plan`, `terraform apply`, and `terraform destroy` (destruction of the created infrastructure) to apply further changes as necessary.

## Create Infrastructure in Azure to Deploy a YDB Cluster {#azure-cluster}

Create an [account](https://portal.azure.com/#home) in Azure and top up your [account](https://portal.azure.com/#view/Microsoft_Azure_GTM/ModernBillingMenuBlade/~/BillingAccounts) account with the amount, sufficient to operate 9 VMs. You can estimate the approximate cost of maintaining infrastructure depending on the region and other circumstances using [calculator](https://azure.com/e/26977c150e854617a888fb3a7d1a399d).

Authentication to the Azure Provider for Terraform goes through the CLI:

1. You can download, install, and configure the Azure CLI by following [these instructions](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Log in using the Azure CLI interactively with the `az login` command.
3. The easiest way to create a pair of SSH keys (Linux, macOS) is to use the `ssh-keygen` command.

After logging into Azure and generating SSH keys, you need to change the default value of the following variables in the root file `variables.tf`:

1. `auth_location`—the name of the region where the infrastructure will be deployed. The command `az account list-locations | grep "displayName"` can obtain a list of available regions depending on the subscription.
2. `ssh_key_path` – path to the public part of the generated SSH key.

Now, being in the `azure` subdirectory, you can run the following sequence of commands to install the provider, initialize modules, and create the infrastructure:

1. `terraform init` – installing the provider and initializing modules.
2. `terraform plan` – creating a plan for future infrastructure.
3. `terraform apply` – create resources in the cloud.

Next, use the commands `terraform plan`, `terraform apply`, and `terraform destroy` (destruction of the created infrastructure) to apply further changes as necessary.

## Creating Infrastructure in Google Cloud Platform to Deploy a YDB Cluster {#gcp-cluster}

Register in the Google Cloud console and [create](https://console.cloud.google.com/projectselector2/home) a project. Activate your [payment account](https://console.cloud.google.com/billing/manage) and top it up with funds to launch nine VMs. You can estimate the approximate cost in [calculator](https://cloud.google.com/products/calculator).

Set up GCP CLI:

1. Activate [Compute Engine API](https://console.cloud.google.com/apis/api/compute.googleapis.com/metrics) and [Cloud DNS API](https://console.cloud.google.com/apis/api/dns.googleapis.com/metrics).
2. Download and install GCP CLI by following [these instructions](https://cloud.google.com/sdk/docs/install).
3. Go to the `.../google-cloud-sdk/bin` subdirectory and run the `./gcloud compute regions list` command to get a list of available regions.
4. Run the command `./gcloud auth application-default login` to configure the connection profile.

Go to the `gcp` subdirectory (located in the downloaded repository), and in the `variables.tf` file set the current values for the following variables:

1. `project` – the project's name that was set in the Google Cloud cloud console.
2. `region` – the region where the infrastructure will be deployed.
3. `zones` – list of availability zones in which subnets and VMs will be created.

Now, being in the `gcp` subdirectory, you can run the following sequence of commands to install the provider, initialize modules, and create the infrastructure:

1. `terraform init` – installing the provider and initializing modules.
2. `terraform plan` – creating a plan for future infrastructure.
3. `terraform apply` – create resources in the cloud.

Next, use the commands `terraform plan`, `terraform apply`, and `terraform destroy` (destruction of the created infrastructure) to apply further changes as necessary.

## Creating an Infrastructure in Yandex Cloud to Deploy a YDB Cluster {#yc-cluster}

To create infrastructure in Yandex Cloud using Terraform, you need:

1. Prepare the cloud for work:

   - [Register](https://console.yandex.cloud) in Yandex Cloud.
   - [Connect](https://yandex.cloud/en/docs/billing/concepts/billing-account) payment account.
   - [Make sure](https://billing.yandex.cloud) that there are enough funds to create nine VMs.

2. Install and configure Yandex Cloud CLI:

   - [Download](https://yandex.cloud/en/docs/cli/quickstart) Yandex Cloud CLI.
   - [Create](https://yandex.cloud/en/docs/cli/quickstart#initialize) profile

3. [Create](https://yandex.cloud/en/docs/tutorials/infrastructure-management/terraform-quickstart#get-credentials) service account using the CLI.

4. [Generate](https://yandex.cloud/en/docs/cli/operations/authentication/service-account#auth-as-sa) Authorized key in JSON format for connecting Terraform to the cloud using the CLI: `yc iam key create --service-account-name <acc name> --output <file name> --folder-id <cloud folder id>`. Information about the created key will be displayed in the terminal:

   ```text
   id: ajenap572v8e1l...
   service_account_id: aje90em65r69...
   created_at: "2024-09-03T15:34:57.495126296Z"
   key_algorithm: RSA_2048
   ```

   The authorized key will be created in the directory where the command was executed.

5. [Configure](https://yandex.cloud/en/docs/tutorials/infrastructure-management/terraform-quickstart#configure-provider) Yandex Cloud Terraform provider.

6. Download this repository with the command `git clone https://github.com/ydb-platform/ydb-terraform.git`.

7. Go to the `yandex_cloud` directory in the downloaded repository and make changes to the following variables in the `variables.tf` file:

   - `key_path` – path to the SA key generated using the CLI.
   - `cloud_id` – cloud ID. You can get a list of available clouds with the command `yc resource-manager cloud list`.
   - `folder_id` – Cloud folder ID. Can be obtained with the command `yc resource-manager folder list`.

Now, being in the `yandex_cloud` subdirectory, you can run the following sequence of commands to install the provider, initialize modules, and create the infrastructure:

1. `terraform init` – installing the provider and initializing modules.
2. `terraform plan` – creating a plan for future infrastructure.
3. `terraform apply` – create resources in the cloud.

Next, use the commands `terraform plan`, `terraform apply`, and `terraform destroy` (destruction of the created infrastructure) to apply further changes as necessary.
