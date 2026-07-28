---
title: "Подготовка к развертыванию"
url: "https://ydb.tech/docs/ru/devops/deployment-options/ansible/initial-deployment/deployment-preparation?version=v26.1"
doc_path: "ru/devops/deployment-options/ansible/initial-deployment/deployment-preparation"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/deployment-options/ansible/initial-deployment/deployment-preparation.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/deployment-options/ansible/initial-deployment/deployment-preparation.md"
description: "Предварительные требования Выберите топологию для установки."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Подготовка к развертыванию

## Предварительные требования {#prerequisites}

### Выберите топологию для установки {#topology-select}

Перед установкой выберите подходящую топологию кластера YDB — от неё зависит количество необходимых серверов и дисков:

**Для начала работы с YDB**, рекомендуется выбрать топологию `mirror-3dc-3-nodes`. Для этого потребуется всего 3 сервера и 9 дисков для пользовательских данных — это самый простой и быстрый способ создать пилотный кластер.

**Для масштабных развёртываний** выберите одну из следующих опций:

- `mirror-3-dc` — для кластеров, размещённых в нескольких дата-центрах. Потребуется не менее 9 серверов и 9 дисков для пользовательских данных.
- `block-4-2` — для размещения кластера в одном дата-центре. Потребуется не менее 8 серверов и 8 дисков для пользовательских данных.

В каждом сервере должен быть хотя бы один отдельный диск для пользовательских данных. Рекомендуется также добавить отдельный небольшой диск под операционную систему. Подробнее о различных вариантах топологии и избыточности читайте в [этой статье](../../../../concepts/topology.md).

В дальнейшем можно при необходимости [расширять кластер](../../../configuration-management/configuration-v1/cluster-expansion.md) без остановки его работы и прерывания доступа пользователей к данным.

### Настройка серверов {#server-configuration}

> [!NOTE]
> Рекомендуемые требования к серверам:
>
> - 16 CPU (рассчитывается исходя из утилизации 8 CPU узлом хранения и 8 CPU динамическим узлом).
> - 16 GB RAM (рекомендуемый минимальный объем RAM).
> - Дополнительные SSD-диски для данных, не менее 120 GB каждый.
> - Доступ по SSH.
> - Сетевая связность между машинами в кластере.
> - ОС: Ubuntu 18+, Debian 9+.
> - Доступ в интернет для обновления репозиториев и скачивания необходимых пакетов.
>
> Подробнее см. [Системные требования и рекомендации для YDB](../../../concepts/system-requirements.md).

При использовании виртуальных машин у публичного облачного провайдера рекомендуется следовать [Развёртывание инфраструктуры для кластера YDB с помощью Terraform](../preparing-vms-with-terraform.md).

### Настройка программного обеспечения {#nastrojka-programmnogo-obespecheniya}

Для работы с проектом на локальной (промежуточной или установочной) машине потребуется:

- Python 3 версии 3.10+
- Поддерживаются версии Ansible core начиная с 2.11 и до 2.18
- Рабочая директория на сервере с SSH-доступом ко всем серверам кластера

> [!TIP]
> Рекомендуется хранить рабочую директорию и все файлы, созданные в ходе этого руководства, в репозитории [системы управления версиями](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F%D0%BC%D0%B8), например [Git](https://git-scm.com/). Если несколько DevOps-инженеров будут работать с развёртываемым кластером, они должны взаимодействовать в общем репозитории.

Если Ansible уже установлен, можно перейти к разделу [«Настройка проекта Ansible»](deployment-preparation.md#ansible-project-setup). Если Ansible ещё не установлен, установите его одним из следующих способов:

<details>
<summary>Установка Ansible глобально</summary>

На примере Ubuntu 22.04 LTS:

- Обновите список пакетов apt командой `sudo apt-get update`.
- Обновите пакеты командой `sudo apt-get upgrade`.
- Установите пакет `software-properties-common` для управления источниками программного обеспечения вашего дистрибутива — `sudo apt install software-properties-common`.
- Добавьте новый PPA в apt — `sudo add-apt-repository --yes --update ppa:ansible/ansible`.
- Установите Ansible — `sudo apt-get install ansible-core` (убедитесь, что устанавливаемая версия не выше 2.18 и не меньше 2.11; установка пакета просто `ansible` приведёт к устаревшей и неподходящей версии).
- Проверьте версию Ansible core — `ansible --version`.

</details>

<details>
<summary>Установка Ansible в виртуальное окружение Python</summary>

На примере Ubuntu 22.04 LTS:

- Обновите список доступных deb пакетов — `sudo apt-get update`.
- Установите пакет `python3-venv` для управления Python виртуальными окружениями — `sudo apt-get install venv`.
- Создайте директорию, где будет создано виртуальное окружение. Например, `mkdir venv-ansible`.
- Создайте виртуальное окружение Python — `python3 -m venv venv-ansible`, где `venv-ansible` - путь к директории созданной на предыдущем шаге.
- Активируйте виртуальное окружение — `source venv-ansible/bin/activate`. Все дальнейшие действия с Ansible выполняются внутри виртуального окружения. Выйти из него можно командой `deactivate`.
- Установите рекомендуемую версию Ansible с помощью команды `pip3 install "ansible-core>=2.11,<2.19"` (убедитесь, что устанавливаемая версия не выше 2.18 и не меньше 2.11). Проверьте установленную версию Ansible — `ansible --version`.

</details>

Для получения дополнительной информации и других вариантов установки ознакомьтесь с [руководством по установке Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html).

## Настройка проекта Ansible {#ansible-project-setup}

### Установка YDB Ansible плейбуков {#ustanovka-ydb-ansible-plejbukov}

{% list tabs %}

- Через requirements.yaml

  ```bash
  cat <<EOF > requirements.yaml
  roles: []
  collections:
    - name: git+https://github.com/ydb-platform/ydb-ansible
      type: git
      version: latest
  EOF
  ansible-galaxy install -r requirements.yaml
  ```

- Однократно

  ```bash
  ansible-galaxy collection install git+https://github.com/ydb-platform/ydb-ansible.git,latest
  ```

{% endlist %}

После выполнения подготовительных мероприятий можно переходить к развёртыванию системы. Выберите инструкцию в соответствии с вашей конфигурацией:

- [Развёртывание кластера с использованием конфигурации V1](deployment-configuration-v1.md)
- [Развёртывание кластера с использованием конфигурации V2](deployment-configuration-v2.md)
