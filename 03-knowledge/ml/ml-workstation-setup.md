---
title: "机器学习工作站配置"
filename: ml-workstation-setup
summary: 本笔记记录了在戴尔 Precision 3660（RTX 3090）上搭建 ML 工作站的实操方案。由于 ACPI 电源及 Nvidia 驱动 IRQ 冲突等兼容性问题放弃了 CentOS 7.9，转而采用 Ubuntu 部署。详细列出了 Ubuntu 下配置 VNC、frp 内网穿透以及搭建 Miniconda、JupyterHub、Docker 和 Spark 等开发环境的软件技术栈。
tags:
  - machine-learning
  - workstation
  - ubuntu
  - nvidia-driver
  - docker
aliases:
  - 机器学习工作站配置
  - 双系统GPU环境搭建
status: completed
date created: 星期一, 五月 19日 2025, 2:05:17 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

本笔记详细记录了一台用于深度学习和大数据处理的 **ML 工作站（Dell Precision 3660 品牌机）** 的硬件配置以及 Windows + Linux 双系统环境搭建过程，并对安装过程中遇到的系统兼容性问题及解决方案进行了总结。

---

## 2. 硬件配置

- **机型**：Dell Precision 3660 品牌塔式工作站
- **显卡**：NVIDIA GeForce RTX 3090 (24GB VRAM)
- **存储**：1TB NVMe SSD（系统盘与热数据） + 4TB HDD（冷数据与备份）
- **CPU/内存**：16 核（16C） Intel 处理器 + 64GB DDR5 RAM

---

## 3. 双系统安装实操

### 3.1. Windows 系统安装

- 采用出厂预装的 Windows 11 专业版，预留未分配的磁盘空间给 Linux 分区。

### 3.2. Linux 系统安装排坑

#### 3.2.1. 方案一：CentOS 7.9 (不推荐)

在尝试在此硬件平台上安装 CentOS 7.9 时，遇到了严重的硬件兼容性问题：

> [!danger] 兼容性警告
>
> 1. **ACPI 电源管理问题**：系统关机、重启指令失效。
>    - *临时解决方案*：在 GRUB 引导项中添加 `reboot=p` 或 `acpi=force` 参数可部分缓解。
> 2. **NVIDIA 显卡驱动安装失败**：强行安装 NVIDIA 官方驱动时报错：
>    `No IRQ to the card! Can't install driver...`
>    - *结论*：此显卡驱动 IRQ 中断分配问题在旧内核（CentOS 7.9 的 3.10 内核）下 **无法解决**。

#### 3.2.2. 方案二：Ubuntu 22.04 LTS (推荐)

由于 CentOS 内核过旧，最终决定转向现代的 Ubuntu 操作系统，硬件支持良好，显卡驱动正常安装。

1. **系统安装**：
   - 制作 USB 启动盘，划分磁盘分区进行安装。
2. **安全与备份**：
   - 启用 Timeshift 等系统级冷备份工具。
3. **远程接入服务**：
   - 配置 VNC (TigerVNC/x11vnc) 远程桌面服务。
   - 配置 SSH 密钥登录并禁用密码登录。

---

## 4. 软件安装与 ML 开发环境配置

Ubuntu 系统安装完毕后，部署以下开发工具链：

### 4.1. 网络与运维

- **frp 内网穿透**：配置 `frpc` 客户端，将工作站的 SSH（22）和 JupyterHub（8000）端口穿透映射至具有公网 IP 的云服务器上，实现外网远程访问。
- **1Panel 面板**：开源的 Linux 运维管理面板，用于简化容器与资源监控。

### 4.2. 容器环境

- **Docker & NVIDIA Container Toolkit**：
  - 安装 Docker Engine。
  - 安装 NVIDIA Container Toolkit，使 Docker 容器内可以直接调用物理 GPU 进行深度学习训练。

### 4.3. Python 编程与多用户环境

- **Miniconda**：安装轻量级 Python 环境管理器。
- **JupyterHub**：配置多用户 Jupyter Notebook 集中式管理服务，支持按组划分工作站的 CPU 和 GPU 算力。

### 4.4. 大数据与计算组件

- **JDK**：安装 OpenJDK 8/11。
- **Apache Spark**：部署本地单机版或伪分布式 Spark 计算引擎，以便进行大规模特征工程处理。
