---
title: "Podman安装"
filename: podman-container-management-guide
summary: Podman是免守护进程且支持无根模式的容器管理工具。作为Docker的安全替代方案，它使用相同命令行参数，支持podman-compose管理多容器。本文涵盖Podman在Ubuntu上的安装、镜像源配置、安全存储参数调节及权限映射的最佳实践。
tags: [podman, containerization, rootless-containers]
aliases: [Podman安装, 容器管理, Docker替代方案]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:55 上午
date modified: 星期五, 六月 19日 2026, 12:07:29 中午
---

<!-- toc -->

## 1. 简介

一个类似 Docker 的容器管理工具

## 2. 安装

```shell
sudo apt update && sudo apt install podman && sudo apt install podman-compose && sudo apt install podman-docker
```

## 3. 配置

- 查询配置

```
# /etc/containers/registries.conf
unqualified-search = ["docker.io", "quay.io"] #配置查询地址
```

- 存储配置

| **字段** | **默认值示例** | **说明** |
| ----------- | -------------------------------------------- | ----------------------------------------- |
| `graphroot` | `/home/user/.local/share/containers/storage` | **主要数据存储目录**，包含镜像和容器的层数据。 |
| `runroot` | `/run/user/UID/containers` | **运行时数据目录**，用于存储运行时所需的文件，如锁和临时文件。通常不需要修改。 |

```
# /etc/containers/storage.conf
[storage]
# 将 graphroot 更改为您的新系统路径
driver = "overlay"
graphroot = "/data/podman/graph"
runroot = "/data/podman/run"
```

## 4. 使用

|**命令**|**作用**|
|---|---|
|`podman machine start`|启动 Podman 虚拟机。|
|`podman machine stop`|停止运行中的 Podman 虚拟机。|
|`podman machine ls`|列出所有已创建的 Podman 虚拟机。|
|`podman machine rm <name>`|删除指定的 Podman 虚拟机。|

| **Docker 命令** | **Podman 命令** | **作用** |
| --------------------------- | --------------------------- | --------------- |
| `docker run ...` | `podman run ...` | 创建并运行一个新容器。 |
| `docker ps -a` | `podman ps -a` | 列出所有运行中和已停止的容器。 |
| `docker start <ID>` | `podman start <ID>` | 启动一个已停止的容器。 |
| `docker stop <ID>` | `podman stop <ID>` | 优雅地停止一个运行中的容器。 |
| `docker rm <ID>` | `podman rm <ID>` | 移除一个已停止的容器。 |
| `docker exec -it <ID> bash` | `podman exec -it <ID> bash` | 在运行中的容器内执行命令。 |

## 5. podman.socket 管理

```bash
systemctl status podman.socket # root 用户
systemctl start podman.socket
systemctl restart podman.socket
systemctl stop podman.socket
systemctl enable podman.socket

systemctl --user status podman.socket # 普通用户

curl --unix-socket $XDG_RUNTIME_DIR/podman/podman.sock http://d/v4.0.0/libpod/info
curl --unix-socket /run/podman/podman.sock http://d/v4.0.0/libpod/info #测试
```

## 6. 拓展信息

### 6.1. 与 Docker 的区别

| 特性 | Docker | Podman |
| ------- | ------------------------------ | ---------------------------------- |
| **架构** | 客户端-服务器，有守护进程 | 无守护进程，直接作为进程运行 |
| **安全性** | 守护进程需要 root 权限，可能存在安全风险 | 无需 root 权限，更安全 |
| **命令** | `docker [command]` | `podman [command]`，与 Docker 几乎完全兼容 |
| **Pod** | 原生不支持，需要额外工具（如 Docker Compose） | 原生支持，可以直接管理 Pod |

> 镜像是互通的

### 6.2. podman.socket 与 Dockerd 的区别

简单来说，**`podman.socket` 只是一个“翻译官”，而 `dockerd` 是一个“大管家”。**

Podman 的设计初衷就是为了摆脱“大管家”模式。以下是为什么你应该启动 `podman.socket` 而不是寻找 `dockerd` 替代品的深层原因：

---

#### 6.2.1. 架构本质的区别：监听 Vs. 控制

- **`dockerd` (Daemon):** 它是一个持久运行的重量级进程。它负责下载镜像、管理网络、读写日志、监控容器状态。如果 `dockerd` 挂了，你的所有容器管理功能都会瘫痪。

- **`podman.socket` (Socket Activation):** 它平时几乎不占资源。它的唯一工作是 **监听请求**。当有外部工具（如 Docker Compose 或 IDE）通过 API 访问时，它才临时唤起一个 Podman 进程来处理任务。任务结束，Podman 进程随之消失。

#### 6.2.2. 安全性的降级与隔离

Podman 的核心卖点是 **Rootless (无根运行)**。

- 如果你试图寻找一个像 `dockerd` 那样的全局守护进程，你通常需要以 root 权限运行它。这会引入单点故障风险：一旦守护进程被攻破，攻击者就拿到了宿主机的最高权限。

- **`podman.socket`** 可以运行在 **用户级**（User Space）。每个普通用户都可以启动自己的 `podman.socket`，管理属于自己的容器，彼此互不干扰，且不需要任何特权。

#### 6.2.3. 符合 Unix 的“简单”哲学

Podman 遵循的是 **Fork/Exec 模型**，这和你的 Shell 运行命令是一样的：

- 当你运行 `podman run`，Podman 进程直接派生（Fork）出容器进程。

- 容器进程的父进程就是 Podman，这使得 Linux 内核的审计（Audit）系统能清晰地记录是谁启动了什么。

- **`podman.socket`** 只是为了兼容那些 **习惯了 C/S（客户端/服务器）架构** 的旧工具（如传统的 Docker API 调用者）而提供的“补丁”，它并不参与容器的生命周期管理。

#### 6.2.4. 总结对比

|**维度**|**dockerd 模式**|**podman.socket 模式**|
|---|---|---|
|**存在意义**|管理容器的核心大脑|仅作为兼容 Docker API 的接口|
|**进程关系**|容器是 `dockerd` 的子进程|容器是独立的，由 `conmon` 监控|
|**资源消耗**|始终常驻内存|仅在有 API 请求时响应|
|**系统集成**|必须通过 Docker 指令管理|可直接通过 `systemd` 像普通服务一样管理|

## 7. 参考资料

- [官方链接](https://podman.io/get-started)
