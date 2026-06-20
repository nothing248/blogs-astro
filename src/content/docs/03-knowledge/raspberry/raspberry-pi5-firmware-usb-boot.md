---
title: "树莓派5固件更新"
filename: raspberry-pi5-firmware-usb-boot
description: 树莓派 5 固件更新与 USB 引导配置指南。涵盖通过 rpi-eeprom 更新 EEPROM 固件，利用 raspi-config 界面或手动修改底层 BOOT_ORDER 代码实现 USB 优先引导。同时指导使用 Raspberry Pi Imager 烧录启动盘，并针对移动硬盘供电不足、USB 3.0 线材干扰等常见硬件故障提供排查建议。
tags:
  - raspberry-pi
  - eeprom
  - boot-order
  - firmware-update
  - usb-boot
aliases:
  - 树莓派5固件更新
  - 树莓派5USB启动设置
  - EEPROM启动顺序配置
status: completed
date created: 星期五, 二月 27日 2026, 2:06:33 下午
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 准备工作

- **Pi Imager 烧录工具**：[官方软件下载](https://www.raspberrypi.com/software/)
- **可靠的 SD 卡**（用于系统初次初始化与固件升级）
- **高速 USB 存储设备**（如 USB 3.0 优盘、移动硬盘或 NVMe 固态硬盘盒子）

---

## 2. 固件与系统更新

在修改任何底层启动选项前，强烈建议将树莓派的 EEPROM 引导装载程序（Bootloader）升级到最新版本，以获得最佳的 USB 3.0 兼容性与稳定性。

```bash
# 1. 更新本地软件包列表
sudo apt update

# 2. 确保已安装官方的 EEPROM 更新管理工具
sudo apt install rpi-eeprom -y

# 3. 检查并自动应用固件更新
sudo rpi-eeprom-update -a
```

> [!NOTE]
> 如果当前已经是最新版固件，系统会输出 `BOOTLOADER: up-to-date`。若执行了更新，必须重启树莓派（`sudo reboot`）以载入新固件。

---

## 3. 配置 USB 优先启动

树莓派 5 支持灵活调整引导顺序，以下提供两种配置方法。

### 3.1. 方法 A：使用 raspi-config 交互界面（推荐）

这是最直观且不易出错的方法：

1. 在终端中打开系统配置工具：

   ```bash
   sudo raspi-config
   ```

2. 使用键盘方向键选择 **Advanced Options**（高级选项）。
3. 选择 **Boot Order**（启动顺序）。
4. 选中 **USB Boot**（USB 启动）。
5. 选定后，根据提示保存退出，选择 **Yes** 重新启动。

> [!TIP]
> 开启 USB 启动模式后，当未连接任何可引导的 USB 设备时，树莓派会自动回退（Fallback）至 SD 卡引导。

### 3.2. 方法 B：直接修改与核对 EEPROM 参数

如需从底层验证或修改引导顺序，可通过 EEPROM 配置文件完成：

- **读取当前 EEPROM 配置**

```bash
vcgencmd bootloader_config
```

- **理解 BOOT_ORDER 底层代码**

在输出内容中查找 `BOOT_ORDER` 字段。树莓派 5 的引导顺序采用从右向左的解析机制（`4` 代表 SD 卡，`1` 代表 USB 存储）：

- **`BOOT_ORDER=0xf41`**：优先尝试从 SD 卡启动，失败后尝试 USB 引导。
- **`BOOT_ORDER=0xf14`**：**优先尝试从 USB 引导**，失败后回退至 SD 卡。

---

## 4. 制作并配置 USB 启动盘

1. 在电脑上运行 **Raspberry Pi Imager**。
2. **选择操作系统**：如 `Raspberry Pi OS (64-bit)`。
3. **选择存储卡**：插入并选中你的 **USB 闪存盘或移动硬盘**。
4. 确认无误后点击烧录，等待校验完成。
5. 将烧录好的 USB 存储设备插入树莓派 5 后侧的 **蓝色 USB 3.0 接口**。
6. 取出原有的 SD 卡，或者保持插卡状态（在配置了 `0xf14` 的情况下系统将优先读取 USB 分区）。

---

## 5. 硬件排查与避坑指南

> [!CAUTION]
> **外接硬盘供电不足**
> 树莓派 5 的 USB 接口输出电流最大为 1.6A（需搭配 PD 5V 5A 电源）。当使用机械硬盘或部分高能耗 NVMe 固态硬盘时，易发生启动报错或运行中掉盘。建议配备官方 **27W USB-C 电源适配器**，或为移动硬盘接入额外的独立供电。

> [!WARNING]
> **USB 3.0 电磁干扰**
> 劣质的 USB 3.0 连接线或硬盘盒的塑料壳屏蔽效果较差，会在 2.4GHz 频段产生高频辐射，干扰树莓派的 WiFi 及无线键鼠信号。如遇启动困难或网络不稳定，请尝试更换具有屏蔽层的高规格连接线，或者尝试将设备接入其他 USB 接口。

> [!NOTE]
> **多存储设备启动规则**
> 当同时插入 SD 卡与配置好系统的 USB 设备，且 EEPROM 已设为 `BOOT_ORDER=0xf14` 时，引导加载程序会直接绕过并忽略 SD 卡上的系统分区，优先读取 USB 存储进行引导。
