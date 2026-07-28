---
title: "Security changelog"
url: "https://ydb.tech/docs/en/security-changelog?version=v26.1"
doc_path: "en/security-changelog"
version: "v26.1"
lang: "en"
source_path: "en/core/security-changelog.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/security-changelog.md"
description: "Fixed in YDB 22.4.44, 2022-11-28 CVE-2022-28228."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Security changelog

## Fixed in YDB 22.4.44, 2022-11-28 {#28-11-2022}

### CVE-2022-28228

Out-of-bounds read was discovered in YDB server. An attacker could construct a query with an insert statement that would allow them to access confidential information or cause a crash.

Link to CVE: [https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28228).

Credits: Maxim Arnold.

## Fixed in YDB Go SDK v3.53.3, 2023-10-17 {#17-10-2023}

### CVE-2023-45825

Token in custom credentials object can leak through logs.

Link to CVE: [https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-45825](https://nvd.nist.gov/vuln/detail/CVE-2023-45825).

Credits: Sergey Foster.
