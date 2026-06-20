---
title: "甲骨文云白嫖指南"
filename: oracle-cloud-free-tier-setup-guide
description: Oracle Cloud Infrastructure (OCI) 提供极高性价比的“始终免费”套餐。本文汇总了免费实例的申请额度（如 4 核 24G ARM 实例、200G 磁盘），并提供了详细的初始化配置步骤，包括保活脚本部署、防火墙策略开放以及一键开启 BBR 网络加速（fq+bbr）。适用于希望在云端部署长期稳定且低成本服务的开发者。
tags: [oracle-cloud, oci, cloud-computing, vps, networking, linux-admin]
aliases: [甲骨文云白嫖指南, Oracle云初始化配置, OCI免费套餐]
status: completed
date created: 星期日, 十二月 21日 2025, 11:05:29 上午
date modified: 星期五, 六月 19日 2026, 12:07:17 中午
---

<!-- toc -->

## 1. 简介

Oracle Cloud Infrastructure (OCI) 是甲骨文提供的云计算平台。其“始终免费 (Always Free)”服务因其慷慨的硬件配置而在开发者圈内广受欢迎，特别是 ARM 架构的实例。

## 2. 始终免费额度说明

| 资源类型 | 免费额度详情 | 备注 |
| :--- | :--- | :--- |
| **AMD 实例** | 最多 2 个微型实例 (VM.Standard.E2.1.Micro) | 1/8 OCPU, 1GB 内存 |
| **ARM 实例** | 最多 4 个 OCPU 和 24GB 内存 (Ampere A1) | 可灵活分配给 1-4 个实例 |
| **存储** | 合计 200 GB 块存储 | 建议单个实例分配 50GB-100GB |
| **流量** | 每月 10 TB 出站流量 | 带宽通常为 1Gbps-4Gbps |

> [!tip]
> **跨区域建议**：通过升级为“付费账户”（仅做信用卡验证，不扣费）可解锁跨区域订阅，并可复制配置到最多 3 个不同的地理区域。

## 3. 初始化配置实战

### 3.1. 实例保活 (防止停机)

Oracle 会监控实例资源利用率，若长期闲置可能被回收。可使用以下脚本模拟负载：

```shell
# 运行保活脚本 (限制 CPU/内存/带宽在合理范围内)
bash <(wget -qO- --no-check-certificate https://gitlab.com/spiritysdx/Oracle-server-keep-alive-script/-/raw/main/oalive.sh) 
```

### 3.2. 防火墙配置 (彻底开放端口)

OCI 实例默认防火墙非常严格，建议彻底清空并卸载默认持久化工具（请确保已在云控制台安全组中开启端口）：

```shell
# 允许所有流量
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F

# 卸载 netfilter-persistent 以防重启失效
apt-get purge netfilter-persistent -y && reboot
```

### 3.3. 网络加速：开启 BBR

BBR 可以显著提升跨国网络的传输速率。

- **一键安装脚本**：

```shell
wget --no-check-certificate -O /opt/bbr.sh https://github.com/teddysun/across/raw/master/bbr.sh
chmod +x /opt/bbr.sh
/opt/bbr.sh 
```

- **手动开启 BBR**：

```shell
# 写入配置
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

# 验证状态
sysctl net.ipv4.tcp_congestion_control # 输出应包含 bbr
lsmod | grep bbr # 应有 bbr 模块显示
```

## 4. 参考资料

- [Oracle Cloud Always Free 官方说明](https://www.oracle.com/cloud/free/)
- [OCI 实例配置最佳实践](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/launchinginstance.htm)
