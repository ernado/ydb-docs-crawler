---
title: "Добавление групп хранения"
url: "https://ydb.tech/docs/ru/maintenance/manual/adding_storage_groups?version=v26.1"
doc_path: "ru/maintenance/manual/adding_storage_groups"
version: "v26.1"
lang: "ru"
source_path: "ru/core/maintenance/manual/adding_storage_groups.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/maintenance/manual/adding_storage_groups.md"
description: "По мере роста объема хранимых данных может понадобиться добавление дисков в кластер YDB. Диски могут быть добавлены в уже существующие узлы или вместе с новыми"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Добавление групп хранения

По мере роста объема хранимых данных может понадобиться добавление дисков в кластер YDB. Диски могут быть добавлены в уже существующие узлы или вместе с новыми узлами. Для того, чтобы ресурсы новых дисков стали доступны БД, необходимо добавить [группы хранения](../../concepts/glossary.md#storage-groups).

Чтобы добавить новые группы хранения, воспользуйтесь утилитой [YDB DSTool](../../reference/ydb-dstool/index.md).

Просмотрите список пулов хранения кластера:

```bash
ydb-dstool -e <bs_endpoint> pool list
```

`<bs_endpoint>` - эндпоинт произвольного [узла хранения](../../concepts/glossary.md#storage-node) кластера.

> Пример результата:
>
> ```text
> ┌──────────────┬──────────────────┬────────────────┬──────┬──────────────┬──────────────┐
> │ BoxId:PoolId │ PoolName         │ ErasureSpecies │ Kind │ Groups_TOTAL │ VDisks_TOTAL │
> ├──────────────┼──────────────────┼────────────────┼──────┼──────────────┼──────────────┤
> │ [1:1]        │ /Root/testdb:ROT │ mirror-3-dc    │ ROT  │ 1            │ 9            │
> └──────────────┴──────────────────┴────────────────┴──────┴──────────────┴──────────────┘
> ```

Следующая команда добавит 10 групп в пул `/Root/testdb:ROT`:

```bash
ydb-dstool -e <bs_endpoint> group add --pool-name /Root/testdb:ROT --groups 10
```

В случае успеха команда вернет нулевой `exit status`. Иначе команда вернет ненулевой статус и  
 выведет сообщение об ошибке в `stderr`.

Чтобы проверить возможность добавления групп без фактического добавления, используйте глобальный параметр `--dry-run`. Следующая команда проверит возможность добавления 100 групп в пул `/Root/testdb:ROT`:

```bash
ydb-dstool --dry-run -e <bs_endpoint> group add --pool-name /Root/testdb:ROT --groups 100
```

Параметр `--dry-run` позволяет оценить, какое максимальное число групп можно добавить в пул.
