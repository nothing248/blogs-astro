---
title: "Puppeteer教程"
filename: puppeteer-browser-automation-guide
description: Puppeteer 是一款功能强大的 Node.js 库，允许开发者通过高级 API 控制无头（Headless）或有头 Chrome/Chromium 浏览器。本文涵盖了 Puppeteer 的基础安装方法（含 puppeteer-core 区别），并提供了一个自动化截图的代码示例。适用于网页爬虫、前端自动化测试、PDF 生成及动态页面渲染等场景。
tags: [puppeteer, browser-automation, nodejs, web-scraping, testing]
aliases: [Puppeteer教程, 无头浏览器控制, Chrome自动化]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 星期五, 六月 19日 2026, 12:07:44 中午
---

<!-- toc -->

## 1. 简介

Puppeteer 是 Google 开发的一个 Node 库，它提供了一组高级 API 来控制 Chrome 或 Chromium 浏览器。默认情况下，它以 **无头 (Headless)** 模式运行，但也支持通过配置显示浏览器界面。

## 2. 安装指南

根据你的需求选择不同的安装包：

- **标准安装**：自动下载匹配的 Chromium 二进制文件。

  ```shell
  npm install puppeteer
  ```

- **核心安装**：不下载浏览器，仅安装 API 库（需手动指定本地浏览器路径或连接远程集群）。

  ```shell
  npm install puppeteer-core
  ```

## 3. 核心使用场景

1. **生成页面快照**：将网页保存为 PDF 或图片。
2. **自动化测试**：模拟用户操作（点击、输入、滚动）并验证结果。
3. **爬虫与抓取**：抓取 SPA（单页应用）渲染后的动态数据。
4. **性能分析**：捕获页面的 Timeline 迹线以诊断性能问题。

## 4. 代码示例：快速截图

以下代码演示了如何打开一个页面并将其保存为图片：

```javascript
const puppeteer = require('puppeteer');

(async () => {
  // 启动浏览器
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // 设置视口大小
  await page.setViewport({ width: 1280, height: 800 });
  
  // 访问页面
  await page.goto('https://example.com');
  
  // 截取屏幕并保存
  await page.screenshot({ path: 'example.png' });

  // 关闭浏览器
  await browser.close();
})();
```

## 5. 常用 API 技巧

- **等待加载**：使用 `await page.waitForSelector('.selector')` 确保内容渲染后再操作。
- **执行脚本**：使用 `await page.evaluate(() => { ... })` 在浏览器上下文中执行 JS。
- **模拟移动端**：使用 `await page.emulate(puppeteer.KnownDevices['iPhone 13'])`。

## 6. 参考资料

- [Puppeteer 官方文档](https://pptr.dev/)
- [Puppeteer GitHub 仓库](https://github.com/puppeteer/puppeteer)
- [Puppeteer 快速入门指南](https://developers.google.com/web/tools/puppeteer/get-started)
