---
title: "Work with YDB from Jupyter Notebook"
url: "https://ydb.tech/docs/en/integrations/gui/jupyter?version=v26.1"
doc_path: "en/integrations/gui/jupyter"
version: "v26.1"
lang: "en"
source_path: "en/core/integrations/gui/jupyter.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/integrations/gui/jupyter.md"
description: "Jupyter Notebook is an open-source tool for creating shareable documents that combine code, plain language descriptions, data, rich visualizations, and interact"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Work with YDB from Jupyter Notebook

[Jupyter Notebook](https://jupyter.org) is an open-source tool for creating shareable documents that combine code, plain language descriptions, data, rich visualizations, and interactive controls.

The [ydb-sqlalchemy dialect](https://github.com/ydb-platform/ydb-sqlalchemy/releases) enables working with YDB from tools such as:

- [Pandas](https://pandas.pydata.org/)
- [JupySQL](https://jupysql.ploomber.io/)

## Example

A detailed usage example is available as a [notebook](https://github.com/ydb-platform/ydb-sqlalchemy/blob/main/examples/jupyter_notebook/YDB%20SQLAlchemy%20%2B%20Jupyter%20Notebook%20Example.ipynb).

Prerequisites:

1. Python 3.8+
2. [Jupyter Notebook](https://jupyter.org/install#jupyter-notebook)
3. Existing YDB cluster, a single-node one from [quickstart](../../quickstart.md) will suffice

To run the example, download the notebook file [YDB SQLAlchemy - Jupyter Notebook Example.ipynb](https://raw.githubusercontent.com/ydb-platform/ydb-sqlalchemy/refs/heads/main/examples/jupyter_notebook/YDB%20SQLAlchemy%20%2B%20Jupyter%20Notebook%20Example.ipynb), open it in Jupyter, and follow each cell sequentially, executing code as necessary.
