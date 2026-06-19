---
title: "WireGuard安装"
filename: wireguard-vpn-peer-setup
summary: WireGuard是现代化、极速轻量的VPN组网安全通道协议。本文介绍了在Ubuntu与Windows下生成公私钥并初始化虚拟网卡的步骤。提供一份典型的网络配置文件样例，涵盖了路由地址分配、端口监听声明、节点保持激活的PersistentKeepalive参数，帮助实现跨地域设备组网。
tags: [wireguard, vpn-networking, network-security, peer-to-peer]
aliases: [WireGuard安装, 局域网组网, wg0配置]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 星期五, 六月 19日 2026, 12:09:22 中午
---

<!-- toc -->

## 1. 简介

一个组网工具

## 2. 安装

### 2.1. Ubuntu

```shell
apt install wireguard
cd /etc/wiregurd
wg genkey | sudo tee /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey #生成密钥
```

## 3. Windows

 下载安装 WireGuard

## 4. 配置

- 虚拟网卡配置

```
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = $peer1_privatekey
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE #可选,允许进行不同网口之间数据转发(用于暴露当前节点的的内部网络信息)
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE 

[Peer]
PublicKey = $peer2_publickey
Endpoint = 1.2.3.4:51820 #公网的连接地址
AllowedIPs = 10.0.0.0/24,192.168.2/24 #出站时基于目标地址选择对应的peer,入站时基于源地址选择是否放行
PersistentKeepalive = 25
```

- 开启端口转发配置

```
# /etc/sysctl.conf
net.ipv4.ip_forward=1

systctl -p #进行配置生效
```

> 注意该配置不是必须的，如果需要进行不同的端口(网卡转化)则需要开启该选项

## 5. 管理

```shell
wg #可以查看当前的连接信息
systemctl start wg-quick@wg0
systemctl status wg-quick@wg0
systemctl stop wg-quick@wg0
systemctl restart wg-quick@wg0
```

## 6. 场景

### 6.1. 内网穿透/直连场景

该场景实现 B(内网)、C(内网)设备上的服务可以通过 A(公网)进行公开访问

- B 虚拟网卡配置

```
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.2/24
PrivateKey = $peerB_privatekey

[Peer]
PublicKey = $peerA_publickey
Endpoint = 1.2.3.4:51820 #公网的连接地址
AllowedIPs = 10.0.0.0/24 #此处填写的是网段，也可以填写10.0.0.1/32
PersistentKeepalive = 25
```

> C 设备与 B 设备配置结构相同，但是需要注意配置内的变量信息需要替换

- A 虚拟网卡配置

```
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = $peerA_privatekey

# B设备
[Peer]
PublicKey = $peerB_publickey
AllowedIPs = 10.0.0.2/32 #注意：此处填写10.0.0.2/32
PersistentKeepalive = 25
```

- 关闭端口转发

```
# /etc/sysctl.conf
net.ipv4.ip_forward=0

systctl -p #进行配置生效
```

> 此处是控制 B 与 C 是否可以通过 10.0.0.0/24 网域互相访问的核心步骤。1 代表可以访问，0 代表不可以访问

- 测试

```
# B/C不互通
A ping B/C 通
B ping A 通
B ping C 不通
C ping A 通
C ping B 不通
# B/C 互通
在A/B/C上任意一台设备上ping 另外两个设备都通
```

### 6.2. 中转方案

该场景实现 B(内网 192.168.2.0/24)、C(内网 192.168.1.0/24)内网内服务(对应局域网内的所有设备)可以通过 A(公网)进行公开访问

- B 虚拟网卡配置

```
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.2/24
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
PrivateKey = $peerB_privatekey

[Peer]
PublicKey = $peerA_publickey
Endpoint = 1.2.3.4:51820 #公网的连接地址
AllowedIPs = 10.0.0.0/24,192.168.1.0/24 #192用于访问C内的局域网
PersistentKeepalive = 25
```

- C 虚拟网卡配置

```
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.3/24
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
PrivateKey = $peerC_privatekey

[Peer]
PublicKey = $peerA_publickey
Endpoint = 1.2.3.4:51820 #公网的连接地址
AllowedIPs = 10.0.0.0/24,192.168.2.0/24 #192用于访问B内的局域网
PersistentKeepalive = 25
```

- A 虚拟网卡配置

```
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
PrivateKey = $peerA_privatekey

# B设备
[Peer]
PublicKey = $peerB_publickey
AllowedIPs = 10.0.0.2/32,192.168.2.0/24 #注意：此处填写10.0.0.2/32
PersistentKeepalive = 25

# C设备
[Peer]
PublicKey = $peerC_publickey
AllowedIPs = 10.0.0.3/32,192.168.1.0/24 #注意：此处填写10.0.0.2/32
PersistentKeepalive = 25
```

- 开启端口转发

```
# /etc/sysctl.conf
net.ipv4.ip_forward=1

systctl -p #进行配置生效
```

## 7. 拓展信息

### 7.1. 与内网穿透区别

- 不需要端口进行一一映射，直接映射出的是 ip 地址

## 8. 参考资料

- [三方资料](https://zhuanlan.zhihu.com/p/447375895)
- [官方链接](https://www.wireguard.com/install/)
