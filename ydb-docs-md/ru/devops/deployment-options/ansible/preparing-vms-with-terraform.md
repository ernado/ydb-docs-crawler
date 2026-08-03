---
title: "Развёртывание инфраструктуры для кластера YDB с помощью Terraform"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/preparing-vms-with-terraform?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/preparing-vms-with-terraform"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/preparing-vms-with-terraform.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/preparing-vms-with-terraform.md"
description: "Развернуть кластер YDB для использования в production можно тремя рекомендованными способами: с помощью Ansible, Kubernetes или вручную. Если вариант с Kubernet"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Развёртывание инфраструктуры для кластера YDB с помощью Terraform

Развернуть кластер YDB для использования в production можно тремя рекомендованными способами: с помощью [Ansible](initial-deployment/index.md), [Kubernetes](../kubernetes/index.md) или [вручную](../manual/index.md). Если вариант с Kubernetes практически самодостаточен, то для вариантов с Ansible и вручную нужен SSH-доступ к правильно сконфигурированным серверам или виртуальным машинам.

В статье описывается, как создать и настроить необходимый для работы кластера YDB набор виртуальных машин у различных облачных провайдеров с помощью Terraform.

**[Terraform](https://www.terraform.io/)** – это программное обеспечение с открытым исходным кодом для управления инфраструктурой по модели «инфраструктура как код» (Infrastructure as Code). Такой же подход используется в Ansible, системе управления конфигурациями. Terraform и Ansible работают на разных уровнях: Terraform управляет инфраструктурой, а Ansible настраивает окружения на ВМ:

![AiC_scheme](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/deployment-options/ansible/_assets/terraform/AiC_scheme.png)

Конфигурация настройки окружения ВМ описывается в YAML-формате, а инфраструктурный код пишется на [HCL](https://github.com/hashicorp/hcl) (язык конфигурации Terraform). Основной логической единицей записи в HCL является «блок». Блок состоит из ключевого слова, идентифицирующего его тип, названия и фигурных скобок, обозначающих тело блока. Например, так может выглядеть блок управления виртуальным сервером в AWS:

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

Блоки могут располагаться друг за другом в одном файле и быть независимыми, могут ссылаться друг на друга и быть зависимыми, а также могут вкладываться друг в друга.

Основные типы блоков:

- `resource` – блок инициализации ресурса инфраструктуры (ВМ, сеть, подсеть, диск, DNS-зона и т.д.);
- `provider` – блок инициализации провайдера, версии API и данных для аутентификации;
- `variable` – переменная как со значением по умолчанию, так и пустая для хранения данных, введённых пользователем или переданных другими блоками;
- `output` – вывод данных в терминал и сохранение в переменной;
- `data` – переменная для запроса данных от внешних облачных ресурсов, не представленных в создаваемой инфраструктуре;
- `module` – логическая группировка ресурсов, которые можно переиспользовать несколько раз в рамках одного или разных проектов;
- `terraform` – блок настройки поведения самого Terraform, включая версию Terraform и используемых провайдеров, а также настройки бэкенда, который используется для хранения состояния Terraform.

Блоки записываются в файлы с расширением `.tf` и логически группируются в директориях, которые в терминологии Terraform называют модулями. Модуль обычно состоит из следующих файлов:

- `main.tf` – основной файл, в котором находится код инфраструктуры. Может быть несколько файлов, содержащих инфраструктурный код.
- `variables.tf` – локальные переменные модуля, которые принимают данные от других модулей или имеют значения по умолчанию.
- `outputs.tf` – переменные, которые содержат результаты работы ресурса (IP-адреса ВМ, ID сетей/подсетей и т.д.).

Модули подключаются к проекту в корневом файле `main.tf` следующим образом:

```
module "vpc" {
  source                     = "./modules/vpc"
  subnets_count              = var.subnets_count
  subnets_availability_zones = var.availability_zones
}
```

В примере подключается модуль `vpc` (имя модуля назначается при подключении). Обязательный параметр – это `source`, путь к директории, где располагается модуль. `subnets_count` и `subnets_availability_zones` – это переменные внутри модуля `vpc`, которые принимают значения из переменных глобального уровня `var.subnets_count` и `var.availability_zones`.

Модули, как и блоки, располагаются друг за другом в корневом `main.tf` проекта. Основное преимущество модульного подхода организации проекта – возможность легко управлять логически связанными наборами ресурсов. Поэтому [репозиторий](https://github.com/ydb-platform/ydb-terraform) с готовыми Terraform-сценариями организован следующим образом:

```text
.
├── README.md
├── README_RU.md
├── aws
│   ├── README.md
│   ├── README_RU.md
│   ├── main.tf
│   ├── modules
│   │   ├── dns
│   │   ├── eip
│   │   ├── instance
│   │   ├── key_pair
│   │   ├── security
│   │   └── vpc
│   └── variables.tf
├── azure
│   ├── README.md
│   ├── README_RU.md
│   ├── main.tf
│   ├── modules
│   │   ├── dns
│   │   ├── resource_group
│   │   ├── security
│   │   ├── vm
│   │   └── vpc
│   └── variables.tf
├── ...
```

Поддиректории содержат два `readme`, файл `variables.tf` с локальными переменными модуля и основной файл `main.tf`, который подключает модули из поддиректории `modules`. Набор модулей зависит от облачного провайдера. Базовые модули, функционально одинаковые для всех провайдеров, имеют одинаковые названия:

- `vpc` – модуль управления облачной сетью и подсетями;
- `dns` – модуль управления DNS-зоной и DNS-записями;
- `security` – модуль управления группами безопасности;
- `instance` – модуль управления ВМ.

Чтобы воспользоваться готовыми Terraform-сценариями из репозитория, нужно скачать репозиторий командой `git clone https://github.com/ydb-platform/ydb-terraform.git`, внести изменения в конфигурационный файл Terraform `~/.terraformrc`, задать актуальные значения глобальных переменных сценария и скачать CLI того облачного провайдера, где будет создана инфраструктура.

Если вы планируете использовать несколько провайдеров, можно добавить следующий код в `~/.terraformrc`, который установит пути скачивания для всех провайдеров, описанных ниже:

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

Если уже используются Terraform-провайдеры, представленные в [официальном репозитории](https://registry.terraform.io/browse/providers), они продолжат работать.

## Обзор разворачиваемой инфраструктуры {#obzor-razvorachivaemoj-infrastruktury}

Далее приведены пошаговые инструкции создания инфраструктуры в [AWS](preparing-vms-with-terraform.md#aws-cluster), [Azure](preparing-vms-with-terraform.md#azure-cluster), [GCP](preparing-vms-with-terraform.md#gcp-cluster), [Yandex Cloud](preparing-vms-with-terraform.md#yc-cluster). Предложенные примеры Terraform-сценариев развертывают однотипную инфраструктуру:

- Виртуальные машины в трёх зонах доступности;
- Облачная сеть, публичные и приватные подсети (по подсети на зону доступности);
- Приватная DNS-зона;
- Группы безопасности, разрешающие ICMP и трафик на портах: 22, 65535, 19001, 8765, 2135.

Большинство параметров кластера регулируются (количество ВМ, объём и тип подключаемого диска, количество сетей, домен DNS-зоны и т.д.), однако значения по умолчанию являются минимально рекомендованными. Их изменение в меньшую сторону может привести к проблемам.

## Создание инфраструктуры в AWS для развертывания YDB кластера {#aws-cluster}

Создайте [аккаунт](https://console.aws.amazon.com) в AWS и пополните баланс на сумму, достаточную для работы 9 ВМ. Рассчитать примерную стоимость содержания инфраструктуры в зависимости от региона и прочих обстоятельств можно с помощью [калькулятора](https://calculator.aws/#/createCalculator/ec2-enhancement).

Создайте пользователя и ключ подключения в AWS Cloud для работы AWS CLI:

1. Пользователь создаётся в разделе Security credentials → Access management → [Users](https://console.aws.amazon.com/iam/home#/users) → Create User.
2. На следующем шаге нужно назначить права пользователю. Выберете `AmazonEC2FullAccess`.
3. После создания пользователя – перейдите в него, откройте вкладку `Security credentials` и нажмите кнопку **Create access key** в секции **Access keys**.
4. Из предложенных вариантов наборов опций выберете `Command Line Interface`.
5. Далее придумайте тег для разметки ключа и нажмите кнопку **Create access key**.
6. Скопируйте значения полей `Access key` и `Secret access key`.

Установите [AWS CLI](https://aws.amazon.com/cli/) и выполните команду `aws configure`. Введите значения полей `Access key` и `Secret access key` сохраненные ранее. Отредактируйте файлы `~/.aws/credentials` и `~/.aws/config` следующим образом:

1. Добавьте `[AWS_def_reg]` в `~/.aws/config` перед `region = ...`.
2. Добавьте `[AWS]` перед секретной информацией о ключах подключения.

Перейдите в директорию `aws` в скачанном репозитории и отредактируйте следующие переменные в файле `variable.tf`:

1. `aws_region` – регион, в котором будет развернута инфраструктура.
2. `aws_profile` – имя профиля безопасности из файла `~/.aws/credentials`.
3. `availability_zones` – список зон доступности региона. Формируется из названия региона и порядковой буквы. Например, для региона `us-west-2` список зон доступности будет выглядеть так: `["us-west-2a", "us-west-2b", "us-west-2c"]`.

Теперь, находясь в поддиректории `aws`, можно выполнить последовательность следующих команд для установки провайдера, инициализации модулей и создания инфраструктуры:

1. `terraform init` – установка провайдера и инициализация модулей.
2. `terraform plan` – создание плана будущей инфраструктуры.
3. `terraform apply` (повторное выполнение) – создание ресурсов в облаке.

Далее используются команды `terraform plan`, `terraform apply` и `terraform destroy` (уничтожение созданной инфраструктуры).

## Создание инфраструктуры в Azure для развертывания YDB кластера {#azure-cluster}

Создайте [аккаунт](https://portal.azure.com/#home) в Azure и пополните [счёт](https://portal.azure.com/#view/Microsoft_Azure_GTM/ModernBillingMenuBlade/~/BillingAccounts) аккаунта на сумму, достаточную для работы девяти ВМ. Рассчитать примерную стоимость содержания инфраструктуры в зависимости от региона и прочих обстоятельств можно с помощью [калькулятора](https://azure.com/e/26977c150e854617a888fb3a7d1a399d).

Аутентификация в провайдере Azure для Terraform осуществляется через CLI:

1. Скачать, установить и настроить Azure CLI можно, следуя [этой](https://learn.microsoft.com/ru-ru/cli/azure/install-azure-cli) инструкции.
2. Авторизоваться в Azure с помощью Azure CLI можно в интерактивном режиме командой `az login`, а для создания пары SSH-ключей (Linux, macOS) проще всего будет воспользоваться командой `ssh-keygen`.

После авторизации в Azure и генерации SSH-ключей нужно изменить дефолтное значение следующих переменных в корневом файле `variables.tf`:

1. `auth_location` – название региона, где будет развернута инфраструктура. Список доступных регионов в зависимости от подписки можно получить командой `az account list-locations | grep "displayName"`.
2. `ssh_key_path` – путь к публичной части сгенерированного SSH-ключа.

Теперь, находясь в поддиректории `azure`, можно выполнить последовательность следующих команд для установки провайдера, инициализации модулей и создания инфраструктуры:

1. `terraform init` – установка провайдера и инициализация модулей.
2. `terraform plan` – создание плана будущей инфраструктуры.
3. `terraform apply` (повторное выполнение) – создание ресурсов в облаке.

Далее используются команды `terraform plan`, `terraform apply` и `terraform destroy` (уничтожение созданной инфраструктуры).

## Создание инфраструктуры в Google Cloud Platform для развертывания YDB кластера {#gcp-cluster}

Зарегистрируйтесь в Google Cloud Console и [создайте](https://console.cloud.google.com/projectselector2/home) проект. Активируйте [платежный аккаунт](https://console.cloud.google.com/billing/manage) и пополните его средствами для запуска девяти ВМ. Рассчитать стоимость можно в [калькуляторе](https://cloud.google.com/products/calculator).

Настройте GCP CLI:

1. Актируйте [Compute Engine API](https://console.cloud.google.com/apis/api/compute.googleapis.com/metrics) и [Cloud DNS API](https://console.cloud.google.com/apis/api/dns.googleapis.com/metrics).
2. Скачайте и установите GCP CLI, следуя [этой](https://cloud.google.com/sdk/docs/install) инструкции.
3. Перейдите в поддиректорию `.../google-cloud-sdk/bin` и выполните команду `./gcloud compute regions list` для получения списка доступных регионов.
4. Выполните команду `./gcloud auth application-default login` для настройки профиля подключения.

Перейдите в поддиректорию `gcp` (находится в скаченном репозитории) и в файле `variables.tf` задайте актуальные значения следующим переменным:

1. `project` – название проекта, которое было задано в облачной консоли Google Cloud.
2. `region` – регион, где будет развернута инфраструктура.
3. `zones` – список зон доступности, в которых будут созданы подсети и ВМ.

Теперь, находясь в поддиректории `gcp`, можно выполнить последовательность следующих команд для установки провайдера, инициализации модулей и создания инфраструктуры:

1. `terraform init` – установка провайдера и инициализация модулей.
2. `terraform plan` – создание плана будущей инфраструктуры.
3. `terraform apply` (повторное выполнение) – создание ресурсов в облаке.

Далее используются команды `terraform plan`, `terraform apply` и `terraform destroy` (уничтожение созданной инфраструктуры).

## Создание инфраструктуры в Yandex Cloud для развертывания YDB кластера {#yc-cluster}

Для создания инфраструктуры в Yandex Cloud с помощью Terraform нужно:

1. Подготовить облако к работе:

   - [Зарегистрироваться](https://console.yandex.cloud) в Yandex Cloud.
   - [Подключить](https://cloud.yandex/ru/docs/billing/concepts/billing-account) платежный аккаунт.
   - [Убедится](https://billing.yandex.cloud/) в наличии достаточного количества средств для создания девяти ВМ.

2. Установить и настроить Yandex Cloud CLI:

   - [Скачать](https://cloud.yandex/ru/docs/cli/quickstart) Yandex Cloud CLI.
   - [Создать](https://cloud.yandex/ru/docs/cli/quickstart#initialize) профиль

3. [Создать](https://cloud.yandex/ru/docs/tutorials/infrastructure-management/terraform-quickstart#get-credentials) сервисный аккаунт с помощью CLI.

4. [Сгенерировать](https://cloud.yandex/ru/docs/cli/operations/authentication/service-account#auth-as-sa) авторизованный ключ в JSON формате для подключения Terraform к облаку с помощью CLI: `yc iam key create --service-account-name <acc name> --output <file name> --folder-id <cloud folder id>`. В терминал будет выведена информация о созданном ключе:

   ```text
   id: ajenap572v8e1l...
   service_account_id: aje90em65r69...
   created_at: "2024-09-03T15:34:57.495126296Z"
   key_algorithm: RSA_2048
   ```

   Авторизованный ключ будет создан в директории, где вызывалась команда.

5. [Настроить](https://cloud.yandex/ru/docs/tutorials/infrastructure-management/terraform-quickstart#configure-provider) Yandex Cloud Terraform провайдера.

6. Скачать данный репозиторий командой `git clone https://github.com/ydb-platform/ydb-terraform.git`.

7. Перейти в директорию `yandex_cloud` (директория в скаченном репозитории) и внести изменения в следующие переменные, в файле `variables.tf`:

   - `key_path` – путь к сгенерированному авторизованному ключу с помощью CLI.
   - `cloud_id` – ID облака. Можно получить список доступных облаков командой `yc resource-manager cloud list`.
   - `folder_id` – ID Cloud folder. Можно получить командой `yc resource-manager folder list`.

Теперь, находясь в поддиректории `yandex_cloud`, можно выполнить последовательность следующих команд для установки провайдера, инициализации модулей и создания инфраструктуры:

1. `terraform init` – установка провайдера и инициализация модулей.
2. `terraform plan` – создание плана будущей инфраструктуры.
3. `terraform apply` (повторное выполнение) – создание ресурсов в облаке.

Далее используются команды `terraform plan`, `terraform apply` и `terraform destroy` (уничтожение созданной инфраструктуры).

> [!NOTE]
> С помощью Yandex Cloud провайдера можно не только создавать инфраструктуру для дальнейшего развертывания на ней YDB кластера с помощью [Ansible](initial-deployment/index.md), но и управлять [serverless или dedicated](https://yandex.cloud/ru/services/ydb) версией YDB прямо из Terraform. О возможностях работы с YDB в Yandex Cloud читайте в разделе [Работа с YDB через Terraform](https://cloud.yandex/ru/docs/ydb/terraform/intro) документации Yandex Cloud.
