---
title: "NaiveProxy配置"
filename: naiveproxy-setup-guide
description: NaiveProxy 是一款基于 Caddy 的高性能代理工具，通过利用 Chrome 网络栈提供极强的抗探测能力。本文介绍了其服务端的安装与配置方法，包括使用 xcaddy 编译带插件的 Caddy、TLS 证书设置以及前置代理配置。同时提供了简单的客户端 JSON 配置示例，适用于需要高隐蔽性网络代理的场景。
tags: [naiveproxy, caddy, proxy, network-security]
aliases: [NaiveProxy配置, Caddy代理]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:20 下午
date modified: 星期五, 六月 19日 2026, 12:06:40 中午
---

<!-- toc -->

## 1. 简介

NaiveProxy 使用 Chrome 的网络栈来伪装流量，使其在特征上与普通的 HTTPS 流量完全一致，从而具备极强的探测防御能力。它通常作为 Caddy 的一个插件运行。

## 2. 安装

由于 NaiveProxy 需要特定的 `forwardproxy` 插件，建议使用 `xcaddy` 进行自定义编译：

```shell
# 使用 xcaddy 编译集成 naive 插件的 Caddy
~/go/bin/xcaddy build --with github.com/caddyserver/forwardproxy@caddy2=github.com/klzgrad/forwardproxy@naive
```

## 3. 配置

### 3.1. 服务端配置 (Caddyfile)

服务端需要配置 TLS 证书以及 `forward_proxy` 插件：

```text
{
  # 自定义 HTTPS 端口号
  https_port 1008 
  order forward_proxy before file_server
}

:1008, [example.com] {
  # TLS 证书路径（请替换为实际路径）
  tls /root/certs/[example.com]/fullchain.pem /root/certs/[example.com]/key.pem
  
  # 前置代理配置，需确保已安装对应插件
  forward_proxy {
    # 设置基础身份认证
    basic_auth [username],[password]
    hide_ip
    hide_via
    probe_resistance
    # upstream socks5://127.0.0.1:1007 # 可选：上游代理
  }
  
  # 伪装站点的静态文件路径
  file_server {
    root /root/html/Kelvin
  }
  
  # 反向代理（可选，用于进一步伪装）
  #reverse_proxy {
  #  to 127.0.0.1:2023
  #}
}
```

### 3.2. 客户端配置 (config.json)

客户端通过 JSON 文件定义监听端口和上游代理服务器：

```json
{
  "listen": "socks://127.0.0.1:1080",
  "proxy": "https://[username]:[password]@[example.com]"
}
```

## 4. 运行

### 4.1. 服务端运行

```shell
# 启动 Caddy
caddy run --config Caddyfile
```

### 4.2. 客户端运行

下载对应的二进制文件并执行：

```shell
./naive config.json
```

## 5. 参考资料

- [NaiveProxy 官方 GitHub 仓库](https://github.com/klzgrad/naiveproxy)
- [Caddy 官方文档](https://caddyserver.com/docs/)
