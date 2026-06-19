---
title: "SuperProductivity配置"
filename: super-productivity-todo-tool
summary: Super Productivity 是一款开源、跨平台的待办事项与任务管理应用。本文介绍了其多端覆盖情况，并重点分析了在 Android 端通过 WebDAV（如 AList 挂载的云存储）同步时遇到的 NoRevAPIError 错误。通过切换到本地存储挂载的 WebDAV 成功规避了该问题，是解决同步故障的重要参考。
tags: [todo, productivity, open-source, webdav]
aliases: [SuperProductivity配置]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:22 上午
date modified: 星期五, 六月 19日 2026, 12:08:51 中午
---

<!-- toc -->

## 1. 简介

Super Productivity 是一款专为程序员和其他数字工作者设计的任务管理工具。它集成了待办事项、时间跟踪和任务管理功能，且不依赖于特定的云服务，支持数据本地存储或通过 WebDAV 同步。

## 2. 多端支持

- **移动端**：Android (支持 Google Play 和 APK 安装)。
- **桌面端**：macOS, Windows, Linux。

## 3. 常见问题与解决方案

### 3.1. WebDAV 同步报错：NoRevAPIError

在 Android 端使用 WebDAV 协议进行数据同步时，如果后端使用的是基于 Cloudflare 代理的 AList 服务，可能会触发 `NoRevAPIError` 错误。

> [!error] 故障现象
> 配置 WebDAV 后，Android 客户端无法成功读取或写入同步文件，报错信息指向版本修订相关 API 异常。

> [!success] 解决思路
> **切换同步源**。经测试，如果 WebDAV 指向的是基于 AList 本地存储（而非经过 Cloudflare 代理的远程存储）的服务，该问题通常会消失。猜测是由于 Cloudflare 的某些安全机制或 AList 在处理远程修订时的延迟/接口限制导致了该错误。

## 4. 参考文档

- [Super Productivity GitHub 项目地址](https://github.com/johannesjo/super-productivity)
