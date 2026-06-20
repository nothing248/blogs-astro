---
title: "机器学习数学基础"
filename: machine-learning-mathematics
description: 本笔记系统梳理了面向机器学习的数学基础体系。内容涵盖微积分与极限理论（数列/函数极限与梯度）、初等与特殊函数（双曲及伽马函数）、概率论核心（全概率、贝叶斯与一维/多维概率分布），以及数理统计基础（期望、方差、协方差矩阵、抽样分布、大数定律与中心极限定理），并完整保留了丰富的数学公式与原理图解。
tags:
  - math
  - calculus
  - probability-theory
  - statistics
aliases:
  - 机器学习数学基础
  - 微积分与概率统计汇总
status: completed
date created: 星期二, 二月 25日 2025, 3:24:19 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

本笔记全面总结了机器学习与大模型开发所依赖的数学基础知识，包括 **微积分与极限基础**、**初等/高级函数性质**、**随机事件与概率分布** 以及 **数理统计与估算理论**，旨在提供结构清晰的数学参考字典。

---

## 2. 计算与极限基础

### 2.1. 数的系统与基本性质

- **实数 (Real Number)**：与数轴上的点一一对应。有理数与无理数在实数集上是稠密的（即任何两个实数之间都存在无数个有理数和无理数）。
- **乘方与对数转换**：
  - 加法与乘法转换：$a^{c+d} = a^c \cdot a^d$
  - 乘法与加法转换：$\ln(c \cdot d) = \ln c + \ln d$

> [!warning] 运算边界
> 必须保证分母不为 0，偶次根式的底数非负，对数函数的真数大于 0。

### 2.2. 数列及其极限

