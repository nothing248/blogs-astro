---
title: "SQL五大分类"
filename: sql-language-classifications
description: SQL 数据库语言的完整分类指南。系统梳理了五大核心子集：数据定义 DDL（CREATE、ALTER）、数据操作 DML（INSERT、UPDATE）、数据查询 DQL（SELECT）、数据控制 DCL（GRANT）和事务控制 TCL（COMMIT、ROLLBACK），并补充了用于调优的维护命令 DAL（EXPLAIN）。通过对比表与直观比喻，明确阐述了各子集的命令边界与应用场景。
tags:
  - sql
  - database
  - ddl
  - dml
  - transaction-control
aliases:
  - SQL五大分类
  - DDL与DML区别
  - 事务控制命令TCL
status: completed
date created: 星期五, 十二月 26日 2025, 7:08:04 晚上
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

根据对数据库操作的性质不同，通常将 SQL 划分为 **5 大核心子集**。

为了直观地理解，我们可以把数据库比作一座“图书馆”：**DDL** 负责盖楼和做书架，**DML** 负责放书和取书，**DQL** 负责找书，而 **DCL/TCL** 负责门卫安全和确保书籍归还流程不出错。

---

## 1. SQL 语言完整分类表

### 1.1. DDL (Data Definition Language) - 数据定义语言

用于定义或修改数据库的 **结构（Schema）**。它不操作具体数据，而是操作存储数据的“容器”。

- **核心关键词**：`CREATE` (创建), `ALTER` (修改结构), `DROP` (删除), `TRUNCATE` (清空表数据但保留结构)。
- **操作对象**：数据库、表、索引、视图、触发器。

### 1.2. DML (Data Manipulation Language) - 数据操作语言

用于对表中的 **数据进行增、删、改**。

- **核心关键词**：
  - `INSERT`：向表中插入新行。
  - `UPDATE`：更新现有行的数据。
  - `DELETE`：删除表中的行。
- **注意**：DML 操作通常需要提交（Commit）才能永久生效。

### 1.3. DQL (Data Query Language) - 数据查询语言

这是 SQL 中使用频率最高的部分，专门用于从数据库中 **检索数据**。

- **核心关键词**：`SELECT`。
- **常用子句**：`WHERE` (过滤), `ORDER BY` (排序), `GROUP BY` (分组), `JOIN` (多表连接)。
- **说明**：虽然有些分类将 DQL 归入 DML，但在实际工程中，查询（Query）通常被独立出来讨论。

### 1.4. DCL (Data Control Language) - 数据控制语言

用于定义数据库的 **访问权限和安全级别**。

- **核心关键词**：
  - `GRANT`：赋予用户某种权限（如查询或修改权限）。
  - `REVOKE`：收回已授予用户的权限。
- **场景**：DBA（数据库管理员）用来管理谁能看哪些表。

### 1.5. TCL (Transaction Control Language) - 事务控制语言

用于管理数据库的 **事务**，确保 ACID 特性（原子性、一致性、隔离性、持久性）。

- **核心关键词**：
  - `COMMIT`：提交事务，将更改永久保存。
  - `ROLLBACK`：回滚事务，撤销未提交的更改。
  - `SAVEPOINT`：在事务中设置保存点，以便部分回滚。

---

## 2. 总结对比图

|**缩写**|**全称**|**主要功能**|**常用命令**|
|---|---|---|---|
|**DDL**|Data Definition|定义、修改、删除 **结构**|`CREATE`, `DROP`, `ALTER`|
|**DML**|Data Manipulation|增、删、改 **数据**|`INSERT`, `UPDATE`, `DELETE`|
|**DQL**|Data Query|**查询** 检索数据|`SELECT`|
|**DCL**|Data Control|控制用户 **权限**|`GRANT`, `REVOKE`|
|**TCL**|Transaction Control|管理 **事务** 提交/回滚|`COMMIT`, `ROLLBACK`|

---

### 2.1. 进阶补充：行政类命令 (Administrative Commands)

除了上述五大类，还有一类通常被称为 **DAL (Data Administration Language)**，用于数据库的维护和性能分析，例如：

- `DESC` / `DESCRIBE`：查看表结构。
- `USE`：切换当前数据库。
- `EXPLAIN`：分析 SQL 执行计划（调优必备）。
