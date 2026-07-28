---
title: "Contributing to YDB documentation"
url: "https://ydb.tech/docs/en/contributor/documentation/?version=v26.1"
doc_path: "en/contributor/documentation/"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/documentation/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/documentation/index.md"
description: "YDB follows the \"Documentation as Code\" approach, meaning that the YDB documentation is developed using similar techniques and tools as its main C++ source code"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Contributing to YDB documentation

YDB follows the "Documentation as Code" approach, meaning that the YDB documentation is developed using similar techniques and tools as its main C++ source code.

The documentation source code consists of Markdown files and YAML configuration files located in the [ydb/docs folder of the primary YDB GitHub repository](https://github.com/ydb-platform/ydb/tree/main/ydb/docs). The compiler for this source code is an open-source tool called [Diplodoc](https://diplodoc.com/en/). See [its documentation](https://diplodoc.com/docs/en/) for details on its Markdown syntax flavor, configuration options, extensions, and more.

The process of suggesting changes to the documentation source code is mostly similar to changing any other YDB source code, so most of [Development process: working on a change for YDB](../suggest-change.md) applies. The main additional considerations are:

- [Extra precommit checks](https://github.com/ydb-platform/ydb/actions/workflows/docs_build.yaml) run for pull requests to the documentation. One of these checks posts a comment with a link to an online preview of the changes or a list of errors.
- The code review process includes additional steps. See [Review process for YDB documentation](review.md) and [YDB documentation style guide](style-guide.md).
- For small changes like fixing a typo, you can use the "Edit this file" feature in the GitHub web interface. Each documentation page has an "Edit on GitHub" link (represented by a pencil icon in the top-right corner) that directs you to the page's source code in the GitHub web interface.

After a pull request to the documentation is merged into the `main` branch, the [CI/CD pipeline](https://github.com/ydb-platform/ydb/actions/workflows/docs_release.yaml) automatically deploys it to the YDB website. Documentation is also automatically deployed for stable YDB server versions from `git` branches named `stable-*`, where these versions are developed. If C++ code and documentation for a feature were committed separately and a new stable branch was forked between these commits, backporting some changes to the stable branch might be necessary. The same applies to typo fixes and other "bug fixes" to the documentation content. See [Manage YDB Releases](../manage-releases.md) for more details on the YDB release process.

## See also

- [YDB Documentation Structure](structure.md)
- [YDB documentation genres](genres.md)
- [GitHub documentation](https://docs.github.com/en)
- [Git documentation](https://git-scm.com/doc)
