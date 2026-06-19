---
status: completed
filename: api-gateway-architecture-functions-and-patterns
title: "API Gateway"
summary: 本笔记系统梳理了 API 网关在微服务体系中的核心职责与设计模式。涵盖了身份验证与安全策略（Auth）、动态负载均衡、断路器熔断机制、协议转换（如 HTTP/JSON 到 gRPC/Protobuf）及服务发现。同时，探讨了网关在全链路监控、计费审计、流量限流及分布式缓存方面的关键作用，旨在构建高性能、高可用的系统统一入口。
aliases: [API Gateway, 系统入口设计, 流量网关职责]
tags: [后端开发, API 网关, 微服务架构, 服务发现, 负载均衡, 系统安全, 后端工程, 架构设计]
date created: 星期二, 二月 25日 2025, 3:23:34 下午
date modified: 星期四, 六月 18日 2026, 9:15:00 晚上
---

<!-- toc -->

## 1. API 网关：微服务的流量门户

API 网关是系统的统一入口，负责处理所有客户端请求并将其路由到正确的后端服务。

## 2. 核心功能矩阵

### 2.1. 安全与防御 (Security)

- **身份验证 (Authentication)**：集中处理 JWT、OAuth2 验证。
- **权限控制 (Authorization)**：细粒度的 API 访问权限管理。
- **安全过滤**：防止 SQL 注入、跨站脚本及恶意爬虫攻击。

### 2.2. 流量治理 (Traffic Management)

- **负载均衡**：在多个后端实例间分配流量。
- **熔断与断路 (Circuit Breaking)**：当后端服务异常时快速失败，防止雪崩。
- **限流与整形**：针对 IP 或用户进行 QPS 限制，保障核心业务。

### 2.3. 协议与服务发现 (Mediation)

- **协议转换**：支持前端 RESTful 接口与后端 gRPC 或 Dubbo 的透明转换。
- **服务发现集成**：与 Consul、Nacos 等注册中心联动，动态获取服务端点。

### 2.4. 观测与审计 (Observability)

- **统一日志**：记录所有请求的访问轨迹。
- **计费与计量**：针对 SaaS 场景实现按调用量收费。
- **全链路追踪**：注入 TraceID，配合分布式跟踪系统（如 SkyWalking）。

---

## 3. 架构演进：边缘网关 vs 业务网关

> [!note] 选型建议
>
> - **边缘层**：关注基础设施，如域名解析、SSL 卸载、DDoS 防护。
> - **业务层**：关注逻辑，如 API 编排、特定协议转换、业务鉴权。
