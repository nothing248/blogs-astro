---
title: "Fiddler抓包教程"
filename: fiddler-http-debugging-proxy
summary: Fiddler 是一款强大的 HTTP 抓包与调试代理工具。本笔记介绍了 Fiddler Classic 的核心用法，包括启用 SSL 解密、配置手机端远程调试及证书安装流程。针对常见问题，提供了报文乱码修复、过滤远程请求以及 Android 7.0+ 高版本 HTTPS 抓包的解决方案，并对比了 Classic 版与 Everywhere 版本的收费模式差异。
tags: ["Fiddler", "HTTP-Proxy", "Packet-Capture", "Mobile-Debugging", "HTTPS"]
aliases: ["Fiddler抓包教程", "手机抓包配置", "Fiddler证书安装"]
status: completed
date created: 星期一, 九月 22日 2025, 5:12:53 下午
date modified: 星期五, 六月 19日 2026, 11:59:04 中午
---

<!-- toc -->

## 1. 简介

**Fiddler** 是一款位于浏览器（或客户端应用）与服务器之间的 HTTP 代理工具。它能够记录并检查所有进出的 HTTP(S) 流量，允许开发者修改请求和响应，是 Web 调试与性能分析的必备工具。

---

## 2. 核心功能配置

### 2.1. 开启 HTTPS 解析

默认情况下，Fiddler 无法查看加密的 HTTPS 内容。

- **操作**：`Tools` -> `Options` -> `HTTPS` -> 勾选 `Decrypt HTTPS traffic`。
- **注意**：需根据提示在系统中安装 Fiddler 生成的根证书。

### 2.2. 手机端远程调试

1. **PC 端配置**：`Tools` -> `Options` -> `Connections` -> 勾选 `Allow remote computers to connect`。
2. **重启 Fiddler** 以使配置生效，并记录下 PC 的 IP 地址和 Fiddler 监听端口（默认 8888）。
3. **手机端配置**：
    - 将手机与 PC 连接到同一 Wi-Fi。
    - 在手机 Wi-Fi 设置中配置 **手动代理**，指向 PC 的 IP 和端口。
    - **证书安装**：手机浏览器访问 `http://<PC_IP>:<Port>`，下载并安装 `FiddlerRoot certificate`。

---

## 3. 常见问题排查

- **报文乱码**：通常是因为请求被 Gzip 或 Deflate 压缩。点击 Fiddler 顶部的黄色条提示“Response is encoded. Click to decode”或开启自动解压工具栏按钮。

  ![](http://qiniu.sxyxy.top/20231023121608.png?image=image)

- **仅抓取远程连接请求**  

    ![](http://qiniu.sxyxy.top/20231023121713.png?image=image)

- **证书无法安装**：部分 Android 设备需手动将证书后缀名改为 `.crt` 后，从“系统设置 -> 安全 -> 从存储盘安装证书”中导入。
- **Android 7.0+ 无法抓取 HTTPS**：由于系统不再信任用户自行安装的证书，需通过 Root 手机并将证书移至系统证书目录，或在 App 代码中显式信任用户证书。

---

## 4. 版本差异

- **Fiddler Classic**：免费版，仅限 Windows 系统，功能最为稳健成熟。
- **Fiddler Everywhere**：收费版（订阅制），跨平台支持（Mac, Linux, Windows），界面更现代，支持云协作。

---

## 5. 参考资料

- [Fiddler Classic 官方文档](https://www.telerik.com/fiddler/fiddler-classic)
- [Android 7.0+ 抓包进阶指南](https://juejin.cn/post/7197233138271027255)
