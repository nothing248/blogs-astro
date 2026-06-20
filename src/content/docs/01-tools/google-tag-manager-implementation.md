---
title: "GTM安装"
filename: google-tag-manager-implementation
description: Google Tag Manager（GTM）是免费的网站代码管理系统，用于避免硬编码部署跟踪代码。本文提供GTM安装及触发逻辑详解。介绍如何将核心JS基础代码放置于HTML的head与body节点中，并通过变量和触发器配合将第三方分析标签动态注入网站中。
tags: [google-tag-manager, gtm, tag-management, marketing-analytics]
aliases: [GTM安装, 代码管理, GTM触发器]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:33 下午
date modified: 星期五, 六月 19日 2026, 11:59:49 中午
---

<!-- toc -->

## 1. 简介

一款免费代码管理工具，可以避免前端硬编码来部署代码。

## 2. 安装

- 创建账号  
  - [创建账号链接](https://tagmanager.google.com/#/home)
  - 创建成功之后会获取一段 JS 的 **基础代码**
    ![](http://qiniu.sxyxy.top/20230926161809.png?images=images)

- 安装代码
  - 初次创建会获取下面样例的代码，如果不小心关闭，可以在 **Admin > Install Google Tag Manage** r 查看到该代码是信息
  - 需要将获取到的代码放置在每个页面上。**建议尽可能靠前(例如 head 标签头部)**
  - 代码样例

```js
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','***');</script>
<!-- End Google Tag Manager -->
```

## 3. 原理

GTM 底层是将在管理页面配置的信息把成 js 文件(**<https://www.googletagmanager.com/gtm.js?id=GTM-123>**)

> 其中 G-123 代码的容器 ID

## 4. 权限

用于共享并且管理 GTM 容器

- 阅读权限(Read)  
  只能查看不能修改
- 修改权限(Edit)  
  可以修改代码，但是不能提交版本
- 审批权限(Approve)  
  可以提交版本，但是不能发布版本
- 发布权限(Publish)  
  可以发布版本

## 5. 配置

### 5.1. 变量配置(Variable)

变量是获取数据的方式，通过配置变量可以将数据传递给 Tag。

- 内置变量类型  
不需要格外配置，仅需要进行开启就可以  
  ![内置变量类型](http://qiniu.sxyxy.top/20230926163529.png?images=images)

- 自定义变量类型  
需要手动进行配置  
  ![自定义变量类型](http://qiniu.sxyxy.top/20230926164247.png?images=images)

- 变量详解
  - DataLayer 类型
    一种也有的 GTM 数据上报方式

    ```js
    window.dataLayer.push({ecommnerce:null})
    window.dataLayer.push({
        event:"",
        ecommnerce:{
            transaction_id:"123",
            items:[{
                item_id:1
            }]
        },
    })
    ```

    > 如果希望 GTM 根据上报数据触发 Tag，则 event 参数为必传值
    >
    > push 只能上报对象，不能上报数组
    >
    > 如果上报对象内部有嵌套对象，建议每次上报新数据时手动将嵌套对象置空({ecommerce: null})。因为 GTM 中对象是合并操作。

    ![DataLayer 变量配置](http://qiniu.sxyxy.top/20230926184945.png?images=images)
  - Custom JavaScript 变量类型
    自定义 js 脚本  
    ![Custom JavaScript 变量配置](http://qiniu.sxyxy.top/20230926184455.png?images=images)
  - JavaSript Varaible 类型  
    获取页面全局变量  
    ![JavaSript Varaible 变量配置](http://qiniu.sxyxy.top/20230926184829.png?images=images)

### 5.2. 代码配置(Tag)

代码是用于实现特定功能的一段程序。

- 内置代码类型  
Google 系支持的表单配置方式的代码

  ![内置代码类型](http://qiniu.sxyxy.top/20230926185515.png?images=images)
- 三方代码类型
非 Google 系的内置的三方的表单配置方式的代码

  ![](http://qiniu.sxyxy.top/20230926185625.png?images=images)
- 自定义代码类型
可以编辑 script 脚本来进行直接(相当与将脚本直接部署在页面)

  ![](http://qiniu.sxyxy.top/20230926185830.png?images=images)

### 5.3. 触发器配置(Trigger)

- 内置触发器类型  
可以直接使用触发条件(例如页面加载等、元素点击)

  ![内置触发器类型](http://qiniu.sxyxy.top/20230926190001.png?images=images)
- 自定义触发器类型
可以根据 dataLayer 中 event 参数来自定义触发时机

  ![自定义触发器类型](http://qiniu.sxyxy.top/20230926190057.png?images=images)

> 如果需要自定义触发器，请确保 dataLayer.push 的对象有 event 参数信息
>
> 触发器支持子级条件过滤

## 6. 模版

模版是通过模版语法(受限制的 JS 语法)来自定义自己的代码类型、变量类型。

- 模板商城  
三方开发者发布出来的模版

  ![模版商城](http://qiniu.sxyxy.top/20230926191120.png?images=images)
- 自定义模版  
自己自定义的模版

  ![自定义模版](http://qiniu.sxyxy.top/20230926191221.png?images=images)

> 模板仅支持代码与变量，不支持触发器

## 7. 测试(Preview)

用于在发布之前进行测试，以确保 GTM 配置是否正确

- 定位预览页面  
用于确认在那个页面进行预览页面

  ![预览页面](http://qiniu.sxyxy.top/20230926192150.png?images=images)

> 预览测试过程中，页面发生跳转不会中断预览链接

- 预览面板  
用于监测测试过程的中间数据与状态

  ![预览面板](http://qiniu.sxyxy.top/20230926192758.png?images=images)

> 预览面板对应的 URL 链接可以进行三方分享

## 8. 发布(Submit)

发布是将对应工作区(一批配置项)进行上线的操作。只有发布的的工作区才会在正式环境上生效

- 发布操作
用于创建版本(发布版本)
  
  ![发布操作](http://qiniu.sxyxy.top/20230926193751.png?images=images)
- 查看生效版本
用于查看当前生效的版本(发布版本)

  ![查看版本](http://qiniu.sxyxy.top/20230926194358.png?images=images)

> 默认工作区限制 **3 个**，请合理划分工作区。

## 9. 拓展信息

- GTM 存在大小限制，在超过 70%时，可以在 Versions Tab 中看到达到的上限的的百分比大小。
  
  ![](http://qiniu.sxyxy.top/20230926163057.png?images=images)
- GTM 预览时默认会开启新窗口来展示预览页面(可能导致浏览器插件不可以使用)  
  **安装 Tag Assistant Legacy (by Google)浏览器插件** 可以不开启新窗口。
- GTM 网络限制
  - GTM 生成的 gtm.js 文件不受墙的限制
  - GTM 的配置管理界面受网络限制，需要自行挂载代理

## 10. 参考资料

- [官方链接](https://developers.google.com/tag-manager/quickstart?hl=zh-cn)
