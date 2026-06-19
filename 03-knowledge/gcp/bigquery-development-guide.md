---
title: "BigQuery开发手册"
filename: bigquery-development-guide
summary: Google BigQuery 数仓开发与优化指南。系统解析了嵌套结构拍平（UNNEST 与 LEFT JOIN 结合防数据漏查）、重复数据 JSON 转换检测、数据集恢复等核心 SQL 用法。详细对比了分区与聚簇的降费提速策略，剖析了半连接（IN/EXISTS/JOIN）和 MERGE 增量更新的性能表现与限制，并总结了 API 变量定义与跨区域操作的局限性。
tags:
  - bigquery
  - sql-optimization
  - partition-clustering
  - merge-upsert
  - unnest-array
aliases:
  - BigQuery开发手册
  - BQ分区与聚簇
  - BigQuery的UNNEST操作
status: completed
date created: 星期日, 一月 11日 2026, 11:12:43 上午
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

## 1. 简介

Google BigQuery 是 Google Cloud 提供的完全托管、Serverless 的企业级数据仓库解决方案。

## 2. SQL

### 2.1. 数据类型

- STRUCT 对应的结构

### 2.2. 恢复删除的数据集

```sql
UNDROP SCHEMA `dataset_id`;
```

### 2.3. 创建表

```sql
CREATE TABLE my_dataset.my_table (
    column1 INT64,
    column2 STRING,
    column3 DATE
);
```

### 2.4. 插入数据

```sql
INSERT INTO my_dataset.my_table (column1, column2, column3)
VALUES
  (2, 'Jane Smith', '2023-02-01'),
  (3, 'Bob Johnson', '2023-03-01');
```

### 2.5. 表关联

- **CROSS JOIN**

```sql
SELECT * FROM a, b;
SELECT * FROM a CROSS JOIN b;
```

- **INNER JOIN**

```sql
SELECT * FROM a INNER JOIN b;
```

- **LEFT JOIN**

```sql
SELECT * FROM a LEFT JOIN b;
```

- **RIGHT JOIN**

```sql
SELECT * FROM a RIGHT JOIN b;
```

- **FULL JOIN**

```sql
SELECT * FROM a FULL JOIN b;
```

### 2.6. 查看操作

- **UNNEST 操作**
  - **表层级**

  ```sql
  SELECT user_pseudo_id, value.string_value AS location 
  FROM `*.*.events_20231113`, UNNEST(event_params) 
  WHERE key='page_location' 
  LIMIT 1000;
  ```

  - **字段层级**

  ```sql
  SELECT user_pseudo_id, (
      SELECT value.string_value 
      FROM UNNEST(event_params) 
      WHERE key = "page_location"
  ) AS location 
  FROM `*.*.events_20231113` 
  LIMIT 1000;
  ```

  > [!NOTE]
  > 两者查询量一致，但表层查询不返回空值，字段层级可能返回空值。

- **窗口操作**
  - 行层级
  - 数据层级

- **查看表记录所有列的重复值**

```sql
WITH DuplicateRows AS (
  SELECT *, COUNT(*) OVER (PARTITION BY t) AS row_count
  FROM (
    SELECT *, TO_JSON_STRING(a) AS t -- 将记录转化为 JSON 格式进行整体比对
    FROM `1.2.3` AS a
  )
)
SELECT *
FROM DuplicateRows
WHERE row_count > 1;
```

---

## 3. 优化

### 3.1. 分区表

按照指定列将大表进行分区存储，以降低查询费用与查询时间（查询条件满足时会过滤掉非匹配的分区数据，降低扫描量）。

- **分区分类**：
  - 整数列范围
  - 时间单位列
  - 提取时间分区
- **分区修饰符**：  
  `table_name$partition_id`

> [!NOTE]
> 分区表支持通过 API 方式创建。

### 3.2. 聚簇表

按照指定列（聚簇列）进行排序分块，以降低查询费用与查询时间（查询条件满足时会过滤掉非匹配的分块数据，降低扫描量）。

- **聚簇字段支持分类**：
  - STRING
  - INT64
  - NUMERIC
  - BIGNUMERIC
  - DATE
  - DATETIME
  - TIMESTAMP
  - BOOL
  - GEOGRAPHY

  > [!WARNING]
  > 聚簇列应当选择非重复度较高的列。

---

## 4. API 相关

...

---

## 5. 常见的查询

### 5.1. 场景一：半查询

在 BigQuery (BQ) 中，实现“从 B 表中获取 ID 存在于 A 表中的数据”有几种常用的方法。这本质上是一个 **半连接 (Semi-join)** 的操作。

#### 5.1.1. 使用 `IN` 子查询 (最直观)

这是最符合逻辑直觉的方法，适用于 A 表中的 ID 数量不是天文数字的情况。

```sql
SELECT *
FROM `your_project.dataset.B`
WHERE id IN (
  SELECT id 
  FROM `your_project.dataset.A`
);
```

#### 5.1.2. 使用 `EXISTS` (性能通常更优)

对于大型数据集，`EXISTS` 通常比 `IN` 效率更高，因为引擎在找到匹配项后会立即停止扫描该行。

```sql
SELECT b.*
FROM `your_project.dataset.B` AS b
WHERE EXISTS (
  SELECT 1 
  FROM `your_project.dataset.A` AS a 
  WHERE a.id = b.id
);
```

#### 5.1.3. 使用 `INNER JOIN` (最常用)

如果你不仅需要 B 表的数据，后续还可能需要 A 表中的其他字段，或者你更习惯连接操作，可以使用 `JOIN`。

