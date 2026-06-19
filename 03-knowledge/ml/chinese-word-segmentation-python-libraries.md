---
status: completed
filename: chinese-word-segmentation-python-libraries
title: "中文分词"
summary: 本笔记整理了自然语言处理 (NLP) 中最基础的预处理环节——中文分词的 Python 开源工具矩阵。罗列了业界应用最广的结巴分词 (jieba)、北大开源的多领域分词器 (pkuseg)、基于双向 LSTM 模型的高准度分词库 (FoolNLTK) 以及清华大学研发的高效词法分析套件 (THULAC)。为构建搜索召回系统、文本挖掘与情感分析提供前置分词组件的快速选型入口。
aliases: [中文分词, Python 分词库, jieba 分词]
tags: [人工智能, NLP, 自然语言处理, 文本挖掘, Python, jieba]
date created: 星期二, 二月 25日 2025, 3:23:33 下午
date modified: 星期四, 六月 18日 2026, 15:25:00 晚上
---

<!-- toc -->

## 1. 核心定位

中文不同于英文有天然的空格作为单词边界，因此在进行 NLP（自然语言处理）任务（如词嵌入、意图识别、搜索引擎倒排索引）之前，必须将连续的汉字序列切分为有意义的词汇，此即 **中文分词 (Word Segmentation)**。

---

## 2. Python 主流开源分词库选型

### 2.1. [jieba (结巴分词)](https://github.com/fxsjy/jieba)

业界最经典、生态最繁荣的中文分词组件。支持精确模式、全模式和搜索引擎模式，并允许挂载自定义业务词典。

- **安装**：`pip install jieba`
- **特点**：基于前缀词典实现高效的词图扫描，利用 Viterbi 算法解码隐藏状态。

### 2.2. [pkuseg (北大分词)](https://github.com/lancopku/pkuseg-python)

由北京大学推出的多领域开源中文分词工具。

- **特点**：与 jieba 的通用模型不同，pkuseg 提供针对新闻、网络、医药、旅游等 **不同垂直领域** 的优化模型，特定领域的切分准确度更高。

### 2.3. [FoolNLTK](https://github.com/rockyzhengwu/FoolNLTK)

- **特点**：可能不是最快的，但号称是基于深度学习（BiLSTM 模型）的最准的开源中文分词库。除了分词，还自带词性标注 (POS) 和实体识别 (NER) 能力。

### 2.4. [THULAC (清华词法分析)](https://github.com/thunlp/THULAC-Python)

清华大学自然语言处理与社会人文计算实验室推出的一套中文词法分析工具包。

- **特点**：速度极快，同时包含了分词和词性标注两项核心能力。
