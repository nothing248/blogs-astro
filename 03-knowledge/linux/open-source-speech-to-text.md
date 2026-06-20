---
title: "stt-services"
filename: open-source-speech-to-text
description: 本文梳理了主流开源语音转文字（STT/ASR）服务框架。主要包括已停止维护但具里程碑意义的 Mozilla DeepSpeech（需 Python 3.6）、OpenAI 推出的强大通用语音识别模型 Whisper、百度飞桨平台的 PaddleSpeech 以及阿里开源的 FunASR 框架。为开发者进行自动语音识别选型提供参考。
tags:
  - speech-to-text
  - asr
  - deepspeech
  - whisper
  - paddle-speech
  - funasr
aliases:
  - stt-services
  - speech-recognition
  - open-source-asr
status: completed
---

<!-- toc -->

## 1. 开源语音转文字（STT/ASR）服务

本文汇总了目前业界主流的开源语音转文字（Speech-to-Text / Automatic Speech Recognition）服务与框架，以便进行技术选型。

### 1.1. DeepSpeech (Mozilla)

由 Mozilla 开发的基于 TensorFlow 的开源语音识别引擎。

- **现状说明**：当前该项目已处于 **停止维护** 状态。
- **运行环境**：由于依赖旧版本库，Python 版本通常需要锁定在 `3.6`。
- **相关资源**：
  - [GitHub 仓库](https://github.com/mozilla/DeepSpeech)
  - [官方文档 (v0.9.3)](https://deepspeech.readthedocs.io/en/r0.9/?badge=latest)
  - [预训练模型下载](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3)

### 1.2. Whisper (OpenAI)

由 OpenAI 开源的多语言通用语音识别模型，具有极高的准确率和鲁棒性，支持翻译与转录。

- **优势**：支持多种语言，能够应对复杂的背景噪音，社区活跃度极高（衍生出如 `whisper.cpp` 等高性能推理实现）。
- **相关资源**：
  - [GitHub 仓库](https://github.com/openai/whisper)

### 1.3. PaddleSpeech (PaddlePaddle)

基于百度飞桨（PaddlePaddle）平台开发的易用、高效的语音方向开发套件。

- **优势**：对中文语音识别（ASR）、语音合成（TTS）、声音分类等任务支持极为友好，提供一键式预测和部署。
- **相关资源**：
  - [GitHub 仓库](https://github.com/PaddlePaddle/PaddleSpeech)

### 1.4. FunASR (达摩院)

由阿里巴巴达摩院开源的语音端到端学习及开放包，致力于构建工业级的语音识别、语音端点检测（VAD）等工具。

- **优势**：具备极强的工程落地能力，支持中文高精度实时转写及多场景定制。
- **相关资源**：
  - [GitHub 仓库](https://github.com/alibaba-damo-academy/FunASR)
