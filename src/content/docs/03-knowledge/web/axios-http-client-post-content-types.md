---
status: completed
filename: axios-http-client-post-content-types
title: "Axios POST 参数"
description: 本笔记提炼了开源 JavaScript 网络请求库 Axios 的核心业务痛点。重点针对 POST 请求场景，详细演示了三种不同 `Content-Type` 头部的参数封装策略：默认的 JSON 格式（application/json）、用于文件上传及原生表单的 `FormData` 格式（multipart/form-data），以及结合 `Qs` 库处理传统表单提交（application/x-www-form-urlencoded）的代码实战，为前后端对接提供标准接口模版。
aliases: [Axios POST 参数, Content-Type 区别, axios 传参格式]
tags: [前端开发, JavaScript, Axios, HTTP 协议, 网络请求, Vue.js, API 接口]
date created: 星期二, 二月 25日 2025, 3:24:16 下午
date modified: 星期四, 六月 18日 2026, 13:25:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Axios** 是一个基于 Promise 的 HTTP 库，可用在浏览器和 node.js 中，也是目前前端框架（Vue/React）与后端微服务进行 API 交互的事实标准。

---

## 2. 核心难点：POST 请求数据的三种封装方式

在向后端发送 POST 请求时，数据格式（Payload）与请求头 `Content-Type` 必须严格对齐，否则后端无法解析接参。以下是三种最常见交互场景的代码封装。

### 2.1. 方式一：默认 JSON 格式

这是现代 RESTful API 的绝对主流。

- **请求头**：`Content-Type: application/json`
- **封装策略**：直接传入 JavaScript 原生 Object 或字典，Axios 会在底层自动调用 `JSON.stringify()`。

```javascript
import axios from 'axios'

let data = { "code": "1234", "name": "yyyy" };

axios.post(`${this.$url}/test/testRequest`, data)
  .then(res => {
      console.log('res=>', res);            
  });
```

### 2.2. 方式二：原生表单 / 文件上传格式

主要用于 **包含文件流 (File/Blob)** 的提交，或后端仅接收硬核表单数据的场景。

- **请求头**：`Content-Type: multipart/form-data`
- **封装策略**：必须手动实例化并挂载浏览器的 `FormData` 对象。Axios 会自动识别其类型并配置正确的 `Boundary` 请求头。

```javascript
import axios from 'axios'

let data = new FormData();
data.append('code', '1234');
data.append('name', 'yyyy');
// data.append('file', fileObject); // 挂载文件

axios.post(`${this.$url}/test/testRequest`, data)
  .then(res => {
      console.log('res=>', res);            
  });
```

### 2.3. 方式三：传统 URL 编码表单格式

这是一种老式的、形如 URL 查询字符串的传参方式（如 `code=1234&name=yyyy`），常见于对接老旧的 PHP/Java 遗留系统或某些严格的 OAuth 网关。

- **请求头**：`Content-Type: application/x-www-form-urlencoded`
- **封装策略**：为了将 JS 对象转换为拼接好的 URL 字符串，强烈建议引入并使用官方推荐的辅助库 `qs` (Querystring)。

```javascript
import axios from 'axios'
import qs from 'qs' // npm install qs

let data = { "code": "1234", "name": "yyyy" };

axios.post(`${this.$url}/test/testRequest`, qs.stringify(data))
  .then(res => {
      console.log('res=>', res);            
  });
```

## 3. 参考资料

- [Axios 官方 GitHub 仓库与高级配置](https://github.com/axios/axios)
