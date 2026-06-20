---
title: "模型量化"
filename: model-quantization
description: 模型量化是模型部署与优化的核心技术之一，通过将权重和激活值从高精度浮点数（如 FP32）映射到低精度定点数（如 INT8）来缩减模型大小、降低内存占用并加速推理。本笔记整理了模型量化的定义、主要优势，并引向 TensorFlow Lite 官方训练后量化技术文档，为边缘端和移动端模型部署优化提供指引。
tags:
  - mlops
  - model-compression
  - quantization
  - tensorflow-lite
aliases:
  - 模型量化
  - 模型压缩与加速
status: completed
date created: 星期二, 二月 25日 2025, 3:24:21 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

**模型量化（Model Quantization）** 是深度学习模型压缩与加速的核心技术之一。它通过将模型参数（权重和偏置）及激活值从高精度浮点数（例如 32 位浮点数 `FP32`）转换为低精度数值（例如 16 位浮点数 `FP16` 或 8 位整数 `INT8`），从而达到减小模型体积和加快运算速度的目的。

---

## 2. 核心优势

- **缩减模型大小**：将模型从 `FP32` 量化到 `INT8`，可以减小接近 75% 的磁盘占用空间和内存占用。
- **加速推理**：低精度定点数运算（如 `INT8`）在许多硬件设备（如手机 CPU、NPU、GPU）上的计算速度通常显著快于浮点数运算。
- **降低能耗**：减少了内存带宽读取和计算单元的能耗，非常适合资源受限的边缘设备或移动端设备。

---

## 3. 常见量化方法

1. **训练后量化 (Post-Training Quantization, PTQ)**：
   模型训练完成后，直接通过算法对模型的权重和激活值进行静态或动态量化。操作简单，不需要重新训练模型。
2. **量化感知训练 (Quantization-Aware Training, QAT)**：
   在模型训练阶段插入伪量化算子，使模型学会在精度受限的情况下进行参数调整，通常可以获得比 PTQ 更高的模型最终精度。

---

## 4. 参考资料

- [TensorFlow Lite 训练后量化指南 (Post-training quantization)](https://www.tensorflow.org/lite/performance/post_training_quantization?hl=zh-cn)
