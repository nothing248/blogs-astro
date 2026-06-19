---
status: completed
filename: ubuntu-linux-initialization-and-operations-guide
title: "Ubuntu 初始化"
summary: 本笔记总结了全新安装 Ubuntu Linux 服务器后的标准初始化与排障运维流程。详细提供了替换国内 APT 镜像源（以阿里云 Jammy 为例）及配置免密 Sudo 用户的脚手架命令。深入探讨了基于 Netplan 的现代网络配置，并涵盖了通过 `sshd_config` 开启 X11 转发实现 Windows/Mac 远程访问 Linux 图形化应用的方法。最后，针对服务器长期运行可能遭遇的 Systemd-journal 日志占用过多磁盘及 20 分钟自动挂起问题，给出了底层的清理与服务禁用解决方案。
aliases: [Ubuntu 初始化, Linux 换源, Ubuntu 网络配置, X11 转发]
tags: [Linux, Ubuntu, 运维部署, Netplan, APT, SSH, X11, Systemd]
date created: 星期一, 十二月 1日 2025, 9:59:24 上午
date modified: 星期四, 六月 18日 2026, 13:55:00 晚上
---

<!-- toc -->

## 1. 系统基础初始化 SOP

### 1.1. 替换国内 APT 镜像源 (以 Ubuntu 22.04 Jammy 为例)

原始源速度极慢，部署前首选替换为阿里云等国内源：

```bash
# 备份原配置
cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 写入阿里云镜像源
cat << 'EOF' > /etc/apt/sources.list
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
EOF

# 刷新索引并执行升级
apt update && apt upgrade -y
```

### 1.2. 用户与权限初始化

创建日常运维用户并赋予免密 `sudo` 权限（避免使用 root 直接操作）：

```bash
useradd -m -s /bin/bash yangxy 
passwd yangxy

# 修改 sudoers (推荐使用 visudo 确保语法安全)
echo "yangxy ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
```

---

## 2. 现代网络配置 (Netplan)

Ubuntu 抛弃了传统的 `/etc/network/interfaces`，全面转向 YAML 格式的 Netplan 引擎。

1. **查看网卡**：`ip link show`
2. **编辑配置**：修改 `/etc/netplan/` 目录下的 YAML 文件（如 `50-cloud-init.yaml`）。
3. **安全赋权**：`chmod 600 /etc/netplan/*.yaml`
4. **应用测试**：

   ```bash
   netplan try    # 测试配置，如果失去连接，几秒后会自动回滚
   netplan apply  # 永久应用生效
   ```

> [!warning] 云端实例配置覆盖坑点
> 如果重启后发现自定义的 Netplan 配置丢失，通常是被云服务商的 `cloud-init` 进程还原了。
> 需在 `/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg` 中写入：`network: {config: disabled}` 以接管控制权。

---

## 3. 远程桌面与图形化透传 (X11 Forwarding)

当需要在没有显示器的服务器上运行 Linux 图形化应用（如 IDE、浏览器），并将窗口直接显示在本地 Mac/Windows 电脑上时，可使用 SSH 的 X11 转发功能。

### 3.1. 服务端配置 (Ubuntu)

编辑 `/etc/ssh/sshd_config`：

```ini
X11Forwarding yes
```

*执行 `systemctl restart sshd` 生效。*

### 3.2. 本地客户端配置

- **Mac 用户**：安装开源的 `XQuartz` 服务。
- **Windows 用户**：安装 `VcXsrv` 或 `Xming` 并在后台运行。

**本地终端连接命令**：

```bash
ssh -X user@your_ubuntu_ip
# 登录后直接在终端输入图形化应用命令（如 gedit），窗口将自动在你的本地电脑上弹出！
```

*(注：Windows 下使用 Xming 时，若遇到本地 localhost IPv6 解析优先导致的连接失败，需配置系统的 DNS 解析顺序。)*

---

## 4. 系统级排障与优化

### 4.1. 解决服务器 20 分钟自动挂起断网

若通过 `journalctl` 发现报错 `system is about to suspend`，说明服务器因无物理按键操作自动休眠了。
**解法**：彻底屏蔽系统的休眠内核服务：

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

### 4.2. Systemd-Journald 日志无限膨胀导致磁盘枯竭

`systemd` 接管了所有服务日志，默认可能会吞噬大量磁盘空间。

```bash
# 查看当前日志体积
journalctl --disk-usage 

# 紧急瘦身：仅保留 100M
journalctl --vacuum-size=100M

# 彻底关闭本地落盘 (慎用)：
# 修改 /etc/systemd/journald.conf，设置 Storage = none 并 systemctl restart systemd-journald
```

### 4.3. 一键挂载终端全局网络代理

在 `/etc/profile` 或 `~/.bashrc` 中注入 alias 快捷指令：

```bash
alias proxy='export http_proxy=http://192.168.56.1:2080 && export https_proxy=http://192.168.56.1:2080'
alias unproxy='unset http_proxy; unset https_proxy' 
```
