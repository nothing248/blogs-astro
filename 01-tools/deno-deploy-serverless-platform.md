---
title: "Deno部署指南"
filename: deno-deploy-serverless-platform
summary: Deno Deploy 是专为 Deno 运行时的全球分布式 Serverless 部署平台。支持快速验证的 Playground 沙盒与绑定 Git 仓库的 Project 生产应用。面向第一方开发提供 Standard 部署，面向 SaaS 平台提供 Subhosting 托管模式以运行非信任代码。内容涵盖使用 deployctl 命令行及 HTTP API 进行自动化部署，并利用 V8 Isolate 技术实现高效安全隔离。
tags: ["Deno", "Serverless", "Deno-Deploy", "Cloud-Platform", "Backend"]
aliases: ["Deno部署指南", "deployctl使用", "Subhosting详解"]
status: completed
date created: 星期五, 十二月 5日 2025, 3:42:14 下午
date modified: 星期五, 六月 19日 2026, 11:58:33 中午
---

<!-- toc -->

## 1. 简介

**Deno Deploy** 是一个专为 Deno 打造的 **Serverless** 部署平台。它通过在靠近用户的全球边缘节点运行代码，提供极速的响应能力。Deno Deploy 充分利用了 Deno 内置的 TypeScript 支持和安全特性，是现代边缘计算的代表性产品。

---

## 2. 费用与注册