> [!WARNING]
> 如果 A 表中的 ID 有重复，直接 `JOIN` 会导致 B 表的结果也出现重复。建议先对 A 表进行 `DISTINCT` 处理。

```sql
SELECT b.*
FROM `your_project.dataset.B` AS b
INNER JOIN (
  SELECT DISTINCT id 
  FROM `your_project.dataset.A`
) AS a
ON b.id = a.id;
```

#### 5.1.4. 方案对比与建议

|**方法**|**优点**|**缺点**|**适用场景**|
|---|---|---|---|
|**IN**|代码简洁，易于理解|当子查询结果集极大时性能可能下降|中小规模数据集|
|**EXISTS**|性能稳定，处理大数据集表现好|语法稍微复杂一点点|大规模数据集，去重逻辑内置|
|**INNER JOIN**|扩展性强，方便获取两表字段|需要手动处理 A 表重复 ID 否则会产生笛卡尔积|需要关联 A 表其他字段时|

---

### 5.2. 场景二：更新数据

在 BigQuery 中，使用 `MERGE` 语句可以实现“增量更新”或“同步”逻辑。它允许你在一个语句中同时完成 **INSERT（插入）**、**UPDATE（更新）** 和 **DELETE（删除）** 操作。

通常的场景是：**用 B 表（源表/变动数据）去更新 A 表（目标表/主表）。**

#### 5.2.1. 标准 MERGE 语法模板

```sql
MERGE `your_project.dataset.A` AS T  -- T 代表 Target（目标表）
USING `your_project.dataset.B` AS S  -- S 代表 Source（源表/新数据）
ON T.id = S.id                       -- 匹配条件

-- 1. 如果 ID 匹配：更新 A 表的数据
WHEN MATCHED THEN
  UPDATE SET 
    T.name = S.name,
    T.update_time = S.update_time,
    T.status = S.status

-- 2. 如果 ID 在 B 表有，但在 A 表没有：插入新行
WHEN NOT MATCHED BY TARGET THEN
  INSERT (id, name, update_time, status)
  VALUES (id, name, update_time, status)

-- 3. (可选) 如果 ID 在 A 表有，但在 B 表已经没了：删除 A 表对应行
WHEN NOT MATCHED BY SOURCE THEN
  DELETE;
```

#### 5.2.2. 核心逻辑说明

1. **WHEN MATCHED**:
    当 ON 条件成立时触发。通常用于更新现有记录的信息（例如价格变动、状态更新）。

2. **WHEN NOT MATCHED BY TARGET**:
    当源表 B 有新 ID，而目标表 A 还没有时触发。这就是常见的 INSERT 逻辑。

3. **WHEN NOT MATCHED BY SOURCE**:
    这是高级用法。如果某条数据在 A 表里，但这次 B 表（全量同步）里没出现，说明该数据可能已被物理删除，此时可以清理 A 表。

#### 5.2.3. 性能优化最佳实践

- **分区对齐 (Partitioning)**:
    如果 A 表是按天分区的（例如 partition_date），在 ON 条件中一定要包含分区字段，这样 BQ 只需要扫描特定的分区，能极大节省扫描费用并提升速度。

    ```sql
    ON T.id = S.id AND T.partition_date = S.partition_date
    ```

- **处理重复**:
    `MERGE` 语句要求源表 B 中匹配 ON 条件的行必须是唯一的。如果 B 表中有重复的 id，BQ 会报错。建议在 USING 后面先对 B 表做一个去重处理（例如使用 `QUALIFY ROW_NUMBER()...`）。

- **仅更新变动行**:
    在 WHEN MATCHED 后面可以加额外的 AND 条件，只有当数据真的发生变化时才执行更新，减少写入量：

    ```sql
    WHEN MATCHED AND T.status != S.status THEN
      UPDATE SET T.status = S.status
    ```

---

## 6. 拓展信息

### 6.1. 表名命名规则

- 数字、字符、下划线
- 长度 1024 字符限制

### 6.2. SQL 注意事项

- `DECLARE`、`SET` 等 SQL 语法在 API 调用与定时任务配置时可能会报错，开发时请尽量避免使用该语法。

### 6.3. 跨区域操作

- 不支持跨区域的数据集或 Cloud Storage 的数据写入。
- 不支持跨区域（大区域或者小区域）的数据关联查询。

### 6.4. 限制

- `WITH` 语法不能用于 `CREATE` 语句中。
- `DECLARE` 变量不能直接用于 `LIMIT` 后面。

### 6.5. 拍平

**默认情况下，如果数组为空（Empty Array）或为 `NULL`，该条记录就不会出现在查询结果中。**

这是因为在 BigQuery 中，使用 `FROM table, UNNEST(array_field)` 这种逗号分隔的语法，在逻辑上等同于 **`CROSS JOIN`**。

#### 6.5.1. 为什么会消失？

`CROSS JOIN` 的规则是：左表的每一行与右表的每一行进行组合。

- 如果右表（即 `UNNEST` 展开后的数组）是空的（0 行），那么 `左表记录 × 0 = 0`。
- 结果就是：该条原始记录在结果集中会被完全过滤掉。

#### 6.5.2. 解决方法：使用 `LEFT JOIN`

如果你希望即便数组为空，也要保留原表中的基本信息（此时数组拍平后的字段会显示为 `NULL`），你需要显式使用 **`LEFT JOIN`**：

```sql
SELECT 
  t.id,
  flattened_item
FROM 
  `your_project.your_dataset.your_table` AS t
LEFT JOIN 
  UNNEST(t.your_array_field) AS flattened_item;
```

---

## 7. 参考资料

- [官方链接](https://cloud.google.com/bigquery/docs?hl=zh-cn)
