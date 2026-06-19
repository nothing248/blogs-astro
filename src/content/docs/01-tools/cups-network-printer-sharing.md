---
title: "CUPS 打印服务器"
filename: cups-network-printer-sharing
summary: CUPS (Common Unix Printing System) 是一款开源的打印机服务程序，支持跨平台的网络打印共享。本笔记详细记录了在 Ubuntu 系统下部署 CUPS 的全过程，包括 `cupsd.conf` 的权限配置、Canon E560 等打印机驱动的手动安装流程，以及在 Windows 和 macOS 客户端连接 IPP 共享打印机的具体步骤，实现了无需本地安装驱动的便捷云打印方案。
tags: ["CUPS", "Printer-Server", "Linux", "IPP", "Network-Sharing"]
aliases: ["CUPS 打印服务器", "Linux 共享打印机", "网络打印配置"]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:57 上午
date modified: 星期五, 六月 19日 2026, 11:58:27 中午
---

<!-- toc -->

## 1. 简介

**CUPS (Common Unix Printing System)** 是一款适用于类 Unix 系统的开源打印系统。通过搭建 CUPS 服务器，可以将本地连接的打印机转化为网络共享打印机，使得局域网内的 Windows、macOS 及移动设备能够通过 **IPP (Internet Printing Protocol)** 协议直接进行打印，从而免去每台电脑重复安装驱动的繁琐过程。

---

## 2. CUPS 服务环境搭建

以下以 **Ubuntu 22.04** 为例进行说明。

### 2.1. 安装 CUPS

```shell
sudo apt update
sudo apt install cups
```

### 2.2. 核心权限配置

编辑 `/etc/cups/cupsd.conf` 以开启 Web 管理界面并放宽访问限制：

```text
# 监听所有网口
Listen 0.0.0.0:631
WebInterface Yes

# 允许外部访问管理页面
<Location />
  Order allow,deny
  Allow all
</Location>

<Location /admin>
  Order allow,deny
  Allow all
</Location>

# 配置文件修改权限（需验证系统用户）
<Location /admin/conf>
AuthType Default
Require user @SYSTEM
Order allow, deny
Allow all
</Location>

# Restrict access to log files...
<Location /admin/log>
AuthType Default
Require user @SYSTEM
Order allow, deny
Allow all
</Location>
```

### 2.3. 重启服务

```shell
sudo systemctl restart cups
```

---

## 3. 打印机驱动安装 (以 Canon E560 为例)

1. 从官方下载 Linux 驱动包（如 `.deb` 格式）。
2. 解压并运行安装脚本：

   ```shell
   # 从该链接 https://in.canon/en/support/0100588502?model = 8992B 下载对应驱动，并 且上传到/opt/software/printer/canon_e560 下
   tar -zxvf cnijfilter-e560series-4.10-1-deb.tar.gz
   sudo ./install.sh
   ```

3. 按照提示完成驱动注册。

---

## 4. 注册与共享

### 4.1. Web 界面注册

访问 `http://<服务器IP>:631/admin`（使用系统用户名密码登录）：

- 点击 **Add Printer**。
- CUPS 通常会自动识别已通过 USB 连接并安装好驱动的打印机。
- 设置共享名称（如 `E560_Share`）。

![](http://qiniu.sxyxy.top/20241128123350.png)

- 如果没有正常识别正手动注册

![](http://qiniu.sxyxy.top/20241128124106.png)

> [!tip] 共享地址格式
> 最终的打印机共享链接通常为：`http://<服务器IP>:631/printers/<打印机名称>`

---

## 5. 客户端连接配置

### 5.1. Windows 配置

1. 打开“设置” -> “打印机和扫描仪” -> “添加设备”。
2. 选择“我需要的打印机不在列表中”。
3. 选择“按名称选择共享打印机”，输入地址：
   `http://<服务器IP>:631/printers/E560_Share`
4. 驱动程序选择“通用 (Generic)” -> “MS Publisher Imagesetter” 或对应的 PCL 驱动即可。

![](http://qiniu.sxyxy.top/20241128114728.png)

### 5.2. macOS 配置

1. “系统设置” -> “打印机与扫描仪” -> “添加打印机”。
2. 选择 **IP** 标签：
   - **地址**：`<服务器IP>:631`
   - **协议**：IPP (Internet Printing Protocol)
   - **队列**：`/printers/E560_Share`
   - **使用**：普通 PCL 打印机 或 自动选择。

![](http://qiniu.sxyxy.top/img_v3_02h2_94f32736-3d60-4024-9803-c9b2b03abe9g.jpg)
