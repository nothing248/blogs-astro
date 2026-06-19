---
title: "Prometheus部署"
filename: prometheus-monitoring-alerting-setup
summary: Prometheus是主流的开源时间序列监控告警系统。本文对其四大核心组件（Prometheus Server、客户端库、Pushgateway、Exporters）的作用进行了拆解。给出了基于Docker Compose配置时序库及编写服务发现、静态抓取目标和监控指标暴露的实践指南。
tags: [prometheus, monitoring, time-series-database, devops]
aliases: [Prometheus部署, 时序监控, 指标抓取配置]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:24 下午
date modified: 星期五, 六月 19日 2026, 12:07:40 中午
---

<!-- toc -->

## 1. 简介

开源的监控告警系统

## 2. 概念

- prometheus server
    核心组件，收集与存储时间序列数据
- CLient Library
    客户端库，为需要监控的服务生成相应的 metrics 并暴露给 Prometheus server
- push gateway
    主要用于短期的 jobs。由于这类 jobs 存在时间较短，可能在 Prometheus 来 pull 之前就消失了, 此，这次 jobs 可以直接向 Prometheus server 端推送它们的 metrics
- Exporters
    用于暴露已有的第三方服务的 metrics 给 Prometheus。
- Alertmanager
    从 Prometheus server 端接收到 alerts 后，会进行去除重复数据，分组，并路由到对收的接受方式，发出报警

## 3. 安装

- 下载

```shell
mkdir /opt/software
cd /opt/software 
wget https://github.com/prometheus/prometheus/releases/download/v3.1.0-rc.1/prometheus-3.1.0-rc.1.linux-amd64.tar.gz
tar -zxvf prometheus-3.1.0-rc.1.linux-amd64.tar.gz
cd prometheus-3.1.0-rc.1.linux-amd64
cp -r prometheus /usr/bin/
```

- 配置

```shell
# /opt/softwareprometheus-3.1.0-rc.1.linux-amd64/prometheus.yml
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager: 9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:10090"]
```

- 启动

```shell
./prometheus --config.file=prometheus.yml --web.listen-address=:10090
# 访问 http://localhost: 10900 查看面板
# 访问 http://localhost: 10900/metrics 查看暴露的指标信息
```

- 配置 systemd

```shell
#/etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus Server
Documentation=https://prometheus.io/docs/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/software/prometheus-3.1.0-rc.1.linux-amd64/prometheus \ # Prometheus 二进制文件的路径
    --config.file=/opt/software/prometheus-3.1.0-rc.1.linux-amd64/prometheus.yml \ # Prometheus 配置文件的路径
    --storage.tsdb.path=/opt/software/prometheus-3.1.0-rc.1.linux-amd64/data \ # Prometheus 数据存储路径
    --web.listen-address=:10090 \ # Prometheus 监听地址和端口
    --web.enable-lifecycle # 允许通过 API 重载配置
Restart=on-failure # 在 Prometheus 崩溃时自动重启
RestartSec=5s # 重启间隔时间

[Install]
WantedBy=multi-user.target
```

- 管理服务

```shell
systemctl restart prometheus 
systemctl start prometheus 
systemctl stop prometheus 
systemctl status prometheus 
```

## 4. Node Exporter 安装

- 下载

```shell
mkdir /opt/software
cd /opt/software 
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
tar -zxvf node_exporter-1.8.2.linux-amd64.tar.gz
cd node_exporter-1.8.2.linux-amd64
cp -r node_exporter /usr/bin/
```

- 配置

```yaml
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ["localhost:10090"]
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'apisix'
    scrape_interval: 10s
    metrics_path: '/apisix/prometheus/metrics'
    static_configs:
      - targets: ['localhost:9091']
```

> 参考：<https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md>

- 启动

```shell
/opt/software/node_exporter-1.8.2.linux-amd64/node_exporter --web.listen-address=:9100
```

- 配置 systemd

```shell
#/etc/systemd/system/prometheus-node.service
[Unit]
Description=Prometheus Node Exporter Server
Documentation=https://prometheus.io/docs/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/software/node_exporter-1.8.2.linux-amd64/node_exporter \
    --web.listen-address=:9100
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target 
```

- 管理服务

```shell
systemctl restart prometheus-node
systemctl start prometheus-node
systemctl stop prometheus-node
systemctl status prometheus-node
```

## 5. 拓展信息

...

## 6. 参考资料

- [官方文档](https://prometheus.io/)
