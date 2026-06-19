---
title: "dbt教程"
filename: dbt-data-transformation-guide
summary: dbt（Data Build Tool）是现代数据栈（MDS）中专注于 ELT 模式下数据转换（Transform）的开源工具。本笔记系统梳理了 dbt 使用软件工程思想管理数据的高效范式，详细解析了其四大核心支柱（模型、ref 依赖管理、数据质量测试及缓慢变化维快照），归纳了从数据源定义到 Staging-Intermediate-Mart 分层模型的设计与编译运行流程。此外，还探讨了 Jinja 模板与 Macro 宏等动态 SQL 编程能力及开发最佳实践。
tags: ["dbt", "ELT", "Data-Transformation", "Data-Warehouse", "Modern-Data-Stack"]
aliases: ["dbt教程", "数据转换工具", "Jinja-SQL"]
status: completed
date created: 星期日, 十二月 21日 2025, 11:05:30 上午
date modified: 星期五, 六月 19日 2026, 11:58:30 中午
---

<!-- toc -->

## 1. 什么是 dbt？为什么需要它？

简单来说，dbt 的核心理念是 **“用软件工程的思想做数据转换”**。它不负责数据的搬运（Extract/Load），只负责数据的转换（Transform），是现代数据栈（Modern Data Stack）中 **ELT** 模式的那个 **T**。

在传统的 ETL 流程中，数据逻辑往往埋藏在复杂的存储过程或可视化工具的配置中，难以版本控制和测试。

**dbt 提出了一个全新的范式：**

- **SQL 为王：** 你只需要编写标准的 `SELECT` 语句，dbt 负责将其转化为数据仓库中的表（Table）或视图（View）。
- **软件化管理：** 引入了代码版本控制（Git）、自动化测试、环境隔离（开发/生产）以及文档自动生成。

---

## 2. 核心概念解析

要快速上手，你需要理解以下四个支柱概念：

### 2.1. A. 模型 (Models)

在 dbt 中，每一个 `.sql` 文件就是一个模型。

- **本质：** 模型就是一条 `SELECT` 语句。
- **物化配置 (Materialization)：** 你可以通过配置决定这个 SQL 运行后是生成一个 `Table`（实体表）、`View`（视图）、还是 `Incremental`（增量更新表）。

### 2.2. B. `ref` 函数：依赖管理的精髓

这是 dbt 最强大的地方。你不再需要写死表名（如 `FROM raw_data.users`），而是使用 `FROM {{ ref('stg_users') }}`。

- **作用：** dbt 会自动解析模型之间的依赖关系，并生成一个 **DAG（有向无环图）**。
- **优势：** 它保证了执行顺序——先运行上游表，再运行下游表。

### 2.3. C. 测试 (Tests)

dbt 将数据质量监控集成到了开发中。

- **Schema Test：** 在 YAML 中配置简单的约束（如 `unique`, `not_null`, `accepted_values`）。
- **Data Test：** 编写自定义 SQL，如果查询返回结果，则测试失败。

### 2.4. D. 快照 (Snapshots)

用于处理 **SCD（缓慢变化维）**。它可以记录数据随时间的变化情况，这在需要追溯历史状态时非常有用。

---

## 3. Dbt 的工作流程（从开发到部署）

作为开发人员，你可以将 dbt 的开发流程类比为应用开发：

1. **初始化：** `dbt init` 创建项目结构。
2. **定义数据源 (Sources)：** 在 YAML 中声明原始数据的位置。
3. **编写模型 (Models)：**
    - **Staging 层：** 对原始数据进行清洗、重命名（1:1 映射）。
    - **Intermediate 层：** 处理复杂的业务逻辑、Join 操作。
    - **Mart 层：** 面向报表或业务终端的最终宽表。
4. **编译与运行：**
    - `dbt compile`：将 Jinja 模板和 SQL 转化为纯 SQL。
    - `dbt run`：在数据库中执行 SQL，生成表。
5. **验证：** `dbt test` 运行测试用例。
6. **文档：** `dbt generate-docs` 自动根据模型注释和依赖关系生成交互式文档网页。

---

## 4. 复杂概念深度剖析：Jinja 与 宏 (Macros)

dbt 引入了 **Jinja** 模板引擎，让 SQL 具备了编程能力。

- **Jinja：** 你可以在 SQL 中使用 `if` 判断、`for` 循环。
  - _场景：_ 如果你需要对 10 个不同的支付方式进行求和，不再需要写 10 行相似 of SQL，用一个循环即可。
- **Macros (宏)：** 类比为函数。你可以编写一段可复用的逻辑（如：将美分转为美元、计算年龄），在多个模型中调用。

```sql
-- 一个简单的宏示例
{% macro to_dollars(column_name) %}
    round({{ column_name }} / 100, 2)
{% endmacro %}

-- 在模型中使用
SELECT id, {{ to_dollars('amount_cents') }} as amount_usd FROM {{ ref('payments') }}
```

---

## 5. 开发建议与最佳实践

> [!tip] 实践指南
>
> 1. **分层架构：** 严禁直接在 Marts 层引用 Raw Data。必须经过 Staging 层，这能极大降低底层结构变动带来的维护成本。
> 2. **版本控制：** 每一个 dbt 项目都应该是一个 Git 仓库。
> 3. **内联文档：** 在编写代码时顺便在 YAML 中写好 `description`，这比事后补文档要高效得多。
> 4. **先测试再上线：** 在 CI/CD 流程中强制执行 `dbt test`。

---

> [!question] 下一步建议
> 为了让你真正掌握，我建议我们进行以下操作：
> 你想让我为你演示如何配置一个标准的 dbt profiles.yml 文件以连接到你的数据库（如 PostgreSQL, Snowflake, BigQuery 等），还是想看一个具体的从原始表到最终报表层的模型演练？
