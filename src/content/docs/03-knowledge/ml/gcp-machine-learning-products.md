---
title: "GCP机器学习产品汇总"
filename: gcp-machine-learning-products
description: 本笔记梳理了谷歌云 (GCP) 旗下主流机器学习与数据处理产品。涵盖敏感信息检测 API (DLP)、内建建模工具 BigQuery ML、大模型与工作流平台 Vertex AI（包含 AutoML 表格预测的要求与拆分规则），以及流批一体计算 Dataflow、可视化数据清洗 Dataprep 和异步队列 Pub/Sub，为 GCP 架构设计提供参考。
tags:
  - google-cloud
  - gcp
  - mlops
  - data-engineering
aliases:
  - GCP机器学习产品汇总
  - 谷歌云数据服务指南
status: completed
date created: 星期二, 二月 25日 2025, 3:23:59 下午
date modified: 星期二, 六月 16日 2026, 6:24:26 晚上
---

<!-- toc -->

## 1. 简介

本笔记梳理了 **Google Cloud Platform (GCP)** 平台在机器学习（ML）与数据工程（Data Engineering）领域的核心产品与技术规范，便于快速检索各类组件的定位、应用场景与注意事项。

---

## 2. 机器学习与智能平台

### 2.1. Cloud Data Loss Prevention (DLP)

- **定位**：用于识别、归类和保护敏感信息的 API 服务。
- **功能**：可自动扫描并脱敏文本、图像和存储中的个人身份信息（PII），如身份证号、电话、信用卡等。

### 2.2. BigQuery ML

- **定位**：直接在 BigQuery 仓库中使用 SQL 语句构建和运行机器学习模型。
- **技术支持**：支持导入训练好的 TensorFlow/PyTorch 模型，并内建了对深度神经网络、线性回归以及 K-Means 聚类的支持。

### 2.3. Vertex AI

- **定位**：GCP 统一的管理式机器学习平台，集成了原有的 AI Platform 与 AutoML。
- **核心组件**：
  - **Kubeflow Pipelines**：构建端到端的弹性 MLOps 工作流。
  - **Metrics API**：用于跟踪和调优模型训练超参数。

### 2.4. AutoML (自动机器学习)

提供低代码/无代码的自动化模型训练服务，主要涵盖四个领域：

1. **文本 (AutoML Text)**：文本分类、实体提取、情感分析。
2. **图像 (AutoML Vision)** 与 **视频 (AutoML Video)**。
3. **表格 (AutoML Tables)**：
   - 支持 **分类**、**回归** 和 **时序预测**。
   - **时序预测数据列要求**：输入数据必须包含 **时间列**、**目标值列** 以及 **序列标识符（Series Identifier）列**。
   - **数据集划分规则**：
     - 支持随机拆分、手动指定拆分。
     - **默认拆分比例为 8:1:1**（训练集 : 验证集 : 测试集）。对于预测模型，系统会自动按事件发生的时间顺序进行前后分割，以防止数据泄露。

> [!warning] 表格时序处理注意事项
> 若时间戳被拆分分布在多个数据列中（如年、月、日分别作为一列），则必须在导入前将其手动合并并转换为标准的 Timestamp 格式。具体可参考 [AutoML Tables 数据最佳实践](https://cloud.google.com/automl-tables/docs/data-best-practices#time)。

---

## 3. 数据集成与流批处理

### 3.1. Cloud Data Fusion

- **定位**：全托管、云原生的图形化数据集成（ETL/ELT）服务。
- **特点**：提供丰富的连接器和插件，可在大规模数据集上进行零代码管道搭建。

### 3.2. Dataflow

- **定位**：基于 Apache Beam 构建的统一的流处理（Streaming）和批处理（Batch）无服务器计算引擎。
- **特点**：高并发、自动弹性缩放、性价比高。

### 3.3. Dataprep (by Trifacta)

- **定位**：一款智能的云端数据准备服务，提供可视化的探索、清洗和预处理功能，专门用于为数据分析和机器学习提供干净的数据源。

### 3.4. Pub/Sub

- **定位**：高并发、异步且可弹性伸缩的发布/订阅消息队列中间件。
- **数据集成**：非常适合用来收集高频流式数据（如传感器、IoT 机器日志），并支持无缝地 **直接流式输出到 BigQuery**、Data Lakes 中。

---

## 4. 经典算法应用

### 4.1. 协同过滤系统 (Collaborative Filtering)

- **定位**：推荐系统的核心算法之一。
- **特点**：通过分析大量相似用户的历史行为数据（如评分、点击等）来推荐相似内容。其局限性是高度依赖历史行为矩阵，容易面临“冷启动”问题。
