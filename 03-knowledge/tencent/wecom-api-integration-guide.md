---
title: "企业微信API对接"
filename: wecom-api-integration-guide
description: 企业微信 (WeCom) 接口集成与加解密开发指南。内容整理了使用 Node.js 库 @wecom/crypto 进行签名生成、数据加解密的代码示例。梳理了基于 corpid 与 corpsecret 换取全局凭证 access_token 的授权机制，介绍了回调模式服务器验证逻辑以及微信客服接口消息同步注意事项。
tags:
  - tengxun
  - wecom
  - api-integration
  - encryption
  - nodejs
aliases:
  - 企业微信API对接
  - 企业微信加解密
  - WeCom接口集成
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:21 上午
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 简介

本文主要介绍企业微信（WeCom）后台接口对接的技术实现，包括官方提供的回调加解密算法、基本的 API 授权机制、接收用户消息的服务器配置流程，以及微信客服模块的对接要点。

---

## 2. 官方加解密库使用

为了保证消息交互的安全性，企业微信在回调模式下发送的报文均经过加密处理。在 Node.js 环境下，建议使用企业微信官方推荐的加解密库 `@wecom/crypto`。

- **依赖安装**

```shell
npm install @wecom/crypto
```

- **签名校验与加解密实现**

```javascript
import { getSignature, decrypt, encrypt } from '@wecom/crypto';

// 1. 签名校验：验证请求是否确实来自企业微信后台
const signature = getSignature(token, timestamp, nonce, ciphered);
if (signature === query.signature) {
    console.log("签名校验成功");
}

// 2. 解密接收到的密文数据
const { message, id } = decrypt(encodingAESKey, ciphered);
console.log("解密后的消息主体与企业Corpid:", { message, id });

// 3. 对准备回复给企业微信的消息执行加密
const replyCiphered = encrypt(encodingAESKey, replyMessage, id);
console.log("加密后的密文数据:", replyCiphered);
```

---

## 3. 授权认证流程

企业微信所有管理接口的调用都必须基于全局凭证 `access_token`。

- **鉴权机制**：
  开发者通过企业微信的 `corpid` (企业 ID) 和应用的 `corpsecret` (应用凭证) 请求微信授权网关换取 `access_token`。

![企业微信授权流程图](http://qiniu.sxyxy.top/20250811175740.png)

---

## 4. 接收消息回调配置

要实现被动接收用户发送的消息，开发者需要在企业微信管理后台配置消息端点（接收消息服务器 URL）。

1. **服务器验证**：当保存配置时，企业微信后台会向填写的 URL 发送一个带有 `echostr` 参数的 GET 请求，开发者需对该密文进行解密并原样返回解密明文，以验证服务器可用性。

   ![服务器验证交互](http://qiniu.sxyxy.top/20250811175929.png)

2. **消息端点接收**：验证通过后，用户发送的消息及系统事件会通过 POST 请求持续投递到该消息端点 URL。

   ![消息接收流](http://qiniu.sxyxy.top/20250811175952.png)

---

## 5. 微信客服接口对接

企业微信提供了对外的“微信客服”能力，可让用户在微信端直接发起咨询，企业在企业微信或自建系统中统一回复。

![微信客服 API](http://qiniu.sxyxy.top/20250811180142.png)

> [!IMPORTANT]
> **消息获取规则**
> 微信客服消息接口拉取历史记录时，**默认是旧消息在前，新消息在后**。如需获取最新产生的客服对话消息，需要向后滚动翻页（基于 `next_cursor`）直至最后一页以检索实时数据。

---

## 6. 参考资料

- [企业微信官方加解密库说明](https://developer.work.weixin.qq.com/document/path/90307)
- [API 授权获取 AccessToken 说明](https://developer.work.weixin.qq.com/document/path/91039)
- [接收消息与事件回调文档](https://developer.work.weixin.qq.com/document/path/90238)
- [企业微信全局错误码/状态码查询工具](https://developer.work.weixin.qq.com/devtool/query?e=40056)
- [微信客服 API 开发文档](https://developer.work.weixin.qq.com/document/path/94670#%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89)
