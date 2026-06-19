---
title: "RSSHub安装"
filename: rsshub-docker-deployment-guide
summary: RSSHub 是一款开源、易于使用的 RSS 生成器，能够将几乎所有内容（如社交媒体、音视频平台、新闻等）转化为 RSS 订阅源。本文提供了基于 Docker Compose 的完整部署配置，涵盖了 Redis 缓存集成、Browserless 渲染引擎连接以及访问密钥（ACCESS_KEY）的安全设置。旨在帮助用户构建私有化的信息流订阅中心，彻底解决信息碎片化问题。
tags: [rsshub, rss, information-retrieval, self-hosted, docker, puppeteer]
aliases: [RSSHub安装, 万物皆可RSS, 订阅源生成器]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:08:16 中午
---

<!-- toc -->

## 1. 简介

RSSHub 是一个由 DIYgod 发起的开源项目，它通过各种路由将不支持 RSS 的网站内容转化为标准化的 RSS 输出。目前已支持数千个路由，涵盖了知乎、微博、Bilibili、Twitter、Instagram 等主流平台。

## 2. 部署指南 (Docker Compose)

为了获得最佳性能（如处理动态渲染页面），建议集成 Redis 和 Browserless（无头浏览器）。

```yaml
services:
  rsshub:
    image: diygod/rsshub:latest
    container_name: rsshub
    restart: always
    ports:
      - "1200:1200"
    networks:
      - media_network
    environment:
      NODE_ENV: production
      # 缓存配置：推荐使用 Redis 提升响应速度
      CACHE_TYPE: redis
      REDIS_URL: "redis://redis:6379/"
      
      # 渲染配置：用于抓取动态加载的页面
      PUPPETEER_WS_ENDPOINT: "ws://browserless:3000"
      
      # 安全配置：防止接口被滥用
      ACCESS_KEY: "[YOUR_SECRET_KEY]"
      
      # 自定义实例描述
      FOLLOW_DESCRIPTION: "My Private RSSHub"
      FOLLOW_USER_LIMIT: 1 # 设置为 1 使实例私有化
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:1200/healthz?key=[YOUR_SECRET_KEY]"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - redis
      - browserless

networks:
  media_network:
    external: true
```

## 3. 核心功能与使用

- **万物皆可 RSS**：通过简单的 URL 规则生成订阅源（如 `https://rsshub.app/bilibili/user/video/2267573`）。
- **规则配置**：支持设置黑白名单、关键词过滤等功能。
- **Browserless 集成**：通过外置的浏览器服务处理反爬虫和复杂脚本渲染。

## 4. 常用环境变量说明

| 变量名 | 说明 |
| :--- | :--- |
| `ACCESS_KEY` | 访问密钥。开启后需在 URL 后附带 `?key=xxx` 才能访问。 |
| `CACHE_EXPIRE` | 缓存过期时间（秒），默认 300 秒。 |
| `PROXY_URL` | 代理地址。若服务器无法访问部分国外网站，可配置此项。 |

## 5. 参考资料

- [RSSHub 官方文档 (中文)](https://docs.rsshub.app/zh/)
- [RSSHub GitHub 仓库](https://github.com/DIYgod/RSSHub)
- [RSSHub 公共实例列表](https://docs.rsshub.app/install/#public-instances)
