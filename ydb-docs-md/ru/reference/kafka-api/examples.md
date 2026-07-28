---
title: "Примеры чтения и записи по Kafka API"
url: "https://ydb.tech/docs/ru/reference/kafka-api/examples?version=v26.1"
doc_path: "ru/reference/kafka-api/examples"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/kafka-api/examples.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/kafka-api/examples.md"
description: "В этой статье приведены примеры чтения и записи в топики с использованием Kafka API. Перед выполнением примеров: Создайте топик. Добавьте читателя."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Примеры чтения и записи по Kafka API

В этой статье приведены примеры чтения и записи в [топики](../../concepts/datamodel/topic.md) с использованием Kafka API.

Перед выполнением примеров:

1. [Создайте топик](../ydb-cli/topic-create.md).
2. [Добавьте читателя](../ydb-cli/topic-consumer-add.md).
3. Если у вас включена аутентификация, [создайте пользователя](../../yql/reference/syntax/create-user.md).

## Начало работы {#how-to-try-kafka-api}

### В Docker {#how-to-try-kafka-api-in-docker}

Запустите Docker по [этой](../../quickstart.md#install) инструкции. Kafka API будет доступен на 9092 порте.

## Примеры работы с Kafka API {#primery-raboty-s-kafka-api}

### Чтение {#chtenie}

При чтении отличительной особенностью Kafka API является отсутствие поддержки опции [check.crcs](https://kafka.apache.org/documentation/#consumerconfigs_check.crcs). Поэтому в конфигурации читателя всегда нужно указывать параметр: `check.crcs=false`.

Ниже даны примеры чтения по Kafka протоколу для разных приложений, языков программирования и фреймворков подключения без аутентификации.  
 Примеры того, как настроить аутентификацию, смотри в разделе [Примеры с аутентификацией](examples.md#authentication-examples)

{% list tabs %}

- Консольные утилиты Kafka

  > [!NOTE]
  > При использовании консольных утилит Kafka с Java 23 и получении ошибки
  >  `java.lang.UnsupportedOperationException: getSubject is supported only if a security manager is allowed`
  >  , либо запустите команду, используя другую версию Java ([как сменить версию Java на macos](https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos))
  >  , либо запустите команду, указав для java флаг `-Djava.security.manager=allow`.
  >  Например: `KAFKA_OPTS=-Djava.security.manager=allow kafka-topics --boostratp-servers localhost:9092 --list`

  ```bash
  kafka-console-consumer --bootstrap-server localhost:9092 \
      --topic my-topic  \
      --group my-group \
      --from-beginning \
      --consumer-property check.crcs=false \
      --consumer-property partition.assignment.strategy=org.apache.kafka.clients.consumer.RoundRobinAssignor
  ```

- kcat

  ```bash
  kcat -C \
    -b <ydb-endpoint> \
    -X check.crcs=false \
    -X partition.assignment.strategy=org.apache.kafka.clients.consumer.RoundRobinAssignor \
    -G <consumer-name> <topic-name>
  ```

- Java

  ```java
  String HOST = "<ydb-endpoint>";
  String TOPIC = "<topic-name>";
  String CONSUMER = "<consumer-name>";

  Properties props = new Properties();

  props.put("bootstrap.servers", HOST);

  props.put("key.deserializer", StringDeserializer.class.getName());
  props.put("value.deserializer", StringDeserializer.class.getName());

  props.put("check.crcs", false);
  props.put("partition.assignment.strategy", RoundRobinAssignor.class.getName());

  props.put("group.id", CONSUMER);
  Consumer<String, String> consumer = new KafkaConsumer<>(props);
  consumer.subscribe(Arrays.asList(new String[] {TOPIC}));

  while (true) {
    ConsumerRecords<String, String> records = consumer.poll(10000); // timeout 10 sec
    for (ConsumerRecord<String, String> record : records) {
        System.out.println(record.key() + ":" + record.value());
    }
  }
  ```

- Spark

  ```java
  public class ExampleReadApp {
    public static void main(String[] args) {
      var conf = new SparkConf().setAppName("my-app").setMaster("local");
      var context = new SparkContext(conf);

      context.setCheckpointDir("checkpoints");
      SparkSession spark = SparkSession.builder()
              .sparkContext(context)
              .config(conf)
              .appName("Simple Application")
              .getOrCreate();

      Dataset<Row> df = spark
              .read()
              .format("kafka")
              .option("kafka.bootstrap.servers", "localhost:9092")
              .option("subscribe", "flink-demo-input-topic")
              .option("kafka.group.id", "spark-example-app")
              .option("startingOffsets", "earliest")
              .option("kafka." + ConsumerConfig.CHECK_CRCS_CONFIG, "false")
              .load();

      df.foreach((ForeachFunction<Row>) row -> {
          System.out.println(row);
      });
    }
  }
  ```

  В примере выше использовался Apache Spark 2.12:3.5.3 с зависимостью на `org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.3`.

- Flink

  ```java
  public class YdbKafkaApiReadExample {

      public static void main(String[] args) throws Exception {
          final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment()
                  .enableCheckpointing(5000, CheckpointingMode.AT_LEAST_ONCE);

          Configuration config = new Configuration();
          config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
          config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "file:///path/to/your/checkpoints");
          env.configure(config);

          KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                  .setBootstrapServers("localhost:9092")
                  .setProperty(ConsumerConfig.CHECK_CRCS_CONFIG, "false")
                  .setGroupId("flink-demo-consumer")
                  .setTopics("my-topic")
                  .setStartingOffsets(OffsetsInitializer.earliest())
                  .setBounded(OffsetsInitializer.latest())
                  .setValueOnlyDeserializer(new SimpleStringSchema())
                          .build();

          env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "kafka-source").print();

          env.execute("YDB Kafka API example read app");
      }
  }
  ```

  В примере выше используется Apache Flink версии 1.20 и [flink datastream connector](https://nightlies.apache.org/flink/flink-docs-release-1.20/docs/connectors/datastream/kafka/) к Kafka.

{% endlist %}

### Запись {#zapis}

{% list tabs %}

- Консольные утилиты Kafka

  > [!NOTE]
  > При использовании консольных утилит Kafka с Java 23 и получении ошибки
  >  `java.lang.UnsupportedOperationException: getSubject is supported only if a security manager is allowed`
  >  , либо запустите команду, используя другую версию Java ([как сменить версию Java на macos](https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos))
  >  , либо запустите команду, указав для java флаг `-Djava.security.manager=allow`.
  >  Например: `KAFKA_OPTS=-Djava.security.manager=allow kafka-topics --boostratp-servers localhost:9092 --list`

  ```bash
  kafka-console-producer --broker-list localhost:9092 --topic my-topic
  ```

- kcat

  ```bash
  echo "test message" | kcat -P \
      -b <ydb-endpoint> \
      -t <topic-name> \
      -k key
  ```

- Java

  ```java
  String HOST = "<ydb-endpoint>";
  String TOPIC = "<topic-name>";

  Properties props = new Properties();
  props.put("bootstrap.servers", HOST);
  props.put("acks", "all");

  props.put("key.serializer", StringSerializer.class.getName());
  props.put("key.deserializer", StringDeserializer.class.getName());
  props.put("value.serializer", StringSerializer.class.getName());
  props.put("value.deserializer", StringDeserializer.class.getName());

  props.put("compression.type", "none");

  Producer<String, String> producer = new KafkaProducer<>(props);
  producer.send(new ProducerRecord<String, String>(TOPIC, "msg-key", "msg-body"));
  producer.flush();
  producer.close();
  ```

- Spark

  ```java
  public class ExampleWriteApp {
  public static void main(String[] args) {
      var conf = new SparkConf().setAppName("my-app").setMaster("local");
      var context = new SparkContext(conf);
      context.setCheckpointDir("path/to/dir/with/checkpoints");
      SparkSession spark = SparkSession.builder()
          .sparkContext(context)
            .config(conf)
            .appName("Simple Application")
            .getOrCreate();

      spark
            .createDataset(List.of("spark-1", "spark-2", "spark-3", "spark-4"), Encoders.STRING())
            .write()
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("topic", "flink-demo-output-topic")
            .option("kafka.group.id", "spark-example-app")
            .option("startingOffsets", "earliest")
            .save();
    }
  }
  ```

  В примере выше использовался Apache Spark 2.12:3.5.3 с зависимостью на `org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.3`.

- Flink

  ```java
  public class YdbKafkaApiProduceExample {
    private static final String TOPIC = "my-topic";

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        Sink<String> kafkaSink = KafkaSink.<String>builder()
                .setBootstrapServers("localhost:9092") // assuming ydb is running locally with kafka proxy on 9092 port
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(TOPIC)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .setKeySerializationSchema(new SimpleStringSchema())
                        .build())
                .setRecordSerializer((el, ctx, ts) -> new ProducerRecord<>(TOPIC, el.getBytes()))
                .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
                        .build();

        env.setParallelism(1)
                .fromSequence(0, 10)
                .map(i -> i + "")
                .sinkTo(kafkaSink);

        // Execute program, beginning computation.
        env.execute("ydb_kafka_api_write_example");
    }
  }
  ```

  В примере выше используется Apache Flink версии 1.20 и [flink datastream connector](https://nightlies.apache.org/flink/flink-docs-release-1.20/docs/connectors/datastream/kafka/) к Kafka.

- Logstash

  ```ruby
    output {
      kafka {
        codec => json
        topic_id => "<topic-name>"
        bootstrap_servers => "<ydb-endpoint>"
        compression_type => none
      }
    }
  ```

- Fluent Bit

  ```ini
    [OUTPUT]
      name                          kafka
      match                         *
      Brokers                       <ydb-endpoint>
      Topics                        <topic-name>
      rdkafka.client.id             Fluent-bit
      rdkafka.request.required.acks 1
      rdkafka.log_level             7
      rdkafka.sasl.mechanism        PLAIN
  ```

{% endlist %}

### Примеры с аутентификацией {#authentication-examples}

Подробнее про аутентификацию смотри в разделе [Аутентификация](auth.md). Ниже есть примеры аутентификации в облачной базе  
 и в локальной базе.

> [!NOTE]
> Сейчас единственным доступным механизмом аутентификации с Kafka API в YDB Topics является `SASL_PLAIN`.

#### Примеры аутентификации в самостоятельно развернутом YDB {#primery-autentifikacii-v-samostoyatelno-razvernutom-ydb}

Для того, чтобы проверить работу с аутентификацией в локальной базе:

1. Создайте пользователя. [Как это сделать в YQL](../../yql/reference/syntax/create-user.md). [Как выполнить YQL из CLI](../ydb-cli/sql.md).
2. Подключитесь к Kafka API, как в примерах ниже. Во всех примерах предполагается, что:

- YDB запущен локально с переменной окружения YDB_KAFKA_PROXY_PORT=9092 - то есть Kafka API доступен по адресу localhost:9092. Например можно поднять YDB в докере, как указано [здесь](../../quickstart.md#install).
- \- это имя пользователя, которое вы указали при создании пользователя.
- \- это пароль пользователя, который вы указали при создании пользователя.

Примеры показаны для чтения, но те же самые параметры конфигурации работают и для записи в топик.

{% list tabs %}

- Консольные утилиты Kafka

  > [!NOTE]
  > При использовании консольных утилит Kafka с Java 23 и получении ошибки
  >  `java.lang.UnsupportedOperationException: getSubject is supported only if a security manager is allowed`
  >  , либо запустите команду, используя другую версию Java ([как сменить версию Java на macos](https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos))
  >  , либо запустите команду, указав для java флаг `-Djava.security.manager=allow`.
  >  Например: `KAFKA_OPTS=-Djava.security.manager=allow kafka-topics --boostratp-servers localhost:9092 --list`

  ```bash
  kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic <topic-name>  \
  --group <consumer-name> \
  --from-beginning \
  --consumer-property check.crcs=false \
  --consumer-property partition.assignment.strategy=org.apache.kafka.clients.consumer.RoundRobinAssignor \
  --consumer-property security.protocol=SASL_PLAINTEXT \
  --consumer-property sasl.mechanism=PLAIN \
  --consumer-property "sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username=\"<username>\" password=\"<password>\";"
  ```

- kcat

  ```bash
  kcat -C \
    -b localhost:9092 \
    -X security.protocol=SASL_PLAINTEXT \
    -X sasl.mechanism=PLAIN \
    -X sasl.username="<username>" \
    -X sasl.password="<password>" \
    -X check.crcs=false \
    -X partition.assignment.strategy=roundrobin \
    -G <consumer-name> <topic-name>
  ```

- Java

  ```java
  String TOPIC = "<topic-name>";
  String CONSUMER = "<consumer-name>";

  Properties props = new Properties();

  props.put("bootstrap.servers", "localhost:9092");

  props.put("key.deserializer", StringDeserializer.class.getName());
  props.put("value.deserializer", StringDeserializer.class.getName());

  props.put("check.crcs", false);
  props.put("partition.assignment.strategy", RoundRobinAssignor.class.getName());

  props.put("security.protocol", "SASL_PLAINTEXT");
  props.put("sasl.mechanism", "PLAIN");
  props.put("sasl.jaas.config", "sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username=\"<username>\" password=\"<password>\";");

  props.put("group.id", CONSUMER);
  Consumer<String, String> consumer = new KafkaConsumer<>(props);
  consumer.subscribe(Arrays.asList(new String[] {TOPIC}));

  while (true) {
    ConsumerRecords<String, String> records = consumer.poll(10000); // timeout 10 sec
    for (ConsumerRecord<String, String> record : records) {
        System.out.println(record.key() + ":" + record.value());
    }
  }
  ```

{% endlist %}
