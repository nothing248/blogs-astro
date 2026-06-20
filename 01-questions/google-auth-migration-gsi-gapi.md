---
title: "Google 认证迁移指南"
filename: google-auth-migration-gsi-gapi
description: 本文解决了 Google OAuth 2.0 授权库（gapi.auth）废弃导致的认证失败问题。由于 Google 强制新应用使用最新的 Google Identity Services (GSI) 库，旧有的 gapi 库已无法直接处理授权。文中提供了详细的迁移方案，包括集成新的 gsi 库、初始化 Token 客户端、通过 `requestAccessToken` 获取令牌，并配合 gapi SDK 调用 Google Analytics API（UA Report）的具体实现代码，实现身份验证与数据访问的解耦。
tags: ["Google-Auth", "OAuth2.0", "GSI", "GAPI", "Google-Analytics"]
aliases: ["Google 认证迁移指南", "gapi.auth 废弃解决方案", "Google Identity Services 迁移"]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:20 下午
date modified: 星期五, 六月 19日 2026, 11:56:50 中午
---

<!-- toc -->

## 1. 背景

- 老版本使用 `gapi.auth` 配合新创建的 Web Application 凭证信息时，会出现以下报错：
- 关键难点：已有 API 代码库多基于 [gapi.auth](https://github.com/google/google-api-javascript-client/blob/master/docs/reference.md) 实现。

```shell
"You have created a new client application that uses libraries for user authentication or authorization that are deprecated. New clients must use the new libraries instead. See the [Migration Guide](https://developers.google.com/identity/gsi/web/guides/gis-migration) for more information."
```

## 2. 原因

Google 更新了 OAuth 2.0 的授权方式，并强制限制新创建的 Web Application 凭证必须使用最新的授权方式，不再兼容旧版的 `gapi.auth` 库进行初始化。

---

## 3. 解决方案

### 3.1. 方案一：沿用旧版（受限）

- 仅适用于以前已创建且未更新的 Web Application 授权文件，继续配合 [gapi.auth](https://developers.google.com/identity/sign-in/web/reference?hl=zh-cn#gapiauth2initparams) 使用。但不推荐用于新项目。

### 3.2. 方案二：迁移至最新 GSI 库（推荐）

最新版 Google 登录方式 [GSI (Google Identity Services)](https://developers.google.com/identity/gsi/web/guides/overview?hl=zh-cn) 将 **身份验证 (Authentication)** 与 **授权 (Authorization)** 进行了分离：

- **Authentication API**：用于获取登录 ID 令牌。
- **Authorization API**：用于获取数据访问令牌。

#### 3.2.1. 集成 SDK

需要在页面中同时加载 `gsi`（用于认证）和 `gapi`（用于调用 Google 产品 API）：

```html
<script src="https://apis.google.com/js/api.js"></script> <!-- gapi库：用于调用Google系产品API -->
<script src="https://accounts.google.com/gsi/client"></script> <!-- gsi库：Google最新版本的用户身份验证库 -->
```

#### 3.2.2. 初始化 Token Client

```js
let client = google.accounts.oauth2.initTokenClient({
    client_id: '[CLIENT_ID_已隐藏]',
    scope: 'https://www.googleapis.com/auth/analytics.readonly',
    callback: res => { 
        // 注意：该回调会在每次调用 requestAccessToken 获取 Token 时触发
        let token = res.access_token;
        console.log('Access Token:', token);
    },
});
```

#### 3.2.3. 获取授权 Token

触发用户授权流程：

```js
client.requestAccessToken();
```

  ![image-20230801194717430](http://qiniu.sxyxy.top/image-20230801194717430.png?image=image)

#### 3.2.4. 使用 Gapi SDK 访问数据

以加载 Google Analytics (UA) Report API 为例：

```js
gapi.load("client", () => {
    // 初始化 gapi SDK 并设置上面获取到的 Token
    gapi.client.setToken({ access_token: token });

    // 加载对应的 API Discovery 文档
    gapi.client.load("https://content.googleapis.com/discovery/v1/apis/analyticsreporting/v4/rest").then(() => {
        // 调用对应 API 获取数据
        gapi.client.analyticsreporting.reports.batchGet({
            resource: {
                reportRequests: [
                    {
                        viewId: '[VIEW_ID_已隐藏]',
                        dateRanges: [{ startDate: '7daysAgo', endDate: 'today' }],
                        metrics: [{ expression: 'ga:sessions' }]
                    }
                ]
            }
        }).then(
            res => console.log('Report Data:', res),
            err => console.error('API Error:', err)
        );
    });
});
```
