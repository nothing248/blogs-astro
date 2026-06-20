---
title: "SFTPGo配置指南"
filename: sftpgo-file-transfer-setup
description: SFTPGo 是一款高性能、事件驱动的全能文件传输服务器。它支持 SFTP、FTP/S、HTTP/S 及 WebDAV 协议，并兼容本地文件系统、S3 及 Azure 等多种存储后端。本文详细介绍了在 Ubuntu 和 CentOS 上的安装流程、基于 SQLite 的核心配置，以及多用户管理与目录权限的初始化步骤。
tags: [sftp, file-transfer, server-admin, storage]
aliases: [SFTPGo配置指南]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:56 上午
date modified: 星期五, 六月 19日 2026, 12:08:33 中午
---

<!-- toc -->

## 1. 简介

SFTPGo 是一种高效、可扩展且事件驱动的文件传输解决方案。它不仅支持多种传输协议，还提供了强大的统一管理面板。

- **多存储后端**：支持本地磁盘、S3 兼容对象存储、Google Cloud Storage、Azure Blob 等。
- **多协议支持**：SFTP, SCP, FTP/S, WebDAV, HTTP/S。
- **事件驱动**：支持在文件上传、下载等事件触发时执行自定义操作。
- **统一管理**：提供功能丰富的 Web 后端，用于管理用户、分组、虚拟目录及带宽配额。

## 2. 安装与管理

### 2.1. 操作系统安装

#### 2.1.1. Ubuntu (PPA)

```shell
sudo add-apt-repository ppa:sftpgo/sftpgo
sudo apt update
sudo apt install sftpgo
```

#### 2.1.2. CentOS (Yum)

```shell
ARCH=`uname -m`
curl -sS https://ftp.osuosl.org/pub/sftpgo/yum/${ARCH}/sftpgo.repo | sudo tee /etc/yum.repos.d/sftpgo.repo
yum update
yum install sftpgo
```

### 2.2. 服务管理

使用 `systemctl` 对服务进行常规操作：

```shell
systemctl start sftpgo
systemctl status sftpgo
systemctl restart sftpgo
```

## 3. 核心配置

### 3.1. 配置文件调整 (`/etc/sftpgo/sftpgo.json`)

```json
{
  "httpd": {
    "bindings": [
      {
        "port": 8080 // Web 管理后台与客户端端口
      }
    ]
  },
  "data_provider": {
    "driver": "sqlite", // 数据库驱动，默认为 sqlite，也可选择 mysql/pgsql
    "name": "/var/lib/sftpgo/sftpgo.db"
  },
  "sftpd": {
    "bindings": [
      {
        "port": 2022, // SFTP 服务监听端口
        "address": "",
        "apply_proxy_config": true
      }
    ]
  }
}
```

### 3.2. 存储目录准备

```shell
# 创建物理存储根目录
mkdir -p /data/sftpgo
chown sftpgo:sftpgo /data/sftpgo/ 
```

## 4. 用户管理初始化

1. **管理员设置**：访问 `http://[IP地址]:8080/web/admin/setup` 初始化管理员账号。
2. **创建主管理员用户**：
   - 用户名：`[管理员A]`
   - 家目录：`/data/sftpgo/`
3. **创建子用户**：
   - 用户名：`[用户X]`
   - 家目录：`/data/sftpgo/home/[用户X]`
4. **目录结构规范**：
   - 在主管理员账号下通过 Web 客户端创建 `home/` 文件夹。
   - 最终结构应为：`/data/sftpgo/home/[用户X]`，确保主管理员可统一审计，子用户仅访问其特定空间。

## 5. 参考资料

- [SFTPGo 官方文档 - 虚拟目录](https://docs.sftpgo.com/devel/virtual-folders/)
- [SFTPGo GitHub 项目地址](https://github.com/drakkan/sftpgo)
