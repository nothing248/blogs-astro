---
title: "Ollama使用教程"
filename: ollama-deployment-guide
description: Ollama 是一款开源的本地大语言模型部署工具，支持在 macOS、Windows 和 Linux 上快速启动 Llama、Qwen 等模型。本笔记整理了 Ollama 的核心功能特点，补充了常用模型拉取、运行的 CLI 命令行操作及核心环境变量配置，并提供了官方模型搜索库链接，以便于开发者本地调试模型。
tags:
  - ollama
  - LLM
  - local-deployment
  - devops
aliases:
  - Ollama使用教程
  - 本地运行大模型
status: completed
date created: 星期二, 二月 25日 2025, 3:24:16 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

**Ollama** 是一个开源的、跨平台的本地大语言模型（LLM）轻量级部署框架。它能够帮助开发者在 macOS、Linux 和 Windows 系统上以极简的方式下载、运行和管理大模型（如 Llama 3、Qwen 2、Gemma 等），并自动提供与 OpenAI 兼容的本地 API 接口。

---

## 2. 常用 CLI 命令

在终端安装完 Ollama 后，可以使用以下命令行进行日常操作：

```shell
# 1. 运行并进入一个模型（若本地不存在，会自动从官网镜像源拉取）
ollama run qwen2

# 2. 仅拉取模型到本地而不直接运行
ollama pull llama3

# 3. 列出当前本地已下载的所有模型
ollama list

# 4. 删除指定的本地模型
ollama rm gemma

# 5. 查看正在运行的模型
ollama ps
```

---

## 3. 进阶配置与环境变量

可以通过配置系统环境变量来自定义 Ollama 的行为：

- **`OLLAMA_HOST`**：指定 API 监听地址和端口，默认为 `127.0.0.1:11434`。如果需要允许外网或局域网访问，可配置为 `0.0.0.0:11434`。
- **`OLLAMA_MODELS`**：配置大模型文件的本地存储路径（默认在当前用户的隐藏文件夹下，常因 C 盘空间不足需要迁移到其他盘符）。

---

## 4. 参考资料

- [Ollama 官方网站](https://ollama.com/)
- [Ollama 官方模型库（支持检索和查看模型参数大小及所需显存）](https://ollama.com/library)
