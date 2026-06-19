---
title: "Grafana可视化面板"
filename: grafana-monitoring-dashboard-setup
summary: Grafana 是一款强大的开源度量分析与可视化套件，支持 Prometheus、MySQL 等多种数据源。本文详述了 Grafana Enterprise 版本的安装与 Systemd 服务配置，重点介绍了匿名访问与嵌套（Embedding）等核心安全配置。通过对比 Prometheus 与 Grafana 的职能差异（存储 vs 展示），阐明了其在监控体系中的核心地位，并提供了面板导入与模板下载的实战指引。
tags: [grafana, monitoring, dashboard, visualization]
aliases: [Grafana可视化面板]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:25 下午
date modified: 星期五, 六月 19日 2026, 11:59:51 中午
---

<!-- toc -->

## 1. 简介

Grafana 是一款跨平台、开源的度量分析和可视化工具。它可以将来自不同数据源（Prometheus, InfluxDB, MySQL, Elasticsearch 等）的数据通过精美的仪表盘展示出来。

## 2. 安装步骤

### 2.1. 软件安装

```shell
mkdir -p /opt/software && cd /opt/software
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-11.4.0.linux-amd64.tar.gz
tar -zxvf grafana-enterprise-11.4.0.linux-amd64.tar.gz
# 将二进制文件链接至系统路径
cp -r grafana-v11.4.0/bin/* /usr/bin/
```

### 2.2. 核心配置 (`conf/defaults.ini`)

```ini
# 允许将 Grafana 面板嵌套在其他网页中 (iframe)
allow_embedding = true

# 开启匿名访问 (无需登录即可查看只读面板)
[auth.anonymous]
enabled = true
org_name = Main Org.
org_role = Viewer
```

### 2.3. 系统服务管理 (Systemd)

创建 `/etc/systemd/system/grafana.service`：

```ini
[Service]
Type=simple
WorkingDirectory=/opt/software/grafana
ExecStart=/usr/bin/grafana server \
    --config /opt/software/grafana/conf/defaults.ini \
    --homepath /opt/software/grafana
Restart=on-failure
```

## 3. 实战使用

### 3.1. 数据源与面板

1. **添加数据源**：在“Connections > Data Sources”中配置 Prometheus 或数据库地址。
2. **导入面板**：通过官方的 [Dashboard 市场](https://grafana.com/grafana/dashboards/) 寻找成熟的模板，直接使用模板 ID 导入即可快速生成监控图表。

## 4. 概念辨析：Prometheus Vs Grafana

| 特性 | Prometheus | Grafana |
| :--- | :--- | :--- |
| **主要功能** | 数据采集、存储、告警 | 数据可视化、仪表盘展示 |
| **数据流** | Pull 模式获取 Metric 数据 | 从数据源 Query 数据并渲染 |
| **存储** | 自带时序数据库 (TSDB) | 不存储业务数据，仅存储配置 |

## 5. 参考资料

- [Grafana 官方文档](https://grafana.com/docs/)
- [Grafana Dashboard 模板市场](https://grafana.com/grafana/dashboards/)
