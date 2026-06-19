---
status: completed
filename: backend-infrastructure-and-communications-overview
title: "后端基础知识"
summary: 本笔记系统回顾了后端开发的核心通信机制与安全架构。涵盖了实时消息通知的四种模式（轮询、长轮询、WebSocket、SSE）及其优劣对比，详述了基于 JWT 与 API 验签的接口安全设计。重点探讨了经典的 C10K 高并发瓶颈问题，并梳理了从容器化编排 (K8s)、分布式追踪到身份管理 (IAM) 的完整后端技术栈全景图。
aliases: [后端基础知识, 通信协议对比, 接口安全规范, C10K 问题]
tags: [后端开发, 高并发, C10K, WebSocket, SSE, 接口安全, 分布式系统, 技术栈, 软件架构]
date created: 星期一, 十二月 1日 2025, 9:59:23 上午
date modified: 星期四, 六月 18日 2026, 9:15:00 晚上
---

<!-- toc -->

## 1. 实时通信与消息通知模式

| 模式 | 机制 | 优点 | 缺点 |
| :--- | :--- | :--- | :--- |
| **短轮询** | 客户端定时发送 HTTP 请求。 | 实现简单。 | 浪费带宽，实时性差。 |
| **长轮询** | 服务端阻塞请求直到有数据。 | 比短轮询实时。 | 仍然频繁建立 HTTP 链接。 |
| **WebSocket** | 全双工 TCP 协议连接。 | 极致实时，开销小。 | 需协议升级，维护连接成本高。 |
| **SSE (Server-Sent)** | 基于 HTTP 的单向流。 | 原生 HTTP 支持，自动重连。 | 仅支持服务端向客户端单向推送。 |

## 2. 接口安全与鉴权体系

- **JWT (JSON Web Token)**：无状态鉴权，适合分布式集群。
- **API 验签 (Signing)**：针对高敏感操作，通过摘要算法保证请求未被篡改，并防止重放攻击。
- **Token 刷新机制**：解决有效期与安全性之间的权衡。

---

## 3. 高并发瓶颈：C10K 问题

**C10K 问题** 是指单台服务器如何同时处理 10,000 个以上的并发连接。核心挑战在于操作系统内核的上下文切换开销与内存管理。

> [!tip] 现代解法
> 采用 **IO 多路复用 (epoll)**、协程 (Goroutines/Asyncio) 及事件驱动架构（如 Nginx/Node.js）。

---

## 4. 后端工业级技术栈全景

1. **流量入口**：API 网关 (Kong/APISIX)、CDN。
2. **运行环境**：Docker 容器化、K8s 编排。
3. **数据平面**：数据库优化、分布式缓存 (Redis)、消息队列 (Kafka)。
4. **运维保障**：日志收集 (ELK)、监控 (Prometheus)、分布式链路追踪 (Zipkin)。
5. **身份治理**：IAM (Identity and Access Management)。

## 5. 参考资料

- [SSE 技术实现深度参考](https://www.cnblogs.com/jesn/p/16267606.html)
