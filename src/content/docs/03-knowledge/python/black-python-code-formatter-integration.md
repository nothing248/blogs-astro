---
status: completed
filename: black-python-code-formatter-integration
title: "Black 格式化"
description: 本笔记记录了极度严谨的 Python 代码格式化工具 Black 的基础用法。阐述了其作为“不妥协的格式化器 (The Uncompromising Code Formatter)”的理念，能够强制消除团队间不同的代码风格争议。提供了通过 pip 的安装命令以及终端格式化指令。同时，演示了将其通过 External Tools 挂载集成至 PyCharm 等主流 IDE 的路径，为提升团队代码审查效率与工程规范度提供指南。
aliases: [Black 格式化, Python 代码规范, Black 教程]
tags: [Python, 工程化, 代码规范, 格式化工具, Black, IDE 集成]
date created: 星期一, 十二月 1日 2025, 9:59:24 上午
date modified: 星期五, 六月 19日 2026, 2:19:05 下午
---

<!-- toc -->

## 1. 工具定位：不妥协的规范

**Black** 是 Python 生态中极具盛名的开源代码格式化工具。它的座右铭是“The Uncompromising Code Formatter（不妥协的代码格式化器）”。
它 **几乎不提供任何可配置的样式选项**，旨在用唯一的标准彻底终结团队内部关于代码风格（如单双引号、换行折叠）的无休止争论，从而让开发者将精力集中在业务逻辑而非排版上。

---

## 2. 安装与基础使用

### 2.1. 安装

```bash
pip install black
```

### 2.2. 终端运行

直接对单个文件或整个目录执行原位格式化覆写：

```bash
black {source_file_or_directory}
```

---

## 3. 现代化 IDE 集成指南

为了在编写代码时实现“保存即格式化”，建议将 Black 集成到常用的 IDE 中。

### 3.1. PyCharm 集成

可以通过配置外部工具 (External Tools) 来实现。
**路径**：`File -> Settings -> Tools -> External Tools`

- **Name**: `Black`
- **Program**: 定位到虚拟环境中的 `black` 可执行文件路径（如 `.venv/bin/black`）。
- **Arguments**: `$FilePath$` (代表当前聚焦的文件)。
- **Working directory**: `$ProjectFileDir$`

*配置完成后，可以为该工具绑定一个快捷键（如 `Ctrl+Alt+L` 的替代），一键格式化当前文档。*

## 4. 参考资料

- [Black GitHub 官方仓库](https://github.com/psf/black)
- [官方 IDE 集成图文文档](https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea)
