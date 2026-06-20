---
status: completed
filename: numpy-scientific-computing-library-cheatsheet
title: "NumPy 教程"
description: 本笔记系统归纳了 Python 数据科学的底层基石 NumPy 库的核心操作指令。涵盖了从构建高维数组 (`zeros`, `linspace`)、探测基础属性 (`shape`, `ndim`)，到复杂的索引切片及形状转换 (`reshape`, `hsplit`) 的代码实战。重点提炼了 NumPy 引以为傲的底层广播机制 (Broadcasting) 算术运算，以及基于通用函数 (ufunc) 与底层 C 优化的线性代数矩阵运算 (`dot`, `linalg.inv`)，是构建机器学习底层数据预处理逻辑的标准参考。
aliases: [NumPy 教程, NumPy 速查, Ndarray 操作, Python 线性代数]
tags: [Python, 机器学习, 数据分析, NumPy, 科学计算, 线性代数]
date created: 星期二, 二月 25日 2025, 3:24:18 下午
date modified: 星期四, 六月 18日 2026, 15:15:00 晚上
---

<!-- toc -->

## 1. 库定位与核心数据结构

**NumPy** 是 Python 科学计算的核心基础库，也是 Pandas, TensorFlow, PyTorch 等上层算法框架的底层数据存储依赖。
其核心对象是 `ndarray`，一种支持极速矢量化运算的多维数组。

---

## 2. 数组构建与初始化

```python
import numpy as np

# 从基础 Python 列表构建
a = np.array([1, 2, 3])

# 快速占位符矩阵
np.zeros((3, 4))       # 3 行 4 列的全 0 矩阵
np.ones((2, 2))        # 全 1 矩阵
np.zeros_like(x)       # 拷贝另一矩阵的 Shape 并用 0 填充

# 序列生成
np.arange(1, 10, 2)    # 类似 Python range，步长为 2
np.linspace(0, 1, 100) # [开始点, 结束点, 元素个数]，生成均匀等差数列
np.logspace(1, 10, 10, base=2) # 生成等比数列

# 随机分布生成
np.random.random((3, 3))    # [0, 1) 均匀分布
np.random.randint(3, size=5)# 0-2 范围内长度为 5 的随机整数
np.random.randn(2)          # 标准正态分布
```

## 3. 基础属性与结构探测

```python
a = np.arange(12).reshape(3, 4)
a.shape     # 输出: (3, 4) 维度的元组
a.ndim      # 输出: 2 维度数量 (秩)
a.size      # 输出: 12 元素总个数
a.dtype     # 输出: int64 元素物理类型
a.itemsize  # 单个元素的物理字节数
```

## 4. 切片、索引与降维提取

```python
b = np.random.random((3, 3))
b[1, 2]     # 提取第二行第三列元素 (索引从 0 开始)
b[:, 1]     # 提取第二列 (所有行的索引 1)
b[:2, 2]    # 提取前两行的第三列

# 高阶：布尔索引或数组索引
i = np.array([0, 2])
a[i]        # 如果 a 是一维，直接提取对应索引；若是多维，则提取 a 的第 1、3 块主维度
```

---

## 5. 广播机制与标量运算

当操作的两个数组形状不同时，NumPy 会触发 **广播 (Broadcasting)** 机制，将较小的数组自动在内存层面“拉伸”以匹配大数组。

```python
a = np.arange(4)            # [0, 1, 2, 3]
b = np.array([1, 2, 3, 4])
b - a                       # 输出: [1, 1, 1, 1]
b ** 2                      # 每个元素平方
b < 20                      # 输出布尔数组: [True, True, True, True]
a * b                       # 对应位置元素的乘积 (注意：不是矩阵乘法)
```

## 6. 通用函数 (ufunc) 与统计聚合

基于 C 语言优化的底层函数，按元素级高速执行。

```python
np.sin(a)
np.mean(a)      # 求所有元素的均值
np.var(a)       # 求方差
np.floor(a)     # 四舍五入取下限 (向下取整)
np.around(a, 2) # 四舍五入保留两位小数
np.argmax(a, axis=0) # 沿特定轴寻找最大值的物理索引
```

## 7. 线性代数核心 (linalg)

```python
a = np.array([[1,2], [3,4]])
b = np.array([[5,6], [7,8]])

a @ b               # 矩阵乘法 (Python 3.5+ 语法)
a.dot(b)            # 传统的矩阵乘法 (内积)

np.linalg.inv(a)    # 矩阵求逆 (Inverse)
np.linalg.det(a)    # 矩阵求行列式 (Determinant)
```

## 8. 矩阵变形与合并拆分

```python
a = np.random.random((3,4))

# 形状变换
a.ravel()           # 将多维矩阵暴力拍平为一维视图
a.reshape(2, 6)     # 修改形状，返回新数组 (-1 代表自动计算剩余维度)
a.resize(2, 6)      # 原地修改数组本身的形状
a.T                 # 矩阵转置 (行列互换)

# 物理拼接与拆分
b = np.hsplit(a, 2) # 水平 (列向) 切割为 2 个块
c = np.vsplit(a, 2) # 垂直 (行向) 切割
np.hstack((a, a))   # 水平合并
np.vstack((a, a))   # 垂直合并
```

## 9. 参考资料

- [NumPy 官方中文文档大全](https://www.numpy.org.cn/)
