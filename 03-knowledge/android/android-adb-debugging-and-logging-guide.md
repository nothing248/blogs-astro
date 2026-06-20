---
status: completed
filename: android-adb-debugging-and-logging-guide
title: "ADB 使用指南"
description: 本笔记详细介绍了 Android 调试桥 (ADB) 的实战用法，专注于移动端应用的日志分析与调试。涵盖了 ADB 工具在 Windows、Mac 和 Linux 下的安装路径，详述了 Wi-Fi 无线配对及连接的操作流程。重点讲解了如何通过 `shell pm` 查询包名，并利用 `logcat` 配合 `grep` 过滤器精准捕获特定应用（如 Chrome 或自定义 App）的错误日志。为开发者和测试人员提供了一套高效、轻量级的终端调试 SOP。
aliases: [ADB 使用指南, Android 终端调试, 日志过滤技巧, ADB 无线连接]
tags: [Android, ADB, 调试工具, 移动开发, 日志分析, Logcat, 运维调试, 自动化测试]
date created: 星期一, 十二月 1日 2025, 9:59:24 上午
date modified: 星期四, 六月 18日 2026, 8:55:00 晚上
---

<!-- toc -->

## 1. ADB 环境安装

ADB (Android Debug Bridge) 是开发与调试的核心组件，建议从官方平台工具库下载：

- **Mac (Darwin)**: [下载链接](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip)
- **Windows**: [下载链接](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)
- **Linux**: [下载链接](https://dl.google.com/android/repository/platform-tools-latest-linux.zip)

---

## 2. 建立设备链接

### 2.1. Wi-Fi 无线配对 (Android 11+)

在开发者选项中开启“无线调试”，获取配对码后执行：

```bash
adb pair [IP_ADDRESS]:[PORT] [PAIRING_CODE]
# 示例：adb pair 192.168.8.164:40361 993794
```

### 2.2. 执行连接

```bash
adb connect [IP_ADDRESS]:[PORT]
# 示例：adb connect 192.168.8.164:41173
```

---

## 3. 应用日志查看与调试

### 3.1. 查找目标应用包名

若不确定包名，可通过关键字模糊查询：

```bash
adb shell pm list packages | grep [Keyword]
# 示例：adb shell pm list packages | grep chrome
```

### 3.2. 精准日志过滤 (Logcat)

利用 `logcat` 捕获异常，并使用 `grep` 过滤特定应用标识：

```bash
# 仅查看错误级别 (*: E) 且包含特定包名的日志
adb logcat '*:E' | grep "[PackageName]"
# 示例：adb logcat '*: E' | grep "com.superproductivity.superproductivity"
```

---

## 4. 常用进阶指令

- **查看设备列表**：`adb devices`
- **重启设备**：`adb reboot`
- **安装应用**：`adb install path/to/app.apk`
- **拉取文件**：`adb pull /sdcard/demo.mp4 ./local_path`

> [!note] 调试技巧
> 在进行生产环境调试时，使用 `adb logcat -v time` 可以打印带有时间戳的日志，方便与后端日志进行联路追踪。
