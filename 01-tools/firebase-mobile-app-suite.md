---
title: "Firebase推送"
filename: firebase-mobile-app-suite
description: Firebase是Google提供的移动端应用开发服务集合。本文系统梳理了其Analytics数据采集与事件上报机制、跨端H5数据桥接原生Android的JS接口设计，以及CloudMessage（FCM）推送的底层架构与后台运行机制。适用于需要在App中集成跨平台埋点和消息推送的技术团队。
tags: [firebase, analytics, cloud-messaging, h5-bridge]
aliases: [Firebase推送, GA4分析, FCM集成]
status: completed
date created: 星期一, 九月 22日 2025, 5:12:53 下午
date modified: 星期五, 六月 19日 2026, 11:59:09 中午
---

<!-- toc -->

## 1. 简介

firebase 是一个 Google 系的免费的工具集合，一般用于 APP 端(Android 和 iOS)三方工具集成。

## 2. 工具概览

1. Analytics  
用于进行用户跟踪数据采集
2. CloudMessage  
消息推送
3. InAppMessage  
消息内推送
4. Config  
远程控制 APP 内配置项
5. DynamicLink(动态链接)
APP 优化版的深度链接
6. Crashlytics  
  APP 崩溃监控
7. A/B Test  
  APP 进行 A/B Test

## 3. 安装

- 创建项目  
Firebase 项目用于统一管理各个工具集合。(需要关联 GCP 账户与 Google Aanlytics 账户)
  
