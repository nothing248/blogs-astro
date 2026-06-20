---
title: "Ollama教程"
filename: ollama-local-llm-deployment
description: Ollama是极简的本地大模型管理和运行框架。本文介绍通过单条命令在本地运行Llama、Qwen等模型的步骤。涵盖守护进程的默认端口监听机制、通过Modelfile定制模型系统提示词与温度参数的方法、以及与WebUI和本地其他开发环境对接的命令行参数。
tags: [ollama, local-llm, ai-infrastructure, modelfile]
aliases: [Ollama教程, 本地大模型, Modelfile配置]
status: completed
date created: 星期三, 五月 27日 2026, 12:02:30 中午
date modified: 星期五, 六月 19日 2026, 12:06:58 中午
---

<!-- toc -->

## 1. 简介

Ollama 是目前最火爆的本地大模型（LLM, Large Language Model）运行框架。它极大地简化了在本地部署、运行和管理开源大模型的流程，让你不需要复杂的显卡配置和环境调优，就能像使用 Docker 一样一条命令跑起 AI 团队。

---

## 2. 安装与核心概念

Ollama 支持 macOS、Linux 和 Windows。你可以直接去官网下载安装包。
安装完成后，Ollama 会在后台启动一个守护进程（Daemon），并默认监听 `127.0.0.1:11434` 端口。

> **核心逻辑**：Ollama 采用了类似 Docker 的架构。你需要先 `pull`（拉取）一个模型镜像，然后通过 `run`（运行）来启动它。

---

## 3. 基础命令详解

在终端（Terminal）或命令行中，你可以通过 `ollama` 命令与框架进行交互：

| 命令 | 功能描述 | 示例 |
| --- | --- | --- |
| **`ollama run`** | 下载并直接启动一个模型，进入交互式对话 | `ollama run deepseek-r1:8b` |
| **`ollama pull`** | 仅下载模型镜像到本地，不自动运行 | `ollama pull llama3` |
| **`ollama list`** | 列出当前本地已下载的所有模型 | `ollama list` |
| **`ollama rm`** | 删除本地的某个模型镜像 | `ollama rm qwen2.5:7b` |
| **`ollama show`** | 查看某个模型的详细信息（如架构、参数量、License 等） | `ollama show deepseek-r1:8b` |
| **`ollama ps`** | 查看当前正在内存/显存中运行的模型 | `ollama ps` |

---

## 4. 进阶：通过 Modelfile 自定义模型

类似于 Dockerfile，Ollama 允许你通过编写 `Modelfile` 来定制属于自己的模型。你可以基于官方模型修改 Prompt（提示词）、参数，甚至导入外部的 GGUF（GPT-Generated Unified Format）文件。

### 4.1. 编写一个 Modelfile 示例

在本地创建一个名为 `Modelfile` 的文件：

```dockerfile
# 1. 指定基础模型 (Base Model)
FROM deepseek-r1:8b

# 2. 调整模型参数 (Parameters)
PARAMETER temperature 0.3
PARAMETER num_ctx 8192

# 3. 注入系统提示词 (System Prompt)
SYSTEM """
你是一位精通 Python 的资深 IT 架构师。
你的回答必须严谨、清晰，代码需要符合 PEP 8 规范。
如果回答中包含缩写名词，必须在括号中同步给出全拼（Full Spelling）。
"""

```

### 4.2. 构建与运行

在 `Modelfile` 所在目录下执行以下命令进行构建：

```bash
ollama create my-python-coach -f ./Modelfile
```

构建完成后，直接运行你自定义的模型：

```bash
ollama run my-python-coach
```

---

## 5. 环境变量与高级配置

通过配置系统环境变量，可以解锁 Ollama 的更多高级能力：

* **`OLLAMA_HOST`**
* **作用**：更改绑定 IP 和端口。
* **详解**：默认是 `127.0.0.1:11434`（仅本地访问）。如果你想让局域网内的其他设备也能访问你的 Ollama 服务，可以将其设置为 `0.0.0.0:11434`。

* **`OLLAMA_MODELS`**
* **作用**：更改模型文件的存储路径。
* **详解**：大模型非常吃硬盘空间。默认情况下，Windows 会存放在 `C:\Users\<username>\.ollama\models`。你可以将其修改到大容量的固态硬盘（SSD, Solid State Drive）分区。

* **`OLLAMA_NUM_PARALLEL`**
* **作用**：处理并发请求的数量（默认值为 1）。如果你有高并发的 API 调用需求，可以适当调大。

---

## 6. API 接入与生态融合

Ollama 原生提供了两套 HTTP（HyperText Transfer Protocol） API 接口，极大地方便了开发者进行二次开发。

### 6.1. 原生 API 接口

* **生成补全 (Generate)**：`POST /api/generate`
* **聊天对话 (Chat)**：`POST /api/chat`

**cURL 调用示例：**

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "deepseek-r1:8b",
  "messages": [
    { "role": "user", "content": "什么是 API？" }
  ],
  "stream": false
}'

```

### 6.2. OpenAI 兼容接口

Ollama 内置了对 OpenAI API 格式的兼容。这意味着在各种开源 WebUI、LangChain 或 LangGraph 项目中，你只需要将 `BASE_URL` 改为 `http://localhost:11434/v1`，并将 `API_KEY` 随便填一个字符串（如 `ollama`），就能无缝替换原本的 OpenAI 服务。

---

## 7. 参考资料

* [官方文档](https://ollama.com/)