![](http://qiniu.sxyxy.top/20250812141553.png)

> [!warning] 注册限制
> 注册必须要拥有 GitHub 账户。

---

## 3. 核心产品概念

### 3.1. Playground Vs Project

- **Playground**：在线沙盒环境。

  > 是一种基于浏览器的交互式代码编辑器。它的设计初衷是让你能够快速地尝试 Deno 代码，而无需在本地进行任何设置。
  > **主要特点：**
  > - **即时体验**：你可以在浏览器中直接编写、运行和部署代码，实时看到结果。
  > - **快速原型**：非常适合验证一个想法、测试一个库或者快速创建一个小型的 Web 服务。
  > - **无本地设置**：你不需要安装 Deno 或任何 CLI 工具。所有操作都在网页上完成。
  > - **临时性**：虽然你的 Playground 代码会被保存，但它的主要用途是快速实验，而不是作为长期、正式的生产应用。
  > - 你可以把 Playground 看作一个“在线沙盒”，它给你一个完全隔离、配置好的环境，让你随时可以开始编码。

- **Project**：正式应用。

  > 是一个正式的、为长期运行而设计的 Deno 应用。它通常与你的代码版本控制系统（如 GitHub）绑定，并支持更复杂的部署和管理流程。
  > **主要特点：**
  > - **与 Git 集成**：项目通常会连接到一个 GitHub 仓库，当你推送新的代码时，Deno Deploy 会自动构建 and 部署你的应用，实现持续部署（CD）。
  > - **完整的应用生命周期**：支持环境变量、自定义域名、日志查看、性能监控等完整的生产环境功能。
  > - **部署方式多样**：除了与 GitHub 集成，你还可以使用 `deployctl` 命令行工具来部署，这使得它很容易集成到 CI/CD 工作流中。
  > - **长期稳定**：项目是为了承载你的正式应用而存在的，不管是个人博客、Web API 还是一个完整的网站。

### 3.2. Standard Vs Subhosting Deploy

- **Standard Deploy**：面向第一方开发者。

  > 是 Deno Deploy 的核心产品，是面向个人开发者和小型团队的一站式服务。它的设计目标是让你能快速、简单地部署自己的第一方项目，比如网站、API、或服务端渲染应用。
  > **主要特点：**
  > - **用户界面（Dashboard）驱动**：大部分操作都在 Deno Deploy 的网页控制台上完成。你可以通过点击按钮来创建项目、查看日志、管理自定义域名等。
  > - **与 Git 集成**：核心工作流通常是与 GitHub 仓库集成。当你向 main 分支推送新代码时，Deno Deploy 会自动触发部署。
  > - **面向第一方代码**：你部署的是你自己编写和控制的代码。
  > - **开箱即用**：提供了所有必要的功能，包括日志、监控、Deno KV 等，无需额外配置。

- **Subhosting**：面向 SaaS 平台。

  > 是一个更高级、更具可编程性的服务，面向 SaaS (软件即服务) 平台。它的设计目标是让你的平台能够安全地运行由你的客户或用户编写的非信任代码。
  > **主要特点：**
  > - **API 驱动**：Subhosting 的核心是其 API。你不是通过网页界面来部署，而是通过 API 调用来创建项目、部署代码、管理域名。这使得你可以将 Subhosting 功能无缝集成到你的产品中。
  > - **隔离和安全**：这是 Subhosting 最重要的特点。它利用 Deno 底层的 V8 isolate 技术，确保不同用户的代码完全隔离，一个用户的代码不会影响到其他用户或你的核心系统。
  > - **大规模管理**：专为需要管理大量小规模部署（每个用户一个部署）的平台而设计。例如，一个低代码平台允许用户编写自定义函数，一个电商平台允许商家添加自定义脚本。
  > - **非信任代码**：Subhosting 解决了运行“非信任代码”这一复杂且有安全风险的挑战，让你无需自己构建和维护一个隔离的沙盒环境。

---

## 4. 安装与初始化

### 4.1. Deno 与 Deployctl 安装

```shell
# 方式一：
npm install -g deno
deno -v
deno install -A jsr:@deno/deployctl --global #部署命令
deployctl -v
# 方式二：
mkdir /opt/software/deno
curl -fsSL https://deno.land/install.sh
deno -v
deno install -A jsr:@deno/deployctl --global --root /opt/software/done #部署命令
cp -r ~/.deno/bin/deno /opt/software/deon/bin
deployctl -v
```

### 4.2. 项目初始化

```
deno init
```

---

## 5. 配置文件 `deno.json`

```json
{
  "tasks": {
    "dev": "deno serve --allow-env --watch main.ts"
  },
  "imports": {
    "@std/assert": "jsr:@std/assert@1"
  },
  "deploy": {
    "project": "[PROJECT_ID_已隐藏]",
    "exclude": [
      "**/node_modules"
    ],
    "include": [],
    "entrypoint": "main.ts"
  }
}
```

---

## 6. 部署工作流

### 6.1. 命令行部署

```shell
deployctl deploy --token=[TOKEN_已隐藏] --project="my-project" main.ts
```

### 6.2. 通过 API 自动化管理 (针对 Subhosting)

- **创建项目**：

```shell
curl -i -X POST \
  https://api.deno.com/v1/organizations/[ORG_ID_已隐藏]/projects \
  -H 'Authorization: Bearer [TOKEN_已隐藏]' \
  -H 'Content-Type: application/json' \
  -d '{ "description": "My first project" }'
```

- **部署项目**：

```shell
curl -i -X POST \
  'https://api.deno.com/v1/projects/[PROJECT_ID_已隐藏]/deployments' \
  -H 'Authorization: Bearer [TOKEN_已隐藏]' \
  -H 'Content-Type: application/json' \
  -d '{
    "entryPointUrl": "main.ts",
    "assets": {
      "main.ts": {
        "kind": "file",
        "content": "Deno.serve((req: Request) => new Response(\"Hello World\"));"
      }
    },
    "envVars": {},
    "description": "My first deployment"
  }'
```

> [!note] 部署限制
> 只有在 Subhosting 的组织类型中才可以使用 API 部署。

---

## 7. 注意事项与限制

- **GitHub 账户限制**：

  > [!warning] GitHub 账户核验
  > 部分新注册或存在异常的 GitHub 账户在绑定 Deno Deploy 时可能会遇到限制，需通过官方人工审核。

- **隔离性**：Deno Deploy 利用 V8 Isolate 技术实现高效隔离，不同部署之间互不干扰。

---

## 8. 参考资料与文档

- [Deno Deploy 官方文档](https://docs.deno.com/deploy/early-access/)
- [Deno Deploy 官方链接](https://app.deno.com/)
- [Deno HTTP 服务语法](https://docs.deno.com/runtime/fundamentals/http_server/)
- [Deno 配置文件指南](https://docs.deno.com/runtime/fundamentals/configuration/)
- [Deno Deploy API 工具](https://apidocs.deno.com/#auth)
