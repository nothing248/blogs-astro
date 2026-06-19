---
title: "Kafka集群部署"
filename: apache-kafka-guide
summary: 介绍分布式消息引擎 Apache Kafka 3.8.0 的安装与配置，包括单机与集群模式下的 listeners 绑定与 Zookeeper 端点设置。提供用于服务控制的 systemd 配置文件与 Topic 创建（kafka-topics）、生产者（kafka-console-producer）及消费者（kafka-console-consumer）的命令行交互操作，并深度总结了消息队列、流存储与实时流处理等核心应用场景。
tags:
  - Kafka
  - 消息引擎
  - 分布式存储
  - 实时流处理
  - 削峰填谷
aliases:
  - Kafka集群部署
  - Kafka Shell命令
  - 实时日志收集
  - 数据变更捕获
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:22 上午
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

Kafka 是一个开源的分布式消息引擎/消息中间件

## 2. 概念

- Broker
- Topic
- Partition
- Producer
- Consumer
- Consumer Group

## 3. 安装

### 3.1. 单机

- 安装

```shell
wget https://dlcdn.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
mv kafka_2.13-3.8.0.tgz /opt/software
cd /opt/software
tar -zxvf kafka_2.13-3.8.0.tgz
mkdir /data/kafka
# 环境变量
export KAFKA_HOME=/opt/software/kafka_2.13-3.8.0
export PATH=KAFKA_HOME/bin:$PATH
```

- 配置

```
# A comma separated list of directories under which to store log files
log.dirs=/data/kafka
# root directory for all kafka znodes.
zookeeper.connect=127.0.0.1:2181 # 192.168.88.22:2181,192.168.88.23:2181
# 监听端口
listeners=PLAINTEXT://192.168.56.104:9092
```

### 3.2. 集群

- 安装

> 参考单机部署

- 配置

```
log.dirs=/data/kafka
# root directory for all kafka znodes.
zookeeper.connect=192.168.56.101:2181,192.168.56.102:2181,192.168.56.103:2181 # 192.168.88.22:2181,192.168.88.23:2181
# 监听端口
listeners=PLAINTEXT://192.168.56.101:9092
```

## 4. 使用

- systemcd

```
[Unit]
Description=Apache Kafka server
Documentation=http://kafka.apache.org/documentation.html
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
Environment=JAVA_HOME=/opt/software/jdk1.8.0_351
ExecStart=/opt/software/kafka_2.13-3.8.0/bin/kafka-server-start.sh /opt/software/kafka_2.13-3.8.0/config/server.properties
ExecStop=/opt/software/kafka_2.13-3.8.0/bin/kafka-server-stop.sh
Restart=on-failure
RestartSec=5
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
```

- 服务端

```
cd /opt/software/kafka_2.13-3.8.0
kafka-server-start.sh config/server.properties
```

- 客户端

```shell
kafka-topics.sh --create --bootstrap-server 192.168.56.101:9092 --replication-factor 3 --partitions 1 --topic test-ken-io  #创建 topic
kafka-console-producer.sh --broker-list 192.168.56.104:9092 --topic test-ken-io
kafka-console-producer.sh --broker-list 192.168.56.104:9092 --topic test-ken-io --property "parse.key=true" --property "key.separator=:"
kafka-console-consumer.sh --bootstrap-server 192.168.56.104:9092 --topic test-ken-io --from-beginning
```

- 可视化  
Kafka Tools

## 5. 应用场景

Kafka 的应用场景通常可以归纳为三大类：**消息队列、流存储 and 流处理**。

### 5.1. 核心应用：作为高性能消息队列 (Messaging Queue)

Kafka 最初就是为高吞吐量日志收集而设计的，作为传统消息队列（如 RabbitMQ）的有力替代品。

- **异步通信与解耦：** 将生产者（数据源）和消费者（数据目标）解耦。例如，用户下单后，系统将“订单创建”事件发送到 Kafka，后续的库存、物流、邮件通知等服务各自独立消费该事件，实现系统间的异步协作。
- **削峰填谷：** 当系统流量突然暴增时（如秒杀活动），Kafka 可以作为缓冲区，接收所有突发流量，然后下游服务可以按照自己稳定的处理能力逐步消费，防止后端系统崩溃。
- **日志收集与聚合：** 集中收集来自数百 or 数千个应用服务器、Web 服务器、数据库等产生的日志（如 Nginx 日志、应用错误日志），并将它们聚合到一个中心平台进行统一处理和分析。

### 5.2. 核心应用：作为分布式存储系统 (Storage System)

Kafka 将所有消息持久化到磁盘，并具备高可用性（通过副本机制），使其成为一个强大的分布式提交日志。

- **流数据持久化：** 将关键业务事件（如用户注册、支付）永久记录下来，允许新的应用程序随时从头开始消费这些历史数据，**实现数据的“回溯”**。
- **数据库变更捕获 (Change Data Capture, CDC)：** 监控数据库（如 MySQL, PostgreSQL）的变更日志（Binlog/WAL），并将这些变更实时地发送到 Kafka。
  - **用途：** 实时同步数据到数据仓库（如 ClickHouse, Elasticsearch），或进行异构数据库之间的数据同步。
- **重放与容错：** 当下游系统（如一个报表服务）出现 Bug 或配置错误时，可以利用 Kafka 中存储的历史数据，重置消费进度，重新处理数据流以修正错误。

### 5.3. 核心应用：作为实时流处理平台 (Stream Processing)

Kafka 结合其内置的 **Kafka Streams** 库或外部的流处理框架（如 Flink, Spark Streaming），可以实现复杂的数据流分析。

- **实时数据转换 (ETL)：** 在数据从源头到达数据仓库的过程中，进行实时的数据清洗、格式转换、脱敏等操作。
- **实时指标计算：** 实时聚合数据流，计算业务关键指标（KPIs），如每秒钟的订单量、网站的实时活跃用户数等。
- **基于事件的复杂处理 (CEP)：** 识别数据流中符合特定模式或规则的事件序列。
  - **示例：** 监测到“用户登录失败 5 次” + “用户尝试重置密码” + “用户 IP 地址变化”等一系列事件，实时触发安全警报。

## 6. 拓展信息

...

## 7. 参考资料

- [官方链接](https://ken.io/note/kafka-cluster-deploy-guide)
- [Kafka Tools](https://www.kafkatool.com/download.html)
