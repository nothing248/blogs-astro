---
status: completed
filename: linux-bash-shell-execution-and-environment-variables
title: "Bash 执行方式"
description: 本笔记深入剖析了 Linux 环境下 Bash Shell 脚本的执行逻辑与环境初始化机制。对比了使用相对/绝对路径执行与使用 `source`/`.` 调用的本质区别（子 Shell 派生与当前 Shell 执行）。重点阐明了登录 Shell（Login Shell）与非登录 Shell（Non-login Shell）的概念差异，以及它们加载环境变量配置文件（如 `/etc/profile`, `~/.bashrc`）的严格先后顺序，为排查运维脚本“环境变量找不到”的经典问题提供理论依据。
aliases: [Bash 执行方式, Shell 环境变量, 登录 Shell, 非交互 Shell]
tags: [Linux, Shell, Bash, 运维, 环境变量, 脚本开发]
date created: 星期二, 二月 25日 2025, 3:24:09 下午
date modified: 星期四, 六月 18日 2026, 11:55:00 晚上
---

<!-- toc -->

## 1. 脚本执行方式与底层机制差异

执行一个 Shell 脚本 (`hello.sh`) 有多种方式，其核心区别在于 **是否派生子 Shell**。

### 1.1. 派生子 Shell 执行 (Sub-shell)

脚本在一个新创建的独立子 Shell 进程中运行，运行完毕后子 Shell 销毁。**脚本内对环境变量（如 `cd`、`export`）的修改不会影响父终端。**

- **相对路径执行**：`./hello.sh` (脚本必须拥有执行权限 `chmod +x`，且需要显式加上 `./` 防止从全局 `$PATH` 中误搜)。
- **绝对路径执行**：`/data/project/hello.sh`
- **作为参数调用**：`sh hello.sh` 或 `bash hello.sh` (此方式无需给脚本赋予 `+x` 权限，也无视文件头部的 `#!/bin/bash` 声明)。

### 1.2. 在当前 Shell 中执行 (Current-shell)

脚本直接在当前的终端环境中被解析执行。**脚本内部的路径跳转或变量申明会立刻污染/改变当前的终端环境。**

- **通过 source 调用**：`source hello.sh`
- **通过小数点调用**：`. hello.sh`

---

## 2. 核心概念：Shell 的运行模式分类

环境变量能否被正确加载，完全取决于当前 Shell 属于哪种模式组合。

### 2.1. 分类 A：登录 Shell vs 非登录 Shell

- **登录 Shell (Login Shell)**：需要输入用户名密码（或通过 SSH 密钥认证）建立的终端会话；或通过带 `-l` / `--login` 参数启动的 Shell（如 `bash -l`, `su - user`）。
  - **加载特征**：会极其彻底地加载全局系统配置。执行顺序为：`/etc/profile` -> `~/.bash_profile` (或 `~/.bash_login` 或 `~/.profile`)。
- **非登录 Shell (Non-login Shell)**：在图形界面打开一个新的终端标签页，或直接输入 `bash`，或使用 `su user`（不带横杠）切换用户产生的会话。
  - **加载特征**：只会加载局部环境文件：`~/.bashrc` -> `/etc/bashrc`。

> [!tip] 判断技巧
> 执行 `echo $0`。如果输出名字前带有一个减号（如 `-bash`），则是登录 Shell；如果不带（如 `bash`），则是非登录 Shell。

### 2.2. 分类 B：交互 Shell vs 非交互 Shell

- **交互 Shell (Interactive Shell)**：用户能在终端里敲代码并得到实时反馈的 Shell。
- **非交互 Shell (Non-interactive Shell)**：通过脚本自动运行的 Shell（例如被 Crontab 定时任务拉起的脚本环境）。

---

## 3. 避坑指南：自动化脚本找不到环境变量

> **核心痛点**：为什么我手动 `./test.sh` 可以跑，把它放到 Crontab 或通过 CI/CD 调用时就报错“命令找不到”？

**根本原因**：
自动化脚本运行在 **非交互、非登录 Shell** 中。在这种模式下，系统 **既不会加载 `/etc/profile` 也不会加载 `~/.bashrc`**。
它仅仅继承父进程传递下来的极少量变量，或仅寻找 `$BASH_ENV` 变量指向的文件。

**解决方案**：
在自动化脚本的开头，**显式地载入环境变量**：

```bash
#!/bin/bash
source /etc/profile
source ~/.bashrc
# ... 接着写业务逻辑 ...
```
