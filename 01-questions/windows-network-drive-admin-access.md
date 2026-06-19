---
title: "Windows 网络驱动器不可见"
filename: windows-network-drive-admin-access
summary: "笔记解决了 Windows 中管理员权限下无法访问网络映射驱动器（Z: 盘等）的经典问题。其根源在于 Windows UAC 的令牌分离机制，导致标准令牌下的映射资源在管理员令牌中不可见。文中提供了三种解决方案：通过注册表项 `EnableLinkedConnections` 强制同步令牌间的连接、在管理员终端手动重新映射，以及在脚本中使用 UNC 路径代替盘符。"
tags: [Windows, Network-Drive, UAC, Admin-Privileges, Registry]
aliases: [Windows 网络驱动器不可见, 管理员权限访问 Z 盘, EnableLinkedConnections 详解]
status: completed
date created: 星期三, 二月 25日 2026, 4:52:17 下午
date modified: 星期五, 六月 19日 2026, 11:57:01 中午
---

<!-- toc -->

## 1. 现象描述

在使用 Windows 时经常遇到：普通用户模式下可以看见映射的 `Z:` 盘，但切换到“以管理员身份运行”的命令提示符或程序时，却提示 `Z:` 盘不存在。

---

## 2. 原因分析：UAC 令牌分离

这是由于 Windows 的 **UAC（用户帐户控制）分离令牌机制** 导致的。

当你登录 Windows 时，系统会创建两个访问令牌：

1. **标准用户令牌**：用于日常操作。
2. **管理员令牌**：只有在“以管理员身份运行”时才会激活。

**关键点**：Windows 将网络映射驱动器视为与令牌绑定的资源。

- 在普通模式下映射的 `Z:` 盘只存在于标准令牌中。
- 管理员模式下的令牌并没有这个映射关系，因此无法识别。

---

## 3. 解决方案

### 3.1. 方案一：修改注册表（一劳永逸）

此操作会让 Windows 在标准令牌和管理员令牌之间共享映射驱动器。

1. 按下 `Win + R`，输入 `regedit`。
2. 定位到路径：
   `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`
3. 新建一个 **DWORD (32 位) 值**。
4. 命名为：`EnableLinkedConnections`。
5. 将其数值数据修改为 `1`。
6. **重启电脑**。

> [!info] 原理
> 这个注册表项会让 Windows 在两个令牌之间同步网络映射关系。

### 3.2. 方案二：在管理员终端重新映射

如果你不想修改注册表，只需在 **管理员权限** 的命令提示符（CMD）中手动再映射一次：

```batch
net use Z: \\服务器地址\共享路径 /persistent:yes
```

### 3.3. 方案三：使用 UNC 路径代替盘符（推荐脚本使用）

在编写脚本或运行命令时，直接使用网络路径可以避开盘符映射问题：

- **不推荐**：`mklink /D "C:\Link" "Z:\Folder"`
- **推荐**：`mklink /D "C:\Link" "\\Server\Share\Folder"`

---

## 4. 验证方法

1. 打开一个 **普通 CMD**，输入 `net use`，确认 `Z:` 盘状态。
2. 打开一个 **管理员 CMD**，输入 `net use`。
   - 如果列表为空，说明就是上述令牌分离问题，方案一可完美解决。
