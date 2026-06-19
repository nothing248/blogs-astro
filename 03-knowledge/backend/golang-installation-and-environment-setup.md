---
status: completed
filename: golang-installation-and-environment-setup
title: "Go 安装教程"
summary: 本笔记记录了 Go 语言开发环境的跨平台基础配置指南。涵盖了在 Windows 系统下通过 MSI 安装包的部署流程，以及在 Linux 环境下通过源码压缩包解压、配置 PATH 环境变量的标准 SOP。此外，重点提供了针对国内网络环境设置 `GOPROXY`（如 goproxy.cn）的配置指令，为快速搭建 Go 语言高效开发环境提供参考。
aliases: [Go 安装教程, Golang 环境变量配置, GOPROXY 设置]
tags: [Golang, Go 语言, 环境配置, 后端开发, 运维部署, Linux]
date created: 星期一, 五月 19日 2025, 2:05:21 下午
date modified: 星期四, 六月 18日 2026, 9:25:00 晚上
---

<!-- toc -->

## 1. 跨平台安装指南

### 1.1. Windows 环境安装

直接下载并运行官方提供的 MSI 安装程序即可自动完成配置：

```powershell
wget https://go.dev/dl/go1.23.4.windows-amd64.msi 
```

### 1.2. Linux 环境安装 (以 Ubuntu/CentOS 为例)

在 Linux 下通常推荐通过压缩包手动解压并注入环境变量：

```bash
# 1. 下载指定版本的压缩包
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz

# 2. 清理旧版本并解压到 /usr/local 目录
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz

# 3. 注入系统环境变量
echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile

# 4. 使环境变量立即生效
source /etc/profile
```

---

## 2. 环境验证与加速配置

### 2.1. 验证安装

安装完成后，检查版本以确保环境变量配置正确：

```bash
go --version 
# 预期输出类似：go version go1.23.4 linux/amd64
```

### 2.2. 国内模块代理配置 (GOPROXY)

为了解决国内拉取 Go Modules 依赖过慢的问题，强烈建议配置国内加速镜像：

```bash
# 启用模块支持并设置代理池
go env -w GOPROXY=https://goproxy.cn,direct 
```

## 3. 参考资料

- [Go 语言官方主页](https://go.dev/)
