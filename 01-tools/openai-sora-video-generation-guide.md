---
title: "Sora视频模型"
filename: openai-sora-video-generation-guide
summary: Sora 是 OpenAI 推出的革命性文本生成视频（Text-to-Video）大模型。本文汇总了 Sora 的官方震撼示例，包括著名的“东京街头时尚女性”及“禅宗花园小矮人”视频及其对应的中英文 Prompt。同时介绍了 2024 年初期的测试资格申请流程与使用步骤，展示了 Sora 在模拟真实世界物理规律及生成超长、连贯视频方面的跨时代能力。
tags: [sora, openai, generative-ai, video-generation, computer-vision, prompt-engineering]
aliases: [Sora视频模型, OpenAI Sora教程, 文本转视频]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:19 下午
date modified: 星期五, 六月 19日 2026, 12:07:01 中午
---

<!-- toc -->

## 1. 简介

Sora 是 OpenAI 开发的一个扩散模型，能够根据文本指令生成长达 60 秒的视频。其核心突破在于能够生成具有高度细节的场景、复杂的摄像机运动，以及充满活力的多角色情感。Sora 不仅理解用户的 Prompt，还能在一定程度上模拟真实世界的物理属性。

## 2. 官方震撼示例

以下是 Sora 发布初期最具代表性的几个演示案例：

### 2.1. 东京街头 (Tokyo Walk)

> [!info] **提示词 (Prompt)**
> **中文**：一位时尚女性走在充满温暖霓虹灯和动画城市标牌的东京街道上。她穿着黑色皮夹克、红色长裙和黑色靴子，拎着黑色钱包。她戴着太阳镜，涂着红色口红。她走路自信又随意。街道潮湿且反光，在彩色灯光的照射下形成镜面效果。
> **English**: A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, a long red dress, and black boots, and carries a black purse. She wears sunglasses and red lipstick. She walks confidently and casually. The street is damp and reflective, creating a mirror effect of the colorful lights.

<video controls preload="none" style="width:100%; border-radius: 8px;">
      <source src="https://cdn.openai.com/sora/videos/tokyo-walk.mp4" type="video/mp4">
</video>

### 2.2. 艺术画廊 (Art Gallery)

> [!info] **提示词 (Prompt)**
> **中文**：参观艺术画廊，里面有许多不同风格的美丽艺术品。
> **English**: Tour of an art gallery with many beautiful works of art in different styles.

<video controls preload="none" style="width:100%; border-radius: 8px;">
      <source src="https://cdn.openai.com/sora/videos/art-museum.mp4" type="video/mp4">
</video>

### 2.3. 禅宗花园球体 (Zen Garden Sphere)

> [!info] **提示词 (Prompt)**
> **中文**：玻璃球的特写视图，里面有一个禅宗花园。球体中有一个小矮人正在耙禅宗花园并在沙子上创造图案。
> **English**: A close up view of a glass sphere that has a zen garden within it. There is a small dwarf in the sphere who is raking the zen garden and creating patterns in the sand.

<video controls preload="none" style="width:100%; border-radius: 8px;">
      <source src="https://cdn.openai.com/sora/videos/zen-garden-gnome.mp4" type="video/mp4">
</video>

## 3. 测试资格与使用流程 (历史回顾)

在发布初期，Sora 仅对受邀的 Red Teamers（红队测试人员）以及部分视觉艺术家、设计师和电影制作人开放，以评估风险。

### 3.1. 申请与使用逻辑

1. **Plus 账户权益**：早期倾向于在 ChatGPT Plus 用户中逐步释放测试名额。
2. **场景描述**：在特定界面输入极致详细的 Prompt，描述场景、镜头运动、光影细节。
3. **视频生成**：云端利用算力集群进行扩散生成，片刻后即可获取高质量视频。

## 4. 技术亮点

- **三维空间一致性**：角色在移动或被遮挡时，能保持身份和外貌的一致性。
- **物理交互模拟**：如笔划过沙子留下痕迹，或者一个人吃饼干留下咬痕。
- **超长连贯性**：支持生成长达一分钟的视频，远超当时其他 AI 视频工具。

## 5. 参考资料

- [OpenAI Sora 官方介绍页](https://openai.com/sora)
- [Sora 技术报告：视频生成模型作为世界模拟器](https://openai.com/research/video-generation-models-as-world-simulators)
