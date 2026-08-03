---
title: "Machine Learning"
url: "https://ydb.tech/docs/ru/concepts/analytics/concepts/ml?version=v26.1"
doc_path: "ru/concepts/analytics/concepts/ml"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/analytics/concepts/ml.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/analytics/concepts/ml.md"
description: "YDB служит эффективной платформой для хранения и обработки данных в ML-пайплайнах. Вы можете использовать привычные инструменты, такие как Jupyter Notebook и Ap"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Machine Learning

YDB служит эффективной платформой для хранения и обработки данных в ML-пайплайнах. Вы можете использовать привычные инструменты, такие как Jupyter Notebook и Apache Spark, на всех этапах жизненного цикла ML-модели.

## Feature Engineering

Используйте YDB в качестве движка для подготовки признаков:

- SQL и [dbt](../../../integrations/migration/dbt.md): Выполняйте сложные аналитические запросы для агрегации «сырых» данных и создания новых признаков. Материализуйте наборы признаков в строковые таблицы для быстрого доступа;
- Apache Spark: Для более сложных преобразований, требующих логики на Python или Scala, используйте [коннектор к Apache Spark](../../../integrations/query-engines/spark.md) для чтения данных, их обработки и сохранения результатов обратно в YDB.

## Обучение моделей {#obuchenie-modelej}

YDB может выступать в роли быстрого и масштабируемого источника данных для обучения моделей:

- Интеграция с Jupyter: Подключайтесь к YDB из [Jupyter Notebook](../../../integrations/gui/jupyter.md) для ad-hoc анализа и прототипирования моделей;
- Распределённое обучение: коннектор к Apache Spark обеспечивает параллельное чтение данных со всех узлов кластера напрямую в Spark DataFrame. Это позволяет загружать обучающие выборки для моделей в PySpark MLlib, CatBoost, Scikit-learn и другие библиотеки.

## Online Feature Store

Сочетание [строковых](../../datamodel/table.md#row-oriented-tables) (OLTP) и [колоночных](../../datamodel/table.md#column-oriented-tables) (OLAP) таблиц в YDB позволяет реализовать на одной платформе не только аналитическое хранилище, но и [Online Feature Store](https://en.wikipedia.org/wiki/Feature_engineering#Feature_stores).

- Используйте строковые (OLTP) таблицы для хранения признаков, требующих точечного чтения с низкой задержкой; это позволяет ML-моделям в реальном времени получать признаки для инференса.
- Используйте колоночные (OLAP) таблицы для хранения исторических данных и пакетного расчёта этих признаков.
