---
status: completed
filename: vite-next-generation-frontend-tooling
title: "Vite 教程"
summary: 本笔记记录了新一代前端构建工具 Vite 的核心定位与基础用法。阐述了其诞生初衷：利用现代浏览器原生支持 ES Modules (ESM) 的特性，取代传统 Webpack 必须先将整个应用彻底抓取并打包后才能提供服务的笨重机制，从而实现极速的冷启动与毫秒级的热更新 (HMR)。并提供了基于 npm 的官方脚手架初始化命令，是现代 Vue 3 和 React 项目的首选构建底座。
aliases: [Vite 教程, 前端构建工具, Vite 原理]
tags: [前端工程化, Vite, 构建工具, ESM, Vue.js, React]
date created: 星期一, 十二月 1日 2025, 9:59:27 上午
date modified: 星期四, 六月 18日 2026, 13:35:00 晚上
---

<!-- toc -->

## 1. 工具定位与架构革命

**Vite** 是一个由 Vue 作者尤雨溪发起的现代前端构建工具，旨在极大地改善前端开发体验。

它之所以能在冷启动和热更新 (HMR) 速度上对传统构建工具（如 Webpack）形成降维打击，核心在于其 **双引擎架构**：

1. **开发环境 (Dev)**：完全放弃预打包。它直接利用现代浏览器对原生 **ES Modules (ESM)** 的支持。当浏览器请求某个文件时，Vite 服务器才会在后台按需编译（利用极速的 Esbuild）并提供该文件，真正实现了 **按需加载** 和 O(1) 的极速启动。
2. **生产环境 (Prod)**：使用高度优化的 **Rollup** 将代码打包，以支持在生产环境中的代码拆分、Tree-Shaking 和老旧浏览器的兼容。

---

## 2. 快速上手与脚手架

使用 Vite 官方脚手架可以一键生成 Vue、React、Svelte 等现代主流框架的启动模板。

```bash
# 推荐：使用最新版脚手架交互式创建项目
npm create vite@latest

# 安装指定依赖到现有项目
npm install -D vite
```

## 3. 参考资料

- [Vite 官方多语言文档](https://vitejs.dev/)
- [Vite GitHub 开源仓库](https://github.com/vitejs/vite)
