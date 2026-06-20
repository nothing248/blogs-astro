---
status: completed
filename: isort-python-import-sorting-utility
title: "isort 格式化"
description: 本笔记简要介绍了旨在提升 Python 项目代码整洁度的导包格式化工具 isort。它能够自动解析当前文件头部的全部 `import` 语句，按照标准库、第三方库、本地项目包等层级进行逻辑分组，并执行强制的字母表排序。提供了基础的控制台执行命令，并指出了将其作为外部工具（External Tools）集成进入 PyCharm 以实现一键格式化的实施路线。
aliases: [isort 格式化, Python import 排序, 代码规范化]
tags: [Python, 工程化, 代码规范, 格式化工具, IDE 集成, isort]
date created: 星期二, 二月 25日 2025, 3:24:07 下午
date modified: 星期四, 六月 18日 2026, 14:35:00 晚上
---

<!-- toc -->

## 1. 工具定位：专注清理 Import 区块

**isort** 是一个用于自动化分类、排序以及格式化 Python 源码文件头部 `import` 导入块的独立工具。
它通常与 `Black` 代码格式化器、`Flake8` 静态检查器一起被视为 Python 现代工程化的“质量三剑客”。

*(安装依赖：`pip install isort`)*

---

## 2. 核心机制与基础操作

isort 的默认行为会将毫无章法的代码引入，根据来源自动重新编排为整齐的几个独立区块：

1. **Python 标准库** (如 `os`, `sys`)
2. **第三方依赖库** (如 `django`, `requests`)
3. **本地第一方包/项目模块**
4. 本地相对路径导入 (`from . import module`)

**终端原位格式化指令**：

```bash
# 扫描指定文件或整个目录，并直接重写保存
isort {source_file_or_directory}
```

---

## 3. 现代化 IDE 集成指南

为了达成“开发时无感，保存时自动排序”的极致体验，建议通过配置外部工具 (External Tools) 来接入 IDE。

### 3.1. PyCharm 集成策略

可完全参考本知识库中关于 Black 的集成方法（[参考 Black 挂载教程](./black.md)）：

- 将 `Program` 指向虚拟环境中的 `isort` 可执行路径。
- 将 `Arguments` 配置为 `$FilePath$`。
- 搭配宏或者快捷键绑定，实现一次按键同时触发 `isort` + `Black`。

## 4. 参考资料

- [isort 官方说明与高级配置指引](https://pycqa.github.io/isort/)
- [GitHub 代码仓库](https://github.com/pycqa/isort/)
