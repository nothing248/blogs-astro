---
title: "树莓派Netplan网络配置"
filename: raspberry-netplan-network-setup
description: 基于 Netplan 的树莓派网络配置与服务优化指南。内容包含编写 YAML 文件为有线 (eth0) 与无线 (wlan0) 网卡配置静态 IP、默认路由及 DNS。同时针对旁路由分流场景，提供了禁用系统 IPv6（防止规则绕过）以及关闭 systemd-resolved 本地缓存（解决 FakeDNS 引起的 SSL 证书错误）的调优方案。
tags:
  - raspberry-pi
  - netplan
  - network-config
  - ipv6
  - dns
aliases:
  - 树莓派Netplan网络配置
  - 树莓派设置静态IP
  - 禁用树莓派IPv6
status: completed
date created: 星期三, 四月 1日 2026, 11:03:08 晚上
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. Netplan 网络配置

在较新的 Ubuntu 及 Debian 系系统（如树莓派官方系统）中，推荐使用 `netplan` 工具进行网络配置。

- **编写配置文件**

修改或新建 `/etc/netplan/01-custom_network.yaml`，配置有线与无线网卡的静态 IP（**此处已隐藏敏感的 WiFi 凭据**）：

```yaml
network:
  version: 2
  wifis:
    wlan0:
      dhcp4: false
      optional: true
      access-points:
        "YOUR-WIFI-NAME":
          password: "[WIFI密码已隐藏]"
      # 设置无线网卡静态 IP
      addresses:
        - 192.168.31.108/24
      # 默认路由配置 (代替已废弃的 gateway4)
      routes:
        - to: default
          via: 192.168.31.1
          metric: 200        // 数值越大优先级越低，无线网络作为备用
      # 域名解析服务器
      nameservers:
        addresses:
          - 114.114.114.114
          - 8.8.8.8
          - 1.1.1.1
  ethernets:
    eth0:
      dhcp4: false
      optional: true
      # 设置有线网卡静态 IP
      addresses:
        - 192.168.8.201/24
      # 默认路由配置
      routes:
        - to: default
          via: 192.168.8.1
          metric: 100        // 有线网络设置较小 Metric 优先出网
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
```

- **配置应用**

```bash
# 测试配置是否存在语法错误，并在 120 秒内自动回滚防失联
sudo netplan try

# 确认无误后应用配置
sudo netplan apply
```

## 2. 关闭 IPv6 服务

> [!WARNING]
> 某些服务（如 Docker 容器）在双栈网络中会优先请求 IPv6 地址，这可能导致旁路由中配置的 IPv4 分流规则无法对其生效。为了确保分流可控，在旁路由网络环境中建议关闭 IPv6。

- **检查当前 IPv6 启用状态**

```bash
ip -6 addr show
# 如果输出为空，代表 IPv6 已禁用；若有输出相关 IP 则代表 IPv6 处于开启状态。
```

- **修改内核参数**

编辑 `/etc/sysctl.conf` 配置文件，在文件末尾追加以下配置：

```text
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```

- **重载内核配置使之生效**

```bash
sudo sysctl -p
```

## 3. 解决 FakeDNS 缓存不一致问题

> [!IMPORTANT]
> 开启 FakeDNS 分流后，路由器端的 DNS 映射缓存会处于动态变化中。若客户端或本地系统缓存了旧的 DNS 解析记录，容易造成 SSL/TLS 握手失败，产生证书解析等错误。

- **临时清理本地 DNS 缓存**

```bash
sudo resolvectl flush-caches
```

- **配置彻底关闭系统缓存**

编辑 `/etc/systemd/resolved.conf` 配置文件，调整 `Cache` 机制，确保每次解析请求都穿透向路由器查询实时结果：

```text
[Resolve]
# 彻底关闭 systemd-resolved 缓存
Cache=no
# 对于本机发出的解析请求也不使用本地缓存
CacheFromLocalhost=no
```

- **重启解析器守护进程**

```bash
sudo systemctl restart systemd-resolved
```
