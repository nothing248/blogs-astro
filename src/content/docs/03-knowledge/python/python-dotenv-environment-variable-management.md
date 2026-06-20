---
status: completed
filename: python-dotenv-environment-variable-management
title: "python-dotenv"
description: 本笔记介绍了 Python 应用程序中用于加载环境变量配置的 `python-dotenv` 库。详细记录了在项目根目录构建 `.env` 文件（包含变量内部引用）的方法，并展示了通过 `load_dotenv()` API 自动寻址与按路径显式加载的实战代码。同时提到了针对 Django 框架的生态衍生组件，为后端服务的配置解耦和安全性管理提供标准化参考。
aliases: [python-dotenv, 环境变量管理, .env 解析]
tags: [Python, 工程化, 环境变量, dotenv, 配置管理, 运维安全]
date created: 星期二, 二月 25日 2025, 3:24:03 下午
date modified: 星期四, 六月 18日 2026, 14:25:00 晚上
---

<!-- toc -->

## 1. 组件简介

`python-dotenv` 是一个能从 `.env` 文件读取键值对并自动将其注入到系统的环境变量（`os.environ`）中的配置加载包。它是遵循“12-Factor App”原则，实现代码与配置彻底解耦的最佳实践工具。

*(安装依赖：`pip install python-dotenv`)*

---

## 2. 基础配置与文件规范

在项目的根目录下创建 `.env` 文件。该文件通常应该被加入 `.gitignore` 以防止敏感密钥泄露。

```text
# .env 示例
HOSTNAME=127.0.0.1
# 支持环境变量的内部动态引用插值
HOST=${HOSTNAME}:80 
```

---

## 3. 核心 API 与加载策略

在程序的入口点（如 `main.py` 或 `manage.py`）的顶部，优先执行加载逻辑。

```python
from pathlib import Path
from dotenv import load_dotenv

# 方式 1：全自动嗅探
# 系统会自动从当前执行目录逐层向上寻找 .env 文件并注入环境变量
# verbose = True 会在找不到文件或发生错误时打印更详细的警告
load_dotenv(verbose=True) 

# 方式 2：显式路径挂载 (推荐，更加严谨)
# 构建当前脚本所在位置相关的绝对路径
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# -----------------
# 加载完成后，即可通过原生 os 模块提取
import os
print(os.getenv("HOST")) 
```

---

## 4. 生态衍生工具

对于大型的 Django 项目，为了更深度地与框架的 `settings.py` 生命周期绑定，社区提供了一个专用的整合包：

```bash
pip install django-dotenv
```

## 5. 参考资料

- [python-dotenv GitHub 官方仓库](https://github.com/theskumar/python-dotenv)
