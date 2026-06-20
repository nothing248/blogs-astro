---
status: completed
filename: ufw-uncomplicated-firewall-configuration-guide
title: "UFW 命令"
description: 本笔记记录了 Ubuntu/Debian 系统下极简防火墙工具 UFW (Uncomplicated Firewall) 的核心操作指南。UFW 作为底层 iptables 的高级前端封装，大幅降低了配置网络访问规则的心智负担。笔记列出了安装指令及最常用的规则配置实战，包括基于端口/协议（TCP/UDP）的开放与拦截，以及基于特定 IP 来源的白名单管控，为服务器网络安全加固提供速查参考。
aliases: [UFW 命令, Ubuntu 防火墙, iptables 前端]
tags: [Linux, 网络安全, 防火墙, UFW, Ubuntu, 运维配置]
date created: 星期二, 二月 25日 2025, 3:24:16 下午
date modified: 星期四, 六月 18日 2026, 12:35:00 晚上
---

<!-- toc -->

## 1. 核心定位：iptables 的极简前端

在 Linux 2.4 内核后，底层提供了一套极其强大的网络数据包处理框架：`netfilter/iptables`。
由于直接编写 `iptables` 规则表非常复杂，Ubuntu 等发行版推出了 **UFW (Uncomplicated Firewall)**。它提供了一层极其人性化的命令行封装，用于快速定义防火墙的流入、流出及 NAT 控制规则。

---

## 2. 核心运维指令速查

### 2.1. 安装与状态检视

```bash
apt install ufw          # 安装工具
sudo ufw status          # 查看防火墙是否启用及当前生效的精简规则列表
sudo ufw status verbose  # 查看包含日志级别、默认策略等详细状态
```

### 2.2. 放行规则 (Allow)

```bash
# 粗粒度：开放特定端口 (TCP/UDP 同时开放)
sudo ufw allow 53 

# 细粒度：精确放行特定端口与协议
sudo ufw allow 80/tcp

# IP 级管控：仅允许特定 IP 访问本服务器所有资源 (白名单)
sudo ufw allow from 192.168.254.254
```

### 2.3. 拦截与规则撤销 (Deny / Delete)

```bash
# 显式拒绝某个服务 (如 SMTP) 的访问
sudo ufw deny smtp

# 撤销已配置的规则 (语法为：delete + 之前创建规则的精确命令)
sudo ufw delete allow 80/tcp
```
