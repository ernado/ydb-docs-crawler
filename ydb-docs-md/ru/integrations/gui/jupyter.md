---
title: "Работа с YDB с помощью Jupyter Notebook"
url: "https://ydb.tech/docs/ru/integrations/gui/jupyter?version=v26.1"
doc_path: "ru/integrations/gui/jupyter"
version: "v26.1"
lang: "ru"
source_path: "ru/core/integrations/gui/jupyter.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/integrations/gui/jupyter.md"
description: "Jupyter Notebook - это инструмент с открытым исходным кодом для создания общедоступных документов, сочетающий в себе код, описания на простом языке, данные, бог"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Работа с YDB с помощью Jupyter Notebook

[Jupyter Notebook](https://jupyter.org) - это инструмент с открытым исходным кодом для создания общедоступных документов, сочетающий в себе код, описания на простом языке, данные, богатую визуализацию и интерактивные элементы управления.

[Диалект ydb-sqlalchemy](https://github.com/ydb-platform/ydb-sqlalchemy/releases) позволяет работать с YDB напрямую из таких инструментов как:

- [Pandas](https://pandas.pydata.org/)
- [JupySQL](https://jupysql.ploomber.io/)

## Пример {#primer}

Подробный пример работы доступен в специальном [ноутбуке](https://github.com/ydb-platform/ydb-sqlalchemy/blob/main/examples/jupyter_notebook/YDB%20SQLAlchemy%20%2B%20Jupyter%20Notebook%20Example.ipynb).

Требования для запуска:

1. Python 3.8+
2. [Jupyter Notebook](https://jupyter.org/install#jupyter-notebook)
3. Существующий кластер YDB, однонодовая инсталляция из [быстрого старта](../../quickstart.md) будет достаточной

Для запуска примера скачайте файл ноутбука [YDB SQLAlchemy - Jupyter Notebook Example.ipynb](https://raw.githubusercontent.com/ydb-platform/ydb-sqlalchemy/refs/heads/main/examples/jupyter_notebook/YDB%20SQLAlchemy%20%2B%20Jupyter%20Notebook%20Example.ipynb), откройте его в Jupyter и последовательно пройдитесь по каждой ячейке, выполняя код по мере необходимости.
