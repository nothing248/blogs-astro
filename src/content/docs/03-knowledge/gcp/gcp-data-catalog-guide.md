---
title: "GCP Data Catalog"
filename: gcp-data-catalog-guide
description: Google Cloud Data Catalog 元数据管理与数据发现服务指南。解决海量企业级数据资产中元数据孤岛、检索困难与合规性问题。核心技术栈包括自动编制的元数据条目（BigQuery、Pub/Sub 等）、基于标记模板的业务元数据分类，以及结合 IAM、DLP 与 Dataplex 的数据安全治理与迁移方案。
tags:
  - gcp
  - data-catalog
  - metadata-management
  - data-governance
aliases:
  - GCP Data Catalog
  - 数据目录
  - 元数据管理
status: completed
date created: 星期一, 五月 19日 2025, 2:05:21 下午
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

## 1. 简介

**Google Cloud Data Catalog**（现已全面整合入 **Google Cloud Dataplex**）是一个完全托管且可扩展的元数据管理服务。它可以帮助组织构建一个统一的数据目录，提高数据资产的可发现性和透明度，从而促进数据驱动的决策。无论是结构化还是非结构化的云端数据，Data Catalog 都能提供强大的搜索和分类功能。

## 2. 概念

- **条目/条目组 (Entry / Entry Group)**
  - **条目 (Entry)**：代表具体的数据资产（如 BigQuery 表、Pub/Sub 主题、文件集等）。每个条目包含其物理路径、类型以及关联的模式信息。
  - **条目组 (Entry Group)**：条目的逻辑容器。Data Catalog 会自动为 GCP 资源创建默认的条目组（如 `@bigquery`），用户也可以针对自定义数据源创建自定义条目组。
- **元数据 (Metadata)**
  - **技术元数据**：由系统自动从底层数据源编制（如列名、数据类型、创建时间、文件大小等）。
  - **业务元数据**：描述数据资产的业务背景（如数据所有者、保留期限、合规要求等），主要通过“标记”来实现。
- **标记/标记模板 (Tag / Tag Template)**
  - **标记模板 (Tag Template)**：定义业务元数据结构的 schema（如包含字段“敏感度等级”、“责任人”等），支持字符串、双精度浮点数、布尔值、枚举和日期时间等多种数据类型。
  - **标记 (Tag)**：根据标记模板生成的键值对实例，并附加到具体的条目或列上。

## 3. 使用

### 3.1. 数据集成

- **自动编制**
  Data Catalog 可以自动抓取并实时编制以下 Google Cloud 服务中的元数据资产：
  - Analytics Hub 关联的数据集。
  - **BigQuery** 数据集、表、模型、日常安排和连接。
  - **Bigtable** 实例、集群和表（包括列族详细信息）。
  - **Dataplex** 数据湖、区域、表和文件集。
  - **Dataproc Metastore** 服务、数据库和表。
  - **Pub/Sub** 主题。
  - **Spanner** 实例、数据库、表和视图。
  - [Vertex AI 模型](https://cloud.google.com/vertex-ai/docs/model-registry/introduction?hl=zh-cn)、[数据集](https://cloud.google.com/vertex-ai/docs/datasets/overview?hl=zh-cn) 和 [Vertex AI Feature Store 资源](https://cloud.google.com/vertex-ai/docs/featurestore/latest/overview?hl=zh-cn)。

### 3.2. 数据发现

- **跨项目全文检索**：支持对整个 Google Cloud 组织内的所有元数据进行集中式的快速全文搜索。
- **结构化查询语法**：支持使用高级过滤语法进行精准定位，如 `type=table`、`name:customer`、`tag:sensitive` 或 `project:my-project`。
- **Schema 级别检索**：支持搜索特定的列名或数据类型，便于分析师发现能够进行关联分析的底层表结构。

### 3.3. 数据安全

- **细粒度访问控制**：与 Cloud IAM 紧密集成，只有具备相应权限的角色才能查看特定条目的元数据或附加标签。
- **列级安全性 (Column-level Security)**：通过分类机制定义政策标记（Policy Tags），将政策标记关联至 BigQuery 表的特定列，限制敏感敏感数据的访问。
- **敏感数据识别 (Cloud DLP 结合)**：可与 Cloud Data Loss Prevention (DLP) 联动，自动扫描敏感信息并自动在 Data Catalog 中为数据打上对应的安全标签。

### 3.4. 数据治理

- **数据资产分类法**：创建层次化的政策标记分类（Taxonomies），为企业内部的所有敏感数据类型确立标准定义。
- **数据沿袭 (Data Lineage)**：在 Dataplex 的赋能下，追踪数据从源头到数仓、再到分析报表（如 Looker 报表）的流动轨迹，方便影响分析和故障排查。
- **业务术语表 (Business Glossary)**：为组织内的业务名词建立标准释义，并与实际的技术资产相关联，消除业务与 IT 之间的沟通壁垒。

## 4. 数据迁移

- **本地及第三方元数据集成**：针对非 Google Cloud 的数据源（如 On-premises RDBMS、Apache Hive 或其他云平台的存储），可以使用 Data Catalog API 或开源的 Connector（例如 Apache Atlas 迁移工具）将元数据注入到 Data Catalog 中。
- **升级至 Dataplex**：对于存量的 Data Catalog 资源，建议逐步迁移并映射至 Dataplex 的湖（Lakes）、区域（Zones）及资产（Assets）管理体系中，以实现数据治理、数据生命周期管理和自动化计算的统一管控。

## 5. 参考资料

- [官方文档](https://cloud.google.com/data-catalog/docs?hl=zh-cn)
