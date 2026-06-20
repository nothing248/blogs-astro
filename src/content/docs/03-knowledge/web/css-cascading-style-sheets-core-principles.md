---
status: completed
filename: css-cascading-style-sheets-core-principles
title: "CSS 基础"
description: 本笔记系统归纳了 Web 前端样式表 CSS 的核心底层原理。深度解析了样式的层叠优先级计算规则（如浏览器默认、行内样式、ID 及类选择器权重），并整理了 `inherit` 和 `initial` 等特殊继承值。详细对比了绝对单位 (px) 与相对单位 (em, rem, vh) 的最佳实践边界。同时，梳理了 `border-box` 盒模型的优势，总结了解决外边距折叠、等高列布局（Flex/Table）及垂直居中等经典 CSS 排版痛点的方案，是前端页面重构的必备基础字典。
aliases: [CSS 基础, 层叠样式表, 盒模型, CSS 选择器权重, rem 与 em]
tags: [前端开发, CSS, Web 设计, UI/UX, 布局排版, HTML]
date created: 星期一, 五月 19日 2025, 2:05:23 下午
date modified: 星期四, 六月 18日 2026, 15:45:00 晚上
---

<!-- toc -->

## 1. 层叠与优先级 (Cascading & Specificity)

CSS 的核心在于处理不同来源样式的冲突逻辑。

### 1.1. 优先级链条

当出现冲突时，浏览器依照以下顺序（由强到弱）决定最终样式：

- `!important` 标记 (破坏层叠规则，谨慎使用)
- 行内样式 (Inline Style, 写在 HTML 标签内)
- ID 选择器 (`#nav`)
- 类 / 伪类 / 属性选择器 (`.class`, `:hover`)
- 标签选择器 (`div`, `p`)

### 1.2. 特殊值属性

- `inherit`：强制子元素继承父元素的该属性值。
- `initial`：强制将属性重置为 CSS 规范设定的初始默认值。

### 1.3. CSS 自定义属性 (CSS 变量)

可以在全局声明并动态复用：

```css
:root {
  --main-font-size: 16px;
}
p {
  /* 第二个参数为 fallback 兜底值 */
  font-size: var(--main-font-size, 13px); 
}
```

---

## 2. 尺寸单位体系 (Units)

### 2.1. 绝对单位

具有固定物理长度的单位（`1in = 25.4mm = 2.54cm = 96px`）。
> **注**：CSS 中的像素 (`px`) 是逻辑像素，它会根据操作系统和屏幕 DPI 缩放，使其视觉大小在不同设备上相对一致。

### 2.2. 相对单位 (响应式核心)

- **`em`**：相对于 **当前元素** 自身的字号 (`font-size`)。若用于 `font-size` 属性，则相对于父元素的字号。
- **`rem` (Root em)**：相对于 **根元素 (`<html>`)** 的字号。避免了 `em` 嵌套导致的尺寸失控。
- **视口单位 (`vh`, `vw`, `vmin`, `vmax`)**：相对于浏览器可视区域的百分比。

> [!tip] 单位使用最佳实践
> 一般原则：使用 **`rem`** 设置全局字号，使用 **`px`** 设置极细边框 (`border`)，使用 **`em`** 设置随字体大小缩放的内边距 (`padding`) 和圆角。

---

## 3. 盒模型与布局陷阱 (Box Model)

### 3.1. 盒模型类型

- `content-box` (默认)：设定的 `width` 仅包含内容区。最终渲染宽度 = width + padding + border。
- **`border-box` (推荐)**：设定的 `width` 包含了边框和内边距。内部内容区自动收缩。

```css
* { box-sizing: border-box; }
```

### 3.2. 外边距折叠 (Margin Collapsing)

- **现象**：普通文档流中，垂直方向上相邻的两个外边距会合并为一个（取最大值，而非相加）。
- **例外**：浮动元素、绝对定位元素、以及 **Flex 弹性盒子** 内的子元素，其外边距 **不会** 发生折叠。

### 3.3. 经典布局解决方案

**A. 等高列布局**

```css
/* 现代 Flex 方案 */
.container { display: flex; }
.left, .right { width: 50%; } /* 两列将自动等高 */

/* 兼容老设备的 Table 方案 */
.container { display: table; }
.left, .right { display: table-cell; width: 50%; }
```

**B. 元素间距 (猫头鹰选择器)**

```css
/* 为容器内除了第一个子元素外的所有子元素添加顶部间距 */
.container > * + * {
    margin-top: 1.5em;
}
```

---

## 4. 拓展避坑：EDM 邮件营销样式开发

编写发往邮箱的 HTML (EDM) 是一项上古技艺：

1. **禁用内部/外部样式表**：许多邮件客户端（如 Gmail, Outlook）会直接剥离 `<style>` 标签，**所有 CSS 必须写成 Inline 行内样式**。
2. **协议限制**：图片与外部链接必须使用绝对路径且为 `http/https` 协议。
3. **禁用现代布局**：绝对不能使用 Flex/Grid，所有布局必须使用嵌套的 `<table>` 来完成。
