---
title: "Histogram"
url: "https://ydb.tech/docs/ru/yql/reference/udf/list/histogram?version=v26.1"
doc_path: "ru/yql/reference/udf/list/histogram"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/udf/list/histogram.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/udf/list/histogram.md"
description: "Набор вспомогательных функций для агрегатной функции HISTOGRAM. В описании сигнатур ниже под HistogramStruct подразумевается результат работы агрегатной функции"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Histogram

Набор вспомогательных функций для [агрегатной функции HISTOGRAM](../../builtins/aggregation.md). В описании сигнатур ниже под HistogramStruct подразумевается результат работы агрегатной функции `HISTOGRAM`, `LinearHistogram` или `LogarithmicHistogram`, который является структурой определенного вида.

## Список функций {#spisok-funkcij}

- `Histogram::Print(HistogramStruct{Flags:AutoMap}, Byte?) -> String`
- `Histogram::Normalize(HistogramStruct{Flags:AutoMap}, [Double?]) -> HistogramStruct` - во втором аргументе желаемая площадь гистограммы, по умолчанию 100.
- `Histogram::ToCumulativeDistributionFunction(HistogramStruct{Flags:AutoMap}) -> HistogramStruct`
- `Histogram::GetSumAboveBound(HistogramStruct{Flags:AutoMap}, Double) -> Double`
- `Histogram::GetSumBelowBound(HistogramStruct{Flags:AutoMap}, Double) -> Double`
- `Histogram::GetSumInRange(HistogramStruct{Flags:AutoMap}, Double, Double) -> Double`
- `Histogram::CalcUpperBound(HistogramStruct{Flags:AutoMap}, Double) -> Double`
- `Histogram::CalcLowerBound(HistogramStruct{Flags:AutoMap}, Double) -> Double`
- `Histogram::CalcUpperBoundSafe(HistogramStruct{Flags:AutoMap}, Double) -> Double`
- `Histogram::CalcLowerBoundSafe(HistogramStruct{Flags:AutoMap}, Double) -> Double`

У `Histogram::Print` есть опциональный числовой аргумент, который задает максимальную длину столбцов гистограммы (в символах, так как гистограмма рисуется в технике ASCII-арт). Значение по умолчанию — 25. Данная функция предназначена в первую очередь для просмотра гистограмм в консоли.
