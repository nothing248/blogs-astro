---
title: "LDAP概念"
filename: openldap-basics-and-concepts
description: OpenLDAP 是一款开源的轻量级目录访问协议（LDAP）实现。本文阐述了 LDAP 协议与 Microsoft Active Directory (AD) 之间的本质区别，明确了 LDAP 作为底层协议与 AD 作为成熟目录服务产品的关系。同时列举了包括 OpenLDAP、Apache Directory Server 在内的多种开源替代方案，为企业级统一身份认证（SSO）及目录管理提供了理论基础。
tags:
  - openldap
  - ldap
  - active-directory
  - identity-management
  - security
  - sso
aliases:
  - LDAP概念
  - 身份管理服务
  - OpenLDAP简介
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:28 上午
date modified: 星期四, 六月 18日 2026, 11:20:00 上午
---

<!-- toc -->

## 1. 简介

LDAP (Lightweight Directory Access Protocol) 即轻量级目录访问协议。OpenLDAP 是该协议的一个开源实现，广泛用于企业级账号管理、统一身份认证（SSO）以及作为后端存储支撑邮件服务、资源管理等系统。

## 2. 核心概念

### 2.1. LDAP 与 Active Directory (AD) 的区别

- **LDAP 是一种协议**：它定义了一套标准和规则，规定了客户端如何与服务器进行通信以查询、修改目录信息。
- **Active Directory 是一个产品**：它是微软开发的目录服务解决方案，底层实现了 LDAP 协议，同时还集成了 DNS、Kerberos 和组策略管理等高级功能。
- **比喻**：LDAP 就像是 SQL 语言规范，而 Active Directory 就像是 SQL Server 数据库软件。

### 2.2. 常见开源实现

除了 OpenLDAP 外，市面上还有其他优秀的目录服务器实现：

- **OpenLDAP**：性能极强，历史悠久，是 Linux 阵营的事实标准。
- **Apache Directory Server**：基于 Java 开发，易于嵌入和扩展。
- **389 Directory Server**：原名为 Red Hat Directory Server，功能丰富且拥有图形化管理界面。
- **FreeIPA**：集成了 LDAP、Kerberos、DNS 的完整 Linux 身份管理方案（类似于 Linux 版的 AD）。

## 3. 结构化组件

- **DN (Distinguished Name)**：条目的唯一标识（如 `cn=admin,dc=example,dc=com`）。
- **OU (Organizational Unit)**：组织单元，用于逻辑划分（如部门、地区）。
- **CN (Common Name)**：通用名称，通常指代具体的对象名。
- **ObjectClasses**：定义了条目必须具备和可以具备的属性。

## 4. 参考资料

- [OpenLDAP 官方网站](https://www.openldap.org/)
- [LDAP 指南 - LDAP.com](https://ldap.com/getting-started-with-ldap/)
- [LDAP vs. Active Directory 深度解析](https://www.okta.com/identity-101/ldap-vs-active-directory/)
