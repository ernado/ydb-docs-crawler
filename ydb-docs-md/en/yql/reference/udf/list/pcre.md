---
title: "Pcre"
url: "https://ydb.tech/docs/en/yql/reference/udf/list/pcre?version=v26.1"
doc_path: "en/yql/reference/udf/list/pcre"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/udf/list/pcre.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/udf/list/pcre.md"
description: "The Pcre library is currently an alias to Hyperscan. Currently available engines: Hyperscan (Intel). Pire (Yandex). Re2 (Google)."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Pcre

The Pcre library is currently an alias to [Hyperscan](hyperscan.md).

Currently available engines:

- [Hyperscan](hyperscan.md) (Intel)
- [Pire](pire.md) (Yandex)
- [Re2](re2.md) (Google)

All three modules provide approximately the same set of functions with an identical interface. This lets you switch between them with minimal changes to a query.

Inside Hyperscan, there are several implementations that use different sets of processor instructions, with the relevant instruction automatically selected based on the current processor. In HyperScan, some functions support backtracking (referencing the previously found part of the string). Those functions are implemented through hybrid use of the two libraries: Hyperscan and libpcre.

[Pire](https://github.com/yandex/pire) (Perl Incompatible Regular Expressions) is a very fast library of regular expressions developed by Yandex. At the lower level, it scans the input string once, without any lookaheads or rollbacks, spending 5 machine instructions per character (on x86 and x86_64). However, since the library almost hasn't been developed since 2011-2013 and its name says "Perl incompatible", you may need to adapt your regular expressions a bit.

Hyperscan and Pire are best-suited for Grep and Match.

The Re2 module uses [google::RE2](https://github.com/google/re2) that offers a wide range of features ([see the official documentation](https://github.com/google/re2/wiki/Syntax)). The main benefit of the Re2 is its advanced Capture and Replace functionality. Use this library, if you need those functions.
