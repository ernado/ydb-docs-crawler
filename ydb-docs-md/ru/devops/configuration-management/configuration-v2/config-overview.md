---
title: "Обзор конфигурации V2"
url: "https://ydb.tech/docs/ru/devops/configuration-management/configuration-v2/config-overview?version=v26.1"
doc_path: "ru/devops/configuration-management/configuration-v2/config-overview"
version: "v26.1"
lang: "ru"
source_path: "ru/core/devops/configuration-management/configuration-v2/config-overview.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/devops/configuration-management/configuration-v2/config-overview.md"
description: "Для развёртывания кластера YDB, добавления в кластер новых узлов и изменения параметров требуется конфигурация. Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Обзор конфигурации V2

Для развёртывания кластера YDB, добавления в кластер новых узлов и изменения параметров требуется конфигурация.

> [!WARNING]
> Эта статья посвящена кластерам YDB, в которых используется [конфигурация V2](index.md). Данный способ конфигурирования пока является экспериментальным и доступен только для версий YDB начиная с v25.1. Для использования в продакшене мы рекомендуем выбирать [конфигурацию V1](../index.md) — она является основной и официально поддерживаемой для всех кластеров YDB.

Конфигурация кластера YDB V2 представляет собой текстовый файл в формате [YAML](https://en.wikipedia.org/wiki/YAML). В минимальном варианте он содержит секцию `config` с различными параметрами, необходимыми для запуска и настройки узлов кластера, а также секцию с метаданными `metadata`. Расширенные возможности для гибкого конфигурирования описаны в статье [Domain-specific language (DSL) конфигурации кластера](dynamic-config-selectors.md). Подробнее о доступных параметрах можно узнать в [справке по конфигурации](config-settings.md).

<details>
<summary>Пример файла конфигурации V2</summary>

```yaml
metadata:
  cluster: ""
  version: 0
config:
  hosts:
    - host: localhost
  drive:
    - type: RAM
  grpc_config:
    port: 2136
  monitoring_config:
    monitoring_port: 8765
```

</details>

## Управление конфигурацией {#upravlenie-konfiguraciej}

![Высокоуровневый обзор управления конфигурацией V2](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/configuration-management/configuration-v2/_assets/config-v2-overview.png)

За управление состоянием конфигурационного файла отвечает сам кластер YDB, и он же является единственным источником правды о том, как он сейчас сконфигурирован. За надёжное сохранение текущего состояния, являющегося источником правды, отвечает механизм [распределённой конфигурации](../../../concepts/glossary.md#distributed-configuration); как это работает технически, подробнее описано в статье [Устройство механизма конфигурации V2](../../../contributor/configuration-v2.md). Узнать текущее состояние конфигурации кластера можно с помощью консольной команды [ydb admin cluster config fetch](../../../reference/ydb-cli/commands/configuration/cluster/fetch.md), а состояние каждого конкретного узла — через его [Embedded UI](../../../reference/embedded-ui/index.md).

Изменение конфигурации кластера YDB осуществляется администратором следующим образом:

1. Сохранение текущего состояния конфигурации кластера в локальный файл через [ydb admin cluster config fetch](../../../reference/ydb-cli/commands/configuration/cluster/fetch.md).
2. Редактирование нужных параметров в файле в текстовом редакторе или любым другим удобным способом.
3. Загрузка изменений обратно на кластер посредством вызова команды [ydb admin cluster config replace](../../../reference/ydb-cli/commands/configuration/cluster/replace.md).

<details>
<summary>Пример изменения конфигурации</summary>

```bash
$ ydb -e grpc://<ydb.example.com>:2135 admin cluster config fetch > config.yaml     # 1
$ vim config.yaml                                                                   # 2
$ ydb -e grpc://<ydb.example.com>:2135 admin cluster config replace -f config.yaml  # 3
```

</details>

Загрузка изменений обратно на кластер не всегда проходит успешно. Помимо базовой валидации корректности конфигурационного файла, у системы есть защита от конкурентного изменения несколькими администраторами. Система инкрементирует поле `metadata.version` при каждом изменении конфигурации и отказывается принимать новую версию, если её номер не совпадает с ожидаемым, так как это означает, что между `fetch` и `replace` было другое изменение, и `replace` его бы стёр. Чтобы минимизировать такие конфликты, можно использовать подход [«Инфраструктура как код»](https://ru.wikipedia.org/wiki/%D0%98%D0%BD%D1%84%D1%80%D0%B0%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0_%D0%BA%D0%B0%D0%BA_%D0%BA%D0%BE%D0%B4): хранить копию конфигурационного файла в репозитории [системы управления версиями](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F%D0%BC%D0%B8) (например, [Git](https://git-scm.com/)) и запускать команды `fetch` и `replace` не вручную, а только из привязанной к этому репозиторию системы [непрерывной интеграции](https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%BF%D1%80%D0%B5%D1%80%D1%8B%D0%B2%D0%BD%D0%B0%D1%8F_%D0%B8%D0%BD%D1%82%D0%B5%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D1%8F) и [доставки](https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%BF%D1%80%D0%B5%D1%80%D1%8B%D0%B2%D0%BD%D0%B0%D1%8F_%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B0) (CI/CD), реагирующей на изменения конфигурационного файла YDB в репозитории и обеспечивающей последовательную отправку всех изменений на кластер YDB.

<details>
<summary>Cхема с подходом «Инфраструктура как код»</summary>

![Cхема с подходом «Инфраструктура как код»](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/devops/configuration-management/configuration-v2/_assets/config-v2-iac.png)

</details>

Каждый узел кластера YDB сохраняет локально копию конфигурации в директорию, указанную в аргументе запуска `ydbd --config-dir`. Эта локальная копия используется в следующих ситуациях:

1. Для применения настроек, которые нужны на самом старте работы узла, ещё до того, как у него появляется возможность начать общаться с другими узлами кластера. Изменение таких настроек может требовать перезапуска узла.
2. Для [первоначального развёртывания](config-overview.md#initial-deployment) и [расширения](config-overview.md#cluster-expansion) кластера.
3. В случае форс-мажора, если с основным механизмом управления конфигурацией возникли проблемы, требующие ручного вмешательства.

Выше описан основной механизм управления конфигурацией V2 YDB. В зависимости от предпочитаемого [способа управления инфраструктурой](../../deployment-options/index.md) может предоставляться дополнительная автоматизация.

## Базовые сценарии использования конфигурации {#bazovye-scenarii-ispolzovaniya-konfiguracii}

### Первоначальное развёртывание кластера YDB {#initial-deployment}

Для конфигурации кластера при первоначальном развёртывании рекомендуется использовать инструкции для выбранного способа управления инфраструктурой:

- [Развёртывание YDB кластера с помощью Ansible](../../deployment-options/ansible/initial-deployment/index.md);
- [Начало работы с YDB в Kubernetes](../../deployment-options/kubernetes/initial-deployment.md);
- [Развёртывание YDB кластера вручную](../../deployment-options/manual/initial-deployment/index.md).

### Обновление конфигурации {#update-config}

Для обновления конфигурации на уже развёрнутом кластере необходимо воспользоваться соответствующими командами в зависимости от способа развёртывания:

- [Обновление конфигурации кластеров YDB, развёрнутых с Ansible](../../deployment-options/ansible/update-config.md);
- [Обновление конфигурации кластеров YDB, развёрнутых вручную](../../deployment-options/manual/update-config.md).

Если изменения конфигурации затрагивают параметры, требующие перезапуска узлов кластера, воспользуйтесь процедурой [rolling restart](../../../reference/ydbops/rolling-restart-scenario.md). Подробнее о ней в зависимости от способа развёртывания:

- [Перезапуск кластера, развёрнутого с помощью Ansible](../../deployment-options/ansible/restart.md);
- [Перезапуск кластера, развёрнутого вручную](../../../reference/ydbops/rolling-restart-scenario.md).

### Расширение кластера {#cluster-expansion}

При [расширении кластера](cluster-expansion.md) конфигурация доставляется на старые и новые узлы по-разному:

- На узлы, существовавшие до расширения, изменения доставляются автоматически при вызове [ydb admin cluster config replace](../../../reference/ydb-cli/commands/configuration/cluster/replace.md).
- Перед первым запуском новых узлов локальная копия доставляется специальной командой [ydb admin node config init](../../../reference/ydb-cli/commands/configuration/node/init.md), а не самим узлом.

## Смотрите также {#smotrite-takzhe}

- [Справка по параметрам конфигурации](config-settings.md)
- [Сравнение конфигураций кластера YDB: V1 и V2](../compare-configs.md)
