---
title: "LangChain入门"
filename: langchain-llm-orchestration
summary: LangChain是面向大语言模型（LLM）的编排框架与应用开发工具包。本文阐述了其作为“胶水”层的定位，深入浅出地讲解了Chat models、Prompt、Vector store等基础模块，解析了以LangChain Expression Language (LCEL) 构建声明式链的运行机制与优势。
tags: [langchain, llm-framework, lcel, ai-agents]
aliases: [LangChain入门, LCEL表达式, 大模型开发]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 星期五, 六月 19日 2026, 12:06:10 中午
---

<!-- toc -->

## 1. 简介

它不是一个大模型本身，而是一个将大模型能力与外部数据和计算逻辑连接起来的 **“胶水”层** 或**“编排工具”。

## 2. 概念

模块 -> 链 -> 代理(Agents)

### 2.1. 模型

- Chat models
- Message
  - system
  - human
  - ai
  - tool_use
  - tool
- Propmt
- Document
  - Loader
  - embeding
- Vector store
  - Retriever
- Struct output
- few-shot examples

### 2.2. LCEL

LangChain 表达式语言（LCEL）是 LangChain 框架中用于 **组合链 (Chains)** 的一种声明式、统一的编程范式。它是构建复杂、可部署和生产就绪的 LLM 应用程序的核心。目标是提供一种简洁、强大且灵活的方式来定义 LLM 应用中的所有逻辑流，包括数据处理、模型调用、内存管理和外部工具集成。

- 管道操作符 `|` 上下文中必须实现的是 Runable 对象(存在自动转化机制，例如：自动将 dict 转化为我 RunnaleMap)
- 前一个输出对应后一个的输入
- 调用的具体的方法以 chains 链 调用时的方法为准
- langserve 底层调用的都是异步格式

## 3. 对象

### 3.1. 核心

- ### Runabble

 with_types
 with_config：允许您为特定的 `Runnable` 组件或整个 Chain **临时设置或覆盖** 运行时配置参数。
 with_fallbacks：为当前的 `Runnable` 组件添加一个或多个 **备用/回退** 的 `Runnable`。如果主组件执行失败（抛出异常），执行器将尝试按顺序运行回退组件。
 with_listeners、
 with_alisteners、
 with_retry

- RunnableMap

 1、`RunnableMap` 是 LangChain 表达式语言 (LCEL) 中的一个核心组件，它允许您 **并行** 地处理输入，并将多个不同的 LangChain `Runnable` 结构组合起来，形成一个新的输出字典。、
 2、然而，在 LangChain 表达式语言 (LCEL) 的上下文中，当这个字典被用于管道操作符 `|` 中时，LangChain 框架会自动将其 **提升 (Promote)** 或 **转换** 为一个特殊的 `Runnable` 对象：**`RunnableMap`**

- RunnablePassthrough

 1、`RunnablePassthrough` 是 LangChain 表达式语言 (LCEL) 中最基础但也最灵活的组件之一。它的设计理念非常简单：**让输入数据原封不动地通过（Pass Through）**，同时提供强大的机制来 **增强** 这个流动的数据
 2、`.assign()` 是 `RunnablePassthrough` 最实用且强大的功能。它允许您在数据流经管道时，**在不改变原始输入的前提下**，向数据上下文中添加额外的键值对

- RunnableLambda

 1、将任何 Python 函数转换为一个 `Runnable` 组件，方便集成自定义预处理或后处理逻辑。
 2、当您在管道操作符 `|` 的上下文中使用一个普通的 Python 函数（无论是 `def` 定义的函数还是 `lambda` 表达式）时，LangChain 运行时会自动将其包装成一个 `Runnable` 对象：**`RunnableLambda`**

- RunnableWithMessageHistory

 1、专门用于 **集成会话记忆（Conversation Memory** 的包装器它的核心作用是将任何现有的 LCEL Chain（一个 `Runnable` 对象）转换为一个具有 **持久化聊天历史** 能力的 Chain，从而实现多轮对话功能

- RunnableSerializable

 1、`RunnableSerializable` 是 LangChain 表达式语言 (LCEL) 中 **`Runnable` 接口的一个特殊子类**，它引入了 **序列化（Serialization）** 的能力。简而言之，它确保任何实现了此接口的组件不仅可以执行 (`invoke`)，还可以被可靠地 **保存（Save）和加载（Load）**。

### 3.2. Agent

- AgentExecutor

 LangChain 框架中用于执行 **Agent（智能体）** 逻辑的核心组件。它将一个语言模型（LLM）与一组工具（Tools）结合起来，使 LLM 能够进行推理，决定下一步要采取的行动，并重复这个过程直到任务完成

- format_scratchpad

 `format_scratchpad`（或相关的格式化函数）是 LangChain Agent 架构中的一个关键概念，它主要用于 **将 Agent 在当前步骤中积累的中间步骤信息格式化成 LLM 可读的文本**，并将其注入到 Agent 的 Prompt 中。

### 3.3. Utils

- langchain_core.utils.function_calling

### 3.4. 配置

- `configurable_fields` 旨在允许您 **细粒度地、动态地修改** `Runnable` 组件实例的 **内部属性或字段**。
- `configurable_alternatives` 旨在允许您在运行时 **完全切换** 正在使用的 `Runnable` **实例**，从一个预定义的选项集合中选择一个。

## 4. 任务类型

- [子查询](https://python.langchain.com/docs/how_to/parent_document_retriever/)：实现基于自然语言查询向量数据库
- [分类](https://python.langchain.com/docs/tutorials/classification/)
- [提取](https://python.langchain.com/docs/tutorials/extraction/)

## 5. Demo

```shell
pip install langchain
pip install -U langchain-google-genai
pip install langchain-community pypdf
```

## 6. 拓展信息

### 6.1. 最大边际相关性（Maximal Marginal Relevance，简称 **MMR**)

是 LangChain 中一种非常重要的 **文档检索（Retrieval）策略。它旨在解决传统基于向量相似度检索的固有缺陷：检索结果可能高度雷同**。

简单来说，MMR 是一种在保持结果对查询 **相关性** 的同时，最大限度提高结果之间 **多样性** 的机制

### 6.2. [tool_example_to_messages](https://python.langchain.com/api_reference/core/utils/langchain_core.utils.function_calling.tool_example_to_messages.html)

## 7. 参考资料

- [文档](https://python.langchain.com/docs/tutorials/retrievers/)
- [官方文档](https://docs.langchain.com/langsmith/observability)
- [git](https://github.com/langchain-ai/langchain)
