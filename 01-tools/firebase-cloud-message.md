---
title: "CloudMessage"
aliases: []
tags: []
status:
date created: 星期四, 六月 18日 2026, 11:33:16 晚上
date modified: 星期五, 六月 19日 2026, 11:59:07 中午
---

<!-- toc -->

## 1. CloudMessage

消息推送工具

- 支持 Firebase 控制或者 API 构建推送消息
- 支持单设备、设置组、

### 1.1. 架构

CLoudMessage 实现架构

![](http://qiniu.sxyxy.top/20230927162030.png?images=images)

### 1.2. 消息类型

- 消息类型

| 消息类型 | 使用场景 |发送方式|
| --- | --- | --- |
| 通知消息 | FCM SDK 自动处理 |1.API 设置 nofification 键 </br> 2.Firebase 设置控制台|
| 数据消息 | 客户端自定义处理  |API 设置 data 键|

- 通知状态

|应用状态|通知|数据|两者皆有|
|---|---|---|---|
|前台|onMessageReceived|onMessageReceived|onMessageReceived|
|后台|系统托盘|onMessageReceived|通知：系统托盘 </br> 数据：在 intent 附加内容中|

> 程序退出不影响推送
