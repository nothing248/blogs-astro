---
title: "Caddy服务器"
filename: caddy-server-setup-config
summary: Caddy 是一款现代化的 HTTP/2 服务器，原生支持自动 HTTPS。本笔记介绍了 Caddy 的安装方式（包管理器及 xcaddy 编译）、核心配置文件 Caddyfile 的编写规范。内容涵盖了静态文件服务、基于插件的前置代理（forward_proxy）、反向代理、WebSocket 支持以及自定义 TLS 证书配置，解决了 Web 服务快速部署与自动化证书管理的实际需求。
tags: ["Caddy", "Web-Server", "HTTPS", "Reverse-Proxy", "xcaddy"]
aliases: ["Caddy服务器", "自动HTTPS网关", "Caddyfile配置"]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:29 下午
date modified: 星期五, 六月 19日 2026, 11:58:10 中午
---

<!-- toc -->

## 1. 简介

**Caddy** 是一款基于 Go 语言编写的高性能 Web 服务器。它以极简的配置和 **原生支持自动 HTTPS** 而闻名。无论是作为静态资源服务器还是反向代理，Caddy 都能在几秒钟内完成部署并自动申请证书。

---

## 2. 安装部署

### 2.1. 系统软件包安装 (RHEL/CentOS)

```shell
yum install yum-plugin-copr
yum copr enable @caddy/caddy
yum install caddy
```

### 2.2. 使用 Xcaddy 手动编译 (含插件)

如果你需要添加特定插件（如前置代理），推荐使用 `xcaddy` 进行构建。需预装 Go v1.20+。

1. **安装 xcaddy**：

   ```shell
   go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest
   ```

2. **编译构建**：

   ```shell
   # 编译带有 output 标志的 caddy 二进制文件
   ~/go/bin/xcaddy build --with [插件名称] --output caddy
   ```

---

## 3. Caddyfile 配置实战

Caddy 的配置文件 `Caddyfile` 结构清晰且语义化。

### 3.1. 基础反向代理与静态文件

```text
{
  https_port 10443 # 自定义 HTTPS 端口
}

example.com {
  # 指定自定义 TLS 证书
  tls /certs/fullchain.pem /certs/privkey.pem

  # 静态文件服务
  handle /static/* {
    uri strip_prefix /static
    file_server {
        root /var/www/static
    }
  }

  # 反向代理至后端服务
  handle {
    reverse_proxy localhost:8080
  }
}
```

### 3.2. WebSocket 代理配置

```text
:1009 {
  tls /certs/fullchain.pem /certs/privkey.pem
  
  @websockets {
    header Connection *Upgrade*
    header Upgrade websocket
  }
  
  reverse_proxy @websockets localhost:8838
}
```

### 3.3. 前置代理 (Forward Proxy)

需安装 `forwardproxy` 插件：

```text
example.com {
  forward_proxy {
    basic_auth username password
    hide_ip
    probe_resistance
  }
  file_server
}
```

---

## 4. 运行管理

```shell
# 以前台模式运行
caddy run --config /path/to/Caddyfile

# 重载配置 (平滑重载)
caddy reload --config /path/to/Caddyfile
```

---

## 5. 参考资料

- [Caddy 官方文档](https://caddyserver.com/docs/)
- [xcaddy 项目地址](https://github.com/caddyserver/xcaddy)
