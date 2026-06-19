---
title: "ShellCrash脚本"
filename: shellclash-installation-guide
summary: ShellCrash 是一款专为 Linux 系统（如路由器、NAS 及服务器）设计的 Clash 管理脚本。它支持多种架构，提供简单直观的交互式命令行界面，能够快速安装和配置 Clash 内核，实现全网透明代理。本文记录了其一键安装流程及注意事项，是 Linux 用户实现自动化网络分流的高效方案。
tags: [linux, proxy, clash, shell]
aliases: [ShellCrash脚本]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:21 下午
date modified: 星期五, 六月 19日 2026, 12:08:35 中午
---

<!-- toc -->

## 1. 简介

ShellCrash（原名 ShellClash）是一个基于 Shell 的 Clash 服务端管理工具，广泛应用于各种基于 Linux 的嵌入式设备或服务器。它以轻量化和高度兼容性著称，支持自动切换内核、订阅管理及规则过滤。

## 2. 安装

> [!warning]
> 请确保你有 root 权限。

使用以下命令执行一键安装脚本：

```shell
# 切换到 root 用户
sudo -i 

# 下载并运行安装脚本
export url='https://fastly.jsdelivr.net/gh/juewuy/ShellCrash@master'
wget -q --no-check-certificate -O /tmp/install.sh $url/install.sh && bash /tmp/install.sh && source /etc/profile &> /dev/null
```

安装完成后，直接在终端输入 `crash` 即可进入交互菜单。

## 3. 配置注意事项

- **内核匹配**：不同的 Clash 内核版本（如 Clash 核心版、Premium 版、Meta 版）对配置文件的格式要求可能存在细微差异。如果出现启动失败，请检查配置文件与当前内核的兼容性。
- **环境异常**：若遇到代理节点在手机端正常但服务器端失效，通常是由于配置文件路径、DNS 劫持策略或加密协议不匹配导致。

## 4. 参考资料

- [ShellCrash 官方博客（常见问题）](https://juewuy.github.io/chang-jian-wen-ti/)
- [ShellCrash GitHub 仓库](https://github.com/juewuy/ShellCrash)
