---
title: "Rust语言入门"
filename: rust-language-installation-and-overview
description: Rust 是一款专注于安全、并发和性能的现代系统级编程语言。本文简要介绍了 Rust 的核心价值，特别是其独特的内存安全保障机制（所有权系统）。同时提供了使用官方工具 rustup 进行环境安装的标准方法，为开发者进入 Rust 生态提供了基础指引。
tags: [rust, systems-programming, memory-safety, installation, cargo]
aliases: [Rust语言入门, Rust安装教程]
status: pending
date created: 星期日, 十月 5日 2025, 5:45:42 下午
date modified: 星期五, 六月 19日 2026, 12:08:19 中午
---

<!-- toc -->

## 1. 简介

Rust 是一款系统编程语言，运行速度极快，防止分段错误，并保证线程安全。它由 Mozilla 主导开发，现已广泛应用于操作系统、浏览器核心、区块链及高性能 Web 后端等领域。

## 2. 核心特性

- **内存安全**：通过独创的“所有权（Ownership）”和“借用检查（Borrow Checker）”机制，在编译期即可消除内存泄漏和竞态条件，无需垃圾回收（GC）。
- **极致性能**：拥有媲美 C/C++ 的运行速度，且支持高度优化的零成本抽象。
- **卓越的工具链**：
  - **Cargo**：集包管理、构建工具、测试运行器于一体。
  - **rustup**：管理不同版本和工具链的安装器。

## 3. 安装指南

推荐通过官方脚本安装 `rustup`，它会自动配置环境并安装最新的稳定版 `rustc` 和 `cargo`。

### 3.1. macOS / Linux

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 3.2. Windows

建议从官网下载并运行 `rustup-init.exe` 桌面程序进行安装。

## 4. 开发第一个程序

使用 Cargo 创建新项目：

```bash
cargo new hello_rust
cd hello_rust
cargo run
```

## 5. 参考资料

- [Rust 官方安装指南](https://www.rust-lang.org/zh-CN/tools/install)
- [Rust 程序设计语言 (The Book)](https://doc.rust-lang.org/book/)
- [Rust By Example (实战教程)](https://doc.rust-lang.org/rust-by-example/)
