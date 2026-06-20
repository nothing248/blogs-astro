---
title: "GCPWorkflows概述"
filename: gcp-workflows-overview
description: GCP Workflows 无服务器全代管编排服务指南。阐述了工作流（YAML/JSON 定义）、步骤控制（call/switch）、内置连接器（自动化轮询）及运行时服务账号概念。总结了微服务编排、IT运维自动化与事件响应应用场景，突出了长达一年有状态持久化的优势，并提供了调用 Compute Engine 连接器启动虚拟机的 YAML 示例。
tags:
  - gcp-workflows
  - serverless-orchestration
  - automation
  - yaml-configuration
aliases:
  - GCPWorkflows概述
  - Google工作流编排
  - Workflows连接器使用
status: completed
date created: 星期三, 十交月 10日 2025, 6:20:42 晚上
date modified: 星期二, 六月 16日 2026, 6:24:21 晚上
---

<!-- toc -->

## 1. 🚀 Workflows 概述

**GCP Workflows** 是 Google Cloud 提供的 **无服务器 (Serverless)**、**全代管** 的编排服务。它允许您将一系列分离的 HTTP 服务、Google Cloud 服务和自定义逻辑 **连接** 起来，形成一个持久、有状态、可靠的 **工作流**。

您可以将 Workflows 视为一个 **业务流程调度器**，用于定义和执行跨越多个步骤的复杂逻辑。

---

## 2. 核心概念

### 2.1. 工作流 (Workflow)

工作流是您在 Workflows 中定义的 **执行蓝图**。它是一个由一系列 **步骤 (steps)** 组成的 **代码文件**，使用 **YAML** 或 **JSON** 格式编写。

- **特点**：工作流是 **有状态** 和 **持久化** 的。这意味着即使在步骤之间有长时间的等待或失败重试，Workflows 也会保存当前状态，并在恢复后从中断的地方继续执行。

### 2.2. 步骤 (Steps)

工作流由一个或多个步骤组成，每个步骤执行一个特定的操作。常见的步骤包括：

- **`call`**：调用另一个服务或 API。
- **`assign`**：将数据赋值给工作流变量。
- **`goto`**：控制流程跳转到另一个步骤（命令式控制）。
- **`switch`**：根据条件执行不同的分支逻辑。
- **`try/except`**：错误捕获和处理。

### 2.3. 连接器 (Connectors)

Workflows 通过内置的 **连接器** 与 Google Cloud 服务深度集成。连接器极大地简化了 API 调用：

- **作用**：连接器负责处理底层的 HTTP 请求构造、身份验证、错误处理以及等待耗时操作（如 BigQuery 任务）完成的 **轮询 (Polling)** 逻辑。
- **示例**：使用 `google.bigquery.v2.jobs.query` 无需手动编写 HTTP 请求、身份验证和轮询状态的代码。

### 2.4. 运行时服务账号 (Runtime Service Account)

Workflows 本身是无权限的，它使用一个 **运行时服务账号** 来执行工作流中的所有操作。

- **作用**：工作流中的所有 API 调用和资源访问权限都由这个服务账号的 **IAM 角色** 决定。您必须确保该服务账号拥有执行工作流中所有步骤所需的权限。

---

## 3. 应用场景（何时使用 Workflows）

Workflows 特别擅长处理 **服务编排** 和 **响应式自动化** 场景。

|**应用场景**|**场景描述**|**典型示例**|
|---|---|---|
|**微服务编排**|将多个小型、解耦的服务（如 Cloud Functions 或 Cloud Run）串联成一个完整的业务流程。|用户注册时：调用 **Function A** (验证) → 调用 **Function B** (写入 DB) → 调用 **Function C** (发送邮件)。|
|**IT/DevOps 自动化**|自动化管理基础设施和重复性运维任务。|部署流程：启动 **VM 实例** → 等待 **VM 启动** → 运行 **配置脚本** → 通知 **部署完成**。|
|**API/任务串联**|串联需要长时间等待的异步 API 或需要重试的外部 API。|调用外部支付 API → **等待回调** 或 **轮询状态**（可等待长达一年）→ 根据结果更新 Firestore。|
|**事件响应**|作为 **Eventarc** 的目标，响应事件（如文件上传），然后执行复杂的处理流程。|**文件上传到存储桶** (Eventarc 触发) → Workflows：解压文件 → 启动 **Dataflow 管道** → 等待 Dataflow 完成。|

---

## 4. Workflows 的主要优势

### 4.1. 完全无服务器 (Truly Serverless)

- **零运维**：您无需管理任何基础设施、虚拟机或集群。
- **按步骤付费**：您只需为工作流中执行的 **步骤** 付费。如果工作流在等待外部 API 响应或等待回调，它会暂停执行，**暂停期间不收费**。

### 4.2. 有状态和持久化

- Workflows 会自动保存状态，可以处理长达 **一年** 的执行时间。即使在执行过程中发生服务中断，它也能在恢复后从上一个成功的步骤继续执行，无需用户干预。

### 4.3. 低延迟和高可伸缩性

- Workflows 启动迅速，延迟低，并且能够瞬时扩展以处理高并发的执行请求，非常适合处理突发或高吞吐量的任务。

### 4.4. 错误处理与重试

- Workflows 提供了强大的 `try/except` 机制和自定义的 **重试策略 (Retry Policies)**。您可以精确控制在发生临时错误（例如 HTTP 503）时，应该如何等待和重试，从而提高流程的健壮性。

---

## 5. Workflows YAML 示例结构

```yaml
main:
  params: [input] # 接收输入参数
  steps:
    - initialize:
        assign:
          - projectId: ${sys.get_env("GCP_PROJECT_ID")}
          - vmName: ${input.vmName} # 从输入中获取 VM 名称

    - call_compute_api:
        call: google.compute.v1.instances.start # 调用 Compute Engine 连接器
        args:
          project: ${projectId}
          zone: "us-central1-a"
          instance: ${vmName}
        result: computeResult

    - check_status:
        # 使用连接器轮询操作状态，直到完成
        call: google.compute.v1.zoneOperations.get
        args:
          project: ${projectId}
          zone: "us-central1-a"
          operation: ${computeResult.name}
        result: opResult
        # Workflows 自动等待和重试，直到操作完成

    - return_result:
        return:
          - "VM 启动操作已完成，状态: ${opResult.status}"
```
