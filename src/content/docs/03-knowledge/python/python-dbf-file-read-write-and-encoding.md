---
status: completed
filename: python-dbf-file-read-write-and-encoding
title: "Python 读取 DBF"
description: 本笔记记录了在 Python 环境下读写 dBase 数据库文件 (.dbf) 的实战方案。针对历史遗留系统常见的中文字符集问题，总结了一套利用 `dbfread` 库结合 Try-Except 进行 `cp936` (GBK)、`gb18030` 及 `utf-8` 级联降级解析的读取策略。同时，提供了使用 `dbf` 库导出并严格映射字段类型（如 C, N, D）构建新 DBF 表的写入代码模板，强调了输出时强依赖 UTF-8 编码以兼容特殊中文字符的注意事项。
aliases: [Python 读取 DBF, dbfread, dbf 写入, dbf 编码问题]
tags: [Python, 数据处理, DBF, 数据清洗, 编码问题, Pandas]
date created: 星期一, 五月 19日 2025, 2:05:22 下午
date modified: 星期四, 六月 18日 2026, 12:05:00 晚上
---

<!-- toc -->

## 1. 核心依赖库

处理遗留的 `.dbf` 文件，通常需要拆分使用两个专门的库：

- **读取**：推荐使用 `dbfread` (仅读，但性能和兼容性较好)。
- **写入**：推荐使用 `dbf`。

```bash
pip install dbfread dbf pandas dask
```

---

## 2. 读取 DBF：终极编码兼容策略

在处理国内历史系统的 DBF 文件时，最容易崩溃的环节是中文字符编码。推荐使用级联 Try-Except 策略，从最常见的 `cp936` (GBK) 逐步降级尝试：

```python
import dask.dataframe as dd  
from dbfread import DBF    
import pandas as pd

def read_dbf_file(file_path):  
    """安全读取 DBF 文件并转化为 Dask/Pandas DataFrame"""    
    try:  
        # 首选尝试：GBK 编码
        dbf_data = DBF(file_path, encoding='cp936')  
        df = pd.DataFrame(iter(dbf_data))  
    except Exception as e:  
        try:  
            # 降级一：最新版的 GB18030 扩展编码
            dbf_data = DBF(file_path, encoding='gb18030')  
            df = pd.DataFrame(iter(dbf_data))  
        except Exception as e1:  
            # 降级二：UTF-8 编码
            dbf_data = DBF(file_path, encoding='utf-8')  
            df = pd.DataFrame(iter(dbf_data))  
            
    # 转为 dask dataframe 处理大数据量
    return dd.from_pandas(df)  
```

---

## 3. 写入 DBF：字段严格映射

写入 DBF 文件时，必须严格定义各列的内部数据类型与长度（如 `C(20)` 代表 20 字节字符串，`N(6,2)` 代表总长 6 位且含 2 位小数的数字）。

```python
import dbf

def write_dbf_file(df, dest_path):  
    """将 DataFrame 严格按字段规范写入 DBF 文件"""
    # 1. 字段类型映射字典 (C: Character, N: Numeric, D: Date)
    type_map = {  
        '科目': "C(20)", '学号': "C(20)", '原始成绩': "N(6,2)"
    }  
    
    # 2. 列名映射字典 (DBF 列名严格受限于 10 个字节，尽量用短拼音)
    name_map = {  
        '科目': "kmmc", '学号': "zkzh", '原始成绩': "yscj"
    }  

    # 执行列名替换
    new_df = df.rename(columns=name_map)  
    
    # 3. 构造构建 DBF 表所需的字段声明列表
    # 示例: ["kmmc C(20)", "zkzh C(20)", "yscj N(6,2)"]
    fields = [f"{name_map[col]} {type_map[col]}" for col in df.columns]  
    
    # 4. 创建并打开 DBF 表
    # db3 格式最通用。注意：为了兼容特殊中文字符，写入时强烈建议使用 utf8
    table = dbf.Table(dest_path, fields, dbf_type='db3', codepage="utf8")  
    table.open(dbf.READ_WRITE)  
    
    # 5. 遍历插入记录
    for row in new_df.to_dict(orient='records'):  
        table.append(row)  
        
    table.close()
```

> [!warning] 写入避坑指南
>
> 1. **字段截断**：DBF 原生头部字段名长度最多仅支持 10 个字节。因此，必须使用 `name_map` 将过长的中文列名映射为短字符。
> 2. **中文编码**：`dbf` 库在写入输出时不支持直接输出 `gb18030`。如果数据内包含特殊的生僻中文字符，强行写入 GBK 可能会崩溃，因此 `codepage="utf8"` 是最稳妥的解决方案。
