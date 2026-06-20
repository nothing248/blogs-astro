---
title: "LDAP教程"
filename: openldap-installation-and-concepts
description: OpenLDAP 是一款高性能的开源 LDAP 服务实现。本文详细介绍了 LDAP 的核心概念（如条目、属性、对象类及 DN），对比了 BDB、HDB 与现代 MDB 数据存储后端的优劣。同时提供了基于 Debian 系的包管理安装及 2.6.x 版本的源码编译步骤，并包含了数据库初始化的 LDIF 配置文件示例，适用于构建企业级统一身份认证系统。
tags: [openldap, ldap, identity-management, sso, linux-admin]
aliases: [LDAP教程, OpenLDAP安装, 目录服务配置]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 星期五, 六月 19日 2026, 12:07:09 中午
---

<!-- toc -->

## 1. 简介

OpenLDAP 是轻量级目录访问协议（LDAP）的开源实现，由 OpenLDAP 项目组维护。它主要用于存储用户信息、组织结构及权限数据，是实现单点登录（SSO）和统一账号管理的核心组件。

## 2. 核心概念

LDAP 目录以树状结构（DIT）存储数据，理解以下术语至关重要：

- **条目 (Entry)**：目录中的基本单元，代表一个对象（如用户、设备）。
- **属性 (Attribute)**：描述条目的键值对，如 `mail`, `uid`, `cn` (Common Name)。
- **对象类 (Object Class)**：定义了条目必须包含或可选包含的属性集合（如 `inetOrgPerson`）。
- **识别名 (DN - Distinguished Name)**：条目的全局唯一标识。
  - 示例：`cn=John Doe,ou=people,dc=example,dc=com`
- **根目录条目 (Root DSE)**：服务器的入口点，描述服务器的功能及根命名上下文。

## 3. 后端存储技术演进

| 后端 | 开发者 | 特点 | 状态 |
| :--- | :--- | :--- | :--- |
| **BDB** | Oracle | 高性能嵌入式数据库，曾是默认后端。 | 已过时 |
| **HDB** | OpenLDAP | BDB 变种，优化了层次化（树状）数据处理。 | 已过时 |
| **MDB** | OpenLDAP | **高性能、无锁 (Lock-free)**。2.4 引入，2.5 成为唯一默认后端。 | **推荐** |

## 4. 安装指南

### 4.1. 快速安装 (Debian/Ubuntu)

```shell
# 安装主程序与工具
sudo apt update && sudo apt install slapd ldap-utils

# 图形化/交互式配置 (设置域名、管理员密码等)
sudo dpkg-reconfigure slapd
```

### 4.2. 源码编译安装 (高级)

适用于需要自定义模块或追求特定版本的场景。

```shell
# 安装编译依赖
sudo apt install build-essential libtool pkg-config libsasl2-dev libssl-dev libgnutls28-dev libltdl-dev

# 下载并解压
wget https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-2.6.9.tgz
tar -xzvf openldap-2.6.9.tgz
cd openldap-2.6.9/

# 编译配置 (启用 MDB 引擎)
./configure --prefix=/opt/software/openldap \
            --enable-modules \
            --enable-slapd \
            --enable-mdb \
            --enable-ldap \
            --enable-crypt \
            --enable-spasswd

make && make test
sudo make install
```

### 4.3. 初始化数据库 (LDIF 示例)

创建 `database.ldif` 用于定义 DIT 根节点及管理员权限：

```ldif
dn: olcDatabase={1}mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: {1}mdb
olcSuffix: dc=[example],dc=com
olcRootDN: cn=admin,dc=[example],dc=com
olcRootPW: {SSHA}[PASSWORD_HASH]
```

执行添加操作：

```shell
/opt/openldap/bin/ldapadd -x -H ldap:/// -D "cn=config" -W -f database.ldif
```

## 5. 参考资料

- [OpenLDAP 官方网站](https://www.openldap.org/)
- [OpenLDAP 软件下载](https://www.openldap.org/software/download/OpenLDAP/openldap-release/)
