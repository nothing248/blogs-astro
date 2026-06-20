---
title: "Java多版本管理"
filename: sdkman-jvm-ecosystem-manager
description: SDKMAN! 是一款用于管理 Unix 系统上多个软件开发工具包（SDK）的并行版本的工具。它提供了一个便捷的命令行界面来安装、切换、列出和移除各种 SDK，特别是在 JVM 生态（如 Java, Groovy, Scala, Maven, Gradle）中表现卓越。本文整理了 SDKMAN 的全局安装、版本管理指令以及通过 .sdkmanrc 实现项目级环境自动切换的实战方法。
tags: [sdkman, java, jvm, version-manager, development-tools, linux-admin]
aliases: [Java多版本管理, SDK管理工具]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:30 上午
date modified: 星期五, 六月 19日 2026, 12:08:27 中午
---

<!-- toc -->

## 1. 简介

SDKMAN! 是一个用于在类 Unix 系统（Linux, macOS, WSL）上管理多个软件开发工具包的工具。它能够极大简化 Java, Maven, Gradle, Kotlin 等开发环境的搭建过程，并支持在不同版本间快速切换。

## 2. 安装指南

建议在安装时自定义目录，以便于全局管理：

```shell
# 指定安装目录 (可选)
export SDKMAN_DIR="/usr/local/sdkman"

# 执行在线安装脚本
curl -s "https://get.sdkman.io" | bash

# 加载环境变量
source "$SDKMAN_DIR/bin/sdkman-init.sh"
```

## 3. 常用操作指令

| 功能 | 命令示例 |
| :--- | :--- |
| **列出支持的所有工具** | `sdk list` |
| **列出特定工具的版本** | `sdk list java` |
| **安装指定版本** | `sdk install java 17.0.12-tem` |
| **设置默认版本** | `sdk default java 17.0.12-tem` |
| **在当前会话切换版本** | `sdk use java 11.0.22-sem` |
| **卸载版本** | `sdk uninstall java 11.0.22-sem` |
| **更新 SDKMAN 本身** | `sdk selfupdate` |

## 4. 进阶技巧：项目级环境切换

在团队协作或多项目开发中，不同项目可能依赖不同的 Java 或构建工具版本。可以使用 `.sdkmanrc` 文件实现自动化：

1. **生成配置文件**：在项目根目录下执行 `sdk env init`。
2. **定义版本**：编辑生成的 `.sdkmanrc`。

   ```text
   java=17.0.12-tem 
   maven=3.9.6
   ```

3. **应用环境**：在此目录下执行 `sdk env` 即可自动切换到定义的版本。

## 5. 参考资料

- [SDKMAN! 官方网站](https://sdkman.io/)
- [SDKMAN! 使用指南](https://sdkman.io/usage)
- [可安装的 SDK 完整列表](https://sdkman.io/sdks)
