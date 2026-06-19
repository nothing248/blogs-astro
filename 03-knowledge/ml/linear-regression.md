---
title: "线性回归模型"
filename: linear-regression
summary: 线性回归是经典的监督学习回归算法。本笔记推导了线性回归的模型数学原理与矩阵表达形式，并指出了其在最小二乘法下的闭式解析解公式。此外，笔记给出了基于 Python Numpy 库的最小二乘解析解手动实现，以及利用 scikit-learn 框架进行线性回归快速建模的代码模板，为算法学习与应用提供参考。
tags:
  - machine-learning
  - regression
  - math
  - numpy
aliases:
  - 线性回归模型
  - 最小二乘法推导
status: completed
date created: 星期二, 二月 25日 2025, 3:23:33 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

**线性回归（Linear Regression）** 是一种用于建立自变量（特征）与因变量（标签）之间线性关系的基础监督学习回归算法。

---

## 2. 模型原理

### 2.1. 样本表示

在单样本情境下，模型输出值 $f(x)$ 由特征的加权和加上偏置项组成：

![单样本公式](http://qiniu.sxyxy.top/20231024142932.png?image=image)

### 2.2. 矩阵表示

当我们将偏置项 $b$ 并入权重向量并写作 $w_0$ 时，所有训练样本可以统一表示为矩阵乘积形式：

![矩阵表示](http://qiniu.sxyxy.top/20231024143414.png?image=image)

> [!note] 维度解析
>
> - $X \in \mathbb{R}^{m \times (d+1)}$：设计矩阵。第一列全为 1（对应偏置项），$m$ 为样本总数，$d$ 为特征维度。
> - $\hat{w} \in \mathbb{R}^{(d+1) \times 1}$：需要学习的参数向量，包含 $\hat{w} = [b, w_1, w_2, \dots, w_d]^T$。
> - $y \in \mathbb{R}^{m \times 1}$：样本真实标签向量。

---

## 3. 闭式解析解 (Closed-Form Solution)

在线性回归中，我们可以通过最小化均方误差（即最小二乘法 Least Squares Method）来推导参数的最优解。当矩阵 $X^T X$ 为满秩矩阵（即非奇异矩阵）时，存在唯一闭式解析解：

![解析解公式](http://qiniu.sxyxy.top/20231024144046.png?image=image)

即：
$$\hat{w}^* = (X^T X)^{-1} X^T y$$

---

## 4. 代码实现

### 4.1. 基于 Numpy 的矩阵解析解手动实现

```python
import numpy as np

def linear_regression_fit(X, y):
    # 为设计矩阵 X 拼接一列全 1 向量（偏置列）
    m = X.shape[0]
    X_b = np.c_[np.ones((m, 1)), X]
    
    # 依据最小二乘公式计算参数 (X^T * X)^(-1) * X^T * y
    w_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    
    # 返回偏置和权重
    return w_best[0], w_best[1:]
```

### 4.2. scikit-learn 快速建模实现

```python
from sklearn.linear_model import LinearRegression

# 1. 实例化线性回归类
model = LinearRegression()

# 2. 拟合训练模型
model.fit(X_train, y_train)

# 3. 输出模型参数与偏置
print("Weights:", model.coef_)
print("Bias:", model.intercept_)

# 4. 模型预测
y_pred = model.predict(X_test)
```
