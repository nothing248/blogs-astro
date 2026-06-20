---
title: "Chrome使用技巧"
filename: google-chrome-tips-search-commands
description: 本笔记汇总了 Google Chrome 浏览器的高级使用技巧。重点介绍了 Google 搜索的高级参数（如 lr, cr, as_qdr）与搜索指令（如 site:, filetype:, numerical range 等）。此外，还提供了针对开发者的实用技巧，如解决 DevTools 无法粘贴的问题以及配置 HSTS 以允许访问特定 HTTP 站点的调试方法。
tags: ["Chrome", "Google-Search", "DevTools", "Browser-Tips", "SEO"]
aliases: ["Chrome使用技巧", "Google搜索指令大全", "Chrome开发调试"]
status: completed
date created: 星期二, 三月 24日 2026, 3:38:04 下午
date modified: 星期五, 六月 19日 2026, 11:59:32 中午
---

<!-- toc -->

## 1. Google 搜索高级指令

在 Chrome 地址栏或 Google 搜索框中利用特定操作符可以大幅提升搜索效率。

### 1.1. 逻辑与过滤指令

- **精确匹配**：`"关键词"`（使用双引号）。
- **排除项**：`关键词 -排除词`。
- **占位符**：`*`（匹配任意单词）。
- **数值范围**：`300..4000`（用于价格、年份等）。

### 1.2. 站点与文件查询

- **特定站点搜索**：`site:example.com 关键词`。
- **查找特定文件类型**：`filetype:pdf 论文`。
- **查找相似网站**：`related:google.com`。
- **查看缓存信息**：`cache:域名`。

---

## 2. 搜索 URL 参数 (高级控制)

通过直接修改 URL 中的参数，可以实现更精细的控制：

- `num=100`：单页返回结果数量（1-100）。
- `lr=lang_zh-CN`：限制语言（如简体中文）。
- `cr=countryUS`：限制国家（如美国）。
- `as_qdr=m2`：限制时间范围（`m2` 为过去两个月，`y` 为年，`d` 为天）。

![](http://qiniu.sxyxy.top/20240119103109.png?image=image)

---

## 3. 开发者进阶技巧

### 3.1. 开启 DevTools 粘贴功能

在某些受限页面，控制台可能禁止粘贴代码。

- **解决方法**：在控制台输入 `allow pasting` 并回车，即可解锁粘贴权限。

### 3.2. 处理 HSTS 证书冲突

如果 Chrome 强制将 HTTP 跳转为 HTTPS 导致本地调试失败，可以清理 HSTS 缓存：

- 访问：`chrome://net-internals/#hsts`。
- 在 "Delete domain security policies" 中输入域名并点击删除。

---

## 4. 常用快捷键

| 快捷键 | 功能 |
| :--- | :--- |
| `Ctrl + Shift + T` | 恢复最近关闭的一个标签页 |
| `Ctrl + L` | 快速聚焦地址栏 |
| `Ctrl + Shift + N` | 开启无痕模式窗口 |
| `Ctrl + F12` (Mac: `Cmd + Option + I`) | 打开开发者工具 |

---

## 5. 参考资料

- [Google 搜索高级技巧图解](https://zhuanlan.zhihu.com/p/136076792)
