---
title: "Windows 开发者模式开启"
filename: windows-mklink-developer-mode
summary: 本笔记介绍了在 Windows 中通过启用“开发者模式”来放宽符号链接（mklink）权限限制的方法。开启开发者模式后，用户可以在普通的 CMD 或 PowerShell 窗口中执行 `mklink` 命令，而不再强制要求“以管理员身份运行”，同时也支持运行未签名的本地脚本，极大提升了开发环境的便利性。
tags: ["Windows", "mklink", "Developer-Mode", "Symbolic-Link"]
aliases: ["Windows 开发者模式开启", "mklink 免管理员权限", "符号链接权限优化"]
status: completed
date created: 星期三, 二月 25日 2026, 5:07:13 下午
date modified: 星期五, 六月 19日 2026, 11:56:58 中午
---

<!-- toc -->

## 1. 开启开发者模式

在 Windows 中开启“开发者模式”（Developer Mode）可以让你在不需要管理员权限的情况下使用 `mklink`，并且能够运行未签名的本地脚本。

### 1.1. 开启步骤 (Windows 10/11)

1. 按下 **`Win + I`** 打开“设置”。
2. 导航路径：

- **Windows 11**: 点击左侧的 **隐私和安全性** > 右侧点击 **面向开发人员**。
- **Windows 10**: 点击 **更新和安全** > 左侧点击 **开发者选项**。

1. 找到 **开发者模式** (Developer Mode) 开关，将其设置为 **开**。
2. 在弹出的确认对话框中点击“是”。

---

## 2. 权限变化原理

开启开发者模式后，系统会自动放宽对 **符号链接（Symbolic Links）** 的权限限制：

- **之前**：必须右键“以管理员身份运行”CMD 才能执行 `mklink /D`。
- **之后**：可以直接在普通的 CMD 或 PowerShell 窗口中运行 `mklink`。

> [!important] 注意
> 开启设置后，建议重新打开一个新的命令行窗口以使设置生效。
