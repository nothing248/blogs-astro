---
status: completed
filename: lua-lightweight-scripting-language-setup
title: "Lua 安装"
description: 本笔记记录了轻量级脚本语言 Lua 的跨平台安装配置指南。涵盖了在 Windows 系统下通过开源安装包的一键部署，以及在 Linux (Ubuntu) 环境下通过 `apt` 包管理器直接安装或通过源码编译（Make）构建最新版本的标准步骤。Lua 因其极低的资源消耗与极快的执行速度，常被广泛应用于游戏引擎嵌入、Redis 原子脚本控制及 Nginx/OpenResty 流量扩展等高性能场景。
aliases: [Lua 安装, Lua 脚本语言, 嵌入式脚本]
tags: [Lua, 脚本语言, 开发环境, Nginx 扩展, Redis 脚本, 后端开发]
date created: 星期一, 五月 19日 2025, 2:05:20 下午
date modified: 星期四, 六月 18日 2026, 9:55:00 晚上
---

<!-- toc -->

## 1. 语言特性简介

Lua 是一种用标准 C 语言编写的轻量级、可扩展的脚本语言。其设计初衷是为了嵌入到其他宿主应用程序中（如 Redis 事务控制、Nginx/OpenResty 流量处理、游戏引擎逻辑层），为系统提供灵活的扩展和定制功能。

---

## 2. 跨平台环境安装

### 2.1. Windows 环境安装

推荐使用社区打包的安装程序进行一键部署：

```powershell
wget https://github.com/rjpcomputing/luaforwindows/releases/download/v5.1.5-52/LuaForWindows_v5.1.5-52.exe
# 下载后运行 exe 文件并配置系统环境变量
```

### 2.2. Linux 环境安装 (以 Ubuntu/CentOS 为例)

**方案 A：通过包管理器快速安装 (推荐旧版本兼容应用)**

```bash
apt install lua5.1 
```

**方案 B：源码编译安装 (推荐获取最新特性)**

```bash
# 1. 下载源码并解压
curl -L -R -O https://www.lua.org/ftp/lua-5.4.7.tar.gz 
tar zxf lua-5.4.7.tar.gz

# 2. 进入目录并执行编译
cd lua-5.4.7
make all test
```

### 2.3. 环境验证

在终端输入以下命令确认编译器版本：

```bash
lua -v
# 预期输出类似：Lua 5.4.7  Copyright (C) 1994-2024 Lua.org, PUC-Rio
```

## 3. 参考资源

- [Lua 官方文档与资源](https://www.lua.org/)
