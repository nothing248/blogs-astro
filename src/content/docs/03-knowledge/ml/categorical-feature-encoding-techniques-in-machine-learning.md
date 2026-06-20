---
status: completed
filename: categorical-feature-encoding-techniques-in-machine-learning
title: "特征编码"
description: 本笔记梳理了机器学习数据预处理阶段处理离散分类变量 (Categorical Features) 的核心编码策略。详细对比了 Label Encoding（一维目标变量的序号化）、Ordinal Encoding（二维输入特征的有顺排号）以及 One-Hot Encoding（独热编码，将分类膨胀为稀疏高维矩阵，消除数值隐性大小关系）。并提供了利用 Python Scikit-learn (`sklearn.preprocessing`) 进行模型实例构建与数组转化的实战代码，为推荐系统及分类任务的特征处理提供标准指引。
aliases: [特征编码, 独热编码, One-Hot Encoding, Label Encoding, 离散特征处理]
tags: [人工智能, 机器学习, 特征工程, Scikit-learn, Python, 数据预处理]
date created: 星期二, 二月 25日 2025, 3:24:10 下午
date modified: 星期四, 六月 18日 2026, 15:45:00 晚上
---

<!-- toc -->

## 1. 业务背景

在机器学习和推荐系统模型（尤其是基于神经网络或线性回归的模型）中，算法底层只能接受数值型矩阵进行数学计算。因此，对于表现为文本或类别的 **离散特征 (Categorical Features)**（如：性别、省份、设备型号），必须进行数值化编码转换。

---

## 2. 核心编码方案对比 (基于 Scikit-learn)

### 2.1. Label Encoding (标签编码)

将 $n$ 个不同的类别值，按内部规则（通常是字母序）映射为 $0 \sim n-1$ 的连续整数。

- **适用场景**：通常 **仅用于一维的目标标签 (Target Variable $y$)**。
- **潜在缺陷**：如果用于输入特征 $x$，算法模型可能会误认为转化后的数字之间存在大小或距离关系（例如认为“北京(1) + 上海(2) = 广州(3)”），这对于无序类别是致命的。

### 2.2. Ordinal Encoding (序数编码)

与 Label Encoding 的实现逻辑类似，同样是转化为 $0 \sim n-1$ 的整数。

- **适用场景**：专门用于处理 **二维输入特征矩阵 ($X$)**。最适合用于 **天然具有排序或大小关系的离散特征**（如：学历：小学 = 0, 中学 = 1, 大学 = 2；VIP 等级：普通 = 0, 银卡 = 1, 金卡 = 2）。在此种场景下，数值大小刚好代表了特征的递进关系。

### 2.3. One-Hot Encoding (独热编码)

消除数值大小暗示的最完美方案。将一个包含 $n$ 种不同值的离散特征，膨胀展开为 $n$ 个二元特征列。该列出现对应值时为 $1$，其余全为 $0$。

- **适用场景**：处理 **无序离散特征**（如颜色：红、黄、蓝）。
- **潜在缺陷**：在特征基数 (Cardinality) 极大时（如：商品 ID、用户 ID），会导致矩阵极度稀疏，产生维度灾难（内存爆炸）。此时需采用 Embedding (嵌入) 或 Target/Hash 编码。

#### 2.3.1. 独热编码实战代码

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder()

# 假设输入是一个 4 行 × 4 列 的特征矩阵
encoder.fit([
    [0, 2, 1, 12],
    [2, 3, 5, 3],
    [1, 3, 2, 12],
    [1, 2, 4, 3]
])

# 将新数据进行编码转化，并输出为常规 Numpy 数组
encoded_vector = encoder.transform([[2, 3, 5, 3]]).toarray()

# 因为每个特征列有不同的独立类别数，转化后的向量维度被膨胀了
print("Encoded vector =", encoded_vector)
# 预期输出: [[0. 0. 1.  0. 1.  0. 0. 0. 1.  1. 0.]]
```

---

## 3. 应对维度灾难的进阶方案

当特征极度离散时，可考虑以下进阶降维编码：

- **Target Encoding (目标编码)**：将离散特征直接映射为当前类别下目标变量 $y$ 的历史均值（需配合交叉验证防止极其严重的数据穿越/过拟合）。
- **Hash Encoding (散列编码)**：利用哈希函数将不定长的字符串强制映射到固定长度的桶中（会产生哈希冲突）。
