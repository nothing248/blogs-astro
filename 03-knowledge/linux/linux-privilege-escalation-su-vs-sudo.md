---
status: completed
filename: linux-privilege-escalation-su-vs-sudo
title: "Linux 提权"
description: 本笔记系统剖析了 Linux 环境下两大提权管理工具 `su` 与 `sudo` 的底层工作机制差异。详细对比了 `su root` 与 `su - root` 在是否重新初始化登录 Shell 环境变量时的表现；深度挖掘了 `sudo` 的进阶参数（`-s` 维持当前环境 vs `-i` 启动隔离新环境），为解决自动化部署中因环境变量缺失导致的执行错误（如 "command not found"）提供了底层排障依据。
aliases: [Linux 提权, su 与 sudo 区别, sudo -i]
tags: [Linux, 系统运维, 安全权限, sudo, Shell, 环境变量]
date created: 星期二, 二月 25日 2025, 3:23:55 下午
date modified: 星期四, 六月 18日 2026, 13:45:00 晚上
---

<!-- toc -->

## 1. 工具核心差异

在 Linux 系统中，普通用户如果需要执行高权限任务，必须进行权限提升。

- **`su` (Switch User)**：彻底“变身”为另一个用户。通常用于长时间停留在 root 视角进行大量配置。**需输入目标用户（如 root）的密码。**
- **`sudo` (Superuser Do)**：以超级用户或其他用户的身份“临时”借用权限执行一条特定指令。**需输入当前执行者自己的密码。**

---

## 2. `su` 核心指令剖析

带不带 `-` (横杠) 是本质的区别，它决定了系统是否为你初始化一个完整的“登录 Shell”。

| 命令组合 | 切换行为解析 |
| :--- | :--- |
| **`su root`** | 切换为 root 身份，但 **不改变当前的工作目录 (pwd)**，且 **不加载** root 的环境变量文件 (`~/.bash_profile` 等)。你依然身处旧环境中。 |
| **`su - root`** <br> *(同 `su -l root`)* | **完全登录模式**。不仅身份切换为 root，工作目录也会被重定向到 `/root`。系统会初始化一个完全隔离的登录 Shell，加载属于 root 的所有环境变量。 |

---

## 3. `sudo` 高阶 Shell 提权 (`-s` vs `-i`)

除了在单条命令前加 `sudo`（如 `sudo systemctl restart nginx`），运维人员也常利用 `sudo` 开启交互式的高权限终端。此时，参数的选择同样决定了环境的纯粹度。

| 命令组合 | 底层机制与环境变量表现 |
| :--- | :--- |
| **`sudo -s`** | 以 root 身份拉起一个新的交互式 Shell。**不切换当前工作目录 (pwd)**。它会 **保留并继承** 大量原用户的环境变量。注意：原用户 `~/.bashrc` 中的配置可能依然生效，容易导致依赖错乱。 |
| **`sudo -i`** | 以 root 身份拉起一个新的 **登录 Shell**。行为类似于 `su - root`。工作目录切换为 `/root`，并丢弃大部分原用户的环境，**彻底加载 root 用户的全套配置**。这是保证环境纯净执行的最优解。 |

### 3.1. `sudo` 直接运行脚本的环境陷阱

- **`sudo -s [command]`**：以提权的非登录 Shell 运行指令。如果指令依赖特定环境变量（如某些特定语言的 Path），将会因环境不完整而报错。
- **`sudo -i [command]`**：以提权的登录 Shell 运行指令。如果是运行 Bash 脚本，该脚本将在一个完全初始化（`source /etc/profile` 等）的完备环境中执行。
