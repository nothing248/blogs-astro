---
title: "warp-config"
filename: cloudflare-warp-guide
summary: 本文档整理了 Cloudflare Warp 虚拟专用网络（VPN）客户端的账户申请、快速脚本配置、WireGuard 配置文件路径（wgcf-account.toml/wgcf-profile.toml）以及 systemd 服务的重启管理命令。提供 OpenAI 服务接入的 CDN 节点检测方法，旨在解决外网访问及网络代理的快速部署问题。
tags:
  - cloudflare
  - warp
  - wireguard
  - vpn
  - proxy
aliases:
  - warp-config
  - cloudflare-warp
status: completed
---

<!-- toc -->

## 1. 简介

**Cloudflare Warp** 是 Cloudflare 推出的一款免费且快速的 VPN/代理软件，基于 WireGuard 协议构建，旨在提高移动设备和计算机的网络安全与访问速度。

## 2. 账户申请

可以通过以下脚本快速申请 Cloudflare Warp 账户密钥：

```shell
bash -c "$(curl -L warp-reg.vercel.app)"
```

## 3. 快速部署与使用

使用社区维护的 Warp 一键配置脚本进行安装与配置：

```shell
bash <(curl -fsSL git.io/warp.sh) help
```

## 4. 配置文件路径

Warp 配置及账户文件默认存放在以下路径：

- **账户信息**：`/etc/warp/wgcf-account.toml`
- **WireGuard 配置**：`/etc/warp/wgcf-profile.toml`

## 5. 服务管理

通过以下 `systemd` 命令启动或重启 WireGuard 服务：

```shell
systemctl restart wg-quick@wgcf
```

## 6. 拓展信息

### 6.1. CDN 节点及代理检测

若要检测 Warp 是否成功代理并查看当前的节点网络状态（常用于验证 ChatGPT 等服务的可访问性），可访问以下检测网址：

[OpenAI / Cloudflare CDN 状态追踪](https://chat.openai.com/cdn-cgi/trace)

## 7. 参考资料

- [P3TERX - Cloudflare WARP 一键配置脚本](https://p3terx.com/archives/cloudflare-warp-configuration-script.html)
