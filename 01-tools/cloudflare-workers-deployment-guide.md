---
title: "Cloudflare配置指南"
filename: cloudflare-workers-deployment-guide
description: Cloudflare 是全球领先 of 云服务商，提供免费 CDN、DDoS 缓解与安全 DNS 等功能。本笔记主要记录了 Cloudflare Workers 边缘无服务器计算平台的开发与部署流程。内容涵盖使用 CLI 工具 Wrangler 进行安装、初始化、OAuth2.0 与 API Token 授权方式，详解了 wrangler.jsonrc 配置文件的常见属性与多 Worker 绑定，以及利用 Zero Trust Tunnel 暴露本地内网服务和边缘证书三级域名的限制。
tags: ["Cloudflare", "Wrangler", "Serverless-Workers", "CDN", "Zero-Trust"]
aliases: ["Cloudflare配置指南", "Wrangler使用", "Cloudflare内网穿透"]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 星期五, 六月 19日 2026, 11:58:17 中午
---

<!-- toc -->

## 1. 简介

**Cloudflare**（常拼写为 Cloudfare）是一个全球的云服务提供商，以其强大的边缘网络和安全防护能力著称。

---

## 2. 作用与核心能力

- **提供免费的 CDN 服务**：加速全球用户的网站访问。
- **提供 DDoS 缓解与防护**：保护源站免受大规模流量攻击。
- **DNS 安全与管理**：提供低延迟、高可用的智能 DNS 解析与 DNSSEC。

---

## 3. Worker 开发流程

**Cloudflare Workers** 是一个无服务器（Serverless）的轻量级计算平台，允许你在全球边缘节点上运行 JavaScript/TypeScript。

### 3.1. 安装 Wrangler CLI

`Wrangler` 是 Cloudflare 官方提供的 Workers 命令行开发工具。

``` shell
npm i -G wrangler@latest
wrangler -v
```

### 3.2. 授权认证

在本地开发或部署前，需要对 Wrangler 进行授权。

```shell
# 方式一: OAuth2.0
wrangler login 

# 方式二：Token
export CLOUDFLARE_API_TOKEN=""
```

> [!warning] 避坑：Wrangler login 授权失效
> 如果遇到本地 `wrangler login` 授权无效或无响应，请尝试：
>
> ```
> 点击两边授权链接进行验证
> ```

### 3.3. 初始化项目

```shell
wrangler init #初始化项目 
```

---

## 4. 部署配置 `wrangler.jsonrc`

```json
# wrangler.jsonrc
/**
 * For more details on how to configure Wrangler, refer to:
 * https://developers.cloudflare.com/workers/wrangler/configuration/
 */
{
 "$schema": "node_modules/wrangler/config-schema.json",
 "name": "wechat-proxy",
 "main": "src/index.ts",
 "compatibility_date": "2025-08-12",
 // "vars": {
 //  "AUTH": "123"
 // },
 "observability": {
  "enabled": true
 },
 "dev": {
  "port": 8000
 }
 /**
  * Smart Placement
  * Docs: https://developers.cloudflare.com/workers/configuration/smart-placement/#smart-placement
  */
 // "placement": { "mode": "smart" }
 /**
  * Bindings
  * Bindings allow your Worker to interact with resources on the Cloudflare Developer Platform, including
  * databases, object storage, AI inference, real-time communication and more.
  * https://developers.cloudflare.com/workers/runtime-apis/bindings/
  */
 /**
  * Environment Variables
  * https://developers.cloudflare.com/workers/wrangler/configuration/#environment-variables
  */
 // "vars": { "MY_VARIABLE": "production_value" }
 /**
  * Note: Use secrets to store sensitive data.
  * https://developers.cloudflare.com/workers/configuration/secrets/
  */
 /**
  * Static Assets
  * https://developers.cloudflare.com/workers/static-assets/binding/
  */
 // "assets": { "directory": "./public/", "binding": "ASSETS" }
 /**
  * Service Bindings (communicate between multiple Workers)
  * https://developers.cloudflare.com/workers/wrangler/configuration/#service-bindings
  */
 // "services": [{ "binding": "MY_SERVICE", "service": "my-service" }]
}
```

### 4.1. 部署项目

```shell
wrangler deploy
```

---

## 5. 内网服务

```
Zero Trust -> 网络 -> Tunnel
```

---

## 6. 拓展信息与限制

- **边缘证书不支持三级域名**
- **wrangler login 授权无效**

```
点击两边授权链接进行验证
```

---

## 7. 参考资料

- [官方链接](https://dash.cloudflare.com/)
- [Wrangler CLI 文档](https://developers.cloudflare.com/workers/wrangler/)
- [Workers 文档](https://developers.cloudflare.com/workers/)
- [Pages 文档](https://developers.cloudflare.com/pages/)
