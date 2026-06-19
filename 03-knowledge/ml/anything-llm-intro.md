---
title: "AnythingLLM简介"
filename: anything-llm-intro
summary: AnythingLLM 是一款全栈开源的多用户 AI 知识库与 RAG 平台，支持无缝对接各大云端与本地大语言模型及向量数据库。本笔记总结了 AnythingLLM 的核心系统定位（支持多模型接入与多向量库），阐述了其基于工作区的文档管理与精细的权限划分机制，并提供了官方参考链接，为构建私有化企业级 RAG 提供基础说明。
tags:
  - anythingllm
  - rag
  - LLM
  - local-knowledge-base
aliases:
  - AnythingLLM简介
  - 全栈知识库工具
status: completed
date created: 星期二, 二月 25日 2025, 3:23:59 下午
date modified: 星期二, 六月 16日 2026, 6:24:26 晚上
---

<!-- toc -->

## 1. 简介

**AnythingLLM** 是一款开源、全栈且功能强大的企业级局部知识库（RAG）应用程序。它能够让用户在保障隐私安全的前提下，将任何非结构化文档（PDF、TXT、DOCX 等）导入并构建知识库，再通过灵活挂接各类云端大模型（如 OpenAI）或本地大模型（如 Ollama）进行智能对话。

---

## 2. 核心特性

- **多模型无缝对接**：支持接入闭源大模型 API（OpenAI, Claude, Gemini），同时也完美支持本地开源模型调用生态（Ollama, Llama.cpp, LM Studio 等）。
- **多样化向量数据库支持**：
  - 内置了轻量级向量存储引擎 LanceDB，开箱即用。
  - 支持连接外部企业级向量数据库，如 Chroma、Pinecone、Qdrant、Milvus 和 Weaviate。
- **基于工作区（Workspaces）管理**：
  - 用户可以创建多个独立的工作区。
  - 每个工作区拥有独立的文档库、提示词（Prompts）系统、向量空间，实现了不同业务线之间的物理数据隔离。
- **内置文档提取器（Document Parser）**：
  - 支持将网页链接、YouTube 视频字幕、本地多样化格式文档自动解析、切片（Chunking）并完成向量化（Embedding）入库。
- **多用户与精细化权限**：
  - 支持多账号体系，提供管理员（Admin）、经理（Manager）、普通用户（User）等多种角色的访问和编辑控制。

---

## 3. 参考资料

- [AnythingLLM 官方网站](https://anythingllm.com/)
- [AnythingLLM 官方文档](https://docs.anythingllm.com/)
