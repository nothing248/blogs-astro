---
status: completed
filename: bigquery-json-column-query-and-unnest-examples
title: "BigQuery JSON 查询"
summary: 本笔记记录了 Google BigQuery 针对原生 JSON 类型列进行高阶查询的实战 SQL 案例。详细演示了如何通过点号路径与 `JSON_VALUE` 函数提取嵌套的 JSON 对象与数组元素（需注意字符串强制类型转换）。重点提供了利用 `JSON_QUERY_ARRAY` 结合 `UNNEST` 和 `LEFT JOIN` 实现复杂 JSON 数组展开（拍平）以提取订单级明细的最佳实践，为半结构化数据清洗提供 SQL 参考。
aliases: [BigQuery JSON 查询, BQ UNNEST, JSON_VALUE, 数组拍平]
tags: [BigQuery, GCP, SQL, JSON, 数据处理, 数据清洗, 半结构化数据]
date created: 星期三, 十二月 10日 2025, 7:31:06 晚上
date modified: 星期四, 六月 18日 2026, 11:35:00 晚上
---

<!-- toc -->

## 1. 核心场景：BigQuery JSON 数据提取与清洗

在 BigQuery 中，使用原生 `JSON` 数据类型可以极大地提升半结构化数据的解析灵活性。以下是核心查询场景实战。

### 1.1. 提取 JSON 内部的简单对象或标量值

通过 `JSON_VALUE` (返回 STRING) 或直接的点号路径提取：

```sql
SELECT 
    sentAt,
    -- 直接提取内部的标量字段（注意：直接提取可能带有双引号）
    context.event_time_utc8 
FROM `truemetrics-admin.yangxy_test.json_data_json`
LIMIT 10;
```

### 1.2. 提取 JSON 内部的特定数组元素

提取数组中指定索引的值，并进行 **强类型转换**（由于 JSON 解析默认返回字符串）：

```sql
SELECT 
    -- 提取 JSON 中 properties 对象下的 bookings 数组的第一个元素的金额
    JSON_VALUE(properties, '$.bookings[0].booking_gmv.amount') AS amount_str
FROM `truemetrics-admin.yangxy_test.json_data_json` 
ORDER BY 
    -- 必须进行 SAFE_CAST 转换后才能进行数值大小排序
    SAFE_CAST(JSON_VALUE(properties, '$.bookings[0].booking_gmv.amount') AS NUMERIC) DESC;
```

> [!warning] 数据类型陷阱
> 使用 `JSON_VALUE` 或 `JSON_QUERY` 等函数从 JSON 中提取值时，BigQuery 默认返回的数据类型总是 `STRING`。在进行数学计算或排序前必须显式执行 `CAST` 或 `SAFE_CAST`。

---

### 1.3. 高阶实战：提取并完全拍平 (Flatten) JSON 数组

当 JSON 字段中包含一个对象数组（如一个订单中包含多个商品），我们需要将其展开，使每个商品独立成为一行，且保留原订单的上下文。

**核心逻辑**：结合 `JSON_QUERY_ARRAY` 将 JSON 数组转化为 BQ 原生数组，再利用 `UNNEST` 和 `LEFT JOIN` 进行展开。

```sql
SELECT
  messageId,
  -- 提取基础字段
  JSON_VALUE(properties, '$.order_no') AS order_no,
  -- 提取拍平后每个子对象内部的具体字段
  JSON_VALUE(booking, '$.booking_gmv.amount') AS booking_gmv_amount
FROM
  `truemetrics-admin.yangxy_test.json_data_json`
LEFT JOIN
  -- 将 JSON 中的 bookings 数组转换为原生 ARRAY <JSON> 并展开为多行
  UNNEST(JSON_QUERY_ARRAY(properties, '$.bookings')) AS booking
ON 1=1;
```

> [!tip] 为什么要用 LEFT JOIN？
> 如果直接使用 `CROSS JOIN` (即 `FROM table, UNNEST(...)`)，当某条记录的 `bookings` 数组为空时，这条原始记录会直接从结果集中消失。使用 `LEFT JOIN ... ON 1=1` 可以确保原表数据不丢失，提取出的子字段为 `NULL`。

## 2. 参考资源

- [Google Cloud BigQuery JSON 数据处理官方文档](https://docs.cloud.google.com/bigquery/docs/json-data?hl=zh-cn#ingest_json_data)
