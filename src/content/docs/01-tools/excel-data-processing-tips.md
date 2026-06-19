---
title: "Excel常用公式"
filename: excel-data-processing-tips
summary: 本笔记汇总了 Excel 数据处理中的常用技巧。涵盖了冻结窗格的视图操作、核心字符串处理函数（LEFT, MID, FIND 等）及其用法示例。此外，还特别提供了解决 Excel 打开 CSV 文件出现中文乱码的方案，包括 ANSI 编码转换及外部数据导入法，旨在提升日常办公中的数据清洗效率。
tags: ["Excel", "Data-Processing", "Functions", "CSV", "Office-Tips"]
aliases: ["Excel常用公式", "CSV乱码解决", "Excel技巧汇总"]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:29 下午
date modified: 星期五, 六月 19日 2026, 11:59:01 中午
---

<!-- toc -->

## 1. 视图效率技巧

### 1.1. 冻结窗格 (固定行列)

在处理长表或宽表时，固定表头是必不可少的操作。

- **操作路径**：选中特定单元格 -> **View (视图)** -> **Freeze Panes (冻结窗格)**。
- **提示**：选中的单元格左上方区域将被固定。

![](http://qiniu.sxyxy.top/20231120160807.png?image=image)

---

## 2. 常用字符串处理函数

Excel 函数是数据清洗的利器，以下是处理字符串的核心公式：

| 函数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `LEFT(A1, n)` | 从左侧截取 n 个字符 | `=LEFT("ExcelTip", 2)` -> `Ex` |
| `RIGHT(A1, n)` | 从右侧截取 n 个字符 | `=RIGHT("ExcelTip", 3)` -> `Tip` |
| `MID(A1, s, n)` | 从第 s 位开始截取 n 个字符 | `=MID("ABCDEFG", 2, 3)` -> `BCD` |
| `FIND(text, A1)` | 查找文本位置（**区分大小写**） | `=FIND("a", "Apple")` -> 错误 |
| `SEARCH(text, A1)` | 查找文本位置（**不区分大小写**） | `=SEARCH("a", "Apple")` -> `1` |

> [!tip] 绝对引用
> 使用 `$A$1` 格式可以固定引用单元格，在拖动填充公式时地址保持不变。

---

## 3. 常见问题处理

### 3.1. 解决打开 CSV 文件中文乱码

**原因**：CSV 通常以 UTF-8 编码存储，而 Excel 默认使用本地 ANSI (如 GBK) 编码打开。

**解决方案**：

1. **另存转换法**：先用记事本或其他编辑器打开 CSV，点击“另存为”，编码选择 **ANSI**，保存后再用 Excel 打开。
2. **导入法 (推荐)**：在 Excel 中点击 **Data (数据)** -> **From Text/CSV (自文本/CSV)**，在弹出的对话框中手动将文件原始编码选择为 **65001: Unicode (UTF-8)**。

---

## 4. 参考资料

- [Microsoft Excel 官方支持中心](https://support.microsoft.com/zh-cn/excel)