![创建项目](http://qiniu.sxyxy.top/20230927113953.png?images=images)

- 创建应用  
针对 Android iOS Web 选择对应应用。并获取到对应的 google-services.json 配置文件
  
![创建应用](http://qiniu.sxyxy.top/20230927114348.png?images=images)

> 如果应用会用于动态链接，则需要填写应用签名。

- 安装应用  
将 Firebase 创建的应该集成到 APP 中
  - 将 google-services.json 文件放置应用根目录
  - 安装 Google 服务 Gradle 插件

    ![](http://qiniu.sxyxy.top/20230927115636.png?images=images)
  - 安装 Firebase SDK

    ![](http://qiniu.sxyxy.top/20230927120603.png?images=images)

## 4. Analytics

用于行为数据采集工具

### 4.1. 初始化

```java
private FirebaseAnalytics mFirebaseAnalytics; #声明
mFirebaseAnalytics = FirebaseAnalytics.getInstance(this); #初始化
```

### 4.2. 上报事件

事件由事件名称与一系列事件参数组成

- 普通事件

```
Bundle bundle = new Bundle();
bundle.putString(FirebaseAnalytics.Param.ITEM_ID, id);
bundle.putString(FirebaseAnalytics.Param.ITEM_NAME, name);
bundle.putString(FirebaseAnalytics.Param.CONTENT_TYPE, "image");
mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.SELECT_CONTENT, bundle);
```

- 电商事件

```java
Bundle itemJeggingsWithIndex = new Bundle(itemJeggings);
itemJeggingsWithIndex.putLong(FirebaseAnalytics.Param.INDEX, 1);
Bundle itemBootsWithIndex = new Bundle(itemBoots);
itemBootsWithIndex.putLong(FirebaseAnalytics.Param.INDEX, 2);
Bundle itemSocksWithIndex = new Bundle(itemSocks);
itemSocksWithIndex.putLong(FirebaseAnalytics.Param.INDEX, 3);
Bundle viewItemListParams = new Bundle();
viewItemListParams.putString(FirebaseAnalytics.Param.ITEM_LIST_ID, "L001");
viewItemListParams.putString(FirebaseAnalytics.Param.ITEM_LIST_NAME, "Related products");
viewItemListParams.putParcelableArray(FirebaseAnalytics.Param.ITEMS,
new Parcelable[]{itemJeggingsWithIndex, itemBootsWithIndex, itemSocksWithIndex});
mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.VIEW_ITEM_LIST, viewItemListParams);
```

> Analytics 的自定义事件参数需要现在 Google Analytic 中进行注册

### 4.3. 设置用户属性

用户属性用于来标识用户的特征

```java
mFirebaseAnalytics.setUserProperty("favorite_food", food);
```

> Analytics 的自定义用户属性需要现在 Google Analytic 中进行注册

### 4.4. 设置用户 ID

用户 ID 需要可以用于跨平台用户关联

```java
mFirebaseAnalytics.setUserId("123456");
```

> 非必须

### 4.5. 查看日志

可以通过日志查看 Firebase 的日志信息。

```shell
adb shell setprop log.tag.FA VERBOSE
adb shell setprop log.tag.FA-SVC VERBOSE
adb logcat -v time -s FA FA-SVC
```

![日志信息](http://qiniu.sxyxy.top/20230927143043.png?images=images)

### 4.6. 调试

可以通过调试面板查看具体的事件等信息

```shell
adb shell setprop debug.firebase.analytics.app PACKAGE_NAME
```

![调试面板](http://qiniu.sxyxy.top/20230927143205.png?images=images)

### 4.7. 拓展信息

- 内置 H5 页面的数据采集方案
  - 方案 1 </br>
        **实施方式:**
        在同一个 GA Property 中创建 Web Stream，并且将数据直接发送到 Web Stream 中。  
        **优势**:  
    - 可以在 H5 页面使用一套埋点  
        **劣势**:  
    - 可能会造成用户(可以传递用户的 app_instance_id 来避免)与会话拆分、影响到归因。
  - 方案 2 </br>
        **实施方式:**  
    - 将 H5 请求转发到 Android 原生应用，然后转发到 GA  
        **优势:**
    - 不会有用户与会话切分，不会影响到归因
        **劣势:**
    - 需要维护两套埋点
        **实施步骤:**
    - H5 页面处理程序

        ```java
        function logEvent(name, params) {
          if (!name) {
          return;
          }
        
          if (window.AnalyticsWebInterface) {
          // Call Android interface
          window.AnalyticsWebInterface.logEvent(name, JSON.stringify(params));
          } else if (window.webkit
          && window.webkit.messageHandlers
          && window.webkit.messageHandlers.firebase) {
          // Call iOS interface
          var message = {
          command: 'logEvent',
          name: name,
          parameters: params
          };
          window.webkit.messageHandlers.firebase.postMessage(message);
          } else {
          // No Android or iOS interface found
          console.log("No native APIs found.");
          }
          }
        
        function setUserProperty(name, value) {
        if (!name || !value) {
        return;
        }
        
        if (window.AnalyticsWebInterface) {
        // Call Android interface
        window.AnalyticsWebInterface.setUserProperty(name, value);
        } else if (window.webkit
        && window.webkit.messageHandlers
        && window.webkit.messageHandlers.firebase) {
        // Call iOS interface
        var message = {
        command: 'setUserProperty',
        name: name,
        value: value
        };
        window.webkit.messageHandlers.firebase.postMessage(message);
        } else {
        // No Android or iOS interface found
        console.log("No native APIs found.");
        }
        }
        ```

    - Android 处理程序

        ```java
        public class AnalyticsWebInterface {
        
            public static final String TAG = "AnalyticsWebInterface";
            private FirebaseAnalytics mAnalytics;
        
            public AnalyticsWebInterface(Context context) {
                mAnalytics = FirebaseAnalytics.getInstance(context);
            }
        
            @JavascriptInterface
            public void logEvent(String name, String jsonParams) {
                LOGD("logEvent:" + name);
                mAnalytics.logEvent(name, bundleFromJson(jsonParams));
            }
        
            @JavascriptInterface
            public void setUserProperty(String name, String value) {
                LOGD("setUserProperty:" + name);
                mAnalytics.setUserProperty(name, value);
            }
        
            private void LOGD(String message) {
                // Only log on debug builds, for privacy
                if (BuildConfig.DEBUG) {
                    Log.d(TAG, message);
                }
            }
        
            private Bundle bundleFromJson(String json) {
                // ...
            }
        
        }
        ```

    - 注册程序

        ```java
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            mWebView.addJavascriptInterface(
            new AnalyticsWebInterface(this), AnalyticsWebInterface.TAG);
        } else {
            Log.w(TAG, "Not adding JavaScriptInterface, API Version: " + Build.VERSION.SDK_INT);
        }
        ```

## 5. CloudMessage

消息推送工具

- 支持 Firebase 控制或者 API 构建推送消息
- 支持单设备、设置组、

### 5.1. 架构

CLoudMessage 实现架构

![](http://qiniu.sxyxy.top/20230927162030.png?images=images)

### 5.2. 消息类型

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

## 6. 拓展信息

- 部分工具服务依赖于 Google Play 服务.
- Firebase ID
  Firebase 中常见的 ID 信息。
  - Firebase Instace ID </br>
    是应用安装的标识。后期被废弃转用 Firebase Installations ID(FID)
  - Firebase Installation ID </br>
    最新版用于安装的标识  
  - Firebase Analytics ID </br>
    用于在 GA 标识用户的 ID

  > Firebase Instace ID 与 Firebase Analytics ID 不一致。

## 7. 参考资料

- [官方文档](https://firebase.google.com/docs?hl=zh-cn)
- [Android 应用签名](https://developers.google.com/android/guides/client-auth?authuser=0&hl=zh-cn)
- [GooglePlay 服务依赖列表](https://firebase.google.com/docs/android/android-play-services?hl=zh&authuser=0)
- [Android Demo 仓库](https://github.com/firebase/quickstart-android.git)
- [Firebase Instance ID](https://firebase.google.com/support/privacy/manage-iids?hl=zh-cn)
- [Firebase Installation ID](https://firebase.google.com/docs/projects/manage-installations?hl=zh-cn#fid-iid)
- [Google API 调试工具](https://developers.google.com/oauthplayground/)
