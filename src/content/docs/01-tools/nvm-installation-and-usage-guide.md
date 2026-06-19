---
title: "Node版本管理"
filename: nvm-installation-and-usage-guide
summary: NVM (Node Version Manager) 是管理 Node.js 版本的必备工具。本文涵盖了 Windows、macOS 及 Linux 环境下的安装方法，特别是针对 Linux 环境下的全局安装策略进行了详细说明。同时整理了 NVM 的常用命令（如版本切换、LTS 安装）以及解决 npm 缺失问题的实战方案，并介绍了如何在 WebStorm 中关联 NVM 管理的 Node 环境。
tags: [nvm, nodejs, javascript, development-tools, linux-admin]
aliases: [Node版本管理, NVM安装教程]
status: completed
date created: 星期二, 三月 24日 2026, 3:38:05 下午
date modified: 星期五, 六月 19日 2026, 12:06:45 中午
---

<!-- toc -->

## 1. 简介

NVM (Node Version Manager) 允许用户在同一台机器上安装和切换多个 Node.js 版本，有效解决了不同项目对 Node 版本依赖不一致的问题。

## 2. 安装指南

### 2.1. Windows 安装

Windows 用户建议使用 `nvm-windows`：

- [下载地址 (GitHub Releases)](https://github.com/coreybutler/nvm-windows/releases)

### 2.2. macOS 安装

推荐使用官方安装脚本：

```shell
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

### 2.3. Linux 全局安装

若需所有系统用户共用一个 NVM 环境：

```shell
su root
mkdir /usr/local/nvm
export NVM_DIR=/usr/local/nvm
# 执行安装脚本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash 

# 将以下配置添加到 /etc/profile 或 /etc/bash.bashrc
export NVM_DIR="/usr/local/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # 加载 nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # 加载 bash_completion
```

> [!warning]
> **覆盖注意**：若普通用户自行安装过 NVM，其 `~/.bashrc` 中的配置会覆盖全局配置。如需使用全局版本，请注释掉个人配置文件中的 NVM 相关行。

## 3. 常用命令

| 命令 | 说明 |
| :--- | :--- |
| `nvm ls-remote` | 列出远程服务器上所有可用的 Node 版本 |
| `nvm list` | 列出本地已安装的 Node 版本 |
| `nvm install --lts` | 安装最新的长期支持版本 (LTS) |
| `nvm install 11.13.0` | 安装指定版本 |
| `nvm use 11.13.0` | 切换到指定版本 |
| `nvm uninstall 11.13.0` | 卸载指定版本 |

## 4. 常见问题处理

### 4.1. Node 安装成功但 Npm 缺失

- **现象**：执行 `node -v` 正常，但 `npm -v` 提示命令未找到。
- **原因**：通常由于网络问题导致 npm 压缩包下载中断或失败。
- **解决方案**：
  1. **重试**：更换网络环境（或设置国内镜像源）后重新执行安装。
  2. **手动补全**：检查 NVM 安装目录下的 `temp` 目录，看是否有已下载的 npm zip 包，手动解压到对应版本的 `node_modules` 目录下。

## 5. 进阶技巧

### 5.1. 关联 IDE (WebStorm)

在 WebStorm 中配置 NVM 路径：
`Preferences | Languages & Frameworks > Node.js and NPM` -> 在 `Node interpreter` 中选择 NVM 路径下的具体版本。

## 6. 参考资料

- [nvm-sh 官方 GitHub](https://github.com/nvm-sh/nvm)
- [nvm-windows 官方 GitHub](https://github.com/coreybutler/nvm-windows)
