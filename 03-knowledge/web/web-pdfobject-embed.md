---
title: "PDFObject预览库"
filename: web-pdfobject-embed
summary: Web 端嵌入 PDF 预览的开源 JavaScript 库 PDFObject 实用指南。内容包括通过静态 HTML 容器承载 PDF，以及使用 PDFObject.embed() 动态生成并挂载 embed 标签的关键代码。此外，针对不支持 PDF 内嵌的移动端浏览器，提供了降级处理与 PDF.js 整合的建议方案。
tags:
  - web
  - pdf
  - pdfobject
  - javascript
  - pdf-viewer
aliases:
  - PDFObject预览库
  - Web嵌入PDF
  - PDFObject使用教程
status: completed
date created: 星期二, 二月 25日 2025, 3:24:00 下午
date modified: 星期二, 六月 16日 2026, 6:24:18 晚上
---

<!-- toc -->

## 1. 简介

`PDFObject` 是一个轻量级、无依赖的 JavaScript 库，用于在 Web 页面中嵌入 PDF 文档。它通过检测浏览器对 PDF 的原生支持情况，自动生成 `<embed>` 标签，并提供平滑的优雅降级逻辑。

## 2. 基础使用

### 2.1. 引入资源

使用 CDN 引入最新版本的 PDFObject 脚本：

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfobject/2.2.12/pdfobject.min.js"></script>
```

### 2.2. 定义容器

在 HTML 中声明一个承载 PDF 的 DOM 节点，并为其设置宽高：

```html
<style>
  .pdf-container {
    width: 100%;
    height: 800px;
    border: 1px solid #ccc;
  }
</style>

<div id="my-pdf-container" class="pdf-container"></div>
```

### 2.3. 初始化嵌入

通过 JavaScript 调用 `PDFObject.embed` 方法：

```javascript
// 参数 1: PDF 文件路径; 参数 2: 目标容器的选择器或 DOM 节点
PDFObject.embed("/assets/documents/sample.pdf", "#my-pdf-container");
```

## 3. 进阶配置项

支持通过第三个参数（配置对象）来自定义 PDF 的打开属性与降级展示：

```javascript
const options = {
  // 控制 PDF 打开时的行为参数（基于 Adobe PDF Open Parameters）
  pdfOpenParams: {
    page: 1,             // 默认显示第一页
    zoom: '100',         // 缩放比例
    pagemode: 'thumbs',  // 侧边栏显示缩略图
    toolbar: 0           // 隐藏工具栏
  },
  // 当浏览器不支持直接预览时的降级 HTML 提示，[url] 会自动被替换为 PDF 文件路径
  fallbackLink: "<p>您的浏览器不支持在线预览该 PDF，您可以直接 <a href='[url]' target='_blank'>点击此处下载 PDF 文件</a> 查阅。</p>"
};

PDFObject.embed("/assets/documents/sample.pdf", "#my-pdf-container", options);
```

> [!WARNING]
> 移动端浏览器（如 iOS Safari、Android Chrome 等）通常不支持直接在页面内嵌预览 PDF 文件。PDFObject 将会自动触发 `fallbackLink` 降级策略。如果移动端在线预览为强需求，建议整合 `PDF.js` 进行渲染。

## 4. 参考资料

- [PDFObject 官方网站](https://pdfobject.com/)
- [PDFObject GitHub 仓库](https://github.com/pipwerks/PDFObject)
