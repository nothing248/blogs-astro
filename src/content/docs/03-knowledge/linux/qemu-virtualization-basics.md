---
title: "qemu-guide"
filename: qemu-virtualization-basics
summary: 本篇笔记为空，需在后续补充 QEMU（Quick Emulator）开源模拟器与虚拟化管理工具的使用。包含底层内核虚拟机（KVM）集成、QEMU 常用命令行虚拟机启动参数、虚拟磁盘文件格式（如 qcow2、raw）的转换与挂载技术。
tags:
  - qemu
  - kvm
  - virtualization
  - hypervisor
  - emulator
aliases:
  - qemu-guide
  - virtual-machines
status: pending
---

<!-- toc -->

## 1. 简介

本篇笔记旨在整理和记录 QEMU 虚拟化模拟器的核心用法与运维操作。

## 2. 待办事项与拓展规划

- [ ] 补充 QEMU 与 Linux 内核虚拟机（KVM）协同工作的原理解析。
- [ ] 整理 `qemu-img` 命令行工具的高频操作（如创建、扩容和转换 `qcow2` 与 `raw` 镜像文件）。
- [ ] 编写使用 `qemu-system-x86_64` 命令行直接无图形启动 Linux 系统的指令模版。
- [ ] 记录桥接网络（Bridge）与 TAP 设备配置，为虚拟机提供独立网络 IP 的操作步骤。
