---
title: "typing.Annotated用法"
filename: typing-annotated-guide
description: Python typing.Annotated 类型提示指南。基于 PEP 593 规范，详述了在不干扰 Mypy 等静态检查器的前提下，将运行时特定元数据附加到类型的机制。解析了参数规范与自动展平规则，提供了 Pydantic V2/V3 中可重用字段约束的定义方法，并展示了通过 get_type_hints 与 get_args 在运行时获取元数据的方法及多版本兼容代码。
tags:
  - python-typing
  - annotated
  - pydantic-v2
  - metadata
  - pep-593
aliases:
  - typing.Annotated用法
  - Pydantic字段约束可重用
  - Python元数据附加
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:19 上午
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

`typing.Annotated` 是 Python `typing` 模块中一个非常强大的工具，它在 **PEP 593** 中被引入，用于为现有类型添加 **上下文特定的元数据（Metadata）**，而不会改变静态类型检查器（如 Mypy、Pyright）对该类型的基本解释。

简单来说，`Annotated` 允许你将运行时所需的信息“捆绑”到类型提示中。

---

## 1. 核心概念：将运行时元数据附加到类型

![](http://qiniu.sxyxy.top/20251015164758.png)

### 1.1. 静态类型检查器的工作方式

对于静态类型检查器（如 Mypy），当它看到 `Annotated[int, ...]` 时，会 **安全地忽略** 所有元数据，只将其视为基础类型 `int`。

```python
from typing import Annotated

# 静态类型检查器只将 UserId 视为 int
UserId = Annotated[int, "这是一个用户 ID"]

def process_id(user_id: UserId) -> int:
    # 静态检查器允许 user_id + 1
    return user_id + 1
```

### 1.2. 运行时工具的工作方式

运行时库（如 Pydantic、FastAPI、SQLAlchemy）可以访问并解析这些附加的元数据，并根据元数据执行特定的逻辑，例如：

- **Pydantic**：将元数据用作字段验证规则、默认值或模式生成。
- **FastAPI**：将元数据用作查询参数、路径参数或请求体的额外配置（如描述、默认值）。
- **其他库**：用于自定义序列化、数据库映射等。

---

## 2. 语法细节和规则

1. **参数数量限制**：`Annotated` 必须至少有两个参数：一个基础类型和至少一个元数据项。
   - `Annotated[int]` 是 **无效** 的。
2. **元数据的顺序**：传递给 `Annotated` 的多个元数据项的 **顺序会被保留**，并且对相等性检查有影响。
3. **嵌套展平**：嵌套的 `Annotated` 类型会被自动展平（Flattened），元数据从最内层开始依次展开。
   - `Annotated[Annotated[int, 'A'], 'B']` 等价于 `Annotated[int, 'A', 'B']`。

---

## 3. 经典应用场景：Pydantic 中的字段约束

`Annotated` 最广泛的应用之一是在 Pydantic (V2 及更高版本) 中，用来代替旧版本中的 `Field` 关键字参数。它允许你将验证约束直接绑定到类型上。

**传统 Pydantic v1 风格：**

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # 字段约束与类型提示分开
    age: int = Field(..., gt=0, description="用户年龄，必须大于0")
```

**使用 `Annotated` 的 Pydantic v2/v3 风格（推荐）：**

```python
from typing import Annotated
from pydantic import BaseModel, Field

# 将 Field 对象作为元数据附加到 int 类型上
PositiveInt = Annotated[int, Field(gt=0)] 
# 注：Field 本身也可以作为元数据传递其他配置

class User(BaseModel):
    # 字段约束直接内联到类型中
    age: PositiveInt 
    
    # 也可以直接在模型定义中使用
    name: Annotated[str, Field(max_length=50, description="用户名")]
```

### 3.1. 优点：创建可重用的约束类型

通过定义 `PositiveInt` 这样的类型别名，你可以在整个项目中重用这个带有约束的类型，而不需要在每个模型中重复 `Field(gt=0)`。

---

## 4. 如何在运行时获取元数据

要在运行时（在自定义代码或库中）访问 `Annotated` 中的元数据，你需要使用 `typing` 模块中的两个函数：

1. **`typing.get_type_hints(obj, include_extras=True)`**：必须传入 `include_extras=True`，才能获取到 `Annotated` 对象本身，而不是被剥离的基础类型。
2. **`typing.get_args(annotated_type)`**：用于提取 `Annotated` 中的参数列表。

```python
from typing import Annotated, get_args, get_type_hints

def my_func(x: Annotated[int, "Min: 0", 100]) -> None:
    pass

# 1. 获取包含元数据的类型提示
hints = get_type_hints(my_func, include_extras=True)
annotated_type = hints['x']
print(annotated_type) 
# 输出: typing.Annotated [int, 'Min: 0', 100]

# 2. 提取参数
args = get_args(annotated_type)
base_type = args[0]  # int
metadata = args[1:]  # ('Min: 0', 100)

print(f"基础类型: {base_type}")
print(f"元数据: {metadata}")
```

---

## 5. 总结

`Annotated` 的作用是作为类型提示和运行时元数据之间的“桥梁”：

|角色|作用|
|---|---|
|**静态检查器**|**忽略** 元数据，只检查基础类型的类型安全。|
|**运行时库**|**提取并使用** 元数据来执行特定的运行时行为（如验证、序列化、文档生成）。|
|**开发者**|创建可重用、语义更丰富的类型别名。|

---

## 6. 拓展

### 6.1. 版本兼容导入

|Python 版本|推荐的导入代码|说明|
|---|---|---|
|**Python >= 3.9**|`from typing import Annotated`|直接从标准库导入，无需安装额外的包。|
|**Python < 3.9 (例如 3.8)**|`from typing_extensions import Annotated`|需要先安装 `pip install typing_extensions`。这是向后兼容的解决方案。|
