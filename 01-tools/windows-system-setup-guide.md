---
title: "Windows初始化"
filename: windows-system-setup-guide
summary: Windows操作系统初始化与运维实践指南。本文归纳了新系统交付时的核心行动项，包含删除原本地账户并安全迁移、加入工作与学校组织账户进行资源同步、安全迁移并替换SSH私钥、配置本地静态hosts以映射主机名，以及使用7zip和WSA等实用软件安装指南。
tags: [windows, system-initialization, ssh-keys, hosts-configuration]
aliases: [Windows初始化, Hosts修改, Win软件管理]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:25 下午
date modified: 星期五, 六月 19日 2026, 12:09:16 中午
---

<!-- toc -->

## 1. 简介

windows 系统使用

## 2. 初始化

### 2.1. 更新用户

- 设置 > 账户 > 其他用户 > 添加账户 > 重启 > 进入到新增账户 > 删除原来用户

### 2.2. 新增组织用户

- 设置 > 账户 > 工作与学校账户 > 链接 > onedriver > 登录

### 2.3. 替换 ssh 密钥

复制原来的 id_rsa、id_rsa.pub 文件到 新设备中

> 可以使用 ssh-keygen 直接生成

### 2.4. 添加 hostname

- C:\Windows\System32\drivers\etc\host 修改该文件

## 3. 软件安装

- 7zip

> 打开方式的文件是 7zip Manager

- 微信

> 需要

- 飞书
- [pycharm](https://aijihuo.cn/jetbrains-activation-codes.html)
- [webstorm](https://aijihuo.cn/jetbrains-activation-codes.html)
- [idea](https://aijihuo.cn/jetbrains-activation-codes.html)
- 360
- utools
  - 需要配置书签搜索地址: C:\Users\*\AppData\Local\Google\Chrome\User Data\Default\Bookmarks
- 鲁大师
- git
- node
- nvm
- miniconda

> 需要配置环境变量

- keepassxc
- sublime
- clash
- vray2N
- 企业微信
- 腾讯会议
- [typora](https://developer.aliyun.com/article/944676)
- jdk

> 需要配置环境变量 JAVA_HOME = PATH =;%JAVA_HOME%/bin;%JAVA_HOME%/jre/bin

- tabby
- office

> 可以使用 [Office Tools Plus](https://otp.landian.vip/zh-cn/download.html#google_vignette) 实现 visio 等软件的安装, 然后使用 [KMS](https://github.com/zbezj/HEU_KMS_Activator/releases) 该工具进行激活。

## 4. 文档迁移

可以使用 onedriver 进行同步

## 5. 项目迁移

- 原来代码检测提交
- 新设备拉取最新代码

## 6. SSH 迁移

手动迁移

## 7. 代理节点迁移

使用订阅 URL 进行迁移

## 8. Ping Localhost -> :: 1 ipv6 解析为 ipv4

```shell
netsh interface ipv6 show prefixpolicies #查看优先级
netsh int ipv6 set prefix ::/96 50 0
netsh int ipv6 set prefix ::ffff:0:0/96 40 1
netsh int ipv6 set prefix 2002::/16 35 2
netsh int ipv6 set prefix 2001::/32 30 3
netsh int ipv6 set prefix ::1/128 10 4
netsh int ipv6 set prefix ::/0 5 5
netsh int ipv6 set prefix fc00::/7 3 13
netsh int ipv6 set prefix fec0::/10 1 11
netsh int ipv6 set prefix 3ffe::/16 1 12
ping localhost
```

## 9. Edge 配置 Copilot

- 需要代理节点
- 需要美区账户(否则可能出现回答已达上限的提示)
