---
title: "AList"
filename: alist-multi-cloud-storage
aliases: ["AList", "云盘挂载", "多盘管理工具"]
tags: ["AList", "云存储", "文件管理", "Linux运维", "Nginx"]
status: completed
description: AList 是一款强大的多云盘文件列表程序，支持多种存储（如阿里云盘、Google Drive、OneDrive等），通过 WebDAV 协议进行文件管理和分享。本笔记详细介绍了在 Linux 环境下的快速安装部署流程，包括使用官方脚本进行一键安装、`systemctl` 服务管理命令，以及如何配置 Nginx 反向代理以实现 HTTPS 访问和自定义域名，有效解决了跨云盘文件统一管理与安全暴露的需求。
date created: 星期二, 一月 13日 2026, 9:31:08 上午
date modified: 星期五, 六月 19日 2026, 11:57:05 中午
---

<!-- toc -->

## 1. AList：多云盘文件列表程序概述

**AList** 是一个功能强大的文件列表程序，它支持挂载多种云存储（包括但不限于阿里云盘、Google Drive、OneDrive、WebDAV 等），并提供统一的 Web 界面进行文件管理、预览和分享。通过 AList，用户可以轻松实现个人或团队在不同云存储服务之间的文件统一管理，极大提升了工作效率和数据整合能力。

## 2. 安装与部署

### 2.1. Linux 环境安装

AList 在 Linux 系统上的安装过程非常便捷，推荐使用官方提供的一键安装脚本。

#### 2.1.1. 快速安装脚本

执行以下 `curl` 命令，下载并运行 AList 的自动安装脚本：

```shell
curl -fsSL "https://alistgo.com/v3.sh" -o v3.sh && bash v3.sh
```

> [!note] 安装说明
> 该脚本会自动检测系统环境并安装 AList，通常还会配置为 systemd 服务，方便后续管理。安装完成后，会提示初始的管理用户名和密码，请务必妥善保存。

#### 2.1.2. 服务管理 (Systemd)

AList 安装后通常会注册为系统服务，可以使用 `systemctl` 命令进行服务的启动、停止、重启和查看状态：

```shell
# 启动 AList 服务
systemctl start alist

# 停止 AList 服务
systemctl stop alist

# 查看 AList 服务状态
systemctl status alist

# 重启 AList 服务
systemctl restart alist
```

### 2.2. 反向代理配置 (Nginx)

为了通过自定义域名和 HTTPS 安全访问 AList，推荐配置 Nginx 反向代理。以下是一个基本的 Nginx 配置示例：

```nginx
server {
  listen 80;
  server_name [你的域名].top; # 替换为你的实际域名，例如 alist.example.com

  location / {
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;
   proxy_set_header Host $http_host;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header Range $http_range;
   proxy_set_header If-Range $http_if_range;
   proxy_redirect off;
   proxy_pass http://127.0.0.1:5244; # AList 默认运行端口
   # 允许上传的最大文件大小，根据需要调整
   client_max_body_size 20000m;
  }
}
```

> [!tip] HTTPS 配置
> 建议为你的域名配置 SSL 证书（如通过 Let's Encrypt），并将 `listen 80` 改为 `listen 443 ssl`，并添加 SSL 证书路径配置，以启用 HTTPS 加密访问。

## 3. 拓展信息

AList 提供了丰富的插件和功能，用户可以根据需求进一步探索其 WebDAV 挂载、文件分享、用户权限管理等高级特性。

## 4. 参考资料

- [AList 官方网站](https://alistgo.com/zh/)
- [AList 反向代理配置指南](https://alistgo.com/zh/guide/install/reverse-proxy.html)
- [AList GitHub 项目](https://github.com/AlistGo/alist/blob/main/README_cn.md)
