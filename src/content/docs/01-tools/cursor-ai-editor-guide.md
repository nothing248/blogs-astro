---
title: "Cursor编辑器"
filename: cursor-ai-editor-guide
description: Cursor 是一款基于 AI 的代码编辑器，集成了 GPT-4 的能力，旨在通过 AI 补全、代码生成、解释及重构等功能大幅提升开发效率。本笔记介绍了其安装方式、核心 AI 功能模块、常用快捷键配置以及 API Key 设置等关键操作，为开发者从传统编辑器过渡到 AI 驱动的编程环境提供了实用的入门参考。
tags: ["Cursor", "AI", "Editor", "IDE", "Productivity"]
aliases: ["Cursor编辑器", "AI代码助手", "GPT-4编辑器"]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:26 下午
date modified: 星期五, 六月 19日 2026, 11:58:29 中午
---

<!-- toc -->

## 1. 简介

**Cursor** 是一款基于 VS Code 开源版本构建的 **AI 优先 (AI-first)** 代码编辑器。它深度集成了大语言模型（如 GPT-4, Claude 3.5 等），能够理解整个项目的上下文，提供远超传统 IDE 的智能编码体验。

---

## 2. 核心 AI 功能

### 2.1. AI 代码补全与预测

- **实时补全**：在输入过程中自动预测下一行或整段代码。
- **上下文感知**：补全内容不仅基于当前文件，还能参考项目中的其他模块。

### 2.2. AI 代码生成 (Composer)

- **指令驱动**：通过自然语言描述（如“创建一个响应式的导航栏组件”），AI 会自动编写代码。
- **全量编辑**：支持一次性修改多个文件，非常适合快速构建原型。

### 2.3. AI 代码解释与重构

- **疑难解答**：选中一段复杂的旧代码，让 AI 解释其逻辑或发现潜在 Bug。
- **智能重构**：提供变量重命名、提取函数、优化循环结构等建议，提升代码质量。

---

## 3. 快捷键配置 (Default)

| 功能 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| **AI 补全/接受** | `Ctrl + Enter` | `Cmd + Enter` |
| **AI 侧边栏聊天** | `Ctrl + L` | `Cmd + L` |
| **行内 AI 编辑** | `Ctrl + K` | `Cmd + K` |
| **全量代码生成** | `Ctrl + I` | `Cmd + I` |
| **命令面板** | `Ctrl + Shift + P` | `Cmd + Shift + P` |

---

## 4. 配置与进阶

### 4.1. AI 模型设置

在设置面板中，用户可以根据需求选择不同的模型：

- **GPT-4 / GPT-4o**：逻辑推理能力强。
- **Claude 3.5 Sonnet**：代码编写风格更接近人类，目前备受推崇。

### 4.2. API 与隐私设置

- **API Key**：支持使用 Cursor 官方订阅或配置自己的 OpenAI/Anthropic API Key。
- **隐私模式**：开启后，代码不会被用于模型训练，适合企业级开发。

---

## 5. 参考资料

- [Cursor 官方网站](https://cursor.sh/)
- [Cursor 官方文档](https://cursor.sh/docs)
- [GitHub 仓库](https://github.com/getcursor/cursor)
