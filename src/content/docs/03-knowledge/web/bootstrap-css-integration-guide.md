---
title: "Bootstrap集成"
filename: bootstrap-css-integration-guide
description: Bootstrap 5 前端 CSS 样式库的集成与配置指南。解决在 Vue 3 项目、Vite/Webpack 现代构建工具及传统普通 HTML 项目中集成并定制 Bootstrap 的问题。核心内容涵盖 NPM 安装、Popper.js 依赖配置、Sass 变量覆写、Grid 响应式网格布局以及基础工具类的应用。
tags:
  - bootstrap
  - css-framework
  - web-integration
  - frontend
aliases:
  - Bootstrap集成
  - Bootstrap教程
  - CSS样式库
status: completed
date created: 星期一, 五月 19日 2025, 2:05:18 下午
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 简介

**Bootstrap** 是全球最受欢迎的前端 HTML、CSS 和 JS 开源框架，用于开发响应式布局、移动设备优先的 Web 项目。在 Bootstrap 5 中，官方彻底移除了对 jQuery 的依赖，全面采用原生 JavaScript（Vanilla JS）重构，并在布局上引入了 CSS Grid 以及更为丰富的 CSS 变量，使得样式的集成与定制更加轻量和高效。

---

## 2. 项目集成

根据不同的技术栈与项目架构，Bootstrap 提供了多种灵活的引入方式：

### 2.1. Vue 项目

在 Vue 3 或 Vue 2 项目中，推荐使用 NPM 管理依赖，并结合打包工具（如 Vite 或 Webpack）进行按需加载：

1. **安装依赖**：
   除了安装 `bootstrap` 本身外，还需要安装 `@popperjs/core`（Bootstrap 的下拉菜单、弹出框等定位组件强依赖于 Popper）：

   ```shell
   npm install bootstrap @popperjs/core
   ```

2. **全局引入（以 Vue 3 的 `main.js` 为例）**：
   在入口文件中直接导入样式与 JS 运行库：

   ```javascript
   import { createApp } from 'vue'
   import App from './App.vue'

   // 导入 Bootstrap 样式与 JS 核心
   import 'bootstrap/dist/css/bootstrap.min.css'
   import 'bootstrap/dist/js/bootstrap.bundle.min.js'

   createApp(App).mount('#app')
   ```

3. **在 Single File Components (SFC) 中按需导入组件**：
   如果不想在 `main.js` 中全局引入 JS，可以利用 ES 模块在具体页面内进行引入与实例化：

   ```javascript
   import { Tooltip } from 'bootstrap'
   ```

### 2.2. 普通项目

对于不需要复杂打包构建的传统 HTML 项目，直接在 HTML 文件中引入官方提供的 CDN 地址是最快捷的方法：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 引入 Bootstrap CSS 样式文件 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <title>Bootstrap CDN Demo</title>
  </head>
  <body>
    <div class="container py-5">
      <h1 class="text-primary">Hello, Bootstrap!</h1>
      <button class="btn btn-success" data-bs-toggle="tooltip" title="提示内容">悬停测试</button>
    </div>

    <!-- 引入 Bootstrap 绑定的 JS 包（包含 Popper.js） -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script>
      // 初始化所有的 Tooltips
      const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
      const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    </script>
  </body>
</html>
```

---

## 3. 拓展信息

### 3.1. 使用 Sass 自定义主题与覆写变量

Bootstrap 5 基于 Sass 构建，允许开发者在打包前重置预设的颜色、间距等系统变量。

- 创建自定义样式文件 `custom.scss`：

  ```scss
  // 1. 导入你想要覆写的默认变量
  $primary: #8a2be2; // 将主色调更改为紫色
  $enable-shadows: true; // 启用组件阴影

  // 2. 导入 Bootstrap 的全部 SCSS 源文件
  @import "node_modules/bootstrap/scss/bootstrap";
  ```

- 在 Vite 中配置：
  在 `vite.config.js` 的 `css.preprocessorOptions` 中加入对应路径，即可让全局应用你的自定义主题。

### 3.2. 响应式断点与网格系统 (Grid System)

Bootstrap 采用 12 列网格布局，其响应式容器断点定义如下：

- `xs`: `<576px` (默认列，如 `col-12`)
- `sm`: `≥576px` (如 `col-sm-6`)
- `md`: `≥768px` (如 `col-md-4`)
- `lg`: `≥992px` (如 `col-lg-3`)
- `xl`: `≥1200px` (如 `col-xl-2`)
- `xxl`: `≥1400px` (如 `col-xxl-1`)

### 3.3. 工具类 (Utilities) 命名规范

- **Spacing**：`m-{size}` (margin), `p-{size}` (padding)。方向有 `t` (top), `b` (bottom), `s` (start/left), `e` (end/right), `x` (horizontal), `y` (vertical)。
- **Flexbox**：`d-flex`, `justify-content-center`, `align-items-center` 等，能极快构建非对称的复杂排版。

---

## 4. 参考资料

- [官方链接](https://getbootstrap.com/docs/5.3/utilities/sizing/#relative-to-the-parent)：关于 Bootstrap 5 中尺寸工具类（Sizing Utilities）的官方文档。
- [Bootstrap 5 中文文档](https://v5.bootcss.com/)：适合国内开发者查阅的非官方翻译文档。
