---
title: "Machine Learning"
url: "https://ydb.tech/docs/en/concepts/analytics/concepts/ml?version=v26.1"
doc_path: "en/concepts/analytics/concepts/ml"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/analytics/concepts/ml.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/analytics/concepts/ml.md"
description: "YDB serves as an effective platform for storing and processing data in ML pipelines. You can use familiar tools, such as Jupyter Notebook and Apache Spark, thro"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Machine Learning

YDB serves as an effective platform for storing and processing data in ML pipelines. You can use familiar tools, such as Jupyter Notebook and Apache Spark, throughout all stages of the ML model lifecycle.

## Feature Engineering

Use YDB as an engine for feature engineering:

- SQL and [dbt](../../../integrations/migration/dbt.md): execute complex analytical queries to aggregate raw data and create new features. Materialize feature sets into row-based tables for fast access;
- Apache Spark: for more complex transformations that require Python or Scala logic, use the [Apache Spark connector](../../../integrations/query-engines/spark.md) to read data, process it, and save the results back to YDB.

## Model Training

YDB can serve as a fast and scalable data source for model training:

- Jupyter Integration: connect to YDB from [Jupyter Notebook](../../../integrations/gui/jupyter.md) for ad-hoc analysis and model prototyping;
- distributed training: the Apache Spark connector enables parallel reading of data from all cluster nodes directly into a Spark DataFrame. This allows you to load training sets for models in PySpark MLlib, CatBoost, Scikit-learn, and other libraries.

## Online Feature Store

The combination of [row-based](../../datamodel/table.md#row-oriented-tables) (OLTP) and [columnar](../../datamodel/table.md#column-oriented-tables) (OLAP) tables in YDB allows you to implement not only an analytical warehouse but also an [Online Feature Store](https://en.wikipedia.org/wiki/Feature_engineering#Feature_stores) on a single platform.

- Use row-based (OLTP) tables to store features that require low-latency point reads; this allows ML models to retrieve features in real time for inference.
- Use columnar (OLAP) tables to store historical data and for the batch calculation of these features.
