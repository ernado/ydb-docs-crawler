---
title: "Kafka API usage examples"
url: "https://ydb.tech/docs/en/reference/kafka-api/examples?version=v26.1"
doc_path: "en/reference/kafka-api/examples"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/kafka-api/examples.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/kafka-api/examples.md"
description: "This example shows a code snippet for reading data from a topic via Kafka API without a consumer group (Manual Partition Assignment)."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Kafka API usage examples

This example shows a code snippet for reading data from a topic via Kafka API without a consumer group (Manual Partition Assignment).  
 You don't need to create a consumer for this reading mode.

Before proceeding with the examples:

1. [Create a topic](../ydb-cli/topic-create.md).
2. [Add a consumer](../ydb-cli/topic-consumer-add.md).
3. If authentication is enabled, [create a user](../../security/authorization.md#user).

## How to try the Kafka API {#how-to-try-kafka-api}

### In Docker {#how-to-try-kafka-api-in-docker}

Run Docker following [the quickstart guide](../../quickstart.md#install), and the Kafka API will be available on port 9092.

## Kafka API usage examples

### Reading

YDB Topics Kafka API lacks support for the [check.crcs](https://kafka.apache.org/documentation/#consumerconfigs_check.crcs) option. Therefore, the following parameter must always be specified in the reader configuration: `check.crcs=false`.

Below are examples of reading using the Kafka protocol for various applications, programming languages, and frameworks without authentication.  
 For examples of how to set up authentication, see [Authentication examples](examples.md#authentication-examples).

{% list tabs %}

- Built-in Kafka CLI tools

  > [!NOTE]
  > If you get the `java.lang.UnsupportedOperationException: getSubject is supported only if a security manager is allowed` error when using Kafka CLI tools with Java 23, perform one of the following steps:
  >
  > - Run the command using a different version of Java ([how to change the Java version on macOS](https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos)).
  > - Run the command with the Java flag `-Djava.security.manager=allow`. For example: `KAFKA_OPTS=-Djava.security.manager=allow kafka-topics --bootstrap-servers localhost:9092 --list`.

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

  In the example above, Apache Spark 2.12:3.5.3, with a dependency on `org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.3`, was used.

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

  In the example above, Apache Flink 1.20 is used with the [Flink DataStream connector](https://nightlies.apache.org/flink/flink-docs-release-1.20/docs/connectors/datastream/kafka/) for Kafka.

{% endlist %}

### Writing

{% list tabs %}

- Built-in Kafka CLI tools

  > [!NOTE]
  > If you get the `java.lang.UnsupportedOperationException: getSubject is supported only if a security manager is allowed` error when using Kafka CLI tools with Java 23, perform one of the following steps:
  >
  > - Run the command using a different version of Java ([how to change the Java version on macOS](https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos)).
  > - Run the command with the Java flag `-Djava.security.manager=allow`. For example: `KAFKA_OPTS=-Djava.security.manager=allow kafka-topics --bootstrap-servers localhost:9092 --list`.

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

  In the example above, Apache Spark 2.12:3.5.3, with a dependency on `org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.3`, was used.

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

  In the example above, Apache Flink 1.20 is used with the [Flink DataStream connector](https://nightlies.apache.org/flink/flink-docs-release-1.20/docs/connectors/datastream/kafka/) for Kafka.

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

### Authentication examples

For more details on authentication, see the [Authentication](auth.md) section. Below are examples of authentication in a cloud database and a local database.

> [!NOTE]
> Currently, the only available authentication mechanism with Kafka API in YDB Topics is `SASL_PLAIN`.

#### Authentication examples in on-prem YDB

To use authentication in a multinode self-deployed database:

1. Create a user. [How to do this in YQL](../../yql/reference/syntax/create-user.md). [How to execute YQL from CLI](../ydb-cli/sql.md).

2. Connect to the Kafka API as shown in the examples below. In all examples, it is assumed that:

   - YDB is running locally with the environment variable `YDB_KAFKA_PROXY_PORT=9092`, meaning that the Kafka API is available at `localhost:9092`. For example, you can run YDB in Docker as described [here](../../quickstart.md#install).
   - is the username you specified when creating the user.
   - is the user's password you specified when creating the user.

Examples are shown for reading, but the same configuration parameters work for writing to a topic as well.

{% list tabs %}

- Built-in Kafka CLI tools

  > [!NOTE]
  > If you get the `java.lang.UnsupportedOperationException: getSubject is supported only if a security manager is allowed` error when using Kafka CLI tools with Java 23, perform one of the following steps:
  >
  > - Run the command using a different version of Java ([how to change the Java version on macOS](https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos)).
  > - Run the command with the Java flag `-Djava.security.manager=allow`. For example: `KAFKA_OPTS=-Djava.security.manager=allow kafka-topics --bootstrap-servers localhost:9092 --list`.

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
