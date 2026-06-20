---
title: "DialogflowCX使用手册"
filename: dialogflow-cx-agents-guide
description: Google Dialogflow CX 智能对话代理（AI Agent）平台使用指南。解析了完全生成、确定性与部分生成三种模式，对比了 Playbook 与 Flows 的流程编排。详述了 DataStore 知识库的数据源导入格式、文档分块机制及地理区域限制，分析了外部系统集成和多语言环境调试方法，并给出了产品在文档一致性、索引延迟等方面的实测结论。
tags:
  - dialogflow-cx
  - ai-agent
  - vertex-ai
  - datastore
  - conversation-design
aliases:
  - DialogflowCX使用手册
  - Playbook与Flows编排
  - Dialogflow多语言配置
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:16 上午
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

## 1. 简介

Google Dialogflow CX 是一款功能强大的 AI Agent 对话代理开发平台，旨在构建复杂、多步骤的对话流。

## 2. 概念

### 2.1. 模式

- **完全生成**：基于 [Vertex AI](https://cloud.google.com/vertex-ai/docs) 构建大型语言模型（LLM），用于理解最终用户意图以及生成代理响应。
- **确定性流程**：使用语言模型来理解对话过程中的最终用户意图。一旦意图确定，即可通过定义好的流程编排对话流和代理响应。
- **部分生成**：结合流程中的可选功能（如 **生成器**、**生成回退**），在某些不需要对代理响应进行确定性控制的对话场景中，使用 LLM 动态响应。

### 2.2. 编排方式

#### 2.2.1. 1 Playbook

- **核心要素**：

```text
# Name 名称
# Goal 是剧本应该完成的任务的高级描述。
# Instructions 是完成剧本目标应采取的高级步骤
# Examples 是终端用户与代理之间的对话示例。这些示例实际上是法学硕士（LLM）的少量提示示例
```

- **示例**：

```text
# Name Default

# Goal
You are an assistant for a shirt store.
Your name is "Samantha".
Your job is to direct customers to other playbooks based on the customer's questions.

# Instructions
- If the customer hasn't been greeted yet, greet the customer,
  introduce yourself, and ask the user how you can help.
- If the customer wants information about the store,
  route them to ${PLAYBOOK: Information}
- If the customer wants to purchase a shirt,
  route them to ${PLAYBOOK: Order}

# Examples
通过交互生成测试案例。支持：添加、编辑、删除或重新排序，总结等操作。
```

> [!NOTE]
> 存在一个默认的 playbook 作为代理的流量入口。

#### 2.2.2. 2 Flows

- **核心要素**：

```text
# Flow 多个节点组成的流
# Intent 意图
# Page 节点
```

- **示例**：
  ![](http://qiniu.sxyxy.top/20250704120712.png)

> [!NOTE]
> Intent（意图）是基于用户配置的训练短语（Training phrases）进行识别和触发的。

### 2.3. DataStore (知识库)

#### 2.3.1. 1 数据源

![](http://qiniu.sxyxy.top/20250704122317.png)

#### 2.3.2. 2 数据导入

- **FAQ 格式 (结构化文件)**：
  ![](http://qiniu.sxyxy.top/20250704123308.png)
- **非结构化数据 (带有元数据)**：
  ![](http://qiniu.sxyxy.top/20250704123643.png)
- **非结构化数据 (不带有元数据)**：

#### 2.3.3. 3 文档的解析分块

![](http://qiniu.sxyxy.top/20250704124352.png)

#### 2.3.4. 4 存储工具

数据存储工具可以根据网站内容和上传的数据，提供由 AI 生成的代理响应。

- **Grounding confidence**：
  ![](http://qiniu.sxyxy.top/20250704132833.png)

- **Summarization bring-your-own-prompt**：

```text
- 支持自定义模型
- 支持自定义 prompt
```

- **Rewriter bring-your-own-prompt**：

```text
- 支持自定义模型
- 支持自定义 prompt
```

### 2.4. 外部系统集成

- Webhook
- Connector
- OpenAPI
- Function

### 2.5. 多语言环境

1. **基于修改 agent 中的 prompt 的方案**（可以基于 Default Start Flow 进行测试）：
   - 基于 prompt 的多语言判断可能不够稳定，优化后虽有改善，但无法百分百避免语言漂移问题。
   - Intent 意图识别需要在训练短语（Training phrases）中手动添加多语言文本才能实现高质量的意图识别。

2. **基于平台原生语言检测功能**：
   - 支持的语言有限，目前部分小语种（如越南语）不支持。

   > 针对识别不出的语言，将按照预设的默认语言环境进行响应。

3. **基于后期部署 API 中的动态参数来匹配不同的环境**：
   - 需要客户端根据用户设置动态切换传入的语言参数。

   > [!IMPORTANT]
   > 不同的语言环境在平台内的很多设置项是独立的，需要为每种语言单独进行配置。

### 2.6. 集成方式

- **API 方式**：
  ![](http://qiniu.sxyxy.top/20250704121154.png)
- **前端组件**：
  ![](http://qiniu.sxyxy.top/20250704123003.png)

## 3. 测试场景

- 基于 Flow 的测试：
  ![](http://qiniu.sxyxy.top/20250704152723.png)

- 基于 Playbook 的测试：
  ![](http://qiniu.sxyxy.top/20250704155238.png)

## 4. 拓展信息

### 4.1. 支持语音交互

### 4.2. 文档与产品实测有出入

![](http://qiniu.sxyxy.top/20250704112823.png)

### 4.3. 关于 DataStore 存在的限制与问题

- 管理入口不一致。
- 按照官方说明，除了 **Website URLs**、**BigQuery**、**Cloud Storage**，其他自定义数据源导入需要提交表单申请。
- 存在区域限制（DataStore 的地理位置必须与 Agent 所在区域完全一致才能访问）。
- **Website URLs** 的抓取方式依赖 Google Search（必须通过网域所有权验证且页面已被 Google Index 索引），**开发中可以手动配置 sitemap 文件辅助抓取**。
- 支持的文件格式有限（目前支持 TXT、PDF、HTML、CSV）。
- TXT 格式的最大文件大小为 2.5MB，其他格式最大为 100MB。
- Index 稳定性欠佳（例如 1.5MB 的文本文件构建索引耗时约 2 小时）。

### 4.4. 模型支持情况

![](http://qiniu.sxyxy.top/20250704155325.png)

## 5. 测试结论

- 产品设计和文档迭代不够成熟，部分功能项逻辑略显混乱。
- 功能配置项较繁琐，存在一定的学习成本。
- 可以快速冷启动，但后期精细化调优和个性化定制的灵活性不足。

## 6. 参考文档

- [官方文档](https://cloud.google.com/dialogflow/cx/docs/concept/data-store)
- [DataStore 入口](https://console.cloud.google.com/gen-app-builder/data-stores?inv=1&invt=Ab10nw&project=[项目X])
- [DataStore 支持区域](https://cloud.google.com/dialogflow/cx/docs/concept/region#avail)
- [DataStore 支持语言](https://cloud.google.com/dialogflow/cx/docs/reference/language)
