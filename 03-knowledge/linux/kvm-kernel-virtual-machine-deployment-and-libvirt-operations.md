---
status: completed
filename: kvm-kernel-virtual-machine-deployment-and-libvirt-operations
title: "KVM 虚拟化"
summary: 本笔记系统整理了基于 Linux 内核的虚拟化技术 KVM (Kernel-Based Virtual Machine) 的底层部署与实操指南。涵盖了宿主机 CPU 硬件虚拟化扩展（VT-x/AMD-V）的指令校验（kvm-ok），以及依赖包 `qemu-kvm` 与 `libvirtd` 守护进程的安装与 systemctl 托管。重点提供了为虚拟机配置底层互通的 Netplan 网桥 (`br0`) YAML 代码，并详细演示了如何通过 `virt-install` CLI 工具自动化拉取并启动 OpenWrt 等虚机镜像，是构建底层私有云计算节点的基础技术文档。
aliases: [KVM 虚拟化, libvirt 管理, QEMU-KVM, virt-install, Linux 网桥]
tags: [Linux, 虚拟化, 云计算, KVM, QEMU, 运维部署, 网络架构]
date created: 星期一, 一月 12日 2026, 10:03:49 上午
date modified: 星期四, 六月 18日 2026, 13:55:00 晚上
---

<!-- toc -->

## 1. 核心架构定位

**KVM (Kernel-Based Virtual Machine)** 是 Linux 内核原生的虚拟化模块。它将 Linux 内核直接转换为一个 Hypervisor（系统管理程序），使得每个虚拟机（VM）都变成 Linux 宿主机上的一个普通进程，直接由内核调度其 CPU 与内存资源。

在实际生产中，KVM 通常与 **QEMU**（提供硬件设备模拟，如网卡、磁盘）和 **Libvirt**（提供统一的虚机管理 API 与 CLI 框架）组合使用。

---

## 2. 宿主机环境校验与安装

### 2.1. 验证 CPU 硬件虚拟化支持

KVM 强依赖于物理 CPU 的 VT-x (Intel) 或 AMD-V 扩展。

```bash
# 方法 1：直接检索 CPU flag
grep -Eoc '(vmx|svm)' /proc/cpuinfo # 输出需大于 0

# 方法 2：使用专用工具 (Ubuntu 下需 apt install cpu-checker)
kvm-ok 
# 期待输出：
# INFO: /dev/kvm exists
# KVM acceleration can be used
```

### 2.2. 核心组件安装

```bash
apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager

# 验证 KVM 内核模块已加载
lsmod | grep kvm
```

### 2.3. Libvirtd 守护进程注册

`libvirtd` 是统一管理网络、存储与虚机的核心管家。

```bash
systemctl enable --now libvirtd
systemctl is-active libvirtd
```

---

## 3. 核心基建：配置底层网络网桥 (Bridge)

为了让虚拟机拥有独立的局域网 IP 并能与外界互通，通常需要在宿主机上搭建一块虚拟网桥（Bridge），将物理网卡绑定其上。
*以下为 Ubuntu 下基于 Netplan 的配置示例 (`/etc/netplan/br0.yaml`)*：

```yaml
network:
  version: 2
  ethernets:
    wlan0:  # 你的实际物理网卡
      dhcp4: false
      dhcp6: false
  bridges:
    br0:    # 声明一个名为 br0 的网桥
      interfaces: [wlan0] # 将物理网卡桥接进来
      dhcp4: false
      addresses: [192.168.1.12/24] # 将原宿主机的 IP 移交至网桥
      routes:
          - to: default
            via: 192.168.1.1
      nameservers:
        addresses: [114.114.114.114, 8.8.8.8]
      parameters:
        stp: false
```

*注：如果不主动配置桥接，KVM / Libvirt 会默认创建一个带 NAT 转换的 `virbr0` 虚拟网桥提供纯出口上网能力。*

---

## 4. 虚机管理实战：CLI 与生命周期

### 4.1. `virt-install` 自动化创建并拉起虚机

利用命令行工具，基于已有的 qcow2 或 img 镜像文件拉起虚机（以部署 OpenWrt 软路由为例）：

```bash
virt-install \
  --name openwrt \
  --ram 512 \
  --vcpus 2 \
  --osinfo detect=on,require=off \
  --disk path=/var/lib/libvirt/images/openwrt_aarch64.qcow2 \
  --network bridge=br0,model=e1000 \
  --force --import --autostart
```

*(如果要挂载 VNC 远程控制台，可追加 `--vnc --vncport=5911 --vnclisten=0.0.0.0`)*

### 4.2. `virsh` 日常高频管控指令

`virsh` 是与 `libvirtd` 通信的标准命令行接口。

```bash
virsh list --all          # 查看所有虚机及状态
virsh start openwrt       # 启动
virsh shutdown openwrt    # 优雅关机 (向虚机发送 ACPI 信号)
virsh destroy openwrt     # 强制断电 (硬杀进程)
virsh suspend openwrt     # 挂起休眠
virsh resume openwrt      # 唤醒

# 销毁与卸载
virsh undefine openwrt --nvram # 彻底从宿主机抹除该虚机的 XML 注册记录（不会删磁盘）

# 配置与控制台
virsh edit openwrt        # 以安全模式打开并修改该虚机的 XML 底层配置
virsh autostart openwrt   # 设置虚机随宿主机开机自启
virsh console openwrt     # 接入虚机的串行控制台终端 (需虚机内部开启 ttyS0 支持)
```

---

## 5. 附录补充知识

### 5.1. Linux 内核模块管理 (`lsmod`)

KVM 作为一个底层模块，可通过标准命令探测：

- `lsmod`：列出当前加载的所有内核模块。
- `sudo modprobe module_name`：智能加载模块。
- `modinfo module_name`：查看该模块的详细参数与版权。

### 5.2. 网卡混杂模式 (Promiscuous Mode)

在搭建软路由或复杂抓包网络时，需要允许网卡接收目的 MAC 地址并非自身的包：

```bash
# 开启混杂模式
ifconfig eth0 promisc
# 验证 (查看是否带有 PROMISC 标志)
ip link show eth0
```
