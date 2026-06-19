---
title: "FileSaver.js"
status: pending
filename: filesaver-js-client-side-file-saving
aliases: [FileSaver.js, 前端文件导出]
tags: [前端开发, JavaScript, 浏览器 API, Blob, 文件导出]
date created: 星期二, 二月 25日 2025, 3:24:05 下午
date modified: 星期四, 六月 18日 2026, 13:05:00 晚上
---

<!-- toc -->

## 1. 待完善：FileSaver.js 前端文件保存库

本笔记旨在记录前端常用的客户端文件保存工具库 `file-saver`。目前仅提供了基于 Blob 对象导出纯文本文件的极简示例。后续需补充导出 Excel/CSV、处理 Base64 图片下载及浏览器兼容性的处理方案。

```javascript
import FileSaver from 'file-saver';
// 构造 Blob 数据载荷
const blob = new Blob(["Hello, world!"], {type: "text/plain;charset=utf-8"});
// 触发浏览器原生下载行为
FileSaver.saveAs(blob, "hello world.txt");
```
