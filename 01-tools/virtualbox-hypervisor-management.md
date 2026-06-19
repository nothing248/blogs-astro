---
title: "VirtualBox安装"
filename: virtualbox-hypervisor-management
summary: VirtualBox是知名的跨平台开源虚拟化平台。本文总结了其在Windows系统下非默认分区安装时出现的磁盘权限报错问题，提供了通过icacls命令强制重置文件夹安全性继承和访问控制列表（ACL）的指令，并给出通过VBoxManage进行虚拟机磁盘克隆的实战用法。
tags: [virtualbox, hypervisor, acl-permissions, vboxmanage]
aliases: [VirtualBox安装, 磁盘克隆, Windows权限修复]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:24 下午
date modified: 星期五, 六月 19日 2026, 12:09:07 中午
---

<!-- toc -->

## 1. 简介

一个虚拟机平台

## 2. 安装软件

### 2.1. 下载安装

- D 盘安装不满足安装条件

```shell
icacls d:\virtualboxs /reset /t /c
icacls d:\virtualboxs /inheritance:d /t /c
icacls d:\virtualboxs /grant *S-1-5-32-545:(OI)(CI)(RX)
icacls d:\virtualboxs /deny  *S-1-5-32-545:(DE,WD,AD,WEA,WA)
icacls d:\virtualboxs /grant *S-1-5-11:(OI)(CI)(RX)
icacls d:\virtualboxs /deny  *S-1-5-11:(DE,WD,AD,WEA,WA)
```

> 注意 virtualbox 默认只能安装在 C 系统盘内，如要安装在 D 盘会出现不满足安全条件的提示，请参考以上命令尝试进行。上述方式不确保一定安装成功，如果安装不成功建议直接安装在 C 盘，之后的虚拟机配置到 D 盘

- 缺少 win32api 与 python core
  ![下载依赖支持](http://qiniu.sxyxy.top/20240613114307.png)

- 安装依赖
  ![](http://qiniu.sxyxy.top/20240613114633.png)

### 2.2. 安装虚拟机

![](http://qiniu.sxyxy.top/20240613114753.png)

### 2.3. 配置网络

- 方案一  
直接使用桥接网络，但是需要路由器配置静态 ip
  ![](http://qiniu.sxyxy.top/20240613121614.png)

- 方案二  
配置双网卡，一个 host-only 用于配置宿主机访问 VM，一个桥接网络用于外网访问
  ![](http://qiniu.sxyxy.top/20240613121918.png)

## 3. 配置虚拟机

- 配置 host-only 网卡对应的静态 ip
  ![](http://qiniu.sxyxy.top/20240613123042.png)
- 配置用户权限

```shell
sudo echo "yangxy ALL=(ALL) NOPASSWD: ALL" >>/etc/sudoers
```

- 配置镜像地址

```shell
mv /etc/apt/sources.list /etc/apt/sources.list.bak
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
```

- 配置 ssh 登录

```shell
sudo apt install openssh-server
```

## 4. 拓展虚拟机

复制虚拟机
![](http://qiniu.sxyxy.top/20240613123344.png)

> 注意此处复制完成之后需要进入虚拟机修改 hostname 与静态 ip 地址

## 5. 管理虚拟机

- 调整 VM 磁盘
  ![](http://qiniu.sxyxy.top/20240613141631.png)

- 调整系统磁盘

```shell
# 拓展分区的方式
fdisk -l #查看当前磁盘情况
fdisk /dev/sda #进去对应磁盘
d #删除指定分区
n #创建指定分区
# 默认选项
w #保存配置
reboot #重启
resize2fs /dev/sda2 #调整分区到文件系统

# 挂载分区的方式
fdisk /dev/sda #进入指定磁盘
n #创建分区
mount /dev/sda /data #挂载分区
```

- 调整内存大小
  ![](http://qiniu.sxyxy.top/20240613143344.png)

## 6. VBmanage 命令

```shell
VBoxmanage startvm slave3 --type headless #以无界面的方式单独运行指定虚拟机
VBoxmanage list vms #查看当前已有的 VM
VBoxmanage list runningvms #查看当前正在运行的 VM
VBoxmanage controlvm slave3 poweroff #关闭指定的 VM
```

> 当前没有命令批量启动 VM 与关闭 VM，所以只能单独启动

## 7. 拓展信息

- 虚拟机与 Virtualbox 的 GUI 页面是个隔离开的，可以直接启动虚拟机而不打开 virtualbox 软件

## 8. 参考资料

- [官方地址](https://www.virtualbox.org/wiki/Downloads)
