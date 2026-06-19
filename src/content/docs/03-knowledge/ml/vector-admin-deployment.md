---
title: "VectorAdmin安装"
filename: vector-admin-deployment
summary: Vector Admin 是由 Mintplex Labs 开发的开源向量数据库可视化管理工具，支持 Chroma 等多种主流向量数据库。本笔记详细整理了通过 Docker Compose 部署 Vector Admin 的配置方案，包括容器网络划分、端口映射以及挂载目录设置，为快速构建向量数据库管理后台提供直接参考。
tags:
  - vector-admin
  - chroma
  - docker
  - vector-database
aliases:
  - VectorAdmin安装
  - 向量数据库管理
status: completed
date created: 星期二, 二月 25日 2025, 3:23:56 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

**Vector Admin** 是一个开源的向量数据库管理平台，能够为 Chroma、Pinecone、Qdrant 等向量数据库提供开箱即用的可视化管理界面与文档处理流水线。

## 2. 安装

### 2.1. 使用 Docker Compose 部署

本节提供 Vector Admin 的 Docker 容器化部署配置。推荐通过挂载本地 `.env` 环境变量文件来进行自定义参数配置。

#### 2.1.1. Docker Compose 配置文件

创建并编辑 `docker-compose.yml` 文件：

```yaml
version: '3.1'

services:
  vector-admin:
    image: mintplexlabs/vectoradmin:latest
    container_name: vector-admin
    restart: always
    ports:
      - "8881:3001"   # 前端与后端主要 API 端口
      - "8885:3335"   # 内部微服务端口
      - "8882:8288"   # 文档处理器端口
    networks:
      - share
    volumes:
      - "./.env:/app/backend/.env"
      - "./data/storage:/app/backend/storage"
      - "./data/hotdir/:/app/document-processor/hotdir"
    env_file:
      - .env

networks:
  share:
    external:
      name: share
```

> [!important] 注意事项
>
> - 外部网络 `share` 必须提前使用 `docker network create share` 创建，以便与其他关联容器进行通信。
> - 在启动前，请确保当前目录下已经存在 `.env` 配置文件。

#### 2.1.2. 启动服务

在 `docker-compose.yml` 所在目录执行以下命令启动容器：

```shell
docker-compose up -d
```

## 3. 参考资料

- [Chroma 官方 Docker 部署文档](https://docs.trychroma.com/production/containers/docker)
- [Vector Admin GitHub 仓库](https://github.com/Mintplex-Labs/vector-admin)
