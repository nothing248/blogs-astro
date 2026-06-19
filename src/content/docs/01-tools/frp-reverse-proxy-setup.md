---
title: "FRP配置"
filename: frp-reverse-proxy-setup
summary: FRP (Fast Reverse Proxy) 是一款高性能的反向代理工具，核心用于将内网服务暴露至公网（内网穿透）。本文介绍了 v0.67.0 版本的安装步骤，详细说明了服务端 (frps) 与客户端 (frpc) 的 TOML 配置文件编写，包括 SSH 与 Web 服务的代理配置。同时提供了通过 Systemd 管理 FRP 服务的实战指南。
tags: [frp, reverse-proxy, intranet-penetration, network]
aliases: [FRP配置]
status: completed
date created: 星期五, 三月 27日 2026, 3:07:05 下午
date modified: 星期五, 六月 19日 2026, 11:59:19 中午
---

<!-- toc -->

## 1. 简介

FRP (Fast Reverse Proxy) 是一款专注于内网穿透的高性能反向代理应用。它通过在具有公网 IP 的节点上部署服务端（frps），将内网节点上的客户端（frpc）流量进行转发，从而实现从公网访问内网服务的目的。

## 2. 安装步骤

从 GitHub Release 页面下载对应架构的二进制文件：

```shell
mkdir -p /opt/software && cd /opt/software
wget https://github.com/fatedier/frp/releases/download/v0.67.0/frp_0.67.0_linux_amd64.tar.gz
tar -zxvf frp_0.67.0_linux_amd64.tar.gz
```

## 3. 配置指南

### 3.1. 服务端配置 (`frps.toml`)

部署在公网服务器上。

```toml
# 服务绑定端口，用于和客户端通信
bindPort = 7000

# 身份验证令牌，必须与客户端保持一致
auth.token = "[SECRET_TOKEN]"

# Web 管理面板配置 (可选)
dashboardAddr = "0.0.0.0"
dashboardPort = 7500
dashboardUser = "admin"
dashboardPwd = "[ADMIN_PASSWORD]"
```

### 3.2. 客户端配置 (`frpc.toml`)

部署在内网设备上。

```toml
# 服务端公网地址
serverAddr = "[PUBLIC_IP]"
serverPort = 7000
auth.token = "[SECRET_TOKEN]"

[[proxies]]
name = "ssh-access"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000 # 通过 公网IP:6000 访问内网 SSH

[[proxies]]
name = "web-service"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = 8081 # 通过 公网IP:8081 访问内网 Web
```

## 4. 服务管理 (Systemd)

创建服务文件 `/etc/systemd/system/frps.service`：

```ini
[Unit]
Description=FRP Server Service
After=network.target

[Service]
Type=simple
ExecStart=/opt/software/frp/frps -c /opt/software/frp/frps.toml
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

使用以下命令控制服务：

```bash
sudo systemctl enable frps
sudo systemctl start frps
sudo systemctl status frps
```

## 5. 参考资料

- [FRP 官方文档](https://gofrp.org/)
- [FRP GitHub 仓库](https://github.com/fatedier/frp)