- **有界数列**：存在常数 $M > 0$，使得对所有项有 $|x_n| \le M$。
  
  ![有界数列定义](http://qiniu.sxyxy.top/20231017123505.png?image=image)
  
  > [!note] 注意
  > 数列的上下界是不唯一的。

- **数列极限**：
  
  ![数列极限定义](http://qiniu.sxyxy.top/20231017122127.png?image=image)

  - **核心性质**：
    - 唯一性：收敛数列的极限是唯一的。
    - 有界性：收敛数列必定是有界的。
    - 夹逼准则（Squeeze Theorem）：若 $y_n \le x_n \le z_n$ 且 $\lim y_n = \lim z_n = A$，则 $\lim x_n = A$。
    - 单调有界原理：单调且有界的数列必有极限。

### 2.3. 级数与绝对值

- （待补充具体收敛性判别法定理）

---

## 3. 函数及其梯度

### 3.1. 初等函数性质

1. **指数函数**：$y = a^x \quad (a > 0, a \neq 1)$，定义域 $\mathbb{R}$，值域 $(0, +\infty)$。
2. **对数函数**：$y = \log_a x \quad (a > 0, a \neq 1)$，定义域 $(0, +\infty)$，值域 $\mathbb{R}$。
3. **幂函数**：$y = x^{\mu}$（$\mu$ 为常数）。当 $\mu$ 为无理数时，通过 $x^{\mu} = e^{\mu \ln x}$ 定义，定义域为 $(0, +\infty)$。
4. **三角函数**：
   - 常用转换恒等式：
     $$\sin^2 x + \cos^2 x = 1$$
     $$\cos 2x = \cos^2 x - \sin^2 x$$
     $$\sin 2x = 2 \sin x \cos x$$
     $$\sin(x \pm y) = \sin x \cos y \pm \cos x \sin y$$
     $$\cos(x \pm y) = \cos x \cos y \mp \sin x \sin y$$

5. **双曲函数**：
   - 双曲正弦：$\sinh x = \frac{e^x - e^{-x}}{2}$
   - 双曲余弦：$\cosh x = \frac{e^x + e^{-x}}{2}$
   - 常用转换恒等式：
     $$\cosh^2 x - \sinh^2 x = 1$$
     $$\cosh 2x = \cosh^2 x + \sinh^2 x$$
     $$\sinh 2x = 2 \sinh x \cosh x$$
     $$\sinh(x \pm y) = \sinh x \cosh y \pm \cosh x \sinh y$$
     $$\cosh(x \pm y) = \cosh x \cosh y \pm \sinh x \sinh y$$

### 3.2. 高级特殊函数

- **$\Gamma$ 函数 (伽马函数)**：它是阶乘在实数和复数域上的延展。
  $$\Gamma(\alpha) = \int_{0}^{\infty} x^{\alpha-1} e^{-x} \, dx \quad (\alpha > 0)$$

### 3.3. 函数极限
  
  ![函数极限定义](http://qiniu.sxyxy.top/20231017124236.png?image=image)

### 3.4. 梯度 (Gradient)

- 对于单变量函数，梯度等同于普通导数 $f'(x)$。
- 对于多元变量函数 $f(x_1, x_2, \dots, x_n)$，梯度是各变量偏导数构成的向量：
  $$\nabla f = \left( \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_n} \right)^T$$
- **几何意义**：梯度向量指向函数值增长最快的方向，其模长代表该方向的最大变化率。

---

## 4. 集合、随机事件与概率

### 4.1. 基础概率概念与运算

- **相互独立**：若 $P(AB) = P(A)P(B)$，则事件 $A$ 与 $B$ 相互独立。
- **随机变量映射**：将随机试验的结果与实数建立映射关系。
  
  ![随机变量映射](http://qiniu.sxyxy.top/20231030171439.png?image=image)

- **集合分配律**：
  - $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$
  - $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
- **德·摩根定律 (De Morgan's Laws)**：
  - $\overline{A \cup B} = \overline{A} \cap \overline{B}$
  - $\overline{A \cap B} = \overline{A} \cup \overline{B}$
- **全概率公式与贝叶斯公式**：
  
  ![全概率公式](http://qiniu.sxyxy.top/20231030170919.png?image=image)
  
  ![贝叶斯公式](http://qiniu.sxyxy.top/20231030171006.png?image=image)

---

## 5. 概率分布与条件分布

### 5.1. 一维概率分布

- **离散分布**：
  - 二项分布：$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$
  - 泊松分布：$P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}$
- **连续分布**：
  - **分布函数 (CDF)** $F(x) = P(X \le x)$：

    ![分布函数](http://qiniu.sxyxy.top/20231030173210.png?image=image)

  - **概率密度 (PDF)** $f(x)$：

    ![概率密度](http://qiniu.sxyxy.top/20231030173335.png?image=image)

  - **随机变量映射定理**：

    ![随机变量映射定理](http://qiniu.sxyxy.top/20231030184055.png?image=image)

  - **经典连续分布**：
    - 均匀分布：

      ![均匀分布](http://qiniu.sxyxy.top/20231030173452.png?image=image)

    - 指数分布：

      ![指数分布](http://qiniu.sxyxy.top/20231030173530.png?image=image)

    - 正态分布：

      ![正态分布](http://qiniu.sxyxy.top/20231030183159.png?image=image)

      ![正态分布性质](http://qiniu.sxyxy.top/20231031143357.png?image=image)

    - 伽马分布：

      ![伽马分布](http://qiniu.sxyxy.top/20231031152313.png?image=image)

### 5.2. 多维联合与条件分布

- **联合分布律与分布函数**：
  
  ![联合分布律](http://qiniu.sxyxy.top/20231030191857.png?image=image)
  
  ![联合分布函数](http://qiniu.sxyxy.top/20231030191954.png?image=image)
  
- **边缘分布**：
  
  ![边缘分布](http://qiniu.sxyxy.top/20231030192110.png?image=image)

- **经典二维分布与变换**：
  - 二维正态分布（$\rho$ 为相关系数）：

    ![二维正态分布](http://qiniu.sxyxy.top/20231031153552.png?image=image)

  - 随机变量之和 $Z = X+Y$（卷积公式）：

    ![卷积公式](http://qiniu.sxyxy.top/20231031111556.png?image=image)

  - 商与积分布（$Z = X/Y$, $Z = XY$）：

    ![商与积分布](http://qiniu.sxyxy.top/20231031111852.png?image=image)

  - 极值分布（$M = \max\{X,Y\}$, $N = \min\{X,Y\}$）：

    ![极值分布](http://qiniu.sxyxy.top/20231031112440.png?image=image)

- **条件分布与独立性定义**：
  - 离散型条件分布：

    ![离散条件分布](http://qiniu.sxyxy.top/20231031110853.png?image=image)

  - 连续型条件分布：

    ![连续条件分布](http://qiniu.sxyxy.top/20231031111057.png?image=image)

  - 独立性判断：

    ![联合独立性](http://qiniu.sxyxy.top/20231031111218.png?image=image)

---

## 6. 数字特征与数理统计

### 6.1. 期望与方差

- **数学期望**：
  
  ![期望定义](http://qiniu.sxyxy.top/20231031112559.png?image=image)
  
  - 期望映射定理与运算定理：

    ![期望映射定理](http://qiniu.sxyxy.top/20231031114207.png?image=image)

    ![期望运算定理](http://qiniu.sxyxy.top/20231031114332.png?image=image)

- **方差 (Variance)**：
  
  ![方差定义](http://qiniu.sxyxy.top/20231031114517.png?image=image)
  
  - 方差常用计算公式与运算定理：

    ![方差常用公式](http://qiniu.sxyxy.top/20231031114744.png?image=image)

    ![方差运算定理](http://qiniu.sxyxy.top/20231031114830.png?image=image)

### 6.2. 协方差、相关系数与矩阵

- **协方差与相关系数**：
  
  ![协方差与相关系数](http://qiniu.sxyxy.top/20231031120143.png?image=image)
  
  - 计算公式与运算定理：

    ![协方差公式](http://qiniu.sxyxy.top/20231031120334.png?image=image)

    ![协方差运算定理](http://qiniu.sxyxy.top/20231031120429.png?image=image)

  - 相关系数性质定理、矩与中心矩：

    ![相关系数定理](http://qiniu.sxyxy.top/20231031120927.png?image=image)

    ![矩与中心矩](http://qiniu.sxyxy.top/20231031121226.png?image=image)

- **协方差矩阵 (Covariance Matrix)**：
  
  ![协方差矩阵定义与性质](http://qiniu.sxyxy.top/20231031121315.png?image=image)
  
  ![协方差矩阵性质](http://qiniu.sxyxy.top/20231031121525.png?image=image)

---

## 7. 样本分布与经典定理

### 7.1. 随机样本与分析图表

- **随机样本**：
  
  ![随机样本](http://qiniu.sxyxy.top/20231031124950.png?image=image)

- **分析工具**：直方图与箱线图（Box Plot）。
  
  ![直方图](http://qiniu.sxyxy.top/20231031140638.png?image=image)
  
  ![箱线图](http://qiniu.sxyxy.top/20231031140711.png?image=image)

- **统计量与经验分布函数**：
  
  ![统计量](http://qiniu.sxyxy.top/20231031140853.png?image=image)
  
  ![经验分布函数](http://qiniu.sxyxy.top/20231031142227.png?image=image)

### 7.2. 常用统计抽样分布

- **$\chi^2$ (卡方) 分布**：
  
  ![卡方分布定义](http://qiniu.sxyxy.top/20231031142545.png?image=image)
  
  ![卡方分布性质](http://qiniu.sxyxy.top/20231031154718.png?image=image)

- **$t$ (学生) 分布**：
  
  ![t 分布](http://qiniu.sxyxy.top/20231031155204.png?image=image)

- **$F$ (费舍尔) 分布**：
  
  ![F 分布](http://qiniu.sxyxy.top/20231031155251.png?image=image)

### 7.3. 核心极限定理

- **大数定律 (Law of Large Numbers)**：
  
  ![大数定律](http://qiniu.sxyxy.top/20231031123217.png?image=image)

- **中心极限定理 (Central Limit Theorem)**：
  
  ![中心极限定理](http://qiniu.sxyxy.top/20231031124028.png?image=image)

- **切比雪夫不等式 (Chebyshev's Inequality)**：
  
  ![切比雪夫不等式](http://qiniu.sxyxy.top/20231031114949.png?image=image)
