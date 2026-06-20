---
status: completed
filename: pdm-modern-python-package-and-dependency-manager
title: "PDM"
description: 本笔记记录了新一代 Python 包和依赖管理器 PDM (Python Development Master) 的核心实操指南。介绍了其基于 PEP 582 提案无需创建虚拟环境 (Virtualenv) 的本地包加载理念。详细列出了从 Python 解释器管理 (`pdm python`)、项目初始化 (`pdm init`) 到依赖增删改 (`pdm add/remove`) 的常用指令。同时，演示了如何在 `pyproject.toml` 中配置自定义脚本映射及设置国内镜像源的方法。
aliases: [PDM, Python 包管理, pyproject.toml 依赖]
tags: [Python, 工程化, PDM, 依赖管理, 虚拟环境, 包管理器]
date created: 星期二, 二月 25日 2025, 3:24:14 下午
date modified: 星期四, 六月 18日 2026, 12:35:00 晚上
---

<!-- toc -->

## 1. 工具定位：颠覆虚拟环境的现代方案

**PDM** 是一款现代的 Python 包和依赖管理器。它最大的特色是支持 **PEP 582** 提案，允许项目将依赖直接安装在项目根目录的 `__pypackages__` 文件夹中，从而 **彻底摆脱对独立虚拟环境 (Virtualenv) 的依赖**。

*(注：PDM 也完美向后兼容支持传统的 Virtualenv 模式)*

---

## 2. 核心操作与生命周期管理

### 2.1. 安装与自动补全

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
# 开启 Bash 环境的命令自动补全
pdm completion bash > /etc/bash_completion.d/pdm.bash-completion 
```

### 2.2. Python 解释器管理

PDM 内置了多版本 Python 探测与管理能力：

```bash
pdm python install --list # 查看所有可安装的远程 Python 版本
pdm python install 3.9.12 # 直接安装指定版本
pdm python list           # 查看本机已安装探测到的解释器
pdm python remove 3.9.12
```

### 2.3. 项目初始化与依赖管理

```bash
pdm init                 # 交互式初始化项目，生成 pyproject.toml

pdm add requests         # 安装最新版本依赖
pdm add requests==2.25.1 # 安装指定版本
pdm update requests      # 升级依赖
pdm remove requests      # 移除依赖
pdm list                 # 展示当前依赖树
```

---

## 3. 进阶：自定义任务执行 (`pdm run`)

在 `pyproject.toml` 中，可通过 `[tool.pdm.scripts]` 定义复杂的命令行快捷方式，类似于 `package.json` 中的 `scripts`。

```toml
[tool.pdm.scripts]
# 1. 数组定义法 (安全传参)
start = {cmd = ["flask", "run", "-p", "54321"]}
# 2. Shell 执行法 (支持管道符)
filter_error = {shell = "cat error.log | grep CRITICAL > critical.log"}
# 3. 函数调用法 (直接触发 Python 函数)
foobar = {call = "foo_package.bar_module:main"}
# 4. 组合任务 (串行执行多个子任务)
all = {composite = ["lint", "test"]}
```

**执行上述脚本**：

```bash
pdm run start
# 若未定义快捷脚本，也可以直接通过 pdm run 触发任何环境内的包命令
pdm run flask run -p 54321
```

---

## 4. 附录：配置国内镜像加速

加速依赖下载速度（全局生效）：

```bash
pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 5. 参考资料

- [PDM 官方英文全文档](https://pdm-project.org/en/latest/)
