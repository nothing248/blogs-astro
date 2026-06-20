---
title: "JetBrains全家桶"
filename: jetbrains-ide-customization
description: JetBrains全家桶编辑器是主流的开发者集成开发环境（IDE）。本文主要介绍针对PyCharm的自定义设置，包含文件模版注释（配置Python脚本开头编码、作者及文件描述等信息）、在IDE内直接配置和运行Jupyter Notebook、以及常用插件和环境变量设置等提升编码体验的实用技巧。
tags: [jetbrains, pycharm, ide-setup, productivity]
aliases: [JetBrains全家桶, PyCharm模板, IDE配置]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:23 下午
date modified: 星期五, 六月 19日 2026, 12:05:27 中午
---

<!-- toc -->

## 1. 简介

全家桶编辑器，支持多个语言

## 2. Pycharm

### 2.1. 自定义注释

#### 2.1.1. 文件注释

```python
# settings -> Editor -> File and Code Templates -> Python Script

# -*- encoding: utf-8 -*-
'''
@File    :   test.py   
@Contact :   nickyang80042@gmail.com
@License :   (C)Copyright 2018-2025
@Desciption :   None

@Modify Time          @Author        @Version        @Desciption
------------          -------        --------        -----------
2024/11/13 19:07       nickyang        1.0             None
'''
```

#### 2.1.2. 函数注释

```python
# settings -> Tools -> Python Intergrated Tools -> Docsstrings -> 选项设置为 reStructuedText # 添加函数注释
# settings -> Editor - General - Smart Keys - Python 开启 Insert type placeholders in the documentation comment stub # 添加类型注释
```

#### 2.1.3. 自定义模板

```python
# File -> Settings -> Editor -> Live Templates -> Python
# 新增 -> Abbreviation(激活键) -> Description(描述信息) -> Template text(模板，可以包含标量 $Time$) -> Edit Variables(定义变量) -> Aplicable(配置适用文件)
```

#### 2.1.4. 拓展工具

```python
pip install black #代码格式化
pip install isort #导包排序
# Preference > Tools > External Tools。
# Program: D:\miniconda\Scripts\black.exe
# Arguments: $FilePath$
# Working directory: $ProjectFileDir$
```

#### 2.1.5. 保存自动运行脚本

```python
# Preference > Tools > File Watchers
# Program: D:\miniconda\Scripts\black.exe
# Arguments: $FilePath$
# Output Path: $FilePath$
# Working directory: $ProjectFileDir$
```

#### 2.1.6. 设置自动保存时间

```python
Preference > Appearance & Behavior > System Settings
```

## 3. 拓展信息

...

## 4. 参考资料

...
