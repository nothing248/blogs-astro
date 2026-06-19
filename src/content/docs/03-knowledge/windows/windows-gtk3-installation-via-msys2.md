---
title: "GTK3 安装"
status: pending
filename: windows-gtk3-installation-via-msys2
aliases: [GTK3 安装, MSYS2 配置]
tags: [Windows, GUI 开发, GTK3, MSYS2, C++]
date created: 星期一, 十二月 1日 2025, 9:59:21 上午
date modified: 星期四, 六月 18日 2026, 11:45:00 晚上
---

<!-- toc -->

## 1. 待完善：Windows 环境下 GTK+3.0 安装指南

本笔记记录了在 Windows 系统下通过 MSYS2 工具链安装 GTK+3.0 图形库的过程。

### 1.1. 操作步骤

1. **安装 MSYS2**：从官网 (`https://www.msys2.org/`) 下载并安装（推荐路径 `d:/msys2`）。
2. **Pacman 安装命令**：

   ```bash
   pacman -S mingw-w64-ucrt-x86_64-gtk3
   ```

3. **环境变量配置**：需将 MinGW 的 bin 目录添加到系统的 Path 中。

![](http://qiniu.sxyxy.top/20250723121207.png)

1. **验证安装**：执行 `pkg-config --cflags gtk+-3.0`。
