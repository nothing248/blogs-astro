---
status: completed
filename: pandas-data-analysis-library-quick-reference
title: "Pandas 教程"
summary: 本笔记是基于 Python 强大的数据分析库 Pandas 的高频实战指令速查字典。涵盖了 Series 和 DataFrame 两种核心数据结构的创建方式。系统整理了按行列分片的数据提取、缺失值清洗（dropna/fillna）、`apply` 广播计算，以及基于 `concat` 和 `merge` 的纵横向拼接表操作。最后，特别标注了利用 `to_csv` 与 `to_parquet` 落盘输出大数据集时的内存管理优势，是数据科学与清洗流必备参考。
aliases: [Pandas 教程, DataFrame 操作, Python 数据分析, Pandas 速查]
tags: [Python, 数据分析, Pandas, 机器学习, 数据清洗, DataFrame, ETL]
date created: 星期一, 十二月 1日 2025, 9:59:22 上午
date modified: 星期四, 六月 18日 2026, 12:45:00 晚上
---

<!-- toc -->

## 1. 核心数据结构

- **Series**：一维数组，带有标签轴（索引）。
- **DataFrame**：二维表格数据结构，包含行索引（Index）与列名（Columns）。

*安装依赖*：`pip install pandas`

---

## 2. 实战指令速查

### 2.1. 创建 DataFrame

```python
import pandas as pd
import numpy as np

# 从字典列表创建
df1 = pd.DataFrame([{"a": 1, "b": 2}]) 
# 创建指定列名的空表
df2 = pd.DataFrame(columns=["a", "b"]) 
# 从 Numpy 多维数组生成，并指定行列名
df3 = pd.DataFrame(np.random.random((2,2)), index=[1, 2], columns=list("ABCD")) 
```

### 2.2. 数据探测与摘要

```python
df.dtypes       # 各列数据类型
df.empty        # 检查是否为空表
df.head()       # 探查前 5 行数据
df.tail()       # 探查后 5 行数据
df.describe()   # 核心数值列的统计摘要（均值、方差、分位数等）
df.nunique()    # 统计每列独立唯一值的个数
df["a"].unique() # 提取某列的所有不重复项
```

### 2.3. 数据过滤与提取 (Indexing & Selecting)

```python
df["a"]               # 提取单列 (返回 Series)
df.loc[:, ["a", "b"]] # 按标签 (Label) 提取所有行的 a, b 两列
df.iloc[0:1, 0:1]     # 按纯数字物理坐标 (Position) 提取
df[df["a"] > 0]       # 布尔掩码提取：过滤 a 列大于 0 的行
```

### 2.4. 缺失值清洗 (Missing Data Handling)

```python
pd.isna(df)             # 矩阵判断所有元素是否为空 (NaN)
df.dropna(how="any")    # 只要行内包含哪怕一个空值，就直接剔除该整行
df.fillna(value=5)      # 将全表的所有空值强行填充为 5
```

### 2.5. 聚合运算与广播 (Compute)

```python
df.mean() # 默认计算每列的平均值
df.groupby(["a"]).sum() # 以 a 列的值进行聚合分组，求其他列的和

# Apply 广播：针对每列应用自定义匿名函数 (此处求极差)
df.apply(lambda x: x.max() - x.min()) 
```

### 2.6. 表级拼接与联结 (Merge & Concat)
>
> [!warning] 拼接前置处理
> 空值 `NaN` 也可能隐式参与合并比对，在执行重要 Merge 前强烈建议先进行清洗过滤。

```python
# 纵向拼接 (UNION ALL，堆叠行)
pd.concat([df1, df2]) 

# 横向联结 (JOIN，根据相同的 a 字段拼接列)
pd.merge(df1, df2, on="a") 
```

### 2.7. 数据落盘与 I/O (Input/Output)

```python
# 数据源读取
pd.read_csv("example.csv", index_col=0) # 指定第 0 列为物理 Index

# 字符串内存缓冲区解析
from io import StringIO
pd.read_csv(StringIO("col1\tcol2\n1\t2"), sep='\t')

# 落盘导出
df.to_numpy() # 剔除索引名，转为纯 Numpy 矩阵
df.to_csv("out.csv", index=False) # 抛弃 DataFrame 自己的前置序号列
```

## 3. 内存优化避坑指南

- `df == False` 这类 **全表级真值判断是危险且错误的**，Pandas 通常要求使用 `.empty` 或具体的列过滤。
- **关于大文件导出**：`to_json()` 默认行为是将整张表在内存中拼接为一个巨大的 JSON 字符串后再落盘，极易引发 OOM（内存溢出）。对于海量数据，强烈推荐使用具备底层优化内存块管理的 `to_csv()` 或高压缩比的列式存储格式 `to_parquet()`。
