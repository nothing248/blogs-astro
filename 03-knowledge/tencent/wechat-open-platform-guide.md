---
title: "微信开放平台概述"
filename: wechat-open-platform-guide
description: 微信开放平台的技术概述。内容涵盖平台定义、核心能力（包括 App/Web 微信登录、微信分享、微信支付以及小程序与 App 的双向互通），并梳理了开发者账号注册、主体认证资质以及 AppID/AppSecret 等安全凭证的获取与安全开发规范。
tags:
  - tengxun
  - wechat
  - open-platform
  - oauth2
  - integrations
aliases:
  - 微信开放平台概述
  - 微信登录接口
  - 微信分享SDK
status: completed
date created: 星期二, 二月 25日 2025, 3:24:08 下午
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 简介

**微信开放平台**（WeChat Open Platform）是腾讯微信团队面向移动端应用、PC 网站应用、公众号及小程序开发者提供的开放接入服务。通过接入该平台，开发者可以利用微信庞大的用户基数与生态能力，实现第三方应用的微信登录、内容分享推广、微信支付等核心功能。

## 2. 核心开放能力

- **微信登录 (OAuth 2.0)**：允许用户通过微信扫码或 App 授权实现第三方平台的一键免注册登录，安全获取用户的 OpenID、UnionID 及基本个人资料。
- **微信分享**：支持将应用内的图文链接、音乐、视频、多媒体文件或小程序卡片，定向分享至微信好友会话、微信群或朋友圈。
- **微信支付**：为第三方移动 App 以及 PC 网页应用集成微信扫码支付与 App 支付接口，打通商业变现路径。
- **小程序互通**：支持在移动 App 中拉起指定的小程序，或在特定场景下从小程序内跳转唤醒关联的移动 App，实现多端生态联动。

## 3. 开发接入流程

1. **注册与认证**
   - 访问 [微信开放平台官网](https://open.weixin.qq.com/) 注册开发者账号。
   - 提交企业/组织主体资质进行年审认证（目前审核服务费为 300 元/年）。**注意：** 绝大多数核心 API（如微信登录与支付）仅对通过资质认证的企业主体开放。

2. **创建与审核应用**
   - 在控制台中新建“移动应用”或“网站应用”。
   - 移动应用需要配置 iOS 的 Bundle ID / Universal Links，或 Android 的应用包名与 MD5 签名。
   - 网站应用需要关联已完成备案的域名。

3. **获取接口凭证**
   - 应用通过微信官方审核后，平台将发放专用的 **`AppID`**（应用唯一标识）与 **`AppSecret`**（应用密钥）。

> [!CAUTION]
> **AppSecret 安全存储规范**
> `AppSecret` 拥有最高的接口调用权限。**严禁** 将其硬编码存放在客户端代码（如 App 客户端、小程序前端或前端 JS）中。所有涉及使用 `AppSecret` 换取令牌（如 OAuth2.0 获取 `access_token`）的逻辑，都必须在开发者自身的安全服务器端完成。

## 4. 参考资料

- [微信开放平台官方网站](https://open.weixin.qq.com/)
- [微信开放平台开发者文档](https://developers.weixin.qq.com/doc/oplatform/Mobile_App/Resource_Center_Homepage.html)
