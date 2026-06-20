---
status: completed
filename: momentjs-date-and-time-manipulation-cheatsheet
title: "Moment.js 教程"
description: 本笔记汇总了 JavaScript 领域最为经典的日期时间处理库 Moment.js 的高频操作 API。系统记录了从字符串的智能解析初始化，到利用 getter 提取时间元数据的实战代码；详述了借助 `subtract`/`add`/`diff` 方法进行时间偏移计算的链式操作；并整理了基于 ISO 8601 令牌的时间字符串格式化与时区（UTC）转化机制，是前端表单校验与后端日志处理中应对时间推算的必备速查字典。
aliases: [Moment.js 教程, 前端时间处理, Moment API]
tags: [前端开发, JavaScript, Node.js, 时间处理, Moment.js, 效率工具]
date created: 星期二, 二月 25日 2025, 3:24:14 下午
date modified: 星期四, 六月 18日 2026, 13:15:00 晚上
---

<!-- toc -->

## 1. 库定位与初始化

**Moment.js** 是 JavaScript 历史中最著名的时间日期处理库，封装了所有针对原生 `Date` 对象难以操作的加减计算、格式转化与边界校验。（*注：原作者已宣布该库进入维护期，新项目可考虑更轻量的 dayjs，但老工程依然对其重度依赖。*）

*依赖安装*：`npm install moment`

**导入与语言本土化**：

```javascript
import moment from 'moment';
// 强制开启中文本土化，影响如“两天前”、“周一”等人类可读字符串的输出
moment.locale("zh-cn"); 
```

---

## 2. 核心操作速查 API

### 2.1. 创建与解析 (Parse)

能够自动推断复杂的 ISO 8601 字符串格式，或通过第二个参数显式强制匹配。

```javascript
const now = moment();                             // 捕获系统当前瞬间
const dt1 = moment("2023-12-25");                 // 基于标准字符推断
const dt2 = moment("12-25-2023", "MM-DD-YYYY");   // 基于严格模板解析
```

### 2.2. 原子数据提取 (Getters)

```javascript
moment().millisecond(); // 提取毫秒
moment().second();      // 提取秒
moment().minute();      // 提取分钟
moment().hour();        // 提取小时 (24H 制)
moment().date();        // 当前月份的第几天 (日)
moment().day();         // 星期几 (0-6，周日为 0)
moment().month();       // 当前年份的第几月 (0-11，一月为 0)
moment().year();        // 获取年份
moment("2012-02", "YYYY-MM").daysInMonth(); // 工具方法：探测该月共有几天 (如 28 或 29)
```

### 2.3. 时间偏移与差值计算 (Math & Diff)

支持极度优雅的 **链式调用**。

```javascript
// 基于当前时间向过去拨动 1 天
moment().subtract({'days': 1}); 
// 基于当前时间向未来推进 1 年零 2 个月
moment().add({'years': 1, 'months': 2}); 

// 取集合中最早或最晚的瞬间
moment.max([moment('2023-01-01'), moment('2024-01-01')]); 

// 时间差距计算 (非常高频的 KPI：算两个日期的跨度)
moment("2007-01-29").diff(moment("2007-01-28"), 'days'); // 结果：1 
```

### 2.4. 格式化输出与人类可读化 (Format)

将内存中的瞬间对象转化为可视化的字符串。

```javascript
moment().format('YYYY-MM-DD HH:mm:ss'); // 最常用的标准入库格式

// 极具特色的人类相对时间播报
moment([2007, 0, 29]).fromNow();                  // 相对今天："16 年前" (基于当前时间)
moment([2007, 0, 29]).from(moment([2011, 0, 29]));// 相对某个特定锚点："4 年前"

// 原生对象转化
moment().toDate();    // 强转回原生的 JS Date 实例
moment().toObject();  // 转化为 JSON 对象 {years: 2023, months: 11 ...}
```

### 2.5. 时区切换 (UTC & Offset)

```javascript
moment().utc();             // 强制将本地时区转变为 UTC 世界协调时（内部偏移量归零）
moment().utcOffset(8);      // 强制为该瞬间挂载 +08:00 (北京时间) 的偏置
```

### 2.6. 布尔查询与边界判断 (Queries)

```javascript
moment().isBefore('2025-01-01');       // 当前瞬间是否在目标时间之前
moment().isSameOrAfter('2024-01-01');  // 是否大于等于该瞬间
moment().isBetween('2023-01-01', '2023-12-31'); // 是否处于区间内

moment.isMoment(obj);  // 校验入参是否为一个合法的 Moment 实例包装体
```

## 3. 参考资料

- [Moment.js Node 环境官方文档](https://momentjs.com/docs/#/use-it/node-js/)
