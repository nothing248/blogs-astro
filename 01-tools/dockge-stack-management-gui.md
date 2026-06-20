---
title: "Dockge安装教程"
filename: dockge-stack-management-gui
description: Dockge 是一款基于 Web 界面的 Docker Compose 栈管理工具，以极简和易用著称。本笔记介绍了 Dockge 的安装部署流程（支持 Podman 环境），重点强调了宿主机与容器内 Stacks 路径一致性的核心配置要求。此外，还对比了 `dockerd` 守护进程与 `podman.socket` 在资源占用与激活机制上的差异，为用户提供了高效、直观的多容器应用管理方案。
tags: ["Dockge", "Docker-Compose", "GUI", "Podman", "Self-Hosted"]
aliases: ["Dockge安装教程", "Docker面板", "Compose栈管理"]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 11:58:47 中午
---

<!-- toc -->

## 1. 简介

**Dockge** 是一款响应迅速、界面现代化的 **Docker Compose 管理器**。它允许用户通过 Web 界面创建、编辑和管理 Compose 栈，特别适合那些喜欢 Compose YAML 格式但又希望拥有可视化操作体验的开发者。

---

## 2. 安装部署

### 2.1. 针对 Podman 环境的准备

Dockge 支持通过 `podman.socket` 与 Podman 进行通信。

```bash
# 启用 Podman 套接字服务
systemctl enable --now podman.socket

# 测试连接
curl --unix-socket /run/podman/podman.sock http://d/v4.0.0/libpod/info
```

### 2.2. 使用 Docker Compose 部署 Dockge

```yaml
services:
  dockge:
    image: louislam/dockge:latest
    ports:
      - 5001:5001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock # 或 podman.sock
      - ./data:/app/data
      # ⚠️ 关键：左右路径必须保持绝对路径一致
      - /data/stacks:/data/stacks 
    environment:
      - DOCKGE_STACKS_DIR=/data/stacks
    restart: unless-stopped
```

---

## 3. 核心机制详解

### 3.1. 路径一致性 (Path Mapping)

Dockge 的一个核心要求是：你挂载给容器的 `STACKS_DIR`（存放 YAML 的目录），在容器内部的挂载路径必须 **等同于** 宿主机的绝对路径。这是为了确保 Dockge 生成的相对路径引用在两者之间保持一致。

### 3.2. Dockerd 与 Podman.socket 差异

- **`dockerd` (Daemon)**：持久运行的重量级进程，负责镜像管理、容器调度等全生命周期。若其崩溃，所有容器管理功能将失效。
- **`podman.socket`**：轻量级的监听机制。仅在收到 API 请求时才临时唤起 Podman 进程，任务结束即释放，资源占用更低。

---

## 4. 参考资料

- [Dockge GitHub 仓库](https://github.com/louislam/dockge)
- [Dockge 官方部署文档](https://dockge.kuma.pet/)
