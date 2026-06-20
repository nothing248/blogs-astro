---
title: "Python加密库使用指南"
filename: python-cryptography-guide
description: Python 应用中基于 cryptography 库实现数据安全传输与存储的方案。内容涵盖通过 pip 安装依赖，以及使用对称加密算法 Fernet 进行开发的关键步骤，包含安全密钥生成、二进制明文加密、密文解密还原的具体 Python 代码示例。提供官方参考文档以供进阶学习。
tags:
  - python
  - cryptography
  - encryption
  - security
aliases:
  - Python加密库使用指南
  - cryptography教程
  - Fernet对称加密
status: completed
date created: 星期二, 二月 25日 2025, 3:23:50 下午
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

## 1. 简介

`cryptography` 是一个功能强大且易于使用的 Python 加密库，旨在为开发人员提供安全且高效的加密原语和配方。

## 2. 安装

使用 `pip` 模块安装工具进行安装：

```shell
pip install cryptography
```

## 3. 使用

### 3.1. 对称加密

使用 `cryptography.fernet` 模块可以方便地进行对称加密。

- **生成密钥 (Key)**

```python
from cryptography.fernet import Fernet

# 生成一个安全的随机密钥
key = Fernet.generate_key()
```

- **数据加密**

```python
from cryptography.fernet import Fernet

fernet = Fernet(key)
# 对二进制明文数据进行加密
cry_res = fernet.encrypt(b'plain text')
```

- **数据解密**

```python
from cryptography.fernet import Fernet

fernet = Fernet(key)
# 对加密后的密文进行解密还原
raw_res = fernet.decrypt(cry_res)
```

## 4. 参考资料

- [官方文档](https://cryptography.io/en/latest/)
