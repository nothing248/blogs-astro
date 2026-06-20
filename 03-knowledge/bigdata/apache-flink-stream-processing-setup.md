---
status: completed
filename: apache-flink-stream-processing-setup
title: "Flink 安装"
description: 本笔记记录了新一代大数据处理引擎 Apache Flink 的核心定位及基础部署流程。阐述了 Flink “批流一体”的核心设计理念（将批处理视为有界的流处理）。提供了在 Linux 系统下单机模式的二进制包下载、环境变量配置及启停指令，为进行实时无界数据流分析提供了初始实验环境。
aliases: [Flink 安装, 流处理引擎, Flink 批流一体]
tags: [大数据, Flink, 流处理, 实时计算, 分布式计算, 运维部署]
date created: 星期三, 十二月 10日 2025, 6:20:42 晚上
date modified: 星期四, 六月 18日 2026, 10:05:00 晚上
---

<!-- toc -->

## 1. Flink 核心架构理念

**Apache Flink** 是一个分布式的流处理引擎，能够对有界（Bounded）和无界（Unbounded）的数据流进行高效的实时计算。

- **批流一体**：Flink 在架构层面上将“批处理”视为流处理的一种特例（即数据流有一个明确的终点边界），从而使用统一的 API 来处理实时流数据和历史存量数据。

---

## 2. 基础环境搭建 (单机 Standalone 模式)

单机模式适合进行本地代码调试与基础 API 验证。

### 2.1. 下载与环境变量注入
>
> [!note] 兼容性提示
> 下载 Flink 时需注意与底层 Hadoop/Scala 版本的兼容性匹配。

```bash
# 获取特定版本的二进制包
wget https://dlcdn.apache.org/flink/flink-1.20.0/flink-1.20.0-bin-scala_2.12.tgz 
tar -zxvf flink-1.20.0-bin-scala_2.12.tgz -C /opt/software

# 配置系统环境变量
export FLINK_HOME=/opt/software/flink-1.20.0
export FLINK_CONF_DIR=$FLINK_HOME/conf
export PATH=$FLINK_HOME/bin:$PATH
```

### 2.2. 本地集群启停与验证

```bash
# 启动单机沙箱集群
start-cluster.sh

# 停止服务
stop-cluster.sh
```

启动成功后，可通过浏览器访问 Flink 的内置 Web 仪表盘监控计算任务：
`http://localhost:8081`

## 3. 参考资料

- [Apache Flink 官方主页](https://flink.apache.org/)
