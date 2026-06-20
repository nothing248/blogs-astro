---
title: "SCSS语法教程"
filename: web-scss-guide
description: CSS 预处理器 SCSS 语法特性与应用指南。内容梳理了 SCSS 核心功能：全局与局部变量（含 !default 默认值）、选择器与属性嵌套规则、混合宏（@mixin/@include）与 @extend 继承、占位符（%）编译优化机制、插值表达式 #{} 动态拼接，以及数值与颜色运算。并对比说明了 SCSS 与 Sass 语法差异。
tags:
  - web
  - scss
  - sass
  - css-preprocessor
  - styling
aliases:
  - SCSS语法教程
  - Sass预处理器
  - CSS排版增强
status: completed
date created: 星期二, 二月 25日 2025, 3:24:18 下午
date modified: 星期二, 六月 16日 2026, 6:24:18 晚上
---

<!-- toc -->

## 1. 简介

SCSS（Sassy CSS）是 CSS 的一种预处理器和扩展语言。作为 CSS3 语法的超集，SCSS 允许开发者使用变量、嵌套、混合宏、继承、函数等高级特性，极大提升了样式代码的复用性与可维护性。

## 2. 语法特性

### 2.1. 变量 (Variables)

SCSS 支持使用 `$` 符号来声明变量。变量分为全局变量和局部变量，同时支持 `!default` 默认值声明。

```scss
$width: 200px;             // 全局变量
$baseLineHeight: 2;
$baseLineHeight: 1.5 !default; // 默认变量。如果在之前未声明该变量，则使用默认值；若已声明，则被覆盖。

div {
  $color: yellow;          // 局部变量（仅在当前选择器作用域内有效）
  color: $color;
}
```

### 2.2. 嵌套 (Nesting)

SCSS 提供了直观的嵌套语法，避免了传统 CSS 中重复书写父选择器的冗余。

- **选择器嵌套与父选择器引用 `&`**

```scss
nav {
  a {
    color: red;
    header & {
      color: green;
    }
  }
}

// 编译后解析为：
nav a {
  color: red;
}
header nav a {
  color: green;
}
```

- **属性嵌套**

针对具有相同前缀的 CSS 属性（如 `font-*`），可以使用属性嵌套：

```scss
.box {
  font: {
    size: 12px;
    weight: bold;
  }  
}

// 编译后解析为：
.box {
  font-size: 12px;
  font-weight: bold;
}
```

- **伪类嵌套**

```scss
.clearfix {
  &:before,
  &:after {
    content: "";
    display: table;
  }
  &:after {
    clear: both;
    overflow: hidden;
  }
}

// 编译后解析为：
.clearfix:before,
.clearfix:after {
  content: "";
  display: table;
}
.clearfix:after {
  clear: both;
  overflow: hidden;
}
```

## 3. 混合宏 (Mixins)

混合宏用于定义可复用的样式块，类似于函数，支持传入参数。

- **声明混合宏**

```scss
// 1. 不带参数的混合宏
@mixin border-radius-default {
  -webkit-border-radius: 5px;
  border-radius: 5px;
}

// 2. 带单参数的混合宏
@mixin border-radius($radius) {
  -webkit-border-radius: $radius;
  border-radius: $radius;
}

// 3. 带多个参数的混合宏
@mixin size($width, $height) {
  width: $width;
  height: $height;
}
```

- **调用混合宏**

使用 `@include` 关键字调用声明好的混合宏：

```scss
button {
  @include border-radius-default;
}

.box {
  @include border-radius(50%);
}

.box-center {
  @include size(500px, 300px);
}

// 编译后解析为：
button {
  -webkit-border-radius: 5px;
  border-radius: 5px;
}
.box {
  -webkit-border-radius: 50%;
  border-radius: 50%;
}
.box-center {
  width: 500px;
  height: 300px;
}
```

## 4. 继承与占位符

### 4.1. 继承 (Extend)

使用 `@extend` 可以继承已有选择器的全部样式，编译时会使用并集选择器进行合并，从而减少代码冗余。

```scss
.btn {
  border: 1px solid #ccc;
  padding: 6px 10px;
  font-size: 14px;
}

.btn-primary {
  background-color: #f36;
  color: #fff;
  @extend .btn;
}

// 编译后解析为：
.btn, .btn-primary {
  border: 1px solid #ccc;
  padding: 6px 10px;
  font-size: 14px;
}
.btn-primary {
  background-color: #f36;
  color: #fff;
}
```

### 4.2. 占位符 (Placeholder Selector)

占位符选择器以 `%` 开头。与普通选择器不同，**如果不被 `@extend` 调用，占位符本身不会被编译到最终的 CSS 文件中**，非常适合编写纯粹的基类。

```scss
%mt5 {
  margin-top: 5px;
}
%pt5 {
  padding-top: 5px;
}

.btn {
  @extend %mt5;
  @extend %pt5;
}

.block {
  @extend %mt5;
  span {
    @extend %pt5;
  }
}

// 编译后解析为：
.btn, .block {
  margin-top: 5px;
}
.btn, .block span {
  padding-top: 5px;
}
```

## 5. 插值与运算

### 5.1. 插值表达式 `#{}`

插值用于在选择器名称或属性名中动态使用变量。注意，插值表达式不能用于动态拼接变量或宏名称。

```scss
$properties: (margin, padding);

@mixin set-value($side, $value) {
  @each $prop in $properties {
    #{$prop}-#{$side}: $value;
  }
}

.login-box {
  @include set-value(top, 14px);
}

// 编译后解析为：
.login-box {
  margin-top: 14px;
  padding-top: 14px;
}
```

### 5.2. 运算 (Operations)

SCSS 支持基本的数学运算（加、减、乘、除）和颜色运算。

```scss
$content: "dynamic text";

.box {
  width: 20px + 8in;           // 混合单位计算（会自动转换单位）
  height: 20px - 5px;
  width: 10px * 2;             // 乘法中仅允许一个数值携带单位

  // 除法运算规则：以下情况将被视为除法运算，而非普通 CSS 分隔符
  $width: 1000px;
  width: $width / 2;           // 1. 使用了变量
  width: round(1.5) / 2;       // 2. 使用了函数
  height: (500px / 2);         // 3. 使用了圆括号包裹
  margin-left: 5px + 8px / 2;  // 4. 作为复杂表达式的一部分

  color: #010203 + #040506;    // 颜色运算 (01+04, 02+05, 03+06 -> #050709)
  content: " #{$content} ";    // 插值提取字符
  cursor: e + -resize;         // 字符串拼接 ("e-resize")
}
```

> [!NOTE]
> 在 Sass 现代规范中，使用 `/` 进行除法已逐渐废弃，推荐使用 `sass:math` 模块中的 `math.div()` 函数。

## 6. 拓展信息

### 6.1. SCSS 与 Sass 的区别

- **Sass (Syntactically Awesome Style Sheets)**：是最初的语法形式，使用缩进和换行代替大括号 `{}` 和分号 `;`。其文件后缀为 `.sass`。
- **SCSS (Sassy CSS)**：是 Sass 3 引入的全新语法格式，完全兼容 CSS3 语法（CSS3 的超集），要求使用分号和花括号。其文件后缀为 `.scss`，更加符合现代前端开发人员的编码习惯。

## 7. 参考资料

- [Sass 官方文档（中文）](https://www.sass.hk/docs/)
