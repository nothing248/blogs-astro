---
title: "WSL2安装"
filename: wsl2-linux-subsystem-setup
summary: WSL2是Windows Subsystem for Linux的升级版，允许在Win下以原生性能运行Linux内核。本文列出WSL2的配置流程，包括分区分离安装、默认发行版指定、使用wsl.conf进行虚拟网卡及网络端口映射优化，以及通过编写自定义配置文件实现跨平台环境与容器无缝集成。
tags: [wsl2, windows-subsystem-for-linux, virtualization, system-integration]
aliases: [WSL2安装, WSL命令行, Linux子系统配置]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:09:26 中午
---

<!-- toc -->

## 1. 简介

一个 windows 运行 Linux 环境

## 2. 安装

```shell
wsl --list --online #查看可用的系统版本
wsl --install -d version_name # 安装指定的系统版本 (可能需要执行两次) #会直接安装到 C 盘中
wsl --list --verbose # 查看当前已经安装的系统版本
wsl --set-version <distribution name> <versionNumber> #设置版本号
wsl --set-default <DistributionName> #设置默认系统
wsl --set-default-version <Version#> # 设置默认版本号
```

## 3. 自定义安装 wsl

- 保留数据

```shell
wsl --shutdown #关闭
wsl --export Ubuntu D:\wsl\ubuntu\ubuntu.tar # 导出
wsl --unregister Ubuntu #卸载
wsl --import Ubuntu D:\wsl\ubuntu D:\wsl\ubuntu\ubuntu.tar --version 2
```

## 4. 运行

```shell
wsl ~ #以home 目录运行
wsl --distribution <Distribution Name> --user <User Name> # 指定版本与用于运行
wsl --status #查看 wsl 配置信息
wsl --version #查看版本号
wsl --shutdown #停止所有虚拟机
wsl --terminate <Distribution Name> # 停止特定虚拟机
wsl --export <Distribution Name> <FileName> #导出发行版
wsl --import <Distribution Name> <InstallLocation> <FileName> #导入发行版
wsl --unregister <DistributionName> #注销发行版
wsl --mount <DiskPath> #装载磁盘与设备
wsl --unmount <DiskPath> # 卸载磁盘
```

## 5. 完善系统

- 更新源

```shell
cp /etc/apt/sources.list /etc/apt/sources.list.bak
vim /etc/apt/sources.list
# 替换为一下内容
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
# 更新源
apt update && apt upgrade -y
# 添加用户权限
sudo echo "yangxy ALL=(ALL) NOPASSWD: ALL" >>/etc/sudoers
```

## 6. 修改配置信息

```shell
# /etc/wsl.conf
[boot]
systemd=true
[network]
hostname=slave1
generateHosts=false #不生成 hosts
[user]
default=yangxy
```

> 直接修改/etc/hostname 等文件可能无效，需要手动修改以上配置文件

## 7. 系统命令

```shell
ubuntu /? #帮助
ubuntu config --default-user root # 设置默认用户
```

## 8. 文件访问

```shell
explorer.exe . #打开 Linux 文件
\\wsl$\ubuntu #打开 linux 文件、
/mnt/c/Users/wys #window 文件
```

## 9. 网络访问

- 使用指定的 IP 地址访问即可
- 或者在宿主机上直接使用 localhost 访问即可

## 10. 局域网桥接与静态 IP 配置

### 10.1. Windows 配置

- 使用 Hyper-v 创建虚拟交换机 wsl-bridge
- 创建.wslconfig 文件

```config
[wsl2]
networkingMode=bridged
vmSwitch=wsl-bridge
dhcp=false
```

> 在 windows 管理员家目录 supervisorctl

### 10.2. WSL 配置

- 使用 wsl import 命令创建多个发行版本
- 添加针对单个发行版本的配置信息

```editorconfig
# 在/etc/wsl.conf下
[boot]
systemd=true
[network]
hostname=slave1
generateResolvConf = false # 禁止启动WSL2时生成/etc/resolv.conf
generateHosts = false # 禁止启动WSL2时修改/etc/hosts
[user]
default=yangxy
```

- 添加静态 ip 配置

```yaml
# 在/etc/netplan/01-netcfg.yaml下
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:   # 替换为你的网络接口名称
      addresses: [192.168.5.122/24]  # 替换为你想要的静态 IP 地址和子网掩码
      routes:
      - to: default
        via: 192.168.5.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]  # 可选：替换为你的 DNS 服务器地址
```

- 完善 DNS 解析

```editorconfig
# 在/etc/resolv.conf
nameserver 8.8.4.4 # 写入你本地最好用的dns就行
```

### 10.3. 路由器配置

配置 DHCP 静态解析

> 综上，所有的子系统共享网络空间，网络当前没有办法完全隔离开

## 11. 拓展信息

- wsl1 vs wsl2
  - 完整的 linux 内核
  - 系统更兼容
  - 速度提升

## 12. 问题

- lsof 命令用不了

```shell
netstat -tln
```

## 13. 参考资料

- [官方链接](https://learn.microsoft.com/zh-cn/windows/wsl/basic-commands#install)
- [高级配置](https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config)
- [三方博客](https://blog.csdn.net/qq_38856939/article/details/116528514)
