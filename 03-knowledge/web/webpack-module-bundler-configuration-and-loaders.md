---
status: completed
filename: webpack-module-bundler-configuration-and-loaders
title: "Webpack 基础"
summary: 本笔记梳理了现代前端工程化的基石——Webpack 模块打包工具的核心概念。系统解析了它的三种打包构建模式 (development/production/none)，以及 `webpack.config.js` 中关于入口 (entry) 与出口 (output) 路径的动态配置方案。重点讲解了打破 Webpack 仅支持 JS/JSON 限制的核心机制——预处理器 Loader（如 `css-loader` 与 `style-loader` 的链式调用），为理解前端项目构建流水线提供理论基础。
aliases: [Webpack 基础, Webpack 配置, loader 解析]
tags: [前端工程化, Webpack, JavaScript, 模块打包, 构建工具]
date created: 星期一, 五月 19日 2025, 2:05:20 下午
date modified: 星期四, 六月 18日 2026, 13:05:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Webpack** 是一个用于现代 JavaScript 应用程序的静态模块打包工具。当 Webpack 处理应用程序时，它会在内部从一个或多个入口点构建一个依赖图 (Dependency Graph)，然后将项目中所需的每一个模块组合成一个或多个 bundles。

---

## 2. 核心运行模式 (`mode`)

Webpack 提供 `mode` 参数以指示系统使用其内置的相应环境优化：

- **`development`**：开启详尽的错误日志与 Source Map，优化本地调试速度。
- **`production`**：默认值。自动触发代码压缩 (Minification)、混淆与 Tree Shaking 剔除死代码。
- **`none`**：关闭一切内部优化。

---

## 3. 预处理器转换机制 (Loaders)

Webpack 开箱 **仅能理解 JavaScript 和 JSON 文件**。
**Loaders** 赋予了 Webpack 处理其他所有类型文件（CSS, 图片, TypeScript, SCSS）的能力，将它们转换为有效的模块，并混入依赖图中。

### 3.1. 经典案例：解析 CSS 文件

- **`css-loader`**：负责解析 `@import` 和 `url()` 等语句，将 CSS 文件读取为字符串并打包进 JS 模块中。
- **`style-loader`**：将上一步打包好的 CSS 字符串，动态生成 `<style>` 标签并插入到 HTML 文档的 `<head>` 中。

> [!warning] Loader 执行顺序
> 在 Webpack 的 `rules.use` 数组中，Loader 的调用顺序是 **从后往前（从右到左）** 执行的。必须先执行 `css-loader` 再执行 `style-loader`。

---

## 4. 核心配置文件 (`webpack.config.js`)

项目根目录下的标准配置文件决定了构建的流水线。

```javascript
const path = require("path");

module.exports = {
    // 1. 上下文目录：入口文件寻址的根目录，默认当前工程根目录
    context: path.resolve(__dirname, "./src"), 
    
    // 2. 入口起点
    // 支持字符串(单入口)、数组(将多个文件融合打入一个入口)、对象(多入口，生成多 bundle)
    entry: "./a.js", 
    
    // 3. 构建模式
    mode: 'none',
    
    // 4. 出口定义
    output: {
        // 输出物理路径绝对目录，默认是 dist/
        path: path.resolve(__dirname, 'dist'), 
        // 产物文件名。支持动态魔法变量，如 [name].js, [hash].js, [chunkhash].js 防止浏览器缓存
        filename: 'bundle.js', 
        // 决定异步加载的 chunk 文件及静态资源在浏览器中请求时的基础 URL 前缀
        publicPath: 'js/', 
        chunkFilename: '[chunkhash].js' //一般异步模块是会 sheng'h 
    },
    
    // 5. 模块处理规则 (Loaders 挂载区)
    module: {
        rules: [
            {
                test: /\.css$/, // 正则匹配目标文件
                use: ['style-loader', 'css-loader'] // 执行顺序：右 -> 左
            }
        ]
    }
}
```

## 5. 使用

- 命令打包

```shell
webpack --entry ./a.js -o dist
```

> 默认名称是 main.js
>
## 6. 拓展信息

### 6.1. 路径信息

- 相对 URL: js ./js
- 相对服务器 URL /js
- 绝对 http 协议 <https://test.example.com>
- 相对 http 协议 //test.example.com

## 7. 参考资料

- [Webpack 官方概念文档](https://webpack.js.org/)
