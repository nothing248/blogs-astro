---
status: completed
filename: scikit-learn-machine-learning-library-overview
title: "sklearn"
summary: 本笔记记录了 Python 生态中最权威的传统机器学习库 Scikit-learn 的核心定位与体系架构。将其庞杂的功能高度概括为六大基石模块：分类、回归、聚类、降维、模型选择与数据预处理。该库以其极其统一且优雅的 API 设计（fit, transform, predict）成为了数据科学家进行基础基线模型构建、特征工程及交叉验证的事实标准工具。
aliases: [sklearn, 机器学习库, Scikit-learn]
tags: [人工智能, 机器学习, Python, Scikit-learn, 数据挖掘, 算法框架]
date created: 星期二, 二月 25日 2025, 3:24:13 下午
date modified: 星期四, 六月 18日 2026, 15:45:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Scikit-learn**（简称 `sklearn`）是基于 NumPy, SciPy 和 Matplotlib 构建的开源 Python 机器学习库。
它封装了绝大多数经典的传统机器学习算法（不包含深度学习），并提供了一套极其统一、优雅且文档完善的 API 接口，是工业界进行数据挖掘和构建 Baseline 模型的首选基石。

---

## 2. 核心架构：六大基石模块

Scikit-learn 的功能体系可清晰地划分为以下六大模块：

### 2.1. 监督学习 (Supervised Learning)

- **分类 (Classification)**：用于预测离散类别标签。包含逻辑回归 (Logistic Regression)、支持向量机 (SVM)、随机森林 (Random Forest)、K-近邻 (KNN) 等。
- **回归 (Regression)**：用于预测连续数值。包含线性回归 (Linear Regression)、岭回归 (Ridge)、Lasso、梯度提升树 (GBDT) 等。

### 2.2. 无监督学习 (Unsupervised Learning)

- **聚类 (Clustering)**：自动发现数据内部隐藏的群体结构。包含 K-Means、DBSCAN、层次聚类等。
- **降维 (Dimensionality Reduction)**：减少数据的特征维度以实现可视化或提升计算效率。包含主成分分析 (PCA)、t-SNE 等。

### 2.3. 工程流水线组件

- **模型选择与评估 (Model Selection)**：用于比较不同算法并寻找最佳参数。包含网格搜索 (Grid Search)、交叉验证 (Cross-Validation)、以及计算各类准确率/召回率指标 (Metrics) 的套件。
- **数据预处理 (Preprocessing)**：建模前的特征工程核心。包含标准化 (StandardScaler)、归一化、特征编码 (OneHotEncoder) 及缺失值插补 (Imputer)。

## 3. 参考资料

- [Scikit-learn 官方综合文档与实战图库](https://scikit-learn.org/stable/)
