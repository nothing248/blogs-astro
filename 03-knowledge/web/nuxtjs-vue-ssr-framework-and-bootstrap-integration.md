---
status: completed
filename: nuxtjs-vue-ssr-framework-and-bootstrap-integration
title: "Nuxt.js 教程"
summary: 本笔记记录了基于 Vue.js 的通用框架（主打服务端渲染 SSR）Nuxt.js 的快速上手指南。区分了 Nuxt 2 与 Nuxt 3 的脚手架初始化命令，并详细梳理了其约定优于配置的核心目录结构（如 layouts, plugins, store 等）。重点提供了一个前端工程化的高阶实战：如何通过引入 `style-resources` 模块，在 Nuxt 项目中全局注入并深度覆盖 Bootstrap-Vue 的默认 SCSS 变量（如 `$primary`），实现深度的 UI 主题定制。
aliases: [Nuxt.js 教程, Vue SSR, Nuxt 目录结构, Bootstrap-Vue 样式覆盖]
tags: [前端开发, Vue.js, Nuxt.js, SSR, Bootstrap, SCSS, Web 框架]
date created: 星期一, 十一月 24日 2025, 9:46:58 上午
date modified: 星期四, 六月 18日 2026, 13:05:00 晚上
---

<!-- toc -->

## 1. 框架定位与初始化

**Nuxt.js** 是一个极其强大的基于 Vue.js 的开源框架，它通过预设合理的最佳实践（约定优于配置），让开发者极其容易地构建具备 **服务端渲染 (SSR)** 或静态站点生成 (SSG) 能力的 Web 应用。

### 1.1. 版本与脚手架安装

- **Nuxt 2 (基于 Vue 2)**

  ```bash
  npx create-nuxt-app <project-name>
  ```

- **Nuxt 3 (基于 Vue 3 + Vite)**

  ```bash
  npx nuxi@latest init <project-name>
  ```

---

## 2. 核心目录结构语义 (以 v2 为例)

Nuxt 的魔法在于它的目录名即代表了底层配置：

- `pages/`：视图模板。Nuxt 会根据此目录下的 `.vue` 文件 **自动生成路由**。
- `components/`：Vue 组件。
- `layouts/`：全局布局结构（如 `default.vue`）。其中 `error.vue` 用于自定义全局错误页。
- `plugins/`：在根 Vue 应用实例化之前需要运行的 JavaScript 插件（如 axios 拦截器、UI 组件库注册）。
- `static/`：静态文件，直接映射到服务器根目录（不会被 Webpack 处理）。
- `assets/`：需要被 Webpack 编译处理的静态资源（如 SCSS、未压缩图片）。
- `store/`：Vuex 状态树。
- `app.html`：**整个文档的骨架入口**。可以在这里定制最底层的 HTML 结构。

---

## 3. 进阶实战：深度修改 Bootstrap-Vue 默认主题色

直接在 Nuxt 中使用 Bootstrap-Vue 时，如果你想修改其默认的蓝色 (`$primary`)，需要通过 SCSS 变量重写机制。

### 3.1. 准备依赖

需安装 SASS 预处理器及全局资源注入模块：

```bash
npm install --save-dev sass sass-loader@10
npm i @nuxtjs/style-resources --save-dev 
```

*(注：SASS 与 Webpack 的版本可能存在兼容性问题。已知可用组合：`bootstrap-vue: ^2.22.0`, `bootstrap: ^4.6.2`, `sass: 1.64.2`, `sass-loader: ^10.5.2`)*

### 3.2. 构建样式变量文件

创建 `~/assets/css/boostrap.scss`，在此文件中 **先定义变量，再引入 Bootstrap 源码**：

```scss
// 1. 覆盖默认变量
$primary: #ff6e40; 
// 也可以引入外部独立的 _variables.scss

// 2. 导入框架底层样式 (注意引入顺序)
@import '~bootstrap/scss/bootstrap.scss';
@import '~bootstrap-vue/src/index.scss';
```

### 3.3. 配置 `nuxt.config.js`

将上述文件注册至全局：

```javascript
export default {
  // 全局注入编译后的 CSS
  css: [
    '~/assets/css/boostrap.scss', 
  ], 
  // 若有纯变量文件，可通过 styleResources 让每个 Vue 组件都能直接使用这些变量而无需手动 @import
  styleResources: {
    scss: [
      // './assets/css/_variables.scss' 
    ]
  }
}
```

## 4. 参考资料

- [Nuxt 官方入门文档](https://nuxt.com/docs/getting-started/introduction)
