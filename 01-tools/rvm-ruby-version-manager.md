---
title: "Ruby版本管理"
filename: rvm-ruby-version-manager
description: RVM是广泛使用的Ruby版本管理器，能够实现单机多版本Ruby环境的共存与自由切换。本文详解在macOS与Linux上通过GPG密钥校验和脚本部署RVM的流程，列举了常用版本查询、切换及gemset虚拟环境隔离的指令，解决了由于Ruby版本冲突导致的开发环境故障。
tags: [ruby, rvm, version-manager]
aliases: [Ruby版本管理, RVM安装, Gemset配置]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:32 上午
date modified: 星期五, 六月 19日 2026, 12:08:21 中午
---

<!-- toc -->

## 1. 简介

一个 ruby 的版本管理工具

---

## 2. 安装

### 2.1. MAC

``` shell
brew install gnupg #安装gpg
gpg --keyserver hkp://pgp.mit.edu --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable --ruby #安装稳定版本
```

---

## 3. 使用

```shell
rvm list
rvm install 3.3.0
rvm use 3.3.0
rvm use 3.3.0 --default
rvm install 3.2.2 --with-openssl-dir=$(brew --prefix openssl@1.1)
```

## 4. 拓展信息

### 4.1. Rvm Ruby Gem Rails Rake 之间的管理

- RVM 是一种管理 Ruby 版本和 Gems 的工具
- Gems 是 Ruby 的软件包管理系统(在项目目录中，使用 bundle install 安装项目所需的 Gem)
- Rails 是一个用于构建 Web 应用程序的框架，基于 Ruby 开发
- Rake 是 Ruby 的构建工具，类似于 Make，主要用于自动执行任务

### 4.2. Openssl 版本要求

| Ruby 版本 | 兼容的 OpenSSL 版本 | 状态与建议 |
| --------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Ruby 3.0.x** | **OpenSSL 1.1.x** (例如 1.1.1) | **核心痛点。** 这些版本不兼容 OpenSSL 3.0 及更高版本。如果您必须安装 Ruby 3.0.x，则需要 **明确指定** 使用 OpenSSL 1.1.x 进行编译。 |
| **Ruby 2.4.x - 2.7.x** | **OpenSSL 1.1.x** | 与 Ruby 3.0.x 类似，需要 OpenSSL 1.1.x 或更早的版本。这些 Ruby 版本已 **结束生命周期 (End of Life)**，不推荐在新项目中使用。 |
| **Ruby 2.3.x 及更早** | **OpenSSL 1.0.x** | 这些版本非常老旧，强烈不建议使用。 |
| **Ruby 3.1.x** | **OpenSSL 1.1.x 或 OpenSSL 3.0+** | 这是 **第一个开始支持 OpenSSL 3.0** 的 Ruby 大版本。理论上它可以同时兼容 1.1.x 和 3.0+，但通常建议直接使用 OpenSSL 3.0 或更新版本进行编译。 |
| **Ruby 3.2.x, 3.3.x, 3.4.x (最新)** | **OpenSSL 3.0+ (首选)** | **推荐方案。** 这些现代 Ruby 版本被设计为与 OpenSSL 3.0 及更高版本完全兼容。这是最安全、最推荐的组合。 |

```
# 使用 RVM
rvm install 3.0.7 --with-openssl-dir=$(brew --prefix openssl@1.1)

# RVM 安装最新版本，通常会自动使用 OpenSSL 3.x
rvm install 3.3.6
# 或明确指定 OpenSSL 3.x
rvm install 3.3.6 --with-openssl-dir=$(brew --prefix openssl@3)
```

### 4.3. Windows 适配

**当前只适配 mac/Linux, windows 请使用其他工具**

## 5. 参考资料

- [官方文档](https://rvm.io/rvm/install)
