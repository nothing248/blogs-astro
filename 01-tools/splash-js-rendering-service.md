---
title: "Splash渲染服务"
filename: splash-js-rendering-service
summary: Splash 是一款轻量级的 JavaScript 渲染服务，常用于爬虫开发中处理动态加载的网页内容。它基于 Docker 部署，通过 HTTP API 提供渲染后的 HTML、截图等信息。本文记录了其 Docker 安装流程及基础面板使用，是绕过前端渲染障碍、获取动态数据的有效方案。
tags: [crawler, javascript, docker, splash]
aliases: [Splash渲染服务]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:28 下午
date modified: 星期五, 六月 19日 2026, 12:08:45 中午
---

<!-- toc -->

## 1. 简介

Splash 是一个带有 HTTP API 的 JavaScript 渲染服务。它是一个带有一些额外功能的轻量级 Web 浏览器，能够异步处理多个网页渲染请求。

## 2. 安装

Splash 推荐通过 Docker 进行部署，以确保环境的一致性。

### 2.1. 前提条件

- 系统已安装并运行 Docker。

### 2.2. 部署步骤

```shell
# 拉取最新版本的 Splash 镜像
docker pull scrapinghub/splash

# 运行容器，映射相关端口
# 8050: HTTP API 接口
# 5023: Telnet 接口
# 8051: HTTPS API 接口
docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
```

## 3. 使用指南

### 3.1. 管理面板

容器启动后，可以通过浏览器访问 `http://localhost:8050` 查看其内置的脚本编辑和调试面板。在该面板中，你可以直接测试 Lua 脚本对目标网页的渲染效果。

![Splash 面板](http://qiniu.sxyxy.top/20240206164238.png?images=images)

## 4. 参考资料

- [Splash 官方文档](https://splash.readthedocs.io/en/stable/)
