---
title: "DuckDB入门"
filename: duckdb-embedded-olap-database
summary: DuckDB 是一款嵌入式、面向 OLAP（在线分析处理）的列式关系型数据库管理系统。本笔记简述了 DuckDB 的定位，并提供了在数据分析决策中如何选择 DuckDB、Pandas 与 Dask 的参考矩阵。通过对比数据规模、偏好语言（SQL vs API）以及部署环境（本地 vs 集群），帮助用户在不同分析场景下选择最合适的数据处理引擎。
tags: ["DuckDB", "OLAP", "Database", "Data-Analysis", "SQL"]
aliases: ["DuckDB入门", "嵌入式分析型数据库", "DuckDB vs Pandas"]
status: completed
date created: 星期三, 十二月 10日 2025, 6:20:44 晚上
date modified: 星期五, 六月 19日 2026, 11:58:53 中午
---

<!-- toc -->

## 1. 简介

**DuckDB** 被称为“数据库界中的 SQLite”，它是一款专注于 **OLAP (在线分析处理)** 的列式关系型数据库管理系统。与传统的数仓不同，它是嵌入式的，无需独立服务器进程即可运行，且对大数据量的聚合查询进行了深度优化。

---

## 2. 技术选型：DuckDB Vs Pandas Vs Dask

在处理数据任务时，可以根据以下决策因素进行选择：

| 决策因素 | 推荐选择：**DuckDB** | 推荐选择：**Dask** (或 Spark) | 推荐选择：**Pandas** |
| :--- | :--- | :--- | :--- |
| **数据规模** | **小于 1TB**，且数据集中在单机 | **大于 1TB**，或需分布式计算 | 小于 10GB（受限于内存） |
| **偏好语言** | 倾向使用 **SQL** 进行分析 | 倾向 **Python (Pandas/NumPy) API** | 灵活的 Python 交互 |
| **部署环境** | **本地** 或单个服务器运行 | **Kubernetes** 或云端集群 | 本地开发环境 |
| **核心优势** | 极速的 SQL 执行与零依赖安装 | 强大的横向扩展能力 | 丰富的数据科学生态 |

---

## 3. 核心特性

- **列式存储**：针对分析型查询（聚合、过滤）具有天然的性能优势。
- **高度集成**：可以与 Python (Pandas/Polars)、R 语言等无缝对接，支持直接查询 Parquet, CSV, JSON 文件。
- **ACID 支持**：通过单一数据库文件提供事务保证。

---

## 4. 参考资料

- [DuckDB 官方文档](https://duckdb.org/docs/)
- [DuckDB Python API 指南](https://duckdb.org/docs/api/python/overview)
