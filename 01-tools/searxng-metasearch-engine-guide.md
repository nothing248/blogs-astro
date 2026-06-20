---
title: "SearXNG安装"
filename: searxng-metasearch-engine-guide
description: SearXNG 是一款开源、免费且尊重隐私的元搜索引擎（Metasearch Engine），它能聚合来自 Google, Bing, DuckDuckGo 等数十个源的搜索结果，且不追踪用户信息。本文提供了基于 Docker Compose 的标准部署方案及核心卷映射配置，并针对“引擎初始化报错”的常见问题提出了关闭冗余源的解决思路，旨在帮助用户搭建私有且纯净的搜索门户。
tags: [searxng, search-engine, privacy, open-source, docker, self-hosted]
aliases: [SearXNG安装, 隐私搜索引擎, 元搜索引擎部署]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:08:29 中午
---

<!-- toc -->

## 1. 简介

SearXNG 是一个隐私友好的元搜索引擎，它是对原始 Searx 项目的高性能分支。它不会收集用户的搜索数据，也不允许第三方（如 Google）建立用户的搜索画像。通过 SearXNG，你可以同时从数十个搜索引擎获取结果，并保持完全的匿名性。

## 2. 部署指南 (Docker Compose)

官方推荐使用 Docker 方式进行部署，以便于管理复杂的 Python 运行环境。

```yaml
services:
  searxng:
    image: docker.io/searxng/searxng:latest
    container_name: searxng
    restart: always
    ports:
      - "8080:8080"
    networks:
      - media_network
    volumes:
      - ./searxng:/etc/searxng:ro       # 映射配置文件目录 (只读)
      - searxng_data:/var/cache/searxng # 缓存数据卷
    environment:
      - SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  media_network:
    external: true

volumes:
  searxng_data:
```

## 3. 配置建议

### 3.1. 初始化设置

首次启动前，需在 `./searxng` 目录下创建 `settings.yml`。

### 3.2. 解决引擎报错问题

> [!warning] **常见痛点**
> 某些上游引擎（如 Google 或特定学术搜索）可能会因为频繁请求、反爬虫或地域限制导致初始化报错（Timeouts / Captcha）。
>
> **解决思路**：
>
> - 在 `settings.yml` 的 `engines` 模块中，将报错的引擎设置为 `disabled: True`。
> - 建议配置代理（Proxy）以提升上游连接的成功率。

## 4. 核心特性

- **多模式搜索**：支持常规网页、图片、文件、地图、音乐、学术、社交媒体等多种垂直搜索分类。
- **响应式设计**：完美适配手机、平板及桌面端浏览器。
- **无追踪**：不存储 Cookie，不记录 IP 行为，且默认移除请求中的跟踪参数。

## 5. 参考资料

- [SearXNG 官方文档](https://docs.searxng.org/)
- [SearXNG GitHub 仓库](https://github.com/searxng/searxng)
- [公共 SearXNG 实例列表](https://searx.space/)
