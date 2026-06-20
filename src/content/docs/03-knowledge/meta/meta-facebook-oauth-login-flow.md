---
title: "Meta OAuth 登录"
filename: meta-facebook-oauth-login-flow
description: Meta (Facebook) 平台的 OAuth 2.0 登录机制与手动授权流程实用指南。详细解决在第三方应用中集成 Facebook 登录、换取与调试长短期 Access Token、以及通过 Marketing API 操作自定义受众（Custom Audiences）的流程。包含核心的 OAuth 2.0 步骤说明、安全规范与 Python SDK 调用示例。
tags:
  - oauth2
  - facebook-login
  - meta-api
  - authentication
aliases:
  - Meta OAuth 登录
  - Facebook 登录流程
  - Access Token 调试
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:24 上午
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

## 1. 简介

Meta (Facebook) 登录基于标准的 **OAuth 2.0** 协议，允许第三方应用以安全、合规的方式访问 Meta 平台上的用户资产（例如用户的基本资料、电子邮箱、广告账户权限以及受众群体管理等）。本指南将深入拆解 Facebook 手动 OAuth 登录流程的核心阶段，并针对如何调试 Access Token、调用受众群体（Custom Audiences）API 进行详细说明。

---

## 2. OAuth 2.0 授权机制

在 Meta 登录体系中，主要包含以下核心概念：

- **Client ID & Client Secret**：应用在 Meta for Developers 注册时生成的应用编号和应用密钥（Secret 需要严格保密）。
- **Redirect URI**：用户授权成功后，Meta 平台重定向回第三方应用的接收端地址。
- **Scope (权限范围)**：请求用户授权的权限列表（例如 `public_profile`, `email`, `ads_management`, `business_management`）。
- **Access Token (访问令牌)**：
  - **短期令牌 (Short-lived Token)**：通常有 2 小时的有效期，通常直接由前端网页 SDK 或基于 Code 兑换获得。
  - **长期令牌 (Long-lived Token)**：有效期通常为 60 天。可以通过在后端调用 Meta Graph API，用短期令牌换取，从而允许服务在后台代表用户执行离线操作。

---

## 3. 手动授权流程步骤 (Manual Flow)

如果无法直接使用 Facebook 官方的 Web 或移动端 SDK，开发者可以通过构造标准的 HTTP 浏览器跳转和 API 调用来完成手动授权：

### 3.1. 阶段一：引导用户进行授权重定向

将用户重定向至 Meta 统一的 OAuth 对话框。URL 格式如下：

```
https://www.facebook.com/v23.0/dialog/oauth?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &state={state-param}
  &scope=email,public_profile
```

> [!IMPORTANT]
> `state` 参数通常包含一个随机生成的 CSRF 预防 Token，第三方应用在回调时必须校验该参数以保证通信安全。

### 3.2. 阶段二：接收授权码 (Authorization Code)

用户在 Meta 对话框中确认授权后，Meta 会将浏览器重定向回你的 `redirect_uri`。你将在 URL 的 Query 参数中获得授权码：

```
http://your-redirect-uri.com/?code=AQD...#_=_
```

### 3.3. 阶段三：使用授权码换取短期 Access Token

从服务端向 Meta 发起 HTTP GET/POST 请求，用授权码兑换短期令牌：

```http
GET https://graph.facebook.com/v23.0/oauth/access_token?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &client_secret={app-secret}
  &code={code-from-step-two}
```

**响应 JSON 示例**：

```json
{
  "access_token": "EAAJzZ...",
  "token_type": "bearer",
  "expires_in": 7199
}
```

### 3.4. 阶段四：获取或延长为长期 Access Token

在服务器端，你可以通过请求将短期用户 Access Token 兑换为长期 Access Token：

```http
GET https://graph.facebook.com/v23.0/oauth/access_token?  
  grant_type=fb_exchange_token&           
  client_id={app-id}&
  client_secret={app-secret}&
  fb_exchange_token={short-lived-token}
```

---

## 4. 广告营销 API 实践：自定义受众

当获取了具备 `ads_management` 或 `ads_read` 权限的 Access Token 后，可以结合 Meta Marketing API 来创建和管理自定义受众（Custom Audiences）。

### 4.1. Python 代码调用示例 (Business SDK)

以下展示如何使用 Meta 官方 Python Business SDK 创建一个受众群体的基本片段：

```python
import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience

# 1. 初始化 API
access_token = '[Access Token已脱敏]'  # 替换为你获取到的长期有效 Token
app_secret = '[App Secret已脱敏]'
app_id = '[App ID已脱敏]'
FacebookAdsApi.init(app_id, app_secret, access_token)

# 2. 初始化广告账户对象
ad_account_id = 'act_1234567890'  # 替换为你的实际广告账户 ID
account = AdAccount(ad_account_id)

# 3. 创建自定义受众
params = {
    'name': 'My New Custom Audience',
    'subtype': 'CUSTOM',
    'description': 'Audience created via Python SDK',
    'customer_file_source': 'USER_PROVIDED_ONLY',
}
audience = account.create_custom_audience(params=params)
print(f"Created Custom Audience with ID: {audience['id']}")
```

---

## 5. 参考文档

- [授权文档](https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow)：Facebook 手动集成登录流程（Manual Flow）的官方开发者指南。
- [API 官方测试工具](https://developers.facebook.com/tools/explorer?method=GET&path=1527919421902618&version=v23.0)：Graph API Explorer，可在线编写与测试所有的 Graph API 请求。
- [全选验证工具](https://developers.facebook.com/tools/debug/accesstoken/?access_token=EAAJzZCL7U0RsBPOPlpWZBRqSz1jwaa7MormOeYvHZBoJ4C6ouR2ki5LIR2YNXH4jexoVOzLqZBKMUI6lLbU635DFVIjKg5GrW1W6cWCwUbLSTveQDD3FREU2wZAGdEK35p6gbAnNB0o4ezakZCc4ZCXqy7sOZBZAikKkhtBSyCvdB0wseSTrXap7cGSUDDelsV5FdmYZBmSdcVLuZAegzWPH7B4vs6ZAyQjMcdUYKdYanWYhpF3j6IG0vl4i&version=v23.0)：Access Token Debugger，用于解密令牌结构、查看有效期、拥有权限、授权应用等信息。
- [受众群体 API](https://developers.facebook.com/docs/marketing-api/audiences/guides/custom-audiences)：官方 Marketing API 开发文档，涵盖基于 customer file 创建自定义受众的方法。
- [facebook 开源仓库](https://github.com/facebook/facebook-python-business-sdk/blob/main/examples/AdAccountCustomAudiencesPostCreateCustomAudience.py)：Facebook Python Business SDK 官方示例源码，展示受众群体的创建与维护。
