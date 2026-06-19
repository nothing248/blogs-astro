---
status: completed
filename: vue-cli-environment-variables-and-modes
title: "Vue CLI"
summary: 本笔记记录了基于 Webpack 的经典前端脚手架 Vue CLI 中关于多环境变量（Environment Variables）与模式（Modes）隔离的核心配置策略。详细对比了四种 `.env` 配置文件的加载优先级与 Git 忽略原则（如 `.env.local` 不入库）。并明确了在项目中如何通过全局注入的对象 `process.env.VUE_APP_XXX` 安全提取这些配置，为构建前端应用的开发、测试及生产隔离环境提供基准参考。
aliases: [Vue CLI, Vue 环境变量, .env 配置]
tags: [前端开发, Vue.js, Vue CLI, 环境变量, 前端工程化, 部署配置]
date created: 星期一, 五月 19日 2025, 2:05:20 下午
date modified: 星期四, 六月 18日 2026, 13:45:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Vue CLI** 是基于 Webpack 的官方标准化前端脚手架（现已进入维护期，被 Vite 替代）。它提供了一套完整的开箱即用的前端项目构建规范。

---

## 2. 核心机制：环境变量与模式 (Modes) 隔离

在现代前端工程中，通常需要为 `development` (开发环境)、`test` (测试环境) 和 `production` (生产环境) 准备不同的 API 请求基址（BaseURL）或调试密钥。Vue CLI 采用根目录下的 `.env` 文件体系来解决此问题。

### 2.1. `.env` 文件优先级加载列表

| 配置文件名 | 作用范围与加载逻辑 |
| :--- | :--- |
| **`.env`** | **全局基础配置**。在所有的环境中都会被加载。 |
| **`.env.local`** | **本地覆盖配置**。在所有环境中加载，但会被 Git 默认忽略。用于存储本地开发者特有的敏感或临时变量。 |
| **`.env.[mode]`** | **模式专属配置**（例如 `.env.production`）。只在对应的构建模式中被载入。 |
| **`.env.[mode].local`** | **本地模式专属**。只在指定模式载入，且被 Git 忽略。 |

*优先级：特定模式（带 `.[mode]`）的优先级高于泛用模式。本地环境（带 `.local`）的优先级高于被 Git 追踪的文件。*

---

## 3. 项目中的使用与读取规范

> [!warning] 命名前缀限制
> 为了防止系统敏感环境变量意外泄露到打包后的客户端代码中，**只有以 `VUE_APP_` 开头的变量才会被 webpack 的 `DefinePlugin` 静态嵌入到最终的客户端捆绑包中。**

**`.env.development` 文件示例**：

```ini
# 正确：能在 Vue 组件中被读取
VUE_APP_SECRET_API_URL=https://dev.api.example.com

# 错误：只能在 webpack 配置文件 (如 vue.config.js) 的 Node 环境中读取，不会被注入到浏览器前端
DB_PASSWORD=123456 
```

**Vue 组件内部调用**：
无论在哪一层级的 JS/Vue 代码中，都可以通过 `process.env` 对象直接读取：

```javascript
export default {
    mounted() {
        console.log("当前环境 API 地址: ", process.env.VUE_APP_SECRET_API_URL);
    }
}
```

## 4. 参考资料

- [Vue CLI 官方指南：环境变量和模式](https://cli.vuejs.org/zh/guide/mode-and-env.html#%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)
