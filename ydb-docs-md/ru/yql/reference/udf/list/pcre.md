---
title: "Pcre"
url: "https://ydb.tech/docs/ru/yql/reference/udf/list/pcre?version=v26.1"
doc_path: "ru/yql/reference/udf/list/pcre"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/udf/list/pcre.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/udf/list/pcre.md"
description: "Библиотека Pcre на данный момент является алиасом к Hyperscan. На данный момент доступны: Hyperscan (Intel). Pire (Яндекс). Re2 (Google)."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Pcre

Библиотека Pcre на данный момент является алиасом к [Hyperscan](hyperscan.md).

На данный момент доступны:

- [Hyperscan](hyperscan.md) (Intel)
- [Pire](pire.md) (Яндекс)
- [Re2](re2.md) (Google)

Все три модуля предоставляют примерно одинаковый набор функций с идентичным интерфейсом, что позволяет переключаться между ними с минимальными изменениями запроса.

HyperScan внутри имеет несколько реализаций с использованием разных наборов процессорных инструкций, среди которых автоматически выбирается нужная в соответствии с текущим процессором. В Hyperscan также доступны отдельные функции с backtracking (возможность сослаться на предыдущую найденную часть строки), которые реализованы через гибридное использование двух библиотек Hyperscan и libpcre.

[Pire](https://github.com/yandex/pire) (Perl Incompatible Regular Expressions) это разработанная в Яндексе очень быстрая библиотека регулярных выражений. На нижнем уровне она просматривает входную строку один раз, подряд, без откатов, и тратит (на x86 и x86_64) по 5 инструкций на символ. Но с 2011-2013 года эта библиотека практически не развивается и как намекает название («i» расшифровывается как incompatible), возможно потребуется адаптировать сами выражения.

Hyperscan и Pire рассчитаны в первую очередь под Grep и Match.

Модуль Re2 использует [google::RE2](https://github.com/google/re2), где реализован широкий ассортимент возможностей ([см. официальную документацию](https://github.com/google/re2/wiki/Syntax)). Основной плюс библиотеки Re2 — развитый функционал по Capture и Replace, если вам нужны эти функции, то рекомендуется пользоваться именно ей.
