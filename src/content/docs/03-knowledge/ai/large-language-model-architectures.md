---
title: "LLM架构流派"
filename: large-language-model-architectures
description: 解析大语言模型（LLM）主流架构流派及当前演进版图。详解 Decoder-only Transformer 稠密模型、Sparse MoE 稀疏专家模型（以细粒度 MoE 为代表）、Mamba/RWKV 等线性注意力状态空间模型（SSM）及 Mamba 与 Transformer 结合的 Jamba 混合架构。同时介绍 DiT 视觉生成标准以及 o1 隐式思维链 System 2 推理新范式。
tags: [大模型架构, 混合专家模型, 线性注意力, Mamba, 隐式思维链]
aliases: [LLM架构流派, Mamba与Transformer, 细粒度MoE, DiT架构]
status: completed
date created: 星期三, 十二月 10日 2025, 7:31:06 晚上
date modified: 星期五, 六月 19日 2026, 12:11:58 中午
---

<!-- toc -->

## 1. 绝对主流：Decoder-only Transformer (稠密模型)

这是目前最经典、生态最成熟的架构。自 GPT-3 以来，几乎所有主流开源模型（如 Llama 3, Qwen 2.5）都沿用此架构。

* **核心原理：** 这是一个“接龙机器”。它利用 **自注意力机制 (Self-Attention)** 关注之前所有的 Token，预测下一个 Token。
* **特点：**
  * **Dense (稠密)：** 每个 Token 经过每一层时，都会激活所有的参数。
  * **KV Cache：** 为了加速推理，需要缓存之前的计算结果（显存消耗大）。
* **瓶颈：** 上下文长度的复杂度是 $O(N^2)$。也就是说，输入长度翻倍，计算量 and 显存要翻 4 倍。这使得它很难处理超长文本（如 100 万字）。
* **代表模型：** Llama 3, Claude 3 (早期版本), Qwen 2.5 (7B/72B)。

---

## 2. 扩容之王：Sparse MoE (稀疏混合专家)

为了突破稠密模型的参数瓶颈（比如想做 1 万亿参数，但跑不动），MoE 成为了巨型模型的标准答案。

* **核心原理：** 如前所述，将模型拆分为多个“专家”，通过 Router 分发任务。
* **当前进化趋势：**
  * **Fine-Grained MoE (细粒度 MoE)：** 以 **DeepSeek-V3** 为代表。它不把专家做成几大块，而是切碎成几十上百个极小的专家（Shared Experts + Routed Experts），极大地提升了知识利用率和负载均衡。
* **代表模型：** GPT-4o, Gemini 1.5 Pro, Mixtral 8x7B/8x22B, DeepSeek-V3。

---

## 3. 长文本挑战者：SSM / Linear RNN (线性注意力)

这是对 Transformer 霸权的“叛逆”。为了解决 Transformer 读长文太慢、太贵的问题，这类架构复兴了 RNN 的思想。

* **核心架构：** **Mamba (SSM - State Space Models)** 和 **RWKV**。
* **核心原理：**
  * 它们不像 Transformer 那样需要“回头看”之前所有的词（存巨大的矩阵）。
  * 它们像传送带一样，把历史信息压缩成一个固定的“状态 (State)”。
  * **优势：** 推理时的显存占用是恒定的，上下文长度几乎可以无限，且计算复杂度是线性的 $O(N)$。
* **缺点：** 在某些需要极高精度回忆（Recall）的任务上，表现略逊于 Transformer。
* **代表模型：** Mamba-2, RWKV-6, Codestral Mamba。

---

## 4. 混血王子：Hybrid Architectures (混合架构)

既然 Transformer 聪明但慢，SSM 快但记忆力稍弱，现在的趋势是将两者结合。

* **Jamba 架构 (Mamba + Transformer)：**
  * **结构：** 像三明治一样。几层 Mamba 层（处理海量上下文，速度快）夹几层 Attention 层（负责精准聚焦和回忆）。
  * **效果：** 既拥有 Transformer 的高质量，又拥有 Mamba 的长窗口和低显存占用。
* **代表模型：** AI21 Jamba, NVIDIA 的一些内部混合模型。

---

## 5. 视觉生成标准：DiT (Diffusion Transformer)

虽然这通常用于生图/生视频，但它本质上是 LLM 架构向视觉领域的跨界。

* **核心原理：** 抛弃了以前生图常用的 U-Net 架构，改用 Transformer 作为骨干网络来处理扩散过程（Diffusion）。
* **为什么重要：** 它证明了 Transformer 架构不仅能理解文字，还能理解图像的“Patch（补丁）”，使得 Scaling Law（规模效应）在视觉领域生效。
* **代表模型：** **Sora (视频)**, **Stable Diffusion 3**, **Flux**, **Imagen 3/4**。

---

## 6. 推理新范式：System 2 / Chain-of-Thought Architectures

这不仅仅是神经网络层的堆叠，而是 **模型 + 强化学习 + 搜索策略** 的系统级架构。

* **核心原理 (O1 / Gemini Thinking)：**
  * **Hidden CoT (隐式思维链)：** 模型在输出最终答案前，会先生成一系列“思维 Token”。这些 Token 对用户不可见，用于模型内部自我反思、纠错和规划。
  * **RLHF 进化：** 训练不再只是让模型模仿人类说话，而是通过强化学习（RL）奖励正确的推理步骤。
* **架构变化：** 输入输出不再是简单的 Prompt -> Response，而是包含了一个动态的“计算时间 (Inference-time Compute)”。模型可以“思考”几秒钟甚至几分钟。

---

## 7. 总结：2025 年 LLM 架构版图

| 架构类型 | 核心特点 | 适用场景 | 代表作 |
| :--- | :--- | :--- | :--- |
| **Decoder-only Transformer** | 稳健、通用、生态好 | 通用助手、代码补全 | Llama 3, Qwen 2.5 |
| **Sparse MoE** | 极高的参数上限、低推理成本 | 顶尖智商模型、云端大模型 | GPT-4o, Gemini 1.5, DeepSeek-V3 |
| **SSM / Linear (Mamba)** | 无限上下文、推理极快 | 长文档分析、端侧设备 | Mamba, RWKV |
| **Hybrid (Jamba)** | 平衡了质量与长窗口 | 企业级长文本应用 | AI21 Jamba |
| **System 2 (Reasoning)** | 会思考、慢推理 | 数学、科研、复杂逻辑 | OpenAI o1, Gemini 2.5 Flash (Thinking) |

目前的趋势是：**小模型用 Dense，大模型用 MoE，超长文本尝试 Hybrid/SSM，复杂任务依赖 System 2。**
