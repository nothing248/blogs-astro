---
status: completed
filename: javascript-prototypal-inheritance-and-constructors
title: "JS 原型链"
summary: 本笔记深入剖析了 JavaScript (ES6 `class` 语法糖出现之前) 的原生面向对象机制。详细解释了基于构造函数 (Constructor) 实例化对象背后的 `new` 关键字执行四部曲。重点拆解了 JavaScript 最核心的继承基石——原型链 (Prototype Chain)。理清了实例对象的隐式原型 `__proto__`、构造函数的显式原型 `prototype` 以及指示器 `constructor` 三者之间的三角指向关系，是攻克 JS 高级编程与面试的核心理论知识。
aliases: [JS 原型链, 原型对象, 构造函数, __proto__ 与 prototype]
tags: [JavaScript, 前端开发, 面向对象, 原型链, 编程基础]
date created: 星期二, 二月 25日 2025, 3:24:22 下午
date modified: 星期四, 六月 18日 2026, 13:05:00 晚上
---

<!-- toc -->

## 1. 面向对象背景

在 ES6 引入 `class` 关键字之前，JavaScript 中并没有传统面向对象语言（如 Java/C++）中的“类”概念。JS 的面向对象是基于 **构造函数 (Constructor)** 和 **原型链 (Prototype Chain)** 实现的。

---

## 2. 对象创建与构造函数

除了直接字面量创建 `var obj = {}` 外，标准的对象生成依赖于构造函数。
*(行业规范：构造函数的首字母必须大写以示区分)*

```javascript

var obj = new Object(); // 通过内置 objet 方案创建

function Star(name, age) { 
    // 实例属性/方法：绑定在 this 上，每个实例对象都独有一份拷贝
    this.name = name; 
    this.age = age;
    this.sing = function() {
        console.log('sing');
    }
}

// 静态属性：直接挂载在构造函数对象上，实例无法访问
Star.gender = 'male'; 

// 实例化
let instance = new Star('刘德华', 18); 
```

### 2.1. 💡 `new` 关键字背后的四部曲

当执行 `new Star()` 时，JS 引擎在底层偷偷做了这四件事：

1. 在内存中创建一个新的空对象 `{}`。
2. 将构造函数内部的 `this` 指针强行绑定到这个新对象上。
3. 执行构造函数内的代码（为新对象添加属性和方法）。
4. 自动返回这个新对象（所以构造函数不需要写 `return`）。

---

## 3. 原型链机制 (核心灵魂)

如果所有方法都写在构造函数的 `this` 上，每次 `new` 对象都会在内存中重新开辟空间存放同一个函数，这会导致极大的内存浪费。**原型对象** 解决了这个问题。

### 3.1. 显式原型：`prototype`

- **定义**：每一个构造函数天生自带一个名为 `prototype` 的对象属性。
- **作用**：我们可以将公用的方法直接挂载到这个对象上。**所有由该构造函数生成的实例，都会自动“共享”这个 `prototype` 空间。**
- *原型的 `this` 指向*：原型对象内的方法，其内部的 `this` 永远指向 **正在调用该方法的实例对象**。

### 3.2. 隐式原型：`__proto__`

- **定义**：每一个实例化的对象天生自带一个 `__proto__` 属性。
- **作用**：这个指针牢牢地指向了它的构造函数的 `prototype` 对象。
- **验证三角关系**：

  ```javascript
  console.log(Star.prototype === instance.__proto__); // 输出: true
  ```

### 3.3. 属性/方法查找机制 (原型链的向上攀爬)

当访问对象的某个属性或方法（如 `instance.sing()`）时：

1. 引擎首先在 `instance` 自身的内部查找。
2. 如果找不到，就会顺着 `__proto__` 爬到构造函数的 `prototype` 对象中去找。
3. 如果还找不到，由于 `prototype` 本身也是一个对象，它也有自己的 `__proto__`（指向全局 `Object.prototype`），以此类推。
4. 直到攀爬到顶端 `Object.prototype.__proto__`（其值为 `null`）时停止。如果仍未找到，则返回 `undefined`。

### 3.4. 身份标识：`constructor`

在每一个原型对象 `prototype` 中，都有一个反向的引路指针 `constructor` 属性，它指向了 **所属的构造函数本身**。

```javascript
console.log(Star.prototype.constructor === Star); // 输出: true
console.log(Star.prototype.constructor); // Star
console.log(Star.prototype == instance.__proto__); // true
```
