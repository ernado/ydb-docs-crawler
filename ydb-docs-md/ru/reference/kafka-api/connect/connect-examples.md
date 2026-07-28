---
title: "Примеры настройки коннекторов"
url: "https://ydb.tech/docs/ru/reference/kafka-api/connect/connect-examples?version=v26.1"
doc_path: "ru/reference/kafka-api/connect/connect-examples"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/kafka-api/connect/connect-examples.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/kafka-api/connect/connect-examples.md"
description: "В разделе приведены примеры файлов настройки коннекторов Kafka Connect для работы с YDB по протоколу Kafka. Из файла в YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Примеры настройки коннекторов

В разделе приведены примеры файлов настройки коннекторов Kafka Connect для работы с YDB по протоколу Kafka.

## Из файла в YDB {#file-to-topic}

Пример файла настроек FileSource-коннектора `/etc/kafka-connect-worker/file-sink.properties` для переноса данных из файла в топик:

```ini
name=local-file-source
connector.class=FileStreamSource
tasks.max=1
file=/etc/kafka-connect-worker/file_to_read.json
topic=<topic-name>
```

## Из YDB в PostgreSQL {#iz-ydb-v-postgresql}

Пример файла настроек JDBCSink коннектора `/etc/kafka-connect-worker/jdbc-sink.properties` для переноса данных из топика в таблицу PostgreSQL. Используется коннектор [Kafka Connect JDBC Connector](https://github.com/confluentinc/kafka-connect-jdbc).

```ini
name=postgresql-sink
connector.class=io.confluent.connect.jdbc.JdbcSinkConnector

connection.url=jdbc:postgresql://<postgresql-host>:<postgresql-port>/<db>
connection.user=<pg-user>
connection.password=<pg-user-pass>

topics=<topic-name>
batch.size=2000
auto.commit.interval.ms=1000

transforms=wrap
transforms.wrap.type=org.apache.kafka.connect.transforms.HoistField$Value
transforms.wrap.field=data

auto.create=true
insert.mode=insert
pk.mode=none
auto.evolve=true
```

## Из PostgreSQL в YDB {#iz-postgresql-v-ydb}

Пример файла настроек JDBCSource коннектора `/etc/kafka-connect-worker/jdbc-source.properties` для переноса данных из PostgreSQL таблицы в топик. Используется коннектор [Kafka Connect JDBC Connector](https://github.com/confluentinc/kafka-connect-jdbc).

```ini
name=postgresql-source
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector

connection.url=jdbc:postgresql://<postgresql-host>:<postgresql-port>/<db>
connection.user=<pg-user>
connection.password=<pg-user-pass>

mode=bulk
query=SELECT * FROM "<topic-name>";
topic.prefix=<topic-name>
poll.interval.ms=1000
validate.non.null=false
```

## Из YDB в S3 {#iz-ydb-v-s3}

Пример файла настроек S3Sink коннектора `/etc/kafka-connect-worker/s3-sink.properties` для переноса данных из топика в S3. Используется коннектор [Aiven's S3 Sink Connector for Apache Kafka](https://github.com/Aiven-Open/s3-connector-for-apache-kafka).

```ini
name=s3-sink
connector.class=io.aiven.kafka.connect.s3.AivenKafkaConnectS3SinkConnector
topics=<topic-name>
aws.access.key.id=<s3-access-key>
aws.secret.access.key=<s3-secret>
aws.s3.bucket.name=<bucket-name>
aws.s3.endpoint=<s3-endpoint>
format.output.type=json
file.compression.type=none
```
