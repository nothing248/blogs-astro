---
title: "Jenkins安装与配置"
filename: jenkins-ci-cd-installation-config
description: Jenkins 是一款广泛使用的开源自动化服务器。本文介绍了在 Ubuntu 环境下的两种安装方式（裸机与 Docker 预留），详述了环境变量（JAVA_HOME/PORT）配置、中文语言包安装及服务管理。重点总结了邮件通知的高频报错（端口/验证/SSL）及节点配置中 RSA-PEM 格式证书的要求，并明确了 Jenkins 对 JDK 11 的版本支持限制。
tags: [jenkins, ci-cd, automation, dev-ops, server-admin]
aliases: [Jenkins安装与配置]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:54 上午
date modified: 星期五, 六月 19日 2026, 11:59:55 中午
---

<!-- toc -->

## 1. 简介

Jenkins 是基于 Java 开发的开源持续集成（CI）工具，旨在提供一个开放易用的软件平台，使软件的持续集成变得可能。

## 2. 安装指南 (Ubuntu)

### 2.1. 裸机安装

```shell
# 添加官方证书与源
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# 执行安装
sudo apt-get update && sudo apt-get install jenkins
```

### 2.2. 初始配置

- **管理员密码**：`/var/lib/jenkins/secrets/initialAdminPassword`
- **端口与环境**：修改 `/etc/systemd/system/.../jenkins.service`（或对应配置文件）：

  ```shell
  Environment="JAVA_HOME=/opt/software/jdk-17.0.12"
  Environment="JAVA_OPTS=-Djava.awt.headless=true"
  Environment="JENKINS_PORT=9999"
  ```

## 3. 维护与管理

### 3.1. 汉化配置

1. 安装 **Locale** 插件。(Manage Jenkins > Plugins > Install locale)
2. 在“Manage Jenkins > System”中设置语言为 `zh_CN`。
3. 若汉化不完全：切换至 `en_US` -> 重启(访问/restart) -> 重新切换 `zh_CN`。

### 3.2. 邮件通知避坑

- **SMTP 端口**：若连接超时，检查端口是否被云厂商封禁（**通常使用 465 且开启 SSL**）。
- **553 错误**：发件人邮箱必须与 SMTP 认证账号完全一致。

## 4. 节点管理

当添加 Linux 凭据用于 SSH 节点连接时，证书要求必须是 **PEM 格式**：

```bash
ssh-keygen -t rsa -m PEM 
```

## 5. 参考资料

- [Jenkins 官方文档](https://www.jenkins.io/)
