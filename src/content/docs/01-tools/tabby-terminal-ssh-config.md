---
title: "Tabby终端配置"
filename: tabby-terminal-ssh-config
description: Tabby 是一款现代化、可高度定制的开源终端模拟器，支持 SSH、Telnet 和串行连接。本文详细介绍了如何利用 Tabby 的 SSH RemoteForward 功能进行端口转化，使远程服务器能够通过本地代理访问受限资源。这是一套提升远程开发和运维灵活性的实用技巧。
tags: [terminal, ssh, proxy, tabby]
aliases: [Tabby终端配置]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:31 下午
date modified: 星期五, 六月 19日 2026, 12:08:56 中午
---

<!-- toc -->

## 1. 简介

Tabby (原名 Terminus) 是一款极具现代感的终端模拟器。它跨平台运行，支持丰富的插件系统和配色方案，是替代传统 SSH 客户端的绝佳选择。

## 2. 进阶技巧：利用 SSH RemoteForward 共享代理

在远程服务器没有外网访问权限，但本地机器有代理时，可以通过 Tabby 的 `RemoteForward` 功能将远程流量转发回本地代理端口。

### 2.1. 配置步骤

1. 在 Tabby 的 SSH 连接设置中，找到 **Port Forwarding** 或类似选项。
2. 添加一条 `RemoteForward` 规则，例如：将远程的 `10810` 端口转发到本地的 `127.0.0.1:10810`（假设本地代理监听在此端口）。
3. 连接成功后，在远程服务器的 shell 中设置环境变量：

```shell
# 在远程服务器执行
export http_proxy=http://127.0.0.1:10810
export https_proxy=http://127.0.0.1:10810

# 测试连接
curl https://www.google.com
```

![Tabby 端口转发配置示例](http://qiniu.sxyxy.top/20240419145308.png?image=blog)

## 3. 参考资料

- [Tabby 官方 GitHub 仓库](https://github.com/Eugeny/tabby)
