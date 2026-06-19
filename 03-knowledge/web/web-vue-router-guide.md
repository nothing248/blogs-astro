---
title: "VueRouter官方插件"
filename: web-vue-router-guide
summary: Vue 官方路由管理器 Vue Router 的核心技术笔记，侧重于 Vue 2.x 项目中常用的 Vue Router v3。内容梳理了路由的基本注册步骤，详细展示了嵌套路由配置、动态路由匹配及全局前置守卫的安全校验实现方式，为构建单页面应用提供规范化路由方案。
tags:
  - web
  - vue
  - vue-router
  - single-page-application
aliases:
  - VueRouter官方插件
  - Vue路由管理器
  - VueRouter使用指南
status: completed
date created: 星期一, 五月 19日 2025, 2:05:17 下午
date modified: 星期二, 六月 16日 2026, 6:24:18 晚上
---

<!-- toc -->

## 1. 简介

`Vue Router` 是 Vue.js 的官方路由管理器。它与 Vue.js 核心深度集成，使构建单页面应用（SPA）时的路由配置变得极具声明式。本文核心基于 Vue Router v3（适配 Vue 2.x 版本）展开。

## 2. 基础配置

在项目中安装对应版本的 Vue Router：

```shell
npm install vue-router@3
```

在工程中定义并配置路由：

```javascript
import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';

// 声明使用插件
Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // 路由懒加载方式
    component: () => import('../views/AboutView.vue')
  }
];

const router = new VueRouter({
  mode: 'history', // 可选择 hash 或 history 模式
  base: process.env.BASE_URL,
  routes
});

export default router;
```

在全局 `main.js` 入口中挂载：

```javascript
import Vue from 'vue';
import App from './App.vue';
import router from './router';

new Vue({
  router, // 注入路由实例
  render: h => h(App)
}).$mount('#app');
```

## 3. 关键功能

### 3.1. 动态路由匹配

在路由路径中使用冒号 `:` 标记动态参数，可在目标组件中通过 `this.$route.params` 获取：

```javascript
const routes = [
  // 动态路由，匹配如 /user/123
  { path: '/user/:id', component: () => import('../views/UserDetail.vue') }
];
```

### 3.2. 全局前置守卫

利用导航守卫控制页面跳转流程，实现鉴权逻辑：

```javascript
router.beforeEach((to, from, next) => {
  const isLogin = !!localStorage.getItem('token');
  if (to.name !== 'login' && !isLogin) {
    // 未登录且前往非登录页，强制跳转至登录页
    next({ name: 'login' });
  } else {
    // 正常放行
    next();
  }
});
```

## 4. 参考资料

- [Vue Router v3 官方文档](https://v3.router.vuejs.org/)
- [Vue Router v4 官方文档 (适用于 Vue 3)](https://router.vuejs.org/)
