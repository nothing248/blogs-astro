---
status: completed
filename: gcp-eventarc-serverless-event-routing
title: "Eventarc"
description: 本笔记介绍了 Google Cloud Eventarc 这一无服务器 (Serverless) 事件路由与集成平台。详细解析了其底层基于 CloudEvents 标准协议及 Cloud Pub/Sub 实现高可靠异步传输的工作原理。梳理了 Eventarc 将 GCP 原生服务事件及外部审计日志统一路由至目标计算资源（如 Cloud Run, Cloud Functions v2, Workflows 及 GKE）的触发器 (Trigger) 机制，是构建事件驱动架构 (EDA) 的核心组件。
aliases: [Eventarc, GCP 事件总线, CloudEvents, 事件驱动架构]
tags: [GCP, Eventarc, Serverless, 云原生, 事件驱动, 架构设计, Pub/Sub, Cloud Run]
date created: 星期三, 十二月 10日 2025, 6:20:42 晚上
date modified: 星期四, 六月 18日 2026, 11:35:00 晚上
---

<!-- toc -->

## 1. 核心概念与工作原理

**Eventarc** 是 Google Cloud 提供的事件总线服务，旨在轻松构建 **事件驱动架构 (Event-Driven Architecture, EDA)**。它能够统一接收、过滤并路由来自各方的系统事件。

### 1.1. 事件源 (Event Sources)

- **GCP 第一方服务**：原生支持绝大多数云产品（如 Cloud Storage 文件上传、BigQuery 任务完成、Firestore 数据变更）。
- **外部或第三方系统**：通过 Cloud Audit Logs (审计日志) 或直连 Pub/Sub 主题接收自定义事件。

### 1.2. 标准化事件格式：CloudEvents

Eventarc 在接收到各类异构事件后，会将其统一封装为开源中立的 **CloudEvents** 标准格式。

- **架构优势**：极大降低了开发者的心智负担，不论事件来源何处，目标服务只需解析一套固定结构的数据契约。

### 1.3. 底层传输机制：Pub/Sub

Eventarc 的高可靠性得益于其底层自动挂载了 **Cloud Pub/Sub** 消息队列。

- 当事件发生时，Eventarc 确保其发布至 Pub/Sub 主题。
- Eventarc 触发器 (Trigger) 本质上是管理着该主题的订阅 (Subscription)，负责稳定地将事件推送至目标。

---

## 2. 触发器 (Triggers) 与目标服务 (Destinations)

Eventarc 的核心操作单元是 **触发器 (Trigger)**，用于定义路由规则：`监听源 -> 过滤条件 -> 目标执行者`。

### 2.1. 过滤规则 (Filters)

支持精细的事件拦截。例如：仅监听特定存储桶 (`bucket = my-data-bucket`) 中特定类型（`google.cloud.storage.object.v1.finalized`）的事件。

### 2.2. 目标服务支持列表

Eventarc 主要将事件以 HTTP POST 请求的方式主动推送（Push）给计算资源：

1. **Cloud Run**：最主流的目标。将事件负载推送至容器化 Web 服务的 URL。
2. **Cloud Functions (第 2 代)**：Eventarc 是触发 Gen 2 函数的标准官方机制。
3. **GKE (Google Kubernetes Engine)**：可直接路由至 K8s 集群内部的服务。
4. **Workflows**：将事件作为输入参数，启动无服务器工作流编排以应对复杂的串行/并行控制。

---

## 3. 核心架构优势

- **完全无服务器 (Serverless)**：无需部署消息代理或中间件，按调用计费，极致伸缩。
- **零丢失保证**：借力 Pub/Sub，实现“至少一次”交付与失败自动重试机制。
