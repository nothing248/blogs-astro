---
status: completed
filename: kibana-visualization-tool-installation-and-setup
title: "Kibana 安装"
summary: 本笔记记录了 ELK 技术栈中可视化分析组件 Kibana 的安装与环境配置流程。详细提供了 Kibana 8.x Linux 二进制包下载、`kibana.yml` 中连接 Elasticsearch 集群的核心参数（IP、鉴权、中文汉化及 SSL 设置），以及通过 systemd 配置服务后台守护进程与开机自启的运维 SOP。此指南旨在协助运维人员快速搭建与 Elasticsearch 无缝对接的日志与指标可视化分析面板。
aliases: [Kibana 安装, ELK 部署, 可视化组件, kibana.yml]
tags: [Kibana, 大数据, Elasticsearch, ELK, 数据可视化, Linux, 运维部署, 日志分析]
date created: 星期三, 十二月 10日 2025, 6:20:41 晚上
date modified: 星期四, 六月 18日 2026, 10:15:00 晚上
---

<!-- toc -->

## 1. 组件简介

**Kibana** 是 Elastic Stack (ELK) 中的数据可视化窗口。它基于 Elasticsearch 的强大检索能力，提供图表、仪表盘绘制及系统监控告警管理功能。

---

## 2. 安装与基础配置

### 2.1. 二进制包获取与解压

```bash
curl -O https://artifacts.elastic.co/downloads/kibana/kibana-8.17.3-linux-x86_64.tar.gz
# 校验哈希完整性 (可选)
curl https://artifacts.elastic.co/downloads/kibana/kibana-8.17.3-linux-x86_64.tar.gz.sha512 | shasum -a 512 -c - 
tar -xzf kibana-8.17.3-linux-x86_64.tar.gz -C /opt/software
```

### 2.2. `kibana.yml` 核心关联配置

位于 `config/kibana.yml`，需配置绑定 IP 及 ES 集群地址：

```yaml
server.port: 5601
# Kibana 绑定的宿主机 IP
server.host: "192.169.3.41"

# Elasticsearch 服务地址池
elasticsearch.hosts: ["http://192.169.3.41:9101","http://192.169.3.41:9102","http://192.169.3.41:9103"]

# Elasticsearch 认证账号 (必须是 kibana_system 角色，不能用超级管理员 elastic)
elasticsearch.username: "kibana_system"
elasticsearch.password: "123qwe"

# 取消严格证书验证 (用于测试环境)
elasticsearch.ssl.verificationMode: none

# 开启原生中文界面支持
i18n.locale: "zh-CN"
```

---

## 3. 生产环境运维部署

> [!warning] 安全限制
> 与 Elasticsearch 类似，Kibana 默认 **禁止使用 root 用户运行**。请配置专门的 `elastic` 账户。

### 3.1. Systemd 守护进程注册

在 `/etc/systemd/system/kibana.service` 写入配置，利用 Node 环境参数限制内存峰值：

```ini
[Unit]
Description=Kibana Service
After=network.target

[Service]
Type=simple
User=elastic
Group=elastic
WorkingDirectory=/opt/software/kibana-8.17.3
ExecStart=/opt/software/kibana-8.17.3/bin/kibana
Restart=on-failure
# 限制 Node.js 内存上限为 4GB
Environment=NODE_OPTIONS="--max-old-space-size=4096"

[Install]
WantedBy=multi-user.target
```

**服务控制指令**：

```bash
systemctl daemon-reload
systemctl enable kibana
systemctl start kibana
systemctl status kibana
```

**访问验证**：
打开浏览器访问 `http://192.169.3.41:5601`，登录需使用 Elasticsearch 主管理员（如 `elastic`）的账密。
