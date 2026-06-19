---
status: completed
filename: vuejs-framework-routing-and-scoped-css-principles
title: "Vue 框架"
summary: 本笔记记录了 Vue.js 前端框架开发中的部分核心概念与避坑技巧。梳理了早期 Vue CLI 创建 Vue 2 项目的指令。重点解析了 Vue 单文件组件中 `scoped` 样式的底层实现原理（通过动态注入形如 `data-v-xxxx` 的属性选择器实现样式隔离），并指出了针对第三方动态渲染 DOM（无法被注入标识）时样式失效的解决方案。此外，明确了 `$router` 中 `path+query` 与 `name+params` 传参的区别，以及在模板事件中通过 `$event` 手动传递原生事件对象的语法。
aliases: [Vue 框架, Scoped CSS 原理, Vue 路由传参, Vue 事件对象]
tags: [前端开发, Vue.js, CSS, 前端路由, 组件化]
date created: 星期一, 五月 19日 2025, 2:05:23 下午
date modified: 星期四, 六月 18日 2026, 13:35:00 晚上
---

<!-- toc -->

## 1. 历史版本初始化 (Vue 2 CLI)

虽然 Vue 2 与旧版 CLI 已进入维护期，但维护老项目时仍需了解：

```bash
npm install -g @vue/cli
vue --version 
vue create project-name # 交互式创建项目
```

*(注：开发 Vue 3 现代项目，强烈推荐使用基于 Vite 的 `npm create vue@latest` 命令，要求 Node.js >= 18.3)*

---

## 2. 核心机制与开发技巧

### 2.1. 组件 Scope 样式的底层原理

在 `.vue` 文件中，给 `<style>` 添加 `scoped` 属性可实现组件级样式隔离。

- **原理**：Vue 底层的编译器会为当前组件模板内的所有 HTML 标签生成并注入一个唯一的自定义属性（如 `data-v-42da6db2`）。同时，将你编写的 CSS 选择器自动改写为包含该属性的组合选择器（例如将 `li` 改写为 `li[data-v-42da6db2]`）。由于哈希值全局唯一，从而实现了样式的绝对隔离。
- **第三方库样式穿透陷阱**：当你引入 ElementUI 或 Bootstrap-Vue 等第三方组件时，它们内部通过 JavaScript 动态插入到全局 DOM 树中的节点，**是不会被 Vue 编译器注入当前组件的哈希标识的**。因此，你的 `scoped` 样式对它们毫无作用。
- **解决方案**：使用 Vue 提供的深度选择器（如 `:deep()`, `>>>`, `/deep/`），强行穿透作用域；或直接在该组件的顶层包裹一个专属的 ID，将需要修改的第三方样式写在非 `scoped` 的 `<style>` 块中。

### 2.2. 路由传参的黄金规则

在使用 Vue Router 编程式导航时，必须牢记匹配组合：

- `path` 必须搭配 `query`（表现为 URL `?id=1`，刷新页面参数不丢失）。
- `name` 必须搭配 `params`（表现为 URL 隐式传参或路由参数 `/user/1`，需要通过 `this.$route.params` 接收）。**绝不能将 `path` 与 `params` 混合使用，否则参数会被直接忽略。**

### 2.3. 事件绑定的双向传参

当你在模板中为组件绑定事件，既想传递自定义参数，又需要保留浏览器原生的 Event 事件对象时，必须显式传递 `$event` 魔法变量：

```html
<button @click="handleClick('custom_string', $event)">提交</button>
```

## 3. 参考资料

- [Vue.js 官方文档](https://vuejs.org/)
