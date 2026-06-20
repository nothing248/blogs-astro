---
title: "sftp-setup"
filename: sftp-server-setup-and-protocol-comparison
description: 本文对比了 FTP、SFTP、FTPS、SCP、SMB 和 WebDAV 等文件传输协议，并以 CentOS 系统为例，详述了如何通过配置 OpenSSH 搭建高安全性的 SFTP 隔离服务。包含受限权限用户创建、根目录 Chroot 严苛所有权与权限控制、sshd_config 规则配置、SFTP 客户端使用及因目录权限过大导致的免密失效（secure 日志）排查方法。
tags:
  - sftp
  - openssh
  - file-transfer
  - chroot
  - centos
  - protocol-comparison
aliases:
  - sftp-setup
  - sftp-guide
  - sftp-chroot
status: completed
---

<!-- toc -->

## 1. 简介

**SFTP**（SSH File Transfer Protocol）是运行在 SSH 协议之上的安全文件传输协议。与传统的 FTP 协议不同，SFTP 的所有传输数据都经过加密，并且仅使用单一的 SSH 默认通道即可完成连接和数据传输。

## 2. 常见文件传输协议对比

| 协议名称 | 运行基础 | 加密性 | 典型特征与场景 |
| :--- | :--- | :--- | :--- |
| **FTP** | TCP 21 (控制) + 随机端口 | 无加密 | 最早期的文件传输协议，支持上传/下载/目录管理，但数据及凭据明文传输，极不安全。 |
| **SFTP** | SSH 协议 (通常端口 22) | 强对称加密 | 随 SSH 服务自带，配置简单，安全性高，广泛用于 Linux 主机间的文件安全交换。 |
| **FTPS** | FTP + SSL/TLS | 强非对称加密 | FTP 的安全扩展版本，数据通过 SSL 加密传输，多用于需要严格防火墙规则的企业外部网。 |
| **SCP** | SSH 协议 | 强对称加密 | 基于 SSH 传输单个文件或目录的简易命令行工具，相比 SFTP 缺少交互式文件管理功能。 |
| **SMB** | TCP 445 (Samba) | 可选加密 | 局域网网络文件共享协议，支持多终端在线挂载编辑，主要在 Windows 局域网生态中使用。 |
| **WebDAV** | HTTP / HTTPS | 可选加密 | 基于 HTTP 的扩展协议，允许客户端进行协同文件编辑，适合云盘或知识库的挂载连接。 |

---

## 3. 搭建安全的 SFTP 隔离服务器

以 CentOS/RHEL 发行版为例，我们将构建一个限制用户的 Shell 登录、且将其文件访问范围限制在指定目录（Chroot）的 SFTP 服务。

### 3.1. 创建受限用户组与用户

```shell
# 创建 sftp 专用的用户组
groupadd sftp

# 创建只读/下载用户，指定 /bin/false 禁用 shell 交互式登录
useradd -m -s /bin/false -G sftp sftp_down

# 创建可上传用户，同样禁用 shell 登录
useradd -m -s /bin/false -G sftp sftp_up

# 为新用户设置安全密码
passwd sftp_down
passwd sftp_up
```

### 3.2. 创建并配置共享目录权限

> [!IMPORTANT]
> **ChrootDirectory 权限要求**：
> SFTP 根目录的所有者必须是 `root`，且该目录及其向上的所有父目录的权限不能对组或其他用户开放写权限（最大权限为 `755`），否则 SSH 登录会直接报错失败。

```shell
# 创建 SFTP 主共享根目录以及专门用于上传的子目录
mkdir -p /sftp_share/upload_test

# 1. 根共享目录所有权必须为 root
chown root:sftp /sftp_share
chmod 755 /sftp_share

# 2. 只有内部子目录才可以赋予普通上传用户写权限
chown sftp_up:sftp /sftp_share/upload_test
chmod 755 /sftp_share/upload_test
```

### 3.3. 配置 sshd 服务

编辑 `/etc/ssh/sshd_config` 配置文件，在文件末尾追加 SFTP 规则：

```text
# 启用内置的 SFTP 子系统（替换旧的外部 sftp 模块）
Subsystem sftp internal-sftp

# 匹配属于 sftp 用户组的所有连接用户
Match Group sftp
    # 将用户的根目录锁定在共享根目录下
    ChrootDirectory /sftp_share
    # 强制仅能执行 SFTP 内置命令，防止用户建立 SSH 会话
    ForceCommand internal-sftp
    # 禁用端口转发，防止通道滥用
    AllowTcpForwarding no
    X11Forwarding no
```

### 3.4. 重新启动 SSH 服务

```shell
# 在重启前检查配置文件语法正确性
sshd -t

# 重启 sshd 服务使配置生效
systemctl restart sshd
```

---

## 4. SFTP 客户端使用指南

### 4.1. 连接命令

可以使用私钥与特定端口连接目标 SFTP 服务器：

```shell
sftp -oPort=22 -oIdentityFile=~/.ssh/id_rsa_sftp user@192.168.1.100
```

### 4.2. 常用交互命令

连接成功后，可输入 `?` 获取内置命令列表：

![SFTP 客户端帮助列表](https://qiniu.sxyxy.top/20230825114811.png?image=image)

---

## 5. 典型故障排查：免密登录失效

### 5.1. 问题现象

客户端配置了 SSH 公钥，但登录 SFTP/SSH 时依然强制提示输入密码。在服务端查看日志（`/var/log/secure` 或 `/var/log/auth.log`）通常可见如下错误：

```text
Authentication refused: bad ownership or modes for directory /home/username/.ssh
```

### 5.2. 解决方案

SSH 对用户家目录及密钥配置文件的权限控制有极严苛的安全校验。需要修复并调小权限：

```shell
# 1. 确保用户家目录不能被其他用户写入
chmod go-w /home/username

# 2. 确保 .ssh 目录仅所有者可读写执行
chmod 700 /home/username/.ssh

# 3. 确保公钥信任文件仅所有者可读写
chmod 600 /home/username/.ssh/authorized_keys
```

---

## 6. 拓展技术专题

### 6.1. Chroot 命令原理解析

`chroot`（Change Root）指令用于在指定的根目录下运行特定的程序。其核心价值在于：

- **增强系统隔离**：为特定进程搭建虚假的根目录结构，防止恶意程序读取或篡改系统级核心文件（如 `/etc`）。
- **建立沙箱测试环境**：方便为多版本依赖包提供彼此隔离的独立目录运行环境。
- **系统引导救急**：在系统挂掉时，用 LiveCD 挂载硬盘系统并 `chroot` 进入环境重新安装引导（GRUB）或修改管理员密码。

### 6.2. 基于 Python 快速搭建临时 FTP 服务器

在没有专门文件服务器时，可利用 Python 模块快速启动一个供局域网传文件的小工具：

```shell
# 安装极速 FTP 运行模块
pip install pyftpdlib

# 在当前目录下以 2121 端口启动一个匿名只读 FTP 共享服务
python -m pyftpdlib -p 2121 -r
```

## 7. 参考资料

- [阿里云开发者社区 - 快速搭建安全 SFTP 服务教程](https://developer.aliyun.com/article/1242857)
- [Linux Story - 如何在 Linux 下使用 SFTP 传输文件](https://linuxstory.org/how-to-use-sftp-to-securely-transfer-files-with-a-remote-server/)
