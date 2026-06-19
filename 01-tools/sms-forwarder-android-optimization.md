---
title: "短信转发器"
filename: sms-forwarder-android-optimization
summary: SmsForwarder 是一款功能强大的 Android 短信与通知转发工具。它能够将接收到的短信、通话记录及应用通知实时转发至 Webhook、邮箱、Telegram 等平台。本文主要介绍了该工具在 Android 平台上的使用限制，以及针对小米等机型的极致省电与常驻后台优化配置方案，以确保服务的稳定运行。
tags: [android, automation, sms, tool]
aliases: [短信转发器]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:08:43 中午
---

<!-- toc -->

## 1. 简介

SmsForwarder 是一个开源的 Android 短信转发工具。它支持高度自定义的转发规则，可以将手机短信、通知等内容同步到各种数字终端。

## 2. 平台限制

- **Android 独占**：目前仅支持 Android 平台，暂无 iOS 版本。
- **后台常驻**：由于 Android 系统的墓碑机制和省电优化，需要手动调整系统设置以保证其不被系统杀掉。

## 3. 极致省电与后台优化（以小米手机为例）

为了确保转发服务 24 小时在线，建议按以下步骤调整设置：

1. **电源管理**：开启超级省电模式（仅针对纯转发备用机）。
2. **启动权限**：关闭所有的自启动管理限制。
3. **通知配置**：关闭不相关的通知管理，保持系统清爽。
4. **硬件节能**：
   - 屏幕亮度调至最低。
   - 开启 **深色模式**。
   - 屏幕刷新率固定为 60Hz。
   - 休眠时间设置为最短（15 秒）。
   - 关闭蓝牙、NFC、定位服务及个人热点。
5. **同步服务**：关闭 Xiaomi Cloud、Google 等所有后台自动同步。
6. **进程限制**：在开发者选项中，将后台进程限制设置为 **“最多一个”**。

## 4. 参考资料

- [SmsForwarder GitHub 项目仓库](https://github.com/pppscn/SmsForwarder)
