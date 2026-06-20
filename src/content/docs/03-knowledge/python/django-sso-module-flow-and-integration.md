---
status: completed
filename: django-sso-module-flow-and-integration
title: "Django SSO"
description: 本笔记详细解析了基于 Django 框架的开源 SSO（单点登录）模块的工作流程。全面梳理了首次登录时浏览器、应用服务器（App Server）与 SSO 授权服务器之间的令牌获取、重定向交互及时序状态流转。涵盖了跨应用免密登录、管理员取消授权以及用户统一登出的底层执行逻辑，为构建企业级多系统互信网关提供理论基础。
aliases: [Django SSO, 单点登录流程, 统一认证时序]
tags: [Python, Django, SSO, 单点登录, 授权, 系统架构, 网络安全]
date created: 星期一, 十二月 1日 2025, 9:59:18 上午
date modified: 星期四, 六月 18日 2026, 14:25:00 晚上
---

<!-- toc -->

## 1. 模块定位

本架构基于 `django-sso` 开源模块，旨在实现多个分离的 App 系统之间共享统一的用户认证状态。

---

## 2. 核心认证时序流程

架构中涉及四大核心节点：

- **`app_server`**：用户首次访问的业务应用。
- **`app_other`**：用户后续访问的其他关联业务应用。
- **`browser`**：客户端浏览器。
- **`sso_server`**：中央认证与授权控制节点。

### 2.1. 初次登录请求流程

1. `browser` -(/login)> `app_server`：用户针对特定的 app 发起访问请求。
2. `app_server` -(/sso/obtain)> `sso_server`：App Server 向中央 SSO 获取颁发的授权凭证。
3. `app_server` -(redirect)> `browser`：App 响应登录请求。返回一个重定向响应，指示重定向到 `sso_server` 的 `/login` (GET)；同时此响应会携带一个 Cookie，用于在浏览器侧记录该授权凭证的 Session。
4. `browser` -(/login GET)> `sso_server`：浏览器获取到 SSO 的中央登录页面。
5. `browser` -(/login POST)> `sso_server`：用户通过 SSO 登录表单输入账密实现认证。
6. `sso_server` -(/sso/event/)> `app_server` -> `browser`：SSO 先将登录成功后的用户信息后台传递给 `app_server`。随后向浏览器下发重定向响应（重定向到 `app_server` 的 `/sso/accept`），并携带用于记录用户信息的 Session Cookie。
7. `browser` -(/sso/accept/)> `app_server`：浏览器重定向回具体的业务 App。
8. `app_server` -(/sso/get/ & /sso/makeused/)> `sso_server`：App Server 获取用户初始的回调链接，并向 SSO 声明将该授权 Token 标记为“已使用”。
9. `app_server` -(redirect)> `browser`：用户彻底登录成功，看到最终业务页面。

### 2.2. 再次登录同一 `app_server`

1. `browser` -(/login)> `app_server`：用户再次请求登录。
2. `app_server` 检测到本地 Session 信息存在且有效，直接重定向到用户的回调链接，无需向 SSO 发起校验。

### 2.3. 登录生态内的其他应用 (`app_other`)

这是 SSO 的核心价值（一处登录，处处通行）：

1. `browser` -(/login)> `app_other`：用户访问新的业务应用。
2. `app_other` -(/sso/obtain)> `sso_server`：获取新的授权凭证。
3. `app_other` -(redirect)> `browser`：重定向浏览器到 `sso_server` 的 `/login` (GET)，并下发凭证 Cookie。
4. `browser` -(/login GET)> `sso_server`：向 SSO 发起登录。**此时 SSO 检测到该浏览器已存在中央认证 Session**，直接响应重定向到 `app_other` 的 `/sso/accept`。
5. `browser` -(/sso/accept/)> `app_other`：携带令牌回跳。
6. `app_other` -(/sso/get/ & /sso/makeused/)> `sso_server`：获取回调连接，核销 Token。
7. `app_other` -(redirect)> `browser`：用户无感登录成功。

---

## 3. 权限控制与登出注销

### 3.1. 管理员取消单一 App 授权

1. `browser` 发起删除请求 -> `sso_server`。
2. `sso_server` -(/sso/event/)> `app_server`：通知业务端删除本地对应的 Session。
3. `sso_server` 返回删除成功给 `browser`。

### 3.2. 用户全局统一登出

1. `browser` -(/logout)> `app_server`：用户在业务端点下线，App Server 删除本地 Session。
2. `app_server` -(/sso/deauthenticate)> `sso_server`：通知中心节点取消该凭证，`sso_server` 销毁对应的中央 Session。
3. `sso_server` 响应 `app_server`，完成全局退出。

## 4. 参考文档

- [django-sso PyPI 项目主页](https://pypi.org/project/django-sso/)
