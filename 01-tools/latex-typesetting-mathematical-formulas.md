---
title: "LaTeX公式"
filename: latex-typesetting-mathematical-formulas
description: LaTeX是一种高质量的专业排版系统，在学术论文与数学公式排版中被广泛应用。本文归纳了LaTeX的基础渲染语法（包含行内公式与块公式）、常见希腊字母及子集运算符标识符、复杂矩阵与方程式排版声明，为撰写科学文档提供高查阅价值的语法速查字典。
tags: [latex, typesetting, mathematical-notation, academic-writing]
aliases: [LaTeX公式, LaTeX语法, 数学公式排版]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:27 下午
date modified: 星期五, 六月 19日 2026, 12:06:14 中午
---

<!-- toc -->

## 1. 简介

一种文本编辑方式、对于数学公式非常友好

## 2. 语法

### 2.1. 基础语法

- 代码

```text
行内
$ f(x) = a+b $
块
$$
f(x) = a + b 
$$
注释
% 这是注释 %
```

- 样例
行内 $ f(x) = a+b $  
块

$$
f(x) = a + b
% 这是注释 %
$$

### 2.2. 常见图标

- 代码

```text
\alpha
\beta
\rho
\chi
\Gamma
\lambda
\subset 
\supset 
\ni
\in
\cap
\cup
\pi
\infty
\overline{AB} 上划线
\binom{n}{k} 组合
\hat{a} 符号
\bar{a} 符号
\geq 大于等于
\leq 小于等于
\ne 不等于
\sqrt{ a} 开方
a^b 上标
a_b 下标
a_{cd} a^{cd} 多内容上下标
\frac{a}{b} 分式
\left(1+\frac{1}{n}\right)^n 括号
\displaystyle\sum_0^n 叠加
\prod^{M}_{i=0} 叠乘
\int_{A_1} \iint_{A_1} 积分
\lim\limits_x 极限
\begin{bmatrix} 
   a & b \\
   c & d
\end{bmatrix} 矩阵
\begin{pmatrix} 
   a & b \\
   c & d
\end{pmatrix} 行列式
```

- 样例

$$
\begin{align*}
&\alpha \\
&\beta\\
&\rho \\
&\chi \\
&\Gamma \\
&\lambda \\
&\pi\\
&\subset \\
&\supset \\
& \ni \\
& \in \\
& \cap \\
& \cup \\
&\infty \\
&\overline{AB} 上划线 \\
&\binom{n}{k} 组合 \\
\hat{a} 符号 \\
\bar{a} 符号 \\
&\geq 大于等于\\
&\leq 小于等于\\
& \ne 不等于\\
&\sqrt{a} 开方\\
&a^b 上标\\
&a_b 下标\\
&a_{cd} a^{cd} 多内容上下标\\
&\frac{a}{b} 分式 \\
&\left(1+\frac{1}{n}\right)^n 括号 \\
&\displaystyle\sum_0^n 叠加 \\
&\prod^{M}_{i = 0} 叠乘 \\
&\int_{A_1} \iint_{A_1} 积分\\
&\lim\limits_x 极限 \\
&\begin{bmatrix}
a & b \\
c & d
\end{bmatrix} 矩阵 \\
&\begin{pmatrix}
a & b \\
c & d
\end{pmatrix} 行列式 \\
\end{align*}
$$

## 3. 换行与对齐

- 代码

```text
\\ 代表换行 &代表对其
\begin{align*}
10&x+ &3&y = 2 \\
3&x+&13&y = 4
\end{align*}
```

- 样例

$$
\begin{align*}
10x+3y &= 2 \\
3x+13y &= 4
\end{align*}
$$

## 4. 拓展信息

...

## 5. 参考资料

- [官方文档](https://www.latex-project.org/)
- [Katex](https://katex.org/docs/supported)
