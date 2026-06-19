---
title: "K8s"
filename: kubernetes-essentials
summary: Kubernetes (K8s) 是一个开源的容器编排平台，旨在解决大规模容器部署中的高可用性、负载均衡、自动伸缩和服务发现等问题。本笔记涵盖了 K8s 的核心概念（控制面板、节点、对象）以及与 Docker Swarm 的对比分析。
tags: [Kubernetes, K8s, DevOps, Container-Orchestration]
aliases: [K8s]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:28 上午
date modified: 星期五, 六月 19日 2026, 12:06:07 中午
---

<!-- toc -->

## 1. 简介

Kubernetes（简称 K8s）是一个用于自动化部署、扩展和管理容器化应用程序的开源系统。

## 2. 核心价值与定位

### 2.1. 面临的挑战

- **高可用性**：容器或宿主机宕机时的自动恢复。
- **负载均衡**：流量在多个容器实例间的智能分配。
- **自动伸缩**：根据实时负载自动增减容器数量。
- **服务发现**：动态 IP 环境下的服务定位。

### 2.2. 解决方案

- **Pod 管理**：最小部署单元，负责容器生命周期。
- **集群调度**：将虚拟机或物理机抽象为资源池进行统一调度。
- **声明式配置**：通过 API 对象（如 Service）实现稳定的网络入口和自动化管理。

## 3. 系统架构

### 3.1. 控制面板 (Control Plane)

- `kube-apiserver`：集群控制的入口。
- `kube-scheduler`：负责 Pod 的调度。
- `kube-controller-manager`：维持集群状态的控制器。
- `etcd`：保存集群所有数据的键值数据库。

### 3.2. 节点组件 (Node)

- **容器运行时**：如 Docker, containerd。
- `kubelet`：确保容器在 Pod 中运行。
- `kube-proxy`：维护网络规则，实现服务发现。

## 4. K8s Vs Docker Swarm

| 特性 | Kubernetes | Docker Swarm |
| :--- | :--- | :--- |
| **设计理念** | 复杂、强大、声明式 | 简单、集成、命令式 |
| **功能** | 功能全面，适用于复杂场景 | 功能精简，适用于基础场景 |
| **学习曲线** | 陡峭 | 平缓 |
| **社区支持** | 庞大，业界标准 | 较小 |
| **使用场景** | 复杂微服务、大型企业级应用 | 小型项目、快速原型开发 |

## 5. 参考资料

- [Red Hat - 什么是 Kubernetes？](https://www.redhat.com/zh/topics/containers/what-is-kubernetes)
