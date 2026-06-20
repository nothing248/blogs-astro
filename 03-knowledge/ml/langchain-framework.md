---
title: "LangChain框架介绍"
filename: langchain-framework
description: LangChain 是一个以大语言模型为核心的开源开发框架，支持 Python 和 TypeScript。本笔记梳理了其六大核心组件（Models、Prompts、Indexes、Memory、Chains、Agents），更新了生态组件 LangSmith 调试监控平台的最新定位，并保留了官方调试指南与社区分析文章链接。
tags:
  - langchain
  - LLM
  - ai-agent
  - python
aliases:
  - LangChain框架介绍
  - LLM开发组件
status: completed
date created: 星期六, 十月 18日 2025, 10:30:13 上午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

**LangChain** 是一个围绕大语言模型（LLM）构建的开源应用开发框架，旨在简化将大模型与外部数据源、计算服务以及工具链相结合的复杂开发过程。目前主要提供 Python 和 JavaScript/TypeScript 两个版本的 SDK。

---

## 2. 六大核心组件

LangChain 将复杂的 LLM 应用拆解为以下六个标准化模块：

1. **Models (模型接口)**：
   - 封装了不同模型提供商（如 OpenAI、Anthropic、Hugging Face 等）的 API，提供统一的调用标准（如 ChatModels 和 LLMs）。
2. **Prompts (提示词管理)**：
   - 提供 PromptTemplate（提示词模板）的创建、序列化、动态参数解析和格式化功能。
3. **Indexes (索引与数据连接)**：
   - 处理外部结构化与非结构化数据的加载、文本切片（Document Loaders, Text Splitters）以及结合向量数据库的语义检索（Vectorstores, Retrievers）。
4. **Memory (记忆/上下文管理)**：
   - 用于在多轮对话中保存和管理历史聊天记录（如 ConversationBufferMemory），克服 LLM 本身无状态的限制。
5. **Chains (调用链)**：
   - 将多个模型接口、提示词模板或者其他组件以流水线（Pipeline）形式进行链式组合，支持复杂的业务逻辑流转。
6. **Agents (智能体)**：
   - 让 LLM 扮演决策核心，根据用户输入动态选择并调用外部工具（Tools），自适应地完成多步骤任务。

---

## 3. 生态体系扩展

### 3.1. LangSmith

**LangSmith** 是 LangChain 官方推出的开发者平台，用于对 LLM 应用进行调试、测试、评估和运行监控。

> [!note] 现状更新
> 相比于早期（2023-2024 年）的内测状态，当前 LangSmith 已经正式面向全球开发者开放。它能够全量追踪 Chain 和 Agent 的每一次调用细节、API 耗时及 Token 消耗，是 LLM 应用走向生产环境（Production）的必备调试监控利器。

---

## 4. 参考资料

- [LangChain 官方调试与排错指南](https://python.langchain.com/docs/guides/debugging)
- [LangChain 官方 GitHub 仓库](https://github.com/langchain-ai/langchain)
- [深入浅出 LangChain 原理解析 (知乎)](https://zhuanlan.zhihu.com/p/651151321)
