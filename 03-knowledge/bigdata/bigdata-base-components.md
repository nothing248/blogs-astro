---
title: "大数据基础组件"
filename: bigdata-base-components
summary: 大数据基础架构核心组件知识图谱。解决大数据平台建设中的组件选型与架构分层问题。核心技术栈包括埋点与爬虫采集，DataX、Airflow等ETL工具，批处理（Spark）、流处理（Flink）计算引擎，HBase、Hive等多种存储介质，以及湖仓一体与实时数仓的架构演进路线。
tags:
  - bigdata
  - etl
  - data-architecture
  - data-warehouse
aliases:
  - 大数据基础组件
  - 大数据技术栈
  - Bigdata Base
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:23 上午
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 组件信息

### 1.1. 数据采集

- **埋点**
  - **Google Analytics**：成熟的商业级前端行为追踪与分析平台。
  - **Baidu 云统计**：国内主流的网站流量及用户行为分析工具。
- **爬虫**
  - **Scrapy**：高效的 Python 异步网络爬虫框架，适用于大规模数据抓取。
- **日志**
  - **Flume**：分布式、高可靠、高可用的海量日志采集、聚合和传输系统。
  - **Logstash**：开源的服务端数据处理管道，支持多数据源同步采集与过滤。
  - **Filebeat**：轻量级日志传送器，占用资源少，常部署在客户端进行日志收集。

### 1.2. ETL 组件

- **DataX**  
[离线开源同步工具](https://github.com/alibaba/DataX)  
阿里开源的异构数据源离线同步工具，通过 Framework + Plug 架构实现高效的同步转换。

- **Google Dataflow**  
Google 云环境下的全托管数据处理服务，原生支持 Apache Beam 引擎，实现批流一体化处理。

- **Airflow**  
[Apache 的开源工具](https://github.com/apache/airflow)  
基于 Python 的分布式任务调度与工作流管理平台，支持以 DAG（有向无环图）定义复杂的任务依赖关系。

- **sqoop**  
Hadoop 与关系型数据库（如 MySQL、Oracle）之间的双向数据传输与转换工具。

- **Kettle**  
经典的开源 GUI 可视化 ETL 工具（现名 Pentaho Data Integration），支持拖拽式构建数据清洗流。

- **canal**  
阿里开源的基于 MySQL 数据库增量日志（Binlog）解析的实时数据订阅与消费组件。

- **StreamSets**  
企业级数据集成平台，支持通过可视化拖拽方式构建复杂的实时数据管道（Data Pipelines）。

### 1.3. 处理组件

- **批处理**
  - **Apache Spark**：基于内存计算的分布式批处理框架，相比 MapReduce 性能有大幅提升。
  - **Hadoop MapReduce**：经典的分布式离线计算框架，适合超大规模数据的离线批处理。
- **流处理**
  - **Apache Flink**：低延迟、高吞吐的分布式实时流处理引擎，支持精确一次（Exactly-Once）语义。
  - **Spark Streaming / Structured Streaming**：基于微批处理（Micro-batch）的准实时流处理引擎。
- **图计算**
  - **Spark GraphX**：基于 Spark 的分布式图计算框架，简化了图的分析与建模。
  - **Apache Giraph**：基于 Pregel 模型的分布式图计算系统，专为大规模社交网络图设计。

### 1.4. 监控组件

- **拓展性**
  - **Prometheus + Grafana**：主流的度量指标监控与可视化组合，广泛用于 Kubernetes 及大数据生态。
  - **Apache Ambari**：Hadoop 生态的集群管理、监控和运维工具，提供直观的 Web UI。
  - **ELK Stack (Elasticsearch, Logstash, Kibana)**：用于大数据组件及应用日志的集中式收集、索引与监控展示。

### 1.5. 存储组件

- **关系型**
  - **MySQL / PostgreSQL**：经典的关系型数据库，常作为元数据存储库（如 Hive Metastore）。
- **非关系型**
  - **HBase**：基于 Hadoop HDFS 的分布式列族 NoSQL 数据库，适合海量半结构化数据的实时读写。
  - **MongoDB**：分布式文档型 NoSQL 数据库，支持灵活的 JSON 结构存储。
  - **Redis**：高性能内存键值缓存与数据库，适用于高并发的临时状态存储。
- **图型**
  - **Neo4j**：目前最主流的图数据库，支持高效的图关系查询（Cypher）。
  - **JanusGraph**：可扩展的分布式图数据库，支持多种后端存储（如 HBase、Cassandra）。
- **数仓类型**
  - **Apache Hive**：基于 Hadoop 的数据数仓工具，将结构化数据映射为表，并提供 SQL 查询（HQL）能力。
  - **ClickHouse**：高性能的列式数据库管理系统（DBMS），专为在线分析处理（OLAP）设计。
  - **Greenplum**：基于 PostgreSQL 核心的 MPP（大规模并行处理）数仓，适合海量数据的复杂分析。

### 1.6. 可视化组件

- **Apache Superset**：现代、轻量级的企业级商业智能（BI） Web 应用程序，支持丰富的图表与 SQL 编辑器。
- **ECharts / AntV**：前端优秀的数据可视化图表库，用于定制化开发报表大屏。
- **Tableau / PowerBI**：行业领先的商业自助式 BI 分析与可视化设计工具。

## 2. 拓展信息

- **理论支持**
  - **Lambda 架构**：将数据通道分为批处理（Batch Layer）与快速处理（Speed Layer），平衡延迟与准确性。
  - **Kappa 架构**：移除批处理层，以流处理（Stream Layer）为核心，通过重播机制解决数据重算问题。
  - **CAP 定理 & BASE 理论**：分布式系统设计的基础理论，权衡一致性、可用性与分区容错性。
- **发展路线**
  - **湖仓一体 (Lakehouse)**：融合了数据湖的低成本、灵活性与数据仓库的事务支持、高查询性能（如 Iceberg, Delta Lake）。
  - **实时数仓**：依托 Flink + ClickHouse/Doris 架构，实现数据源到分析报表秒级响应的端到端实时链路。
- **实现场景**
  - **实时推荐系统**：流式采集用户行为，经 Flink 实时特征计算后写入 Redis，召回引擎检索出个性化推荐列表。
  - **离线用户画像**：通过 Airflow 定期调度 Hive 批处理任务，计算用户多维标签，沉淀数据资产。
- **验证方式**
  - **基准测试**：采用行业标准的 TPC-DS、TPC-H 基准数据集对数仓引擎进行多维复杂查询性能评估。
  - **压力测试**：利用 JMeter 或 Locust 模拟高并发查询与写入，观测集群 CPU、内存、I/O 以及 GC 表现。
