---
status: completed
filename: nodejs-package-managers-comparison-npm-vs-yarn
title: "npm 与 Yarn 对比"
summary: 本笔记简要对比了 Node.js 生态中两大核心包管理器 npm 与 Yarn 的特性差异。从安装模式、锁文件机制（package-lock.json vs yarn.lock）、依赖提升及工作区（Workspace）支持等维度进行了横向评测，并附带了日常开发中最常用的安装、更新与卸载命令速查表。
aliases: [npm 与 Yarn 对比, Node 包管理, npm 常用命令]
tags: [Node.js, npm, Yarn, 前端工程化, 包管理器]
date created: 星期一, 十二月 1日 2025, 9:59:26 上午
date modified: 星期四, 六月 18日 2026, 12:05:00 晚上
---

<!-- toc -->

## 1. 核心特性横向对比

| 评测维度 | npm (Node Package Manager) | Yarn |
| :--- | :--- | :--- |
| **生态集成** | 内置于 Node.js，开箱即用。 | 需要额外单独安装 (`npm i -g yarn`)。 |
| **性能设计** | 现代版本 (v7+) 速度已大幅优化。 | 诞生之初主打并行下载与极速缓存。 |
| **版本锁定机制** | 依赖 `package-lock.json`。 | 依赖 `yarn.lock`，保障环境高度一致性。 |
| **高级特性** | 支持依赖提升 (Hoisting) 与工作区 (npm 7+)。 | 原生支持工作区，Yarn 2+ (Berry) 引入了 PnP 零安装机制及丰富的插件生态。 |

---

## 2. 日常实战命令速查

### 2.1. Npm 基础指令

```bash
npm install               # 根据 package.json 安装完整依赖树
npm install <pkg_name>    # 安装特定包并添加至 dependencies
npm uninstall <pkg_name>  # 卸载指定包
npm update                # 依据版本范围规则更新所有依赖
npm config set registry https://registry.npmmirror.com # 设国内镜像源
```

### 2.2. Yarn 基础指令

```bash
yarn install              # 类似于 npm install
yarn add <pkg_name>       # 类似于 npm install <pkg_name>
yarn remove <pkg_name>    # 类似于 npm uninstall
yarn upgrade              # 升级所有依赖包
yarn config set registry https://registry.npmmirror.com # 设国内镜像源
```
