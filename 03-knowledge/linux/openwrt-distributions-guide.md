---
title: "openwrt-guide"
filename: openwrt-distributions-guide
summary: 本文梳理了主流 OpenWrt 软路由系统的分发版本与编译资源，包括插件丰富的 Lean LEDE 分支、内核前沿 of OpenWrt 官方原版，以及主打稳定性的 Lienol 定制版。提供定制化固件编译的相关参考教程，为家庭或企业级软路由搭建提供选型指导。
tags:
  - openwrt
  - router
  - lede
  - firmware
  - linux-distro
aliases:
  - openwrt-guide
  - soft-router-firmware
status: completed
---

<!-- toc -->

## 1. 简介

**OpenWrt** 是一个针对嵌入式设备的 Linux 操作系统（通常用于软路由与家用路由器）。它提供了高度模块化的网络配置选项和海量的插件，方便用户实现自定义的网络管理及高级网络服务。

## 2. 常见版本与分支

在实际部署中，用户常根据需求选择不同的 OpenWrt 定制编译分支：

### 2.1. Lean LEDE 版本

- **特点**：集成了大量实用的插件与驱动，适合国内用户开箱即用，硬件兼容性良好。
- **GitHub 仓库**：[coolsnowwolf/lede](https://github.com/coolsnowwolf/lede)

### 2.2. 官方版本 (Official OpenWrt)

- **特点**：内核及软件包更新最快，系统干净纯粹，无冗余插件，适合对安全性、稳定性和自主定制要求高的用户。
- **GitHub 仓库**：[openwrt/openwrt](https://github.com/openwrt/openwrt)

### 2.3. Lienol 版本

- **特点**：主打稳定与精简，网络组件优化较好，注重系统的长期运行稳定性。
- **GitHub 仓库**：[Lienol/openwrt](https://github.com/Lienol/openwrt)

## 3. 固件自定义编译

针对特定硬件（如虚拟机 VMware、Ubuntu 环境、X96 Max 等外贸盒子）的自定义编译流程可参考以下教程：

- [自定义编译参考教程](https://syjn.blogspot.com/2023/08/openwrtvmwareubuntuopenwrtx96-max.html)
