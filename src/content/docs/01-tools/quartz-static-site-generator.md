---
title: "Quartz笔记发布"
filename: quartz-static-site-generator
description: Quartz 是一款专为数字花园（Digital Garden）和个人知识库设计的静态网站生成器，能够无缝集成 Obsidian 笔记。它支持反向链接、交互式图谱及类似 Obsidian 的双向链接语法，是发布个人笔记到 Web 端的最佳方案之一。
tags: [quartz, static-site-generator, obsidian, pkm, digital-garden]
aliases: [Quartz笔记发布, 静态网站生成]
status: pending
date created: 星期四, 六月 18日 2026, 5:32:15 下午
date modified: 星期五, 六月 19日 2026, 12:07:52 中午
---

<!-- toc -->

## 1. 简介

Quartz 是一个快速、可高度定制化的静态网站生成器，专门针对 Markdown 笔记进行了优化。它常被用于将本地的 Obsidian 仓库直接发布为具有交互性的网页版“数字花园”。

## 2. 核心特性

- **Obsidian 语法支持**：支持 Wikilinks (`[[...]]`)、Callouts、标签和复杂的 Markdown 扩展。
- **交互式内容**：内置双向链接预览（Popovers）、全局搜索以及交互式关系图谱。
- **极致性能**：基于 Hugo 或纯 JS 实现，生成速度极快，对 SEO 友好。
- **主题化定制**：支持完全的 CSS/TS 定制，能够轻松修改布局与配色。

## 3. 快速开始

1. **克隆模板**：`git clone https://github.com/jackyzha0/quartz.git`
2. **安装依赖**：`npm install`
3. **放置笔记**：将你的 Markdown 文件放入 `content` 目录。
4. **预览与部署**：执行 `npx quartz build --serve`。

## 4. 参考资料

- [Quartz 官方文档](https://quartz.jzhao.xyz/)
- [Quartz GitHub 仓库](https://github.com/jackyzha0/quartz)
