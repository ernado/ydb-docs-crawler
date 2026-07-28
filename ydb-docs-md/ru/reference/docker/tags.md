---
title: "Именование тегов докер-образа <code class=\"yfm-clipboard-inline-code\" role=\"button\" tabindex='0' id=\"inline-code-id-xhw2cdw2\">ydbplatform/local-ydb</code>"
url: "https://ydb.tech/docs/ru/reference/docker/tags?version=v26.1"
doc_path: "ru/reference/docker/tags"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/docker/tags.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/docker/tags.md"
description: "Для докер-образа ydbplatform/local-ydb применяются следующие правила именования для тегов: Тег Описание. latest."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Именование тегов докер-образа <code class="yfm-clipboard-inline-code" role="button" tabindex='0' id="inline-code-id-xhw2cdw2">ydbplatform/local-ydb</code>

Для докер-образа [ydbplatform/local-ydb](https://hub.docker.com/r/ydbplatform/local-ydb) применяются следующие правила именования для тегов:

| Тег | Описание |
| --- | --- |
| `latest` | Соответствует *stable*-версии YDB, проверенной на известных продакшен-кластерах YDB. Тег **latest** пересобирается, когда в проекте [ydb](https://github.com/ydb-platform/ydb/releases) появляется запись о новом релизе YDB. |
| `edge` | Кандидат на следующий *stable*, то есть та версия, которая в данный момент тестируется. В edge можно попробовать новые фичи YDB, но также не следует ожидать стабильности данной сборки. |
| `trunk`, `main`, `nightly` | Последняя версия YDB из кода в основной ветке разработки. Содержит самые последние изменения. Образ пересобирается каждую ночь. |
| `XX.Y` | Соответствует последней версии YDB в мажорном релизе `XX-Y` (со всеми патчами). |
| `XX.Y.ZZ` | Соответствует версии YDB в релизе `XX-Y-ZZ`. |
| `XX.Y-slim` и `XX.Y.ZZ-slim` | Соответствует версиям YDB со специальным образом сжатыми бинарными исполняемыми файлами `ydbd` и `ydb` внутри образа. Версии `*-slim` имеют значительно меньший размер образа, но при этом дольше стартуют. Для сжатия используется утилита [upx](https://github.com/upx/upx). |
