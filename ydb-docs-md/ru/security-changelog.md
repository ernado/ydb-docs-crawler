---
title: "Список изменений безопасности"
url: "https://ydb.tech/docs/ru/security-changelog?version=v26.1"
doc_path: "ru/security-changelog"
version: "v26.1"
lang: "ru"
source_path: "ru/core/security-changelog.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/security-changelog.md"
description: "Исправлено в YDB 22.4.44, 2022-11-28 CVE-2022-28228."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Список изменений безопасности

## Исправлено в YDB 22.4.44, 2022-11-28 {#28-11-2022}

### CVE-2022-28228

В сервере YDB обнаружено чтение за пределами допустимого адресного пространства. Злоумышленник с помощью специально сконструированного запроса с оператором insert может получить доступ к конфиденциальной информации или вызвать сбой.

Ссылка на CVE: [https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28228).

Обнаружено благодаря Максиму Арнольду.

## Исправлено в YDB Go SDK v3.53.3, 2023-10-17 {#17-10-2023}

### CVE-2023-45825

Токен авторизации может утекать через логи

Ссылка на CVE: [https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-45825](https://nvd.nist.gov/vuln/detail/CVE-2023-45825).

Обнаружено благодаря Сергею Фостер.
