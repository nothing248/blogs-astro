---
title: "GA4数据采集"
filename: google-analytics-ga4-guide
summary: Google Analytics 4（GA4）是新一代用户行为数据分析工具。本文聚焦于Web端使用Gtag/GTM以及移动端基于Firebase进行数据采集的最佳实践。分析了会话级来源识别中ga_campaign事件的作用，并解答了DebugView调试模式与BigQuery导出中特定事件未注册导致的not set问题。
tags: [google-analytics, ga4, data-tracking, firebase]
aliases: [GA4数据采集, Gtag配置, DebugView调试]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:33 下午
date modified: 星期五, 六月 19日 2026, 11:59:29 中午
---

<!-- toc -->

## 1. 简介

一个 Google 的数据跟踪分析工具，包含 APP 端(Firebase)、Web 端。并且 GA 主要分为 GA、GA4 两个版本，其中 GA 在 20230701 进行停用，所以该文档主要围绕 GA4 进行。

## 2. 数据采集

### 2.1. Web

- gtag
- gtm

### 2.2. APP

- firebase

> campagin_details 事件 debugView 与报告中不可见.但是上报日志中可以看见, 报告中对应的事件名称为 not set, Biquery 中可以查询到。可以覆写用户来源信息。会话层级的来源信息
>
> APP 调用深链会自动上报 ga_campaign 事件，该事件用于识别会话信息。
>
> FireBase 日志是可以通过 FA FA-SVC 进行过滤(展开日志中包含 app_instance_id 信息)，或者 Logging Event 过滤(app、app/gtm、auto 可以标识采集来源)
>
> Firebase 调试日志，请确保 app_id 是目标 APP，因为手机可能会出现其他安装报的日志信息。
>
> Firebase 生成的 app_istance_id 为 32 的字符串
>
> Firebase 清除数据会开启新会话，但是 app_instance_id 不会变。app_instance_id 只有卸载重新安装变，开发环境下的重新编译也不会变。

### 2.3. Measurement Protocol(MP)

可以实现 Server 端的数据上报

- 在 GA 报表中回去对应的参数
  - measurement_id
  - api_secret

- 构造请求参数

```javascript
let event = {
    "client_id": "x",
        "events": [
        {
            "name": "offline_purchase",
            "params": {
                "engagement_time_msec": "100",
                "session_id": "123"
            }
        }
    ]
}
```

> 如果为了在实时报告中呈现数据，则 engagement_time_msec、session_id 参数为必传参数。
>
> 如果为了 Debug Vuew 中呈现数据，则必须上报 engagement_time_msec、debug_mode: 1 参数。
>
> 如果希望发送事件时间进行回溯(最大回溯 3 天，超过会按照实时进行归类)，则必须上报 timestamp_micros 参数。

- 验证请求

```javascript
const measurement_id = `G-XXXXXXXXXX`;
const api_secret = `<secret_value>`;
fetch(`https://www.google-analytics.com/debug/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}`, {
  method: "POST",
  body: JSON.stringify(event)
});
```

> 该请求用于检验请求构造信息，因为正式环境中发生错误不会返回错误信息。

- 发送请求

```javascript
const measurement_id = `G-XXXXXXXXXX`;
const api_secret = `<secret_value>`;

fetch(`https://www.google-analytics.com/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}`, {
  method: "POST",
  body: JSON.stringify(event)
});
```

- 限制  

![](http://qiniu.sxyxy.top/20231016111107.png?image=image)

> 注意：MP 不是一个完整等同于 gtag 或者 gtm 的数据采集工具，仅仅是一个数据补充工具(因为新用户识别、user_id 识别、会话归因、地理信息识别等需要结合前端才能正常识别)，一般用于将线下订单进行上报等用途。

## 3. 拓展信息

- 老版本 GA VS　新版本 GA(GA4)
  - 新版本优化了针对 APP 的功能，使得针对 APP 的支持更好
  - 老板的 GA 将在标准版本(20230701)、360 版本(20240701)进行停用。
  - 新版本针对数据隐私进行了更好的优化。
- GA4 报告抽样
  - 探索或漏斗报告会加载事件与用户的原始数据，标准报告和 Data API 会使用预处理的数据库表。
  - GA4 免费用户实，限制为 1000 万个事件，GA4 360 限制为 10 亿个事件。
  - 可以通过调整样本总量。调整精确度、请求完整报告(这两个仅限 360 用户)进行解决数据抽样问题。
- GA4 会话识别
  - 会话一段时间内的一组事件的集合
  - 会话的默认过期时间为 30 分钟，用户可以根据需求进行调整
  - 如果涉及到跨域，必须保证 session_id 是一致的，否则会话会重复计算(即使是否 client_id 与 user_id 是一致的)。
  - 互动会话是一个超过 10 秒、有一个转化事件、最少两个 PV 的会话
- GA4 Cookie 信息
  - **_ga: GA1.1.1839118052.1697785623**, 其中 1839118052.1697785623 代表当前用户的 client_id。
  - **_ga_\$Measurement_id\$: GS1.1.1698031837.3.0.1698032076.0.0.0**, 其中 1698031837 时间戳代表的是 session_id,1698032076 时间戳代表的是上一个事件对应的时间戳信息。
- GA4 报告中 Insight 报告邮件订阅错误
  - 过滤请求关键字 **customalertsubscription**
  - 如果对应邮箱有注册 Gmail 但是没有注册 GA，会报内部错误
  - 如果没有注册 Gmail，则添加无效
- GA4 前端页面请求权限验证关系
  - 依赖的是 cookie 的**_Secure**前缀的一系列 Cookie 信息
- 关联 BQ
  - 支持流式导出与 Daily 导出。Admin 权限都可以配置导出。
  - 新增的流，需要重新配置。默认不会导出。

## 4. 参考资料

- [老版本 GA 官网](https://developers.google.com/analytics/devguides/collection/analyticsjs)
- [新版本 GA4 官网](https://developers.google.com/analytics/devguides/collection/ga4/tag-options)
- [MP 官方文档](https://developers.google.com/analytics/devguides/collection/protocol/ga4)
- [GA4 数据抽样文档](https://support.google.com/analytics/answer/13331292?hl=zh-Hans&sjid=16588711683833737684-AP)
- [GA4 数据导出到 BQ 文档](https://support.google.com/analytics/answer/9358801?hl=zh-Hans&sjid=5200249160157794527-AP#zippy=)
- [Consent Mode 文档](https://support.google.com/analytics/answer/9976101?hl=en)
