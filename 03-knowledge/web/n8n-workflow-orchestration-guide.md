---
title: "n8n-guide"
filename: n8n-workflow-orchestration-guide
description: n8n 是一款功能强大的开源自建任务流编排与工作流自动化工具。本笔记详细梳理了 n8n 的核心概念、基于自托管（Self-Hosted）下的 NPM 安装部署流程、包含 SMTP 及 SQLite 的环境变量配置，并提供了 Systemd 守护进程与服务管理命令。此外，针对生产环境设计，给出了包含 HTTP 错误容错、重试策略、多 Item 并发与循环控制、大吞吐 I/O 拆分、流状态动态维护及多层级变量作用域传递（如 customData 与 getWorkflowStaticData）的详细配置标准，提供了企业级自动化流运行的稳健性规范。
tags: [n8n, workflow-automation, self-hosting, server-ops]
aliases: [n8n-guide, workflow-orchestration, self-hosted-n8n]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:52 上午
date modified: 星期五, 六月 19日 2026, 10:21:00 上午
---

<!-- toc -->

## 1. 简介

n8n 是一款强力且易于拓展的节点式任务流编排与自动化工具，能够轻松整合各种 API 与服务。

## 2. 核心概念

- **流 (Workflow)**：整个任务自动化执行的完整链路图，由多个节点连接而成。
- **节点 (Node)**：流中的基本执行单元，负责获取数据、处理逻辑、发送 API 请求或执行脚本等具体操作。

## 3. 安装

> [!info]
> 以下部署环境以自建服务器的 `/opt/software/n8n` 目录为例，提供 NPM 本地安装并使用 Systemd 守护进程运行 of 方案。

### 3.1. NPM 安装

- **创建目录与安装**
  
  ```shell
  cd /opt/software
  mkdir n8n && cd n8n
  mkdir data
  # 国内服务器可以使用淘宝镜像源加速安装
  npm install n8n --registry=https://registry.npmmirror.com
  ```

- **版本更新指令**
  
  ```shell
  # 安装指定版本
  npm install n8n@1.106.3
  # 更新到最新版
  npm update n8n
  ```

- **docker 启动 PostgreSQL**
  
  ```shell
  # 预留的 PostgreSQL 启动配置
  ```

- **配置环境变量**
  
  在 `/opt/software/n8n/.env` 文件中定义本地运行的环境变量，配置数据存储、SMTP 发信服务、SSL 证书以及数据库等：
  
  ```env
  # /opt/software/n8n/.env
  N8N_USER_FOLDER=/opt/software/n8n/data                                 
  
  # 基础网络配置                                                                           
  N8N_PORT=5678                                                                        
  N8N_HOST=0.0.0.0                                                                     
  WEBHOOK_URL=https://example.com                        
  
  # SMTP 邮件发信配置                                                                               
  N8N_EMAIL_MODE=smtp                                                                  
  N8N_SMTP_HOST=smtp.163.com                                                           
  N8N_SMTP_PORT=465                                                                    
  N8N_SMTP_USER=example@163.com                                                   
  N8N_SMTP_PASS=password                                                     
  
  # 数据库配置 (本地测试优先采用 SQLite)                                                                         
  DB_TYPE=sqlite                                                                       
  
  # SSL 证书配置                                                                            
  N8N_PROTOCOL=https                                                                   
  N8N_SSL_KEY=/opt/software/n8n/https/key.key                                  
  N8N_SSL_CERT=/opt/software/n8n/https/cert.crt                                
  
  # 时区等其他配置                                                                       
  GENERIC_TIMEZONE=Asia/Shanghai                                   
  #N8N_EDITOR_BASE_URL=https://your.domain.com/
  ```

- **配置启动命令**
  
  在 `/opt/software/n8n/package.json` 中配置便捷的 NPM scripts，挂载 `.env` 配置文件运行：
  
  ```json
  {                                                                                    
    "scripts": {                                                                       
      "start:n8n": "node --env-file=.env node_modules/n8n/bin/n8n start",              
      "start:n8n-tunnel": "node --env-file=.env node_modules/n8n/bin/n8n start --tunnel",                                                                                   
      "start:n8n-prod": "node --env-file=.env.production node_modules/n8n/bin/n8n start"                                                                                    
    },                                                                                 
    "dependencies": {                                                                  
      "n8n": "^1.97.1"                                                                 
    }                                                                                  
  }
  ```

