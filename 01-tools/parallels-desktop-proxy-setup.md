---
title: "Parallels代理配置"
filename: parallels-desktop-proxy-setup
description: Parallels Desktop 是一款专为 Mac 用户设计的虚拟机软件，支持流畅运行 Windows、Linux 等操作系统。本文聚焦于一个核心实战技巧：如何让虚拟机中的 Windows 系统通过宿主机 Mac 的代理软件联网。涵盖了网络模式切换（桥接 WIFI）以及局域网代理的具体配置步骤，适用于需要在虚拟机中进行科学上网或访问内网资源的场景。
tags: [parallels-desktop, virtualization, macos, networking, windows]
aliases: [Parallels代理配置, Mac虚拟机联网]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:23 下午
date modified: 星期五, 六月 19日 2026, 12:07:22 中午
---

<!-- toc -->

## 1. 简介

Parallels Desktop 是一款在 Mac 平台上性能卓越的虚拟化软件，允许用户在不重启的情况下，在 macOS 中同时运行 Windows 和其他操作系统。其深度集成特性使得文件共享、剪贴板同步和硬件调用极其便捷。

## 2. 进阶技巧：使用宿主机代理

在某些开发或测试环境下，需要虚拟机（如 Windows）使用 Mac 宿主机上的代理软件（如 Clash, V2RayU 等）进行联网。

### 2.1. 切换网络模式

为了让虚拟机能正确识别宿主机的 IP 地址，建议使用桥接模式：

- 操作路径：`Parallels Desktop 菜单` > `设备` > `网络` > `选择：桥接网络 (Wi-Fi/以太网)`。

### 2.2. 宿主机准备

确保你的代理软件已开启 **“允许来自局域网的连接 (Allow connections from LAN)”**。

- 获取宿主机 IP：在 Mac 终端运行 `ifconfig`，找到对应网卡的 IP 地址（例如 `192.168.1.100`）。

### 2.3. 虚拟机配置

在虚拟机中的 Windows 系统内进行如下设置：

- 打开 `设置` > `网络和 Internet` > `代理`。
- 开启 `手动代理设置`。
- **地址 (Address)**：填入宿主机 IP（如 `192.168.1.100`）。
- **端口 (Port)**：填入代理软件监听的局域网端口（通常为 `7890` 或 `1080`）。

> [!note]
> **防火墙注意**：如果配置后仍无法联网，请检查 Mac 宿主机的防火墙设置，确保其没有拦截来自局域网的代理请求。

## 3. 参考资料

- [Parallels Desktop 官方网站](https://www.parallels.cn/)
- [Parallels 网络模式文档](https://kb.parallels.com/4948)
