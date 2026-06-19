---
title: "Clash使用教程"
filename: clash-proxy-client-guide
summary: Clash 是一款流行的开源代理客户端，支持多平台（Windows, Linux, macOS, Android）。本笔记提供了 Clash 的安装说明、订阅节点配置方法以及 Global、Rule 和 Direct 三种模式的切换建议。通过合理配置 Rule 模式，用户可以实现基于规则的智能流量分流，有效优化网络访问速度与稳定性。
tags: ["Clash", "Proxy", "Networking", "Open-Source"]
aliases: ["Clash使用教程", "代理客户端配置", "Clash规则管理"]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:27 下午
date modified: 星期五, 六月 19日 2026, 11:58:15 中午
---

<!-- toc -->

## 1. 简介

**Clash** 是一款基于 Go 开发的开源多平台代理客户端，支持 Shadowsocks, Vmess, Snell, Trojan 等多种协议。通过其强大的规则引擎，用户可以根据域名、IP、GeoIP 等条件实现精准的流量分流。

---

## 2. 安装与初始配置

### 2.1. 下载安装

Clash 拥有多个图形化界面版本（如 Clash for Windows, ClashX, Clash for Android），可根据使用平台在 GitHub 或官方渠道下载对应的安装包。

### 2.2. 订阅节点配置

1. 获取服务商提供的订阅链接（URL）。
2. 在客户端的 **Profiles (配置文件)** 页面，粘贴链接并点击 **Download/Import**。
3. 确保配置文件下载成功并处于选中状态。

---

## 3. 运行模式解析

Clash 通常提供三种核心运行模式，建议根据实际场景切换：

- **Rule (规则模式)**：**推荐日常使用**。根据配置文件中的规则自动分流，国内流量直连，国外流量走代理。
- **Global (全局模式)**：所有流量强制通过代理节点。
- **Direct (直连模式)**：所有流量不经过代理，直接连接目标服务器。

---

## 4. 高级功能

- **日志监控**：通过 **Logs** 页面可以实时查看请求链路，方便排查规则匹配问题。
- **连接管理**：在 **Connections** 页面可以查看当前的活跃连接、所选节点及流量消耗。
- **外部控制**：支持通过 RESTful API 进行远程管理。

---

## 5. 参考资料

- [Clash 核心配置文档 (YAML)](https://clash-meta.gitbook.io/clash.meta-wiki-old-1/config/yaml)
- [Clash 使用指南](https://docs.gtk.pw/)
- [Clash 规则集参考](https://github.com/Loyalsoldier/clash-rules/)
