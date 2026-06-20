---
status: completed
filename: lodash-javascript-utility-library-snippets
title: "Lodash 常用函数"
description: 本笔记是基于经典 JavaScript 工具库 Lodash 的实战代码速查表。提炼了前端业务开发中最常见的数据清洗场景：利用 `_.throttle` 进行函数节流防抖，针对对象数组使用 `_.uniqBy` / `_.uniqWith` 复杂去重、`_.sortBy` / `_.orderBy` 排序提取。还涵盖了利用 `_.pick` 和 `_.omit` 对象裁切，以及借助 `_.reduce` 计算表单修改差异等进阶技巧。同时提到了现代平替工具 Radash 的演进方向。
aliases: [Lodash 常用函数, JS 工具库, js 节流, js 数组去重]
tags: [前端开发, JavaScript, Lodash, 效率工具, 函数式编程, 数据处理]
date created: 星期二, 二月 25日 2025, 3:24:14 下午
date modified: 星期四, 六月 18日 2026, 13:25:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Lodash** 是一个一致性、模块化、高性能的 JavaScript 实用工具库。极大地降低了操作数组、对象及函数的底层门槛。

*安装依赖*：`npm i --save lodash`

---

## 2. 核心业务场景实战代码

### 2.1. 函数节流 (Throttle)

常用于限制高频事件（如 Scroll, Resize, 按钮连击）的执行频率。

```javascript
// 保证每 1000ms 内只执行一次
_.throttle(function(){ 
    console.log("执行逻辑"); 
}, 1000, {
    leading: true,  // 指定调用在节流开始前触发 (首发响应)
    trailing: true  // 指定调用在节流结束后触发 (兜底响应)
});
```

### 2.2. 复杂集合去重与排序 (Collections)

```javascript
let members = [{ 'id': 1, 'name': 'A' }, { 'id': 2, 'name': 'B' }, { 'id': 1, 'name': 'C' }];

// 依据特定键名极速去重 (保留首个碰到的)
_.uniqBy(members, 'id'); 

// 利用自定义对比函数去重 (适用于深层嵌套比对)
_.uniqWith(res.data.results, function (a, b) { 
    return a.member.id === b.member.id; 
}); 

// 基础排序
_.sortBy(members, 'id'); 
// 高阶排序，显式指定降序 (desc) 或 升序 (asc)
_.orderBy(members, 'id', 'desc'); 
```

### 2.3. 数据探查与提取

```javascript
// 从集合中抽取特定列组成新数组
_.map(members, 'id'); 

// 探测集合中是否存在哪怕一个符合断言的元素 (返回布尔值)
_.some(users, { 'user': 'barney', 'active': false }); 

// 获取多个数组的交集
_.intersectionBy([{ 'x': 1 }], [{ 'x': 2 }, { 'x': 1 }], 'x'); 
```

### 2.4. 对象裁切与进阶 (Objects)

```javascript
let target = { "a": 1, "b": 2, "c": 3 };

// 白名单提取：只保留特定的键
_.pick(target, ["a", "c"]); 

// 黑名单剔除：删除特定的键
_.omit(target, ["b"]); 

// 高阶实战：对比新旧两个表单对象，提取出被用户修改过的字段键名集合
let keys_changed = _.reduce(this.req, (result, value, key) => {
    // 若新值与旧值一致，原样返回累加器；若不一致，将该 key 塞入累加器数组
    return _.isEqual(value, this.instance_data[key]) ? result : result.concat(key);
}, []); 
```

---

## 3. 拓展趋势：Radash

随着 ES6+ 原生语法的普及，Lodash 显得过于庞大。**Radash** 是一个更为现代、轻量、完全由 TypeScript 编写的底层工具库替代品，旨在提供更符合直觉的 API 链。

## 4. 参考资料

- [Lodash 官方完整 API 文档](https://www.lodashjs.com/)
- [现代替代品 Radash Wiki](https://www.radash.wiki/array.html)
