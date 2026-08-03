---
title: "PDiskReadLoad"
url: "https://ydb.tech/docs/ru/contributor/load-actors-pdisk-read?version=v26.1"
doc_path: "ru/contributor/load-actors-pdisk-read"
version: "v26.1"
lang: "ru"
source_path: "ru/core/contributor/load-actors-pdisk-read.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/contributor/load-actors-pdisk-read.md"
description: "Тестирует производительность чтения с PDisk. Нагрузка подается от имени VDisk. Актор создает на указанном PDisk чанки, записывает в них случайные данные и выпол"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# PDiskReadLoad

Тестирует производительность чтения с PDisk. Нагрузка подается от имени VDisk. Актор создает на указанном PDisk чанки, записывает в них случайные данные и выполняет чтение из них с указанными параметрами. После снятия нагрузки записанные актором данные удаляются.

Вы можете подать нагрузку двух видов:

- *Постоянная* — актор следит, чтобы одновременно было запущено указанное число запросов. Чтобы подать постоянную нагрузку, задайте нулевую паузу между запросами (например, `IntervalMsMin: 0`, `IntervalMsMax: 0`) и отличный от нуля `InFlightReads`.
- *Интервальная* — актор запускает запросы через заданные промежутки времени. Чтобы подать интервальную нагрузку, задайте ненулевую паузу между запросами (например, `IntervalMsMin: 10`, `IntervalMsMax: 100`). Максимальное количество одновременно выполняемых запросов задается параметром `InFlightReads`. Если его значение равно `0`, то ограничения нет.

## Параметры актора {#options}

Ниже описаны основные параметры актора. Полный список параметров смотрите в файле [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) Git-репозитория YDB.

| Параметр | Описание |
| --- | --- |
| `PDiskId` | Идентификатор нагружаемого PDisk на узле. |
| `PDiskGuid` | Глобально-уникальный идентификатор нагружаемого PDisk. |
| `VDiskId` | Нагрузка подается от имени VDisk со следующими реквизитами:<br>- `GroupID` — идентификатор группы.<br>- `GroupGeneration` — поколение группы.<br>- `Ring` — идентификатор кольца в группе.<br>- `Domain` — идентификатор фэйл-домена в кольце.<br>- `VDisk` — индекс VDisk в фэйл-домене. |
| `Chunks` | Параметры чанка.  <br>`Slots` — количество слотов в чанке, определяет размер записи.  <br>Вы можете указать несколько `Chunks`, и тогда выбор конкретного чанка для чтения будет определяться его `Weight`. |
| `DurationSeconds` | Продолжительность нагрузки в секундах. |
| `IntervalMsMin`,  <br>`IntervalMsMax` | Минимальный и максимальный промежутки времени между запросами при интервальной нагрузке в миллисекундах. Значение промежутка выбирается случайно из указанного диапазона. |
| `InFlightReads` | Количество одновременно обрабатываемых запросов на чтение. |
| `Sequential` | Тип чтения.<br>- `True` — последовательное.<br>- `False` — случайное. |
| `IsWardenlessTest` | Если PDiskReadLoad запускается на кластере, укажите `False`. Иначе (например, при запуске в юнит-тестах) укажите `True`. |

## Примеры {#examples}

Следующий актор читает данные блоками по `32` МБ, в течение `120` секунд, одновременно выполняются `64` запроса (постоянная нагрузка):

```proto
PDiskReadLoad: {
    PDiskId: 1000
    PDiskGuid: 2258451612736857634
    VDiskId: {
        GroupID: 11234
        GroupGeneration: 5
        Ring: 1
        Domain: 1
        VDisk: 3
    }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    Chunks: { Slots: 4096 Weight: 1 }
    DurationSeconds: 120
    IntervalMsMin: 0
    IntervalMsMax: 0
    InFlightReads: 64
    Sequential: false
    IsWardenlessTest: false
}
```

При просмотре результата тестирования наибольший интерес представляет следующее значение:

- `Average speed since start` — средняя скорость чтения с момента запуска в МБ/с, например `1257.148154`.

> [!TIP]
> **Хотите присоединиться к команде разработки YDB?**
>
> Ознакомьтесь с разделами о [команде YDB и открытых вакансиях](https://ydb.tech/ru/careers/), а также о [возможностях для студентов](https://ydb.tech/ru/students/).
