---
status: completed
filename: apache-pulsar-vs-kafka-architecture-comparison
title: "Apache Pulsar 架构"
description: 本笔记深度剖析了分布式消息引擎 Apache Pulsar 的核心架构设计，并将其与业界标杆 Apache Kafka 进行了多维度的横向对比。重点解读了 Pulsar “计算 (Broker) 与存储 (BookKeeper) 分离”的两层架构如何解决 Kafka 存算一体带来的扩容痛点。此外，详细对比了两者在消息消费模型（Pulsar 的统一 Push/Pull 模型与共享订阅 vs Kafka 的严格 Pull 模型）及分层存储等云原生特性上的差异，为企业级实时数据流平台的选型提供理论支撑。
aliases: [Apache Pulsar 架构, Pulsar vs Kafka, 存算分离 MQ, BookKeeper]
tags: [消息队列, Pulsar, Kafka, 分布式架构, 存算分离, 云原生, 大数据, 中间件]
date created: 星期三, 十二月 10日 2025, 6:20:42 晚上
date modified: 星期四, 六月 18日 2026, 10:35:00 晚上
---

<!-- toc -->

## 1. 核心定位：下一代流与队列融合平台

Apache Pulsar 和 Apache Kafka 都是顶级的分布式流处理和消息系统。Pulsar 的终极目标是 **在单一平台上融合流（Kafka 的高吞吐模式）和队列（RabbitMQ 的灵活路由模式）的能力**。

---

## 2. 架构本质区别：存算一体 vs 存算分离

这是两者决定扩展性与弹性上限的根本差异。

### 2.1. Apache Kafka (存算一体)

- **单层架构**：Broker（代理节点）既负责计算逻辑（网络接入、状态维护），也负责将数据持久化写入本地磁盘。
- **痛点**：计算和存储严格耦合。若为了增加存储容量而扩容节点，系统必须在节点间进行大量数据重平衡（Rebalance），耗时极长且极易影响线上性能。

### 2.2. Apache Pulsar (存算分离)

- **两层解耦架构**：
  - **计算层 (Broker)**：无状态，负责路由、订阅管理。可根据流量波动实现 **秒级弹性扩缩容**。
  - **存储层 (Bookies)**：基于 Apache BookKeeper 集群。消息被切分为 Segments 分布式存储。
- **优势**：独立扩容（存储不够加 Bookie，算力不够加 Broker），天然具备云原生优势。

---

## 3. 消费模型：打破 Pull 的桎梏

| 模型特性 | Apache Kafka | Apache Pulsar |
| :--- | :--- | :--- |
| **基础模式** | **严格主动拉取 (Pull)**。利于批处理，依赖消费者自我管理 Offset。 | **流与队列统一模型**。支持推送 (Push) 与拉取。 |
| **独占消费** | 对应 Kafka 的 Consumer Group 单个 Partition 只能被一个线程消费。 | **独占/灾备模式 (Exclusive/Failover)**，行为等同 Kafka。 |
| **共享消费** | **不支持**（若需支持需自己实现复杂的队列分发）。 | **共享模式 (Shared)**：允许多个消费者竞争同一个订阅中的消息，通过 Push 实现负载均衡（类似 RabbitMQ）。 |

---

## 4. 云原生高级特性对比

| 特性维度 | Apache Kafka | Apache Pulsar |
| :--- | :--- | :--- |
| **多租户 (Multi-tenancy)** | 原生支持弱，依赖外部配额控制。 | **原生支持**，在 Namespace 级别进行强隔离和资源硬限制。 |
| **地理跨机房复制** | 需依赖 MirrorMaker 等重量级外部同步工具。 | **内置原生支持 (Geo-Replication)**，配置极简。 |
| **分层存储 (Tiered Storage)** | 历史数据强依赖本地昂贵磁盘（部分商业版刚开始支持）。 | **内置特性**，可自动将冷数据卸载至 S3/HDFS 等廉价对象存储。 |

## 5. 总结：架构选型建议

- **选择 Kafka**：团队技术栈极其成熟，场景单纯为 **极致吞吐量的日志采集与流计算**，且能接受节点扩容时的数据搬迁成本。
- **选择 Pulsar**：
  - 需要用一套基础设施同时替换掉企业内的 Kafka（流）与 RabbitMQ（队列）。
  - 需要在云端实现 **计算与存储的独立秒级弹性扩容**。
  - 核心业务强依赖多租户隔离与异地多活灾备。
