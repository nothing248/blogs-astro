---
title: "Baidu Analytics"
filename: baidu-analytics-setup
summary: 百度统计（百度分析云）是一款类似于 Google Analytics 的网站流量分析工具。本笔记介绍了百度统计的账号注册要点、网站创建流程，以及基础数据采集代码和自定义事件跟踪代码的部署方法，帮助开发者快速在站点中集成流量监控功能。
tags: ["百度统计", "网站分析", "流量监控", "SEO", "数据采集"]
aliases: ["Baidu Analytics", "百度分析云", "网站数据采集"]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:21 下午
date modified: 星期五, 六月 19日 2026, 11:57:40 中午
---

<!-- toc -->

## 1. 简介

**百度统计**（现常称为百度分析云）是百度推出的一款专业网站流量分析工具。它能够帮助网站管理者追踪访问者行为、分析流量来源、监控转化率，并为 SEO 优化提供重要数据支持，是国内网站运营的必备工具之一。

---

## 2. 账号注册与站点创建

1. **注册账号**：访问百度统计官网，使用百度云账号或百度账号进行登录。
2. **创建站点**：在后台点击“新增网站”，填入网站名称、主域名等信息。

    - > [! important] 注意
      > 填写的站点域名必须与实际部署代码的域名保持一致，否则可能无法正常统计数据。

---

## 3. 代码部署

### 3.1. 基础采集代码

获取百度统计提供的 JS 代码片段，并将其安装在网站所有页面的 `</head>` 标签之前。

```javascript
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  // 下方的 XXXXXXXX 为你的站点专属 Token
  hm.src = "https://hm.baidu.com/hm.js?XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
```

### 3.2. 事件跟踪代码

对于按钮点击、下载链接等非跳转行为，可以使用事件跟踪功能：

```javascript
// 语法：_hmt.push(['_trackEvent', category, action, opt_label, opt_value]);
_hmt.push(['_trackEvent', '视频', '播放', '首页Banner', 1]);
```

---

## 4. 拓展信息

- **实时访客**：百度统计提供分钟级的实时流量监控。
- **移动端支持**：除了 Web 端，也支持针对移动 App 的统计分析。

---

## 5. 参考资料

- [百度统计官方帮助中心](https://tongji.baidu.com/web/help/article?id=343&type=0)
