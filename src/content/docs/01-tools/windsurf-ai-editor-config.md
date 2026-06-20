---
title: "Windsurf配置"
filename: windsurf-ai-editor-config
description: Windsurf 是一款主打 Agentic 工作流的新一代 AI 代码编辑器，旨在提供深度辅助的编程体验。本文记录了其全局回复规则配置（强制中文答复）、代理识别问题的修复方案以及其不限量的代码自动补全特性。它是提升开发效率、实现“AI 驾驶”编程的核心工具。
tags:
  - ai
  - editor
  - productivity
  - windsurf
aliases:
  - Windsurf配置
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 2026-06-18
---

<!-- toc -->

## 1. 简介

Windsurf 是一个集成大模型能力的现代编辑器。它不仅支持传统的代码补全，更通过 Agent 模式理解整个项目上下文，协助开发者完成复杂的重构和调试任务。

## 2. 安装与配置

### 2.1. 全局规则配置

为了获得更好的交互体验，建议在设置中配置自定义指令（Custom Instructions）：

```text
总是以中文进行答复。
```

### 2.2. 网络代理配置
>
> [!warning]
> 在某些受限网络环境下，如果代码自动补全功能失效，请检查以下设置：
>
> 1. 确保系统代理已开启。
> 2. 在 Windsurf 设置中勾选 **"Detect Proxy"** 选项。

## 3. 核心优势

- **Agentic Workflow**：能够自主执行多步文件修改和命令运行任务。
- **高性能补全**：提供响应迅速且不限量的上下文感知补全。

## 4. 参考资料

- [Windsurf 官方网站](https://windsurf.com/editor)
