---
title: "FlareSolverr安装"
filename: flaresolverr-docker-installation
description: FlareSolverr 是一款旨在绕过 Cloudflare 等 CDN 反爬限制的开源代理工具。它通过在 Docker 容器中运行 Headless 浏览器来执行挑战验证，并提供 HTTP API 供外部调用。本文记录了基于 Docker Compose 的安装配置步骤，支持时区设置及验证码求解器集成，是自动化抓取受限网页的核心组件。
tags: [flaresolverr, cloudflare, proxy, docker, web-scraping]
aliases: [FlareSolverr安装]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 11:59:11 中午
---

<!-- toc -->

## 1. 简介

FlareSolverr 是一个用于绕过 Cloudflare 和 Google Cloud Armor 挑战的代理服务器。它作为一个接口，可以拦截网页请求，自动解决“等待 5 秒”等 JavaScript 挑战，并将带有有效 Cookie 的 HTML 内容返回给调用方。

## 2. 安装

推荐使用 Docker Compose 进行部署，以简化环境依赖管理。

### 2.1. Docker Compose 配置

创建 `docker-compose.yml` 文件：

```yaml
version: "2.1"
services:
  flaresolverr:
    image: ghcr.io/flaresolverr/flaresolverr:latest
    container_name: flaresolverr
    environment:
      - LOG_LEVEL=${LOG_LEVEL:-info}
      - LOG_FILE=${LOG_FILE:-none}
      - LOG_HTML=${LOG_HTML:-false}
      - CAPTCHA_SOLVER=${CAPTCHA_SOLVER:-none}
      - TZ=Asia/Shanghai
    ports:
      - "${PORT:-8191}:8191"
    volumes:
      - ./config:/config
    networks:
        - local
    restart: unless-stopped
    
networks:
  local:
    external: true
```

## 3. 使用说明

- **端口**：默认监听 `8191` 端口。
- **API 调用**：通过发送 HTTP POST 请求到 `http://localhost:8191/v1` 来启动会话或执行请求。
- **集成**：常用于 Prowlarr、Jackett 等索引管理器中，用于解决 BT 站点的 Cloudflare 验证。

## 4. 参考资料

- [FlareSolverr GitHub 仓库](https://github.com/FlareSolverr/FlareSolverr)
