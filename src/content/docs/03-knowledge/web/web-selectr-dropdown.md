---
title: "Selectr下拉选择组件"
filename: web-selectr-dropdown
description: 开源 JavaScript 下拉选择 UI 组件 Selectr 的技术概述。该组件基于原生 HTML select 标签构建，支持单选、多选、搜索过滤等交互功能。需要特别注意的是，该项目目前已处于停更维护状态，在前端技术选型时建议谨慎使用或转向更为活跃的替代品。
tags:
  - web
  - selectr
  - UI-component
  - dropdown
aliases:
  - Selectr下拉选择组件
  - Selectr多选组件
  - Selectr前端库
status: completed
date created: 星期二, 二月 25日 2025, 3:24:12 下午
date modified: 星期二, 六月 16日 2026, 6:24:18 晚上
---

<!-- toc -->

## 1. 简介

`Selectr` 是一个轻量级、无依赖的开源 JavaScript 下拉选择 UI 组件。它能够将原生的 HTML `<select>` 标签包装成功能更丰富、样式更美观的下拉框，支持过滤搜索、多选及自定义模板渲染。

> [!WARNING]
> 该开源项目目前已经停止维护。在生产环境的技术选型中，请谨慎使用或评估其潜在的兼容性问题，建议考虑使用如 Choices.js 或 Select2 等现代活跃维护的替代方案。

## 2. 核心特性

- **零外部依赖**：不依赖 jQuery 或其他大型 JavaScript 框架。
- **轻量易用**：核心资源体积较小，对首屏加载性能友好。
- **支持多选与搜索**：提供内置的实时关键字检索与标签式多选管理。

## 3. 基础使用示例

```html
<!-- 引入 Selectr 样式文件 -->
<link href="https://cdn.jsdelivr.net/npm/mobius1-selectr@latest/dist/selectr.min.css" rel="stylesheet" type="text/css">

<!-- HTML 声明 select 标签 -->
<select id="my-select" multiple>
  <option value="apple">苹果</option>
  <option value="banana">香蕉</option>
  <option value="orange">橙子</option>
</select>

<!-- 引入 Selectr JS 并初始化 -->
<script src="https://cdn.jsdelivr.net/npm/mobius1-selectr@latest/dist/selectr.min.js" type="text/javascript"></script>
<script>
  new Selectr('#my-select', {
    searchable: true, // 开启过滤搜索
    width: 300       // 设置下拉框宽度
  });
</script>
```

## 4. 参考资料

- [Selectr 官方 GitHub 仓库](https://github.com/Mobius1/Selectr)
- [Selectr 在线交互 Demo (CodePen)](https://codepen.io/Mobius1/pen/QgdpLN)
