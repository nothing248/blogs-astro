---
title: "网络诊断"
filename: network-diagnosis-and-optimization
description: 网络诊断与优化指南，涵盖网速测速工具、ping 与 traceroute 命令行检测延迟及跃点的解析方法。介绍 Windows 接口跃点数调整以优化网络优先级，以及小米路由器 SSH 登录配置。包含 Linux 系统中清除 DNS 缓存与 NetworkManager 重启命令，助力高效排查局域网及互联网连通性故障。
tags:
  - network
  - diagnosis
  - windows
  - linux
  - troubleshooting
aliases:
  - 网络诊断
  - 网络测试
  - 路由测试
  - DNS缓存清理
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:23 上午
date modified: 星期二, 六月 16日 2026, 6:24:27 晚上
---

<!-- toc -->

## 1. 网速测试

进行网络带宽和速率测试时，建议选择多个不同节点进行测试并总结结果，因为不同站点与节点的测试结果可能会有非常大的偏差。

常用测速网站：

- [中国科学技术大学测速站](https://test.ustc.edu.cn/)
- [Speedtest.cn](https://www.speedtest.cn/)
- [Speedtest.net](https://www.speedtest.net/zh-Hans)

## 2. 命令行诊断测试

### 2.1. Ping 测试

使用 `ping` 命令可以检测网络连通性及延迟情况：

```bash
ping 8.8.8.8
```

**响应参数说明：**

- **字节 (Bytes)：** 表示发送的数据包大小，默认为 32 字节 (Windows) 或 56 字节 (Linux/macOS)。
- **时间 (Time)：** 即 **往返时间 (Round-Trip Time, RTT)**，指数据包从源端发送到目标主机再返回所花费的时间，单位为毫秒 (ms)。此值越小，表明网络延迟越低。
- **TTL (Time To Live)：** “生存时间”。表示数据包在被路由器丢弃前允许经过的最大网络跃点数（路由器数量）。每经过一个路由器，TTL 值自动减 1。这可用于估算目标主机操作系统（Windows 初始值通常为 128，Linux/Unix 通常为 64 或 255）及网络跳数。

### 2.2. 路由追踪测试

使用路由追踪可以分析数据包在网络传输中所经过的节点：

```bash
# Windows 环境
tracert www.google.com

# Linux/macOS 环境
traceroute www.baidu.com
```

**输出列含义说明：**

- **第一列（跳数）：** 数据包到达该节点的顺序，从 1 开始递增。
- **第二、三、四列（往返时间 RTT）：** 显示三次探测数据包往返该节点的耗时（毫秒）。可用于定位具体哪个节点开始出现严重延迟或丢包。
- **星号 (`*`)：** 代表该次探测请求超时。这可能是因为节点配置了防火墙策略丢弃 ICMP 请求，或者存在网络拥塞和数据包丢失。
- **第五列（IP 地址/主机名）：** 该跳路由器的 IP 地址或经 DNS 解析后得到的主机名。

## 3. Windows 网络管理

### 3.1. 查看网络连接时间

![](http://qiniu.sxyxy.top/20250709112118.png)

### 3.2. 修改网络优先级

当同时连接有线 and 无线网络时，可以通过修改接口跃点数来调整网络优先级：

1. **调整 TCP/IP 设置：**
   - 进入网络连接属性，选择 **“Internet 协议版本 4 (TCP/IPv4)”** 并点击 **“属性”**。
2. **手动指定跃点数：**
   - 点击右下角的 **“高级”**。
   - **取消勾选** “高级 TCP/IP 设置”窗口最下方的 **“自动跃点”**。
   - 在 **“接口跃点数”** 框中输入一个较小的数字（数值越小优先级越高，例如输入 **10** 赋予其高优先级）。
   - 依次点击 **“确定”** 保存设置。

## 4. 路由器配置

### 4.1. 小米路由器开启 SSH 登录

1. 使用开源补丁工具：[xmir-patcher](https://github.com/openwrt-xiaomi/xmir-patcher)
2. 登录命令：

   ```bash
   ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.31.1
   ```

![](http://qiniu.sxyxy.top/20250709122859.png)

## 5. 常用网络操作

### 5.1. 清除 DNS 缓存与重启服务 (Linux)

在 Linux 环境下，可以通过重启 DNS 服务或网络服务来清理本地缓存：

```bash
# 重启 DNS 解析服务 (systemd-resolved)
systemctl restart systemd-resolved

# 重启网络管理器服务
sudo systemctl restart NetworkManager.service
```

### 5.2. 网络延迟参考标准

根据网络延迟 RTT 的大小，网络质量粗略划分如下：

![](http://qiniu.sxyxy.top/20250709100342.png)
