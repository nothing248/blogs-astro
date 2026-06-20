---
status: completed
filename: matplotlib-python-data-visualization-quickstart
title: "Matplotlib 教程"
description: 本笔记总结了 Python 生态中最经典的底层数据可视化库 Matplotlib 的基础实操。提供了利用 `pyplot` 模块快速绘制折线图与散点图的代码模板，并涵盖了图表关键元素（如标题、坐标轴标签、图例、网格线）的定制化设置。此外，介绍了基于面向对象风格 (Object-Oriented API) 利用 `subplots` 创建多图表布局的进阶画法，为数据科学与探索性数据分析 (EDA) 提供绘图指南。
aliases: [Matplotlib 教程, Python 绘图, 数据可视化]
tags: [Python, 数据分析, 机器学习, 可视化, Matplotlib]
date created: 星期二, 二月 25日 2025, 3:24:03 下午
date modified: 星期四, 六月 18日 2026, 15:35:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Matplotlib** 是 Python 数据科学栈中最底层的 2D 绘图库，也是 Seaborn、Pandas 内置绘图功能的基础支撑。

*(安装依赖：`pip install matplotlib`)*

---

## 2. 基础实战：状态机接口 (`pyplot`)

适用于快速画出简单的统计图表。

```python
import matplotlib.pyplot as plt
import numpy as np

# 生成模拟数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 1. 创建图形对象
plt.figure(figsize=(8, 4)) # 设置画布大小

# 2. 绘制折线图
plt.plot(x, y1, label='Sin(x)', color='blue', linestyle='-', linewidth=2)
# 绘制散点图
plt.scatter(x, y2, label='Cos(x)', color='red', marker='o', s=10)

# 3. 装饰图表
plt.title('Trigonometric Functions') # 主标题
plt.xlabel('X Axis')                 # X 轴标签
plt.ylabel('Y Axis')                 # Y 轴标签
plt.legend(loc='upper right')        # 显示图例并指定位置
plt.grid(True, linestyle='--', alpha=0.6) # 开启浅色虚线网格

# 4. 展示或落盘
plt.savefig('output.png', dpi=300)   # 保存为高清图片
plt.show()                           # 在窗口或 Notebook 中渲染显示
```

---

## 3. 进阶实战：面向对象接口 (OO API)

当你需要在一个画布上 **排列多个子图**，或者进行极其复杂的精细控制时，强烈推荐使用面向对象的方式。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 5, 50)

# fig 代表整个画布窗口，axs 是一个包含多个子坐标系(Axes)的 NumPy 数组
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

# 操作第一个子图
axs[0].plot(x, x**2, color='green')
axs[0].set_title('Square')
axs[0].set_ylabel('y = x^2')

# 操作第二个子图
axs[1].plot(x, np.sqrt(x), color='purple')
axs[1].set_title('Square Root')
axs[1].set_xlabel('x values')

# 自动调整子图间距防重叠
plt.tight_layout()
plt.show()
```

## 4. 参考资料

- [Matplotlib 官方中文社区导览](https://www.matplotlib.org.cn/intro/)
