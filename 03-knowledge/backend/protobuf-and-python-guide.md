---
title: "Protocol Buffers教程"
filename: protobuf-and-python-guide
summary: 介绍 Google 开源的数据序列化协议 Protocol Buffers（Protobuf）。通过详细的三步演练，展示了定义 .proto 消息结构（支持嵌套与 repeated 列表）、运行 protoc 编译器生成 Python 模块，以及使用 Python 脚本进行高效消息序列化（SerializeToString）与反序列化（ParseFromString）的完整实践过程。
tags:
  - Protobuf
  - 数据序列化
  - 二进制传输
  - Python-Protobuf
  - 微服务架构
aliases:
  - Protocol Buffers教程
  - Protobuf序列化原理
  - Python中Protobuf使用
status: completed
date created: 星期三, 十二月 10日 2025, 6:20:41 晚上
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 使用

### 1.1. 🛠️ 步骤一：定义 `.proto` 文件

首先，您需要创建一个名为 `order.proto` 的文件来定义消息结构。

Protocol Buffers

```proto
// order.proto 文件内容

syntax = "proto3"; // 指定使用 Protobuf 3 语法

package com.example.orders; // 包名，有助于避免命名冲突

// 嵌套的消息结构：代表订单中的单个商品
message Item {
  string name = 1;       // 商品名称
  int32 quantity = 2;    // 数量
  double unit_price = 3; // 单价
}

// 外部消息结构：代表整个订单
message Order {
  string order_id = 1;         // 订单唯一 ID
  string customer_name = 2;    // 客户名称
  // 嵌套结构字段：使用 'repeated' 关键字表示这是一个列表（数组）
  repeated Item items = 3;     
  int64 order_timestamp = 4;   // 订单创建时间戳
}
```

---

### 1.2. 🔧 步骤二：生成 Python 代码

接下来，使用 Protobuf 编译器 `protoc` 将 `.proto` 文件编译成 Python 模块。

在命令行中，确保您已安装 `protobuf` Python 库 and `protoc` 编译器，然后运行以下命令（假设 `order.proto` 在当前目录下）：

```shell
protoc --python_out=. order.proto
```

执行成功后，将生成一个名为 `order_pb2.py` 的文件。这个文件包含了 Protobuf 消息对应的 Python 类。

---

### 1.3. 🐍 步骤三：Python Demo 示例

下面是使用生成的 `order_pb2.py` 模块进行序列化和反序列化的 Python 脚本示例。

### 1.4. Python 脚本 (`demo.py`)

```python
import order_pb2 # 导入编译生成的模块
import time
import os

# --------------------------
# 1. 序列化 (Serialization)
# --------------------------

def serialize_order():
    """创建一个 Order 消息实例，填充数据并将其序列化为字节串。"""
    
    # 实例化 Order 消息
    order = order_pb2.Order()
    order.order_id = "ORD-20251208-A001"
    order.customer_name = "张三"
    order.order_timestamp = int(time.time())

    # 实例化并添加第一个嵌套 Item 消息
    item1 = order.items.add() # 使用 repeated 字段的 add() 方法创建新元素
    item1.name = "无线键盘"
    item1.quantity = 1
    item1.unit_price = 499.99

    # 实例化并添加第二个嵌套 Item 消息
    item2 = order.items.add() 
    item2.name = "人体工学鼠标"
    item2.quantity = 2
    item2.unit_price = 199.50
    
    # 打印原始消息内容
    print("--- 原始 Order 消息内容 ---")
    print(order)

    # 将消息序列化为字节串
    serialized_data = order.SerializeToString()
    print(f"\n序列化后的字节串长度: {len(serialized_data)} bytes")
    
    return serialized_data

# --------------------------
# 2. 反序列化 (Deserialization)
# --------------------------

def deserialize_order(serialized_data):
    """接收字节串，将其反序列化为 Order 消息实例并读取数据。"""
    
    # 实例化一个新的 Order 消息对象
    new_order = order_pb2.Order()
    
    # 将字节串解析到新的对象中
    new_order.ParseFromString(serialized_data)
    
    print("\n--- 反序列化后的 Order 消息内容 ---")
    print(f"订单 ID: {new_order.order_id}")
    print(f"客户: {new_order.customer_name}")
    print(f"订单时间戳: {new_order.order_timestamp}")
    print(f"包含 {len(new_order.items)} 个商品项目。")
    
    print("\n--- 商品项目详情 ---")
    for i, item in enumerate(new_order.items):
        total = item.quantity * item.unit_price
        print(f"  项目 {i+1}: {item.name} (数量: {item.quantity}, 单价: {item.unit_price:.2f}, 总计: {total:.2f})")

# --------------------------
# 3. 运行演示
# --------------------------

if __name__ == "__main__":
    # 执行序列化
    binary_data = serialize_order()
    
    # 执行反序列化
    deserialize_order(binary_data)
```

### 1.5. 运行结果（示例输出）

```
--- 原始 Order 消息内容 ---
order_id: "ORD-20251208-A001"
customer_name: "张三"
items {
  name: "无线键盘"
  quantity: 1
  unit_price: 499.99
}
items {
  name: "人体工学鼠标"
  quantity: 2
  unit_price: 199.5
}
order_timestamp: 1670535028

序列化后的字节串长度: 89 bytes

--- 反序列化后的 Order 消息内容 ---
订单 ID: ORD-20251208-A001
客户: 张三
订单时间戳: 1670535028
包含 2 个商品项目。

--- 商品项目详情 ---
  项目 1: 无线键盘 (数量: 1, 单价: 499.99, 总计: 499.99)
  项目 2: 人体工学鼠标 (数量: 2, 单价: 199.50, 总计: 399.00)
```
