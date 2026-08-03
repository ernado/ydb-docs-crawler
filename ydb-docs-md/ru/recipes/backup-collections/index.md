---
title: "Рецепты для коллекций резервных копий"
url: "https://ydb.tech/docs/ru/recipes/backup-collections/?version=v26.1"
doc_path: "ru/recipes/backup-collections/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/backup-collections/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/backup-collections/index.md"
description: "Пошаговые руководства для типовых сценариев работы с коллекциями резервных копий. Начало работы."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Рецепты для коллекций резервных копий

Пошаговые руководства для типовых сценариев работы с коллекциями резервных копий.

## Начало работы {#nachalo-raboty}

- [Создание первой коллекции резервных копий](getting-started.md) — создание коллекции, резервное копирование и мониторинг операций

## Настройка окружений {#nastrojka-okruzhenij}

- [Настройка резервного копирования для разных сред](multi-environment-setup.md) — конфигурация для разработки и продуктовых сред
- [Стратегия резервного копирования для микросервисов](microservices-backup-strategy.md) — организация резервных копий по границам сервисов

## Внешнее хранилище {#vneshnee-hranilishe}

- [Экспорт резервных копий во внешнее хранилище](exporting-to-external-storage.md) — экспорт в S3 или файловую систему для аварийного восстановления
- [Импорт и восстановление резервных копий](importing-and-restoring.md) — восстановление из внешнего хранилища

## Обслуживание {#obsluzhivanie}

- [Обслуживание и очистка резервных копий](maintenance-and-cleanup.md) — управление жизненным циклом и хранилищем
- [Проверка и тестирование резервных копий](validation-and-testing.md) — проверка целостности резервных копий

## См. также {#sm-takzhe}

- [Коллекции резервных копий](../../concepts/datamodel/backup-collection.md)
- [Резервное копирование и восстановление](../../devops/backup-and-recovery/index.md)
- [CREATE BACKUP COLLECTION](../../yql/reference/syntax/create-backup-collection.md)
- [BACKUP](../../yql/reference/syntax/backup.md)
- [RESTORE](../../yql/reference/syntax/restore-backup-collection.md)
- [DROP BACKUP COLLECTION](../../yql/reference/syntax/drop-backup-collection.md)
