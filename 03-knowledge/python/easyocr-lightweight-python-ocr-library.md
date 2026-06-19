---
status: completed
filename: easyocr-lightweight-python-ocr-library
title: "EasyOCR 教程"
summary: 本笔记记录了开源轻量级图像光学字符识别库 EasyOCR 的基础调用方法。该库不仅支持包含简体中文在内的数十种多语言识别，且 API 封装极为精简。提供了一次性将预训练深度学习模型载入内存，并对指定图像执行文本抽取（readtext）的 Python 实战代码，适合用于搭建敏捷的文档扫描与图像文字解析通道。
aliases: [EasyOCR 教程, Python OCR, 图像识别, 文本提取]
tags: [Python, 计算机视觉, OCR, 图像处理, 人工智能]
date created: 星期二, 二月 25日 2025, 3:23:56 下午
date modified: 星期四, 六月 18日 2026, 12:45:00 晚上
---

<!-- toc -->

## 1. 工具定位

**EasyOCR** 是一个开源的 Python 光学字符识别 (OCR) 模块。其底层封装了基于 PyTorch 的深度学习网络，开箱即用，支持超过 80 种语言（包含简体中文和英文）。

*安装依赖*：`pip install easyocr`

---

## 2. 核心调用逻辑

EasyOCR 的识别过程极其精简，主要分为“初始化加载模型”与“执行推理”两步。

> [!tip] 性能优化
> 初始化 `Reader` 对象时会将体积庞大的深度学习模型载入显存或内存，这是一个耗时的重操作。在生产环境中，**必须将其作为单例 (Singleton) 全局初始化一次**，绝不能在每次请求图片时重复实例化。

```python
import easyocr

# 1. 显式加载需要的语言模型组合 (ch_sim: 简体中文, en: 英文)
reader = easyocr.Reader(['ch_sim', 'en']) 

# 2. 执行图像识别提取文本
# readtext 支持本地路径、URL 以及二进制字节流
result = reader.readtext('chinese_sample.jpg')

print(result)
```

## 3. 参考资源

- [EasyOCR 官方 GitHub 仓库](https://github.com/JaidedAI/EasyOCR)
- [官方高级 API 文档](https://www.jaided.ai/easyocr/documentation/)
