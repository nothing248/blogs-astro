---
title: "PyTorch安装指南"
filename: pytorch-getting-started
description: PyTorch 是由 Meta 开源的主流深度学习开发框架，以动态计算图和优秀的硬件加速支持著称。本笔记梳理了 PyTorch 的核心依赖包安装指令，并补充了在 Python 环境下验证 CUDA GPU 加速是否可用的关键检测代码，为深度学习开发环境的搭建与可用性检测提供快速参考。
tags:
  - pytorch
  - python
  - deep-learning
  - cuda
aliases:
  - PyTorch安装指南
  - PyTorch快速入门
status: completed
date created: 星期二, 二月 25日 2025, 3:24:14 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

**PyTorch** 是由 Meta（前 Facebook）AI 研究团队开发的开源机器学习库。它广泛应用于计算机视觉和自然语言处理等深度学习领域，因其 **动态计算图**（Eager Execution）和与 Python 生态的紧密集成，深受科研人员与工程开发者的喜爱。

---

## 2. 安装

通常可以通过 Python 包管理器 `pip` 快速安装 PyTorch 的 CPU 及 GPU（CUDA）通用驱动版本：

```shell
pip install torch torchvision torchaudio
```

> [!tip] 版本选择
> 针对不同的 CUDA 版本，或者对于没有 GPU 的 CPU 环境，推荐访问 PyTorch 官网的 [Start Locally](https://pytorch.org/get-started/locally/) 交互式工具，以获取最精确的安装命令行参数（如指定 `-f https://download.pytorch.org/whl/torch_stable.html` 等源地址）。

---

## 3. 验证 GPU 加速 (CUDA)

安装完毕后，可以通过以下 Python 代码在命令行或 Notebook 中检测 PyTorch 是否已成功识别到系统的 NVIDIA 显卡：

```python
import torch

# 1. 检查 PyTorch 版本
print(f"PyTorch Version: {torch.__version__}")

# 2. 检查 CUDA (GPU) 是否可用
cuda_available = torch.cuda.is_available()
print(f"CUDA Available: {cuda_available}")

if cuda_available:
    # 3. 获取可用 GPU 的数量与名称
    print(f"GPU Count: {torch.cuda.device_count()}")
    print(f"Current GPU Name: {torch.cuda.get_device_name(0)}")
```

---

## 4. 参考资料

- [PyTorch 官方网站](https://pytorch.org/)
- [PyTorch 官方安装指导工具](https://pytorch.org/get-started/locally/)
