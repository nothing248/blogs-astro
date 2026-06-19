---
status: completed
filename: eggjs-backend-framework-quickstart
title: "Egg.js 入门"
summary: 本笔记简明记录了基于 Node.js 的企业级后端服务框架 Egg.js 的初始化与启动流程。涵盖了利用 npm 模板脚手架快速生成 `simple` 类型项目的命令行标准操作，为搭建高内聚、低耦合的 Node.js 应用程序提供初始构建步骤。
aliases: [Egg.js 入门, Node.js 框架初始化]
tags: [Node.js, Egg.js, 后端框架, 初始化配置, Web 开发]
date created: 星期二, 二月 25日 2025, 3:24:00 下午
date modified: 星期四, 六月 18日 2026, 9:25:00 晚上
---

<!-- toc -->

## 1. 框架简介

Egg.js 是阿里开源的、基于 Koa 封装的企业级 Node.js Web 框架，致力于提供高度的扩展性和规范的目录结构约定。

## 2. 快速脚手架安装

通过官方脚手架快速初始化一个基础项目：

```bash
# 创建并进入工作目录
mkdir eggjs_demo && cd eggjs_demo

# 使用 simple 模板初始化项目
npm init egg --type=simple

# 安装依赖
npm install

# 本地启动开发环境
npm run dev
```

## 3. 参考资料

- [Egg.js 官方文档](https://www.eggjs.org/zh-CN/index)