- **配置 Systemd 守护进程**
  
  为了保证 n8n 在后台持久化运行并且防崩溃拉起，创建 `/etc/systemd/system/n8n.service` 配置文件：
  
  ```ini
  [Unit]                                                                                                                                                                           
  Description=n8n - Workflow Automation                                                                                                                                            
  Documentation=https://n8n.io                                                                                                                                                     
  After=network-online.target                                                                                                                                                      
  
  [Service]                                                                                                                                                                        
  Type=simple                                                                                                                                                                      
  WorkingDirectory=/opt/software/n8n                                                                                                                                               
  EnvironmentFile=/opt/software/n8n/.env                                                                                                                                           
  ExecStart=/usr/local/nvm/versions/node/v21.6.2/bin/node /opt/software/n8n/node_modules/n8n/bin/n8n start                                                                         
  Restart=always                                                                                                                                                                   
  RestartSec=10                                                                                                                                                                    
  TimeoutStopSec=300                                                                                                                                                               
  
  [Install]                                                                                                                                                                        
  WantedBy=multi-user.target
  ```

- **重载 systemd 配置**
  
  ```shell
  systemctl daemon-reload
  ```

## 4. 管理

```shell
# 1. 终端调试启动 (直接在前台运行)
cd /opt/software/n8n/
npm run start:n8n

# 2. systemd 系统守护进程管理指令 
systemctl start n8n      # 启动服务
systemctl restart n8n    # 重启服务
systemctl stop n8n       # 停止服务
systemctl enable n8n     # 设置开机自启
```

## 5. 拓展信息

...

## 6. 配置标准

> [!important]
> 在构建生产级工作流（Workflows）时，必须严格执行以下设计标准以提升容错与扩展性。

### 6.1. HTTP 错误处理

- **接口错误捕获**：使用 HTTP 节点内置的错误处理分支或开启捕获异常选项，避免因三方接口故障导致整个流异常中断。
- **逻辑错误捕获**：对返回的 Response 代码（如非 200）进行显式校验。
- **延迟等待**：在遇到接口调用限流或失败后，设计适当的 Wait 延迟机制后重试。

### 6.2. 重试机制

- **节点层级**：针对可能抖动的 HTTP 节点等开启节点自带的层级默认重试（Retry on Fail），并设置合理重试间隔。
- **流控制层级**：如果需要以每次调度为粒度做重试，可设计全局控制循环或延迟任务重试。

### 6.3. 多 item 处理

- **深度优先处理**：n8n 默认会将数组（多个 items）逐个深度优先向下流转。
- **Loop 节点**：使用 Loop 节点（即 Split in Batches）进行小批量或分页控制，实现有序的遍历循环。
- **动态 Loop**：结合代码节点与 IF 条件，自定义设计动态条件的 Loop 节点执行结构。

### 6.4. 任务堆积

- **超时跳出**：如果单个调度的处理周期超出了设定范围，应该设置机制自动超时跳出，防止系统资源过度占满。

### 6.5. I/O 吞吐规范

- **读取数据**：支持一次性大批量拉取源头数据，在工作流内部利用拆解节点化作小批量分批处理。
- **输出数据**：尽可能合并小批量执行的 Items 数据，进行一次性的大批量写入，以降低高频写入带来的数据库或三方 API 的性能压力。

### 6.6. 消息通知

- **流全局捕获**：启用全局 Error Trigger，一旦任何工作流崩溃，自动捕获报错信息。
- **状态回调**：任务结束后根据状态（成功/失败）自动触发回调机制（如发送系统邮件、企业微信 Webhook 等）。

### 6.7. 流动态管理

- 支持对工作流进行动态的 **新增**、**修改** 以及 **删除** 操作。

### 6.8. 变量作用域与数据传递

- **局部变量深度 Copy**：为了防止多个 Item 的对象引用产生内存污染，在跨节点传递或 Code 操作前，优先进行数据深度 Copy（Deep Copy）。
- **执行范围内全局变量**：在单次执行的整个流周期中，可在 Node 中借助 `execution.customData` 传递和共享全局临时变量（注意：此功能通常只在代码/Function 节点内有效）。
- **流范围内全局变量**：需要跨越多次流执行过程持久化某些参数（如同步光标 Cursor），优先使用 `getWorkflowStaticData` 读取与更新。
- **跨流全局环境变量**：如果需要在不同流之间完全共享变量，采用 n8n 自带的 `Vars` 全局变量控制机制（此为企业级付费功能）。

## 7. 参考资料

- [n8n 官方文档 - Self-Hosted 自建托管配置](https://docs.n8n.io/hosting/configuration/user-management-self-hosted/)
