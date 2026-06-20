---
title: "JSZip前端压缩库"
filename: web-jszip-guide
description: Web 前端环境中基于 JSZip 库进行多文件打包与压缩的实践指南。内容涵盖库的安装，以及通过 JavaScript 创建文件、新建文件夹、构建嵌套目录结构并异步生成 Blob 压缩包的关键 API 示例。提供 DEFLATE 压缩算法及压缩等级的配置说明，帮助前端开发优化文件下载体验。
tags:
  - web
  - jszip
  - file-compression
  - javascript
aliases:
  - JSZip前端压缩库
  - JSZip使用教程
  - 前端打包ZIP
status: completed
date created: 星期二, 二月 25日 2025, 3:24:17 下午
date modified: 星期二, 六月 16日 2026, 6:24:18 晚上
---

<!-- toc -->

## 1. 简介

`JSZip` 是一个用于创建、读取和编辑 `.zip` 文件的 JavaScript 库，支持在前端浏览器环境和 Node.js 中运行，主要用于实现前端多文件打包打包下载。

## 2. 安装

通过 npm 包装管理器安装依赖：

```shell
npm install jszip
```

## 3. 使用

以下是使用 `JSZip` 创建文件、文件夹以及生成压缩包的典型代码示例：

```javascript
import JSZip from 'jszip';

const zip = new JSZip();

// 1. 创建文件
zip.file("hello.txt", "hello content");

// 2. 创建文件夹
zip.folder("assets");

// 3. 在嵌套路径中直接创建文件夹与文件
zip.file("assets/info.txt", "nested content");

// 4. 异步生成压缩包 (Blob 格式)
zip.generateAsync({
    type: "blob",
    compression: "DEFLATE",        // 压缩方式。STORE：默认不压缩；DEFLATE：执行压缩
    compressionOptions: {
        level: 9                   // 压缩级别 1~9。1 表示速度最快，9 表示最优压缩率
    }
}).then((content) => {
    // 成功后可在此处理 Blob 数据，例如触发浏览器下载保存
    console.log("生成成功", content);
}).catch((error) => {
    console.error("生成压缩包失败", error);
});
```

## 4. 参考资料

- [JSZip 官方文档](https://stuk.github.io/jszip/)
