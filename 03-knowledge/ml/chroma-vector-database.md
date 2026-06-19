---
title: "Chroma向量数据库"
filename: chroma-vector-database
summary: Chroma 是一款开源的轻量级向量数据库，广泛应用于大模型检索增强生成（RAG）体系中。本笔记提供了通过 Docker Compose 部署 Chroma 并启用 Token 安全验证的配置方案，整合了 Python SDK 下进行连接鉴权、集合操作、向量及文档数据入库以及相似度检索的核心代码，为本地开发提供参考。
tags:
  - chroma
  - vector-database
  - docker-compose
  - python-sdk
aliases:
  - Chroma向量数据库
  - Chroma部署与使用
status: completed
date created: 星期二, 二月 25日 2025, 3:24:16 下午
date modified: 星期二, 六月 16日 2026, 6:24:26 晚上
---

<!-- toc -->

## 1. 简介

**Chroma** 是一个专门针对大语言模型（LLM）应用设计的开源、轻量级嵌入向量数据库。它支持快速存储文档、元数据以及向量嵌入（Embeddings），并提供高效的近邻语义检索服务，是搭建 RAG 系统的核心基础组件。

---

## 2. 使用 Docker Compose 部署

下面提供了一个带有 **Token 令牌认证** 安全机制的 Docker 部署配置方案。

### 2.1. A. 配置文件 `docker-compose.yml`

```yaml
version: '3.1'

services:
  chroma:
    image: chromadb/chroma:latest
    container_name: chroma
    restart: always
    ports:
      - "8889:8000"
    networks:
      - share
    environment:
      # 启用基于 Token 的身份验证
      CHROMA_SERVER_AUTHN_CREDENTIALS: "your_auth_token_here"
      CHROMA_SERVER_AUTHN_PROVIDER: "chromadb.auth.token_authn.TokenAuthenticationServerProvider"
      CHROMA_AUTH_TOKEN_TRANSPORT_HEADER: "X-Chroma-Token"
    volumes:
      - './data:/chroma/chroma'

networks:
  share:
    external:
      name: share
```

> [!important] 安全提示
>
> - 生产环境中请务必将 `CHROMA_SERVER_AUTHN_CREDENTIALS` 替换为高强度的自定义密钥。
> - 外部网络 `share` 须提前通过 `docker network create share` 创建。

### 2.2. B. 启动容器

```shell
docker-compose up -d
```

---

## 3. Python SDK 基础使用

### 3.1. A. 安装官方客户端

```shell
pip install chromadb
```

### 3.2. B. 数据库操作与相似度查询

```python
import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

# 1. 载入环境变量（如果将 Token 写入了本地 env 文件）
load_dotenv('/path/to/your/.chroma_env')

# 2. 实例化 HTTP 客户端，并进行 Token 安全校验
client = chromadb.HttpClient(
    host="localhost",
    port=8889,
    settings=Settings(
        chroma_auth_token_transport_header="X-Chroma-Token",
        chroma_client_auth_credentials="your_auth_token_here",
        chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
    )
)

# 3. 检查服务健康状态
client.heartbeat()

# 4. 创建或获取数据集集合 (Collection)
collection = client.create_collection("my_collection")

# 5. 添加文档、对应向量和元数据
collection.add(
    documents=["This is document1", "This is document2"],
    metadatas=[{"source": "notion"}, {"source": "google-docs"}],  # 用于后续过滤
    ids=["doc1", "doc2"],  # 必须全局唯一
    embeddings=[[1.2, 2.1], [1.2, 2.1]]  # 对应的嵌入维度向量
)
  
# 6. 进行语义相似度查询
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where ={"source": "notion"},             # 可选：按元数据属性过滤
    # where_document ={"$contains ": " document "} # 可选：按文档文本内容过滤
)

print(results)
```

---

## 4. 参考资料

- [Chroma 官方 Docker 部署指南](https://docs.trychroma.com/production/containers/docker)
