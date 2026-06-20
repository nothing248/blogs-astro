---
status: completed
filename: windows-system-commands-and-cmd-enhancements
title: "Windows 命令"
description: 本笔记整理了 Windows 系统下常用的基础网络与进程排障命令（如 netstat 查端口、taskkill 杀进程）。重点对比了原生 CMD、PowerShell 与安装 Clink (增强 CMD) 后的终端体验差异，强调了 Clink 在提供类似 Linux Bash 的路径补全、永久历史记录搜索 (Ctrl+R) 以及 Emacs/Vi 快捷键绑定方面的显著优势。此外，附带了修改 Windows Hosts 文件的系统路径及 BitLocker 磁盘加密的参考线索。
aliases: [Windows 命令, CMD 增强, Clink 终端, Windows 排障]
tags: [Windows, 命令行, 运维, Clink, CMD, 进程管理]
date created: 星期五, 十二月 26日 2025, 7:08:04 晚上
date modified: 星期四, 六月 18日 2026, 11:55:00 晚上
---

<!-- toc -->

## 1. 常用系统排障与操作命令

在 Windows CMD 或 PowerShell 中常用的高频指令：

```cmd
chdir            # 查看当前路径 (类似 Linux pwd)
echo %PATH%      # 查看系统环境变量
explorer .       # 在文件资源管理器中打开当前文件夹
cls              # 清除终端屏幕
netstat -ano | findstr :10801 # 检索特定端口的占用情况 (查看 PID)
taskkill /pid 1234 /f         # 强制杀死指定 PID 的进程
```

## 2. 系统配置路径与设置

- **Hosts 文件绝对路径**：`C:\Windows\System32\Drivers\etc\hosts`
- **默认浏览器劫持修复**：若遭遇 Edge 浏览器自动覆盖默认设置，需前往 `Edge > 设置 > 管理默认浏览器设置` 关闭相关保护选项。
- **Windows BitLocker 加密**：内置驱动器级加密工具，用于保护静态数据（防物理盗窃）。

```
https://www.anquanke.com/post/id/296375#:~:text=BitLocker%20%E6%98%AF%E4%B8%80%E9%A1%B9%E5%86%85%E7%BD%AE,%E5%85%B6%E6%96%87%E4%BB%B6%E7%9A%84%E8%AE%BF%E9%97%AE%E6%9D%83%E9%99%90%E3%80%82
```

---

## 3. 终端体验升级：Clink vs 原生 CMD/PowerShell

Windows 默认的 `cmd.exe` 体验极其简陋，强烈建议安装 **Clink** 增强插件，它为 CMD 注入了 GNU Readline 库的能力。

| 特性评估 | Clink (增强版 CMD) | 默认原生 CMD | 原生 PowerShell |
| :--- | :--- | :--- | :--- |
| **底层引擎** | 基于 `cmd.exe` 叠加了 Bash/Zsh 宏扩展层。 | 传统的 `cmd.exe`。 | 基于 .NET 对象的现代 Shell。 |
| **自动补全体验** | 极其强大。支持模糊匹配、Git 分支提示及路径补全。 | 仅支持基础的 `Tab` 遍历补全。 | 强大的基于对象与函数的补全。 |
| **快捷键与编辑** | 原生支持 **Emacs/Vi 快捷键** 绑定（如 `Ctrl+U` 清行）。 | 仅支持极简的方向键与 Home/End。 | 支持基础快捷编辑功能。 |
| **历史记录检索** | **支持永久保存**，支持像 Linux 一样使用 **`Ctrl+R`** 倒序搜索。 | 仅对当前会话有效，关窗即焚，无搜索功能。 | 永久保存，支持检索。 |

## 4. 参考资料

- [Github: Windows 家庭版升级专业版批处理工具 (CMWTAT)](https://github.com/TGSAN/CMWTAT_Digital_Edition)
- [文件夹权限修改异常处理](https://www.cnblogs.com/malinyan/p/17191183.html)
