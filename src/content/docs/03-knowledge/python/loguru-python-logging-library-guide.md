---
status: completed
filename: loguru-python-logging-library-guide
title: "Loguru 教程"
description: 本笔记总结了 Python 生态中备受推崇的开箱即用日志库 Loguru 的核心实战配置。详细演示了如何摆脱标准库 `logging` 的繁琐 Handler 配置，直接通过 `logger.add()` 接口实现日志的文件输出、按时间/大小的自动滚动拆分（Rotation）、自动清理轮转（Retention）及 Zip 归档。还介绍了利用 `@logger.catch` 装饰器无缝捕获并记录异常堆栈的高阶用法。
aliases: [Loguru 教程, Python 日志管理, Python logging 替代]
tags: [Python, 日志管理, Loguru, 运维排障, 后端开发, 工程化]
date created: 星期二, 二月 25日 2025, 3:24:04 下午
date modified: 星期四, 六月 18日 2026, 14:25:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Loguru** 是一个旨在让 Python 中的日志记录变得有趣且无比简单的第三方开源库。它彻底解决了原生 `logging` 模块需要配置繁琐的 Formatter、Handler 和 Logger 层级的痛点，开箱即可输出带颜色且能定位到具体代码行数的精美日志。

*(安装依赖：`pip install loguru`)*

---

## 2. 核心实战用法

无需任何实例化操作，直接引入全局唯一的 `logger` 对象即可开火。

### 2.1. 基础控制台输出

```python
from loguru import logger

logger.debug("That's it, beautiful and simple logging!")
logger.info("系统正常启动。")
logger.error("发生了致命错误！")
```

### 2.2. 日志文件落盘与生命周期管理 (Rotation & Retention)

使用单一的 `add()` 接口，可以极简地配置出企业级的日志滚动归档策略：

```python
from loguru import logger

# 1. 基础落盘：自带时间戳变量命名
logger.add("logs/file_{time}.log")

# 2. 自动拆分 (Rotation)
logger.add("logs/file_{time}.log", rotation="12:00")  # 每天中午 12 点强制滚动生成新文件
logger.add("logs/file_{time}.log", rotation="1 MB")   # 日志达到 1MB 时自动切分新文件
logger.add("logs/file_{time}.log", rotation="1 week") # 每周切割

# 3. 自动清理旧日志 (Retention)
logger.add("logs/file_{time}.log", retention="10 days") # 自动删除 10 天前的旧日志

# 4. 自动压缩归档 (Compression)
logger.add("logs/file_{time}.log", rotation="50 MB", compression="zip") # 滚动切分后立刻打成 ZIP 包省空间
```

### 2.3. 高阶神器：异常堆栈静默捕获 (`@logger.catch`)

通过装饰器，能够自动捕获函数运行时的所有未处理异常，并连同异常发生时的 **全部局部变量** 和代码追踪堆栈一起详细写入日志，而且不中断上层调用：

```python
@logger.catch
def my_function(x, y, z):
    # 如果 x+y+z 为 0，引发的 ZeroDivisionError 会被 loguru 完美记录
    return 1 / (x + y + z)

my_function(0, 0, 0)
```

## 3. 参考资料

- [Loguru GitHub 项目主页](https://github.com/Delgan/loguru)
