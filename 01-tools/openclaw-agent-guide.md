---
title: "OpenClaw代理"
filename: openclaw-agent-guide
description: OpenClaw 是一款私有的 AI Agent 代理工具，旨在提供安全、可控的智能体管理环境。本文介绍了 OpenClaw 的核心管理命令，包括网关的启动与停止、状态查询及初次配置引导（onboard）。同时指出了关键配置文件的位置及如何获取 Control UI 所需的认证 Token。
tags: [openclaw, ai-agent, proxy, self-hosted, automation]
aliases: [OpenClaw代理, AI代理配置]
status: completed
date created: 星期三, 五月 27日 2026, 11:36:50 中午
date modified: 星期五, 六月 19日 2026, 12:07:03 中午
---

<!-- toc -->

## 1. 简介

OpenClaw 是一个私有的 Agent 代理框架，允许用户在本地或私有云环境中部署和运行 AI 智能体，确保数据的私密性与任务执行的可控性。

## 2. 常用管理命令

通过命令行工具 `openclaw` 可以轻松管理代理服务的生命周期：

```shell
# 管理网关服务
openclaw gateway start    # 启动网关
openclaw gateway stop     # 停止网关
openclaw gateway restart  # 重启网关

# 查看运行状态
openclaw status

# 初次使用引导
openclaw onboard
```

## 3. 配置管理

OpenClaw 的核心配置存储在用户的家目录下。如果需要查看 Control UI 的访问令牌（Token）或其他敏感配置，可以查看以下文件：

```shell
# 查看配置文件内容
cat ~/.openclaw/openclaw.json
```

## 4. 参考资料

- [OpenClaw 官方文档 (中文)](https://docs.openclaw.ai/zh-CN/install)
