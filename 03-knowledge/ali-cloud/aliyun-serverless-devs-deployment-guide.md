---
status: completed
filename: aliyun-serverless-devs-deployment-guide
title: "Serverless Devs"
summary: 本笔记详细介绍了阿里云 Serverless Devs 平台的使用流程，涵盖了工具安装、授权管理及项目初始化。重点解析了 `s.yaml` 配置文件在 FC3（函数计算 3.0）环境下的实战应用，包括自定义运行环境 (Custom Runtime)、环境变量配置、Layer 层集成及 HTTP 触发器定义。通过标准化的 IaC (Infrastructure as Code) 模式，为开发者提供了一套从本地源码到云端全栈部署的完整 SOP。
aliases: [Serverless Devs, 阿里云 FC3 部署, s.yaml 配置手册, 函数计算自动化]
tags: [Serverless, 阿里云, 函数计算, FC3, Serverless Devs, 自动化部署, IaC, 云原生]
date created: 星期一, 十二月 1日 2025, 9:59:17 上午
date modified: 星期四, 六月 18日 2026, 8:45:00 晚上
---

<!-- toc -->

## 1. 工具安装与全局配置

### 1.1. 全局安装

```bash
npm install @serverless-devs/s -g
s -v # 验证安装版本
```

### 1.2. 凭据授权

```bash
s config add    # 引导式添加密钥
s config get    # 查看当前配置
s config delete # 删除失效授权
```

---

## 2. 核心配置文件 s.yaml 解析

以部署一个 Node.js 环境下的 **微信代理应用** 为例，展示 FC3 的标准配置结构：

```yaml
edition: 3.0.0
name: wechat_proxy_stack
access: "tm_aliyun" # 关联授权名称

vars: # 抽离全局变量
  region: "cn-shenzhen"

resources:
  wechat_proxy_app:
    component: fc3
    actions:
      pre-deploy: # 部署前自动执行构建任务
        - run: npm install
          path: .
    props:
      region: ${vars.region}
      functionName: "wechat-proxy-service"
      runtime: "custom.debian10" # 使用自定义运行时
      description: "wechat proxy powered by serverless devs"
      timeout: 10
      memorySize: 512
      cpu: 0.5
      code: .
      customRuntimeConfig:
        command:
          - node
          - index.js
        port: 8000
      environmentVariables: # 注入环境变量
        PATH: /opt/nodejs20/bin:/usr/local/bin:/usr/bin:/bin
      layers: # 挂载公共层（如特定版本的 Runtime）
        - acs:fc:${vars.region}:official:layers/Nodejs20/versions/3
      triggers: # 定义触发器
        - triggerName: http_trigger
          triggerType: http
          triggerConfig:
            authType: anonymous # 允许匿名访问
            methods:
              - GET
              - POST
```

---

## 3. 常用操作指令

- **初始化项目**：`s init` (支持从模版库快速创建)
- **全量部署**：`s deploy` (自动处理资源创建与代码上传)
- **在线调试**：`s invoke` (触发云端函数运行)
- **日志查看**：`s logs`

---

## 4. 延伸资源

- [Serverless Devs 官方手册](https://manual.serverless-devs.com/user-guide/aliyun/#fc3)
- [阿里云函数计算官方链接](https://www.serverless-devs.com/)
