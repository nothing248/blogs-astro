---
title: "ssh-guide"
filename: ssh-guide-and-best-practices
description: 本文系统梳理了 OpenSSH 安全远程登录协议的工作原理与实战指南。涵盖服务端安装配置、端口修改、客户端本地与远程端口转发（-L/-R）的实现语法；重点讲解了 ~/.ssh/config 进阶配置与多级跳板机透明代理工具 assh，对比了现代 Ed25519 与传统 RSA 密钥的安全性与生成命令，并提供 sshpass 及 ssh-agent 的密钥自动托管机制。
tags:
  - ssh
  - openssh
  - port-forwarding
  - assh
  - ed25519
  - security
aliases:
  - ssh-guide
  - ssh-tunnel
  - ssh-config
status: completed
---

<!-- toc -->

## 1. 简介

**SSH**（Secure Shell）是一种在不安全的网络上提供安全远程登录及其他安全网络服务的协议。[OpenSSH](http://www.openssh.com/) 是 SSH 协议的免费开源实现，是当前类 Unix 系统中最主流的远程管理工具。

## 2. 工作原理

SSH 建立连接并进行双向加密通信的过程如下：

1. **发起连接**：客户端向服务端发送联机请求。
2. **协商与传输公钥**：服务器将其自身的公钥发送给客户端。
3. **主机身份验证**：客户端对比服务器公钥是否与本地保存的哈希（`~/.ssh/known_hosts`）匹配，提示用户确认。
4. **会话密钥协商**：双方利用非对称加密算法协商出本次会话的对称密钥。
5. **双向加密通信**：建立安全通道，后续所有传输的数据包都使用对称密钥进行加密。

## 3. 核心组成与认证方式

### 3.1. 核心子协议

- **传输层协议**：提供服务器认证、机密性以及完整性校验。
- **用户认证协议**：向服务器验证客户端用户的合法身份。
- **连接协议**：将加密信息隧道复用为多个逻辑通道。

### 3.2. 认证方式

- **密码认证（口令认证）**：输入远程主机的用户密码。
- **密钥认证（免密登录）**：利用公钥/私钥对进行强身份认证，防范暴力破解。

## 4. 服务端部署与管理

### 4.1. 安装服务

在 Debian/Ubuntu 系统中安装 OpenSSH 服务端：

```shell
sudo apt update
sudo apt install openssh-server
```

### 4.2. 服务配置

编辑 SSH 服务端配置文件 `/etc/ssh/sshd_config` 可以调整监听端口（如将默认的 22 端口改为 23 端口）：

```text
# /etc/ssh/sshd_config
Port 23
```

### 4.3. 管理命令

使用 `systemd` 控制 SSH 服务的状态：

```shell
systemctl start ssh     # 启动服务
systemctl status ssh    # 查看状态
systemctl stop ssh      # 停止服务
```

---

## 5. 进阶使用：SSH 端口转发（隧道）

### 5.1. 本地端口转发 (`-L`)

将发送到本地特定端口的流量，通过 SSH 隧道转发到远程目标主机的指定端口上。

```shell
ssh -L <local_port>:<remote_host>:<remote_port> <ssh_server>
```

> [!NOTE]
> 适用于在本地访问远程内网的数据库或 Web 服务。

### 5.2. 远程端口转发 (`-R`)

将发送到远程服务器特定端口的流量，通过 SSH 隧道转发到本地目标主机的指定端口上。

```shell
ssh -R <remote_port>:<local_host>:<local_port> <ssh_server>
```

> [!NOTE]
> 常用于内网穿透，使公网服务器能访问内网本地开发机。

### 5.3. 密钥分发与免密登录

```shell
# 分发公钥到远程主机以实现免密登录
ssh-copy-id -i ~/.ssh/id_rsa.pub root@webserver1

# 指定特定私钥登录目标服务器
ssh -i ~/.ssh/id_rsa root@webserver1
```

---

## 6. 拓展进阶指南

### 6.1. 验证（Authentication）与授权（Authorization）

- **验证**：确认“你是谁”（即身份核实，如密码或密钥比对）。
- **授权**：确认“你能做什么”（即权限控制，如 `/etc/sudoers` 文件配置）。

### 6.2. sshpass 工具：脚本中的密码自动注入

`sshpass` 是一个免交互式输入密码的 SSH 登录工具，常用于编写需要旧设备兼容的运维脚本。

```shell
# 1. 命令行明文指定密码
sshpass -p "[密码已隐藏]" ssh user@192.168.1.10

# 2. 推荐方式：通过环境变量优雅读取，避免历史命令泄漏密码
export SSHPASS="[密码已隐藏]"
sshpass -e ssh user@192.168.1.10
```

### 6.3. ssh-agent：密钥守护进程

用于管理私钥。当私钥设置了 passphrase 密码保护时，`ssh-agent` 可以缓存私钥解密状态，避免每次连接都重复输入密钥密码。

```shell
ssh-agent bash          # 以新 Shell 方式启动守护进程
eval "$(ssh-agent -s)"  # 以后台进程启动守护进程并导出变量
ssh-add ~/.ssh/id_rsa   # 将指定的私钥添加到 agent 缓存中
ssh-add -l              # 列出当前 agent 缓存的密钥列表
ssh-add -D              # 从当前缓存中移除所有已添加的密钥
ssh-agent -k            # 终止 ssh-agent 服务进程
```

### 6.4. 客户端配置文件 `~/.ssh/config`

通过配置 `~/.ssh/config`，可以为常用的服务器设置别名，简化连接命令，并配置心跳包防止连接卡死。

```text
# 全局默认配置
Host *
    ServerAliveInterval 60    # 每 60 秒发送一次心跳包，防止终端因空闲断开
    ServerAliveCountMax 3     # 允许最大心跳无响应次数为 3
    Compression yes            # 开启网络传输压缩，优化慢网下的传输效率

# 针对特定服务器的别名配置
Host web-prod
    HostName 192.168.100.5
    User yangxy
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes          # 启用密钥转发，使该远程连接能继续调用本地 agent 的密钥
```

之后，你可以使用非常精简的命令直接登录：

```shell
ssh web-prod
```

### 6.5. assh (Advanced SSH Config)：高级透明代理管理

`assh` 是一款基于 Go 语言编写的 SSH 配置辅助工具。它通过更现代的 `~/.ssh/assh.yml` 配置文件，在底层自动将 YAML 配置转换为原生 SSH 配置。特别适合管理复杂的跳板机拓扑网络。

```yaml
# ~/.ssh/assh.yml 配置文件示例
templates:
  base:
    User: root
    Port: 22

hosts:
  # 堡垒机/跳板机配置
  bastion:
    Inherits: base
    HostName: 203.0.113.1

  # 内部网络私有服务器，通过 bastion 自动代理连接
  internal-db:
    Inherits: base
    HostName: 10.0.0.5
    Gateways: [bastion] # 一行配置，SSH 客户端将自动走堡垒机透明代理
```

配置好之后，终端直接运行如下命令即可无缝穿透跳板机：

```shell
ssh internal-db
```

### 6.6. 现代 Ed25519 与传统 RSA 密钥对比

在生成 SSH 密钥对时，建议根据设备兼容性优先选择现代的加密算法。

| 特性维度 | Ed25519 (现代首选) | RSA (传统兼容) |
| :--- | :--- | :--- |
| **数学原理** | 扭曲爱德华曲线（ECC 椭圆曲线密码学） | 大数质因数分解（传统非对称） |
| **密钥长度** | 固定 256 位 | 建议至少 3072 位或 4096 位 |
| **安全性级别** | 极高（256 位抗暴力破解性能优异） | 高（但 2048 位安全性已降低） |
| **计算性能** | 极快（几乎瞬间生成与验证，CPU 开销小） | 较慢（高位密钥对 CPU 的开销相对较大） |
| **公钥大小** | 极小（约 68 字符，复制粘贴体验极佳） | 极大（一长串密集的字符块） |
| **设备兼容性** | 广泛兼容现代云平台、Linux 和 GitHub | 完美兼容所有古董设备、旧路由器和嵌入式系统 |

```shell
# 生成现代强安全性的 Ed25519 密钥（强烈推荐）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 生成兼容旧设备的传统 RSA 4096 位高强度密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

## 7. 运维最佳实践总结

1. **优先使用密钥登录**：关闭远程 SSH 服务端的密码登录选项（`PasswordAuthentication no`），仅允许密钥访问，规避暴力破解。
2. **选择现代加密算法**：在新部署的主机上，优先生成并分发 `Ed25519` 密钥。
3. **统一配置管理**：使用本地 `~/.ssh/config` 配置文件管理服务器别名；在多跳板机内网环境中配合 `assh` 或配置 `ProxyJump` 指令，实现高效的一键登录。

## 8. 参考资料

- [骏马金龙 - SSH 系列进阶教程](https://www.cnblogs.com/f-ck-need-u/p/10484531.html)
