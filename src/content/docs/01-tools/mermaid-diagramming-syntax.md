---
title: "Mermaid流程图"
filename: mermaid-diagramming-syntax
summary: Mermaid是一种使用文本语法绘制图表的开源标记语言。本文提供核心语法详解。内容包含图表流向定义（如TB、LR）、常用五种节点形状的标识符配置、线段与箭头连接关系表示，以及横向和纵向多子图结构的嵌套和样式定义，使流程图渲染高度自动化。
tags: [mermaid, diagrams, markdown-integration, flowcharts]
aliases: [Mermaid流程图, 文本绘图, Mermaid语法]
status: completed
date created: 星期日, 一月 11日 2026, 2:35:39 下午
date modified: 星期五, 六月 19日 2026, 12:06:25 中午
---

<!-- toc -->

## 1. 简介

Mermaid 是一种基于文本的图形绘制语言。它的核心逻辑是：**用简单的符号描述节点（Node）和连线（Link）**。

Code snippet

```
graph TD
  ...内容...
```

---

## 2. 声明图表方向

在首行定义图表的流动方向：

- **TB / TD** (Top to Bottom): 从上到下
- **BT** (Bottom to Top): 从下到上
- **LR** (Left to Right): 从左到右
- **RL** (Right to Left): 从右到左

---

## 3. 节点形状（常用的 5 种）

节点名（如 `A`）是代码里的标识符，括号里的文字是显示在图上的内容。

- **矩形（默认）：** `A[文字]`
- **圆角矩形：** `B(文字)`
- **菱形（判断）：** `C{文字}`
- **圆形：** `D((文字))`
- **平行四边形：** `E[/文字/]` 或 `F[\文字\]`

---

## 4. 连线样式

连线定义了流程的走向，通过不同的符号可以改变线条外观。

- **带箭头的实线：** `A --> B`
- **无箭头的实线：** `A --- B`
- **带文字的实线：** `A -- 文字 --> B` 或 `A -->|文字| B`
- **虚线：** `A -.-> B`
- **加粗线：** `A ==> B`

---

## 5. 复杂流程演示

这是一个结合了判断逻辑和样式的综合案例：

```
graph TD
    Start(开始) --> Input[/输入数据/]
    Input --> Condition{数据合格?}
    
    Condition -- 是 --> Process[处理数据]
    Condition -- 否 --> Error((报错))
    
    Process --> End[结束]
    Error --> Stop[停止]

    %% 还可以给特定节点上色
    style Start fill:#f9f,stroke:#333,stroke-width:2px
    style Error fill:#ff9999
```

---

## 6. 高阶技巧

- **子图 (Subgraphs)：** 如果想把部分流程框在一起，可以使用 `subgraph`。

    ```
    graph LR
        subgraph 准备阶段
            A --> B
        end
        subgraph 执行阶段
            C --> D
        end
        B --> C
    ```

- **多行连线：** 你可以一次性连接多个节点，例如 `A --> B & C --> D`，表示 A 同时指向 B 和 C，然后 B 和 C 都指向 D。
- **特殊字符：** 如果文字里包含特殊符号（如括号），请用引号包裹，例如 `Node["文字 (带括号)"]`。
