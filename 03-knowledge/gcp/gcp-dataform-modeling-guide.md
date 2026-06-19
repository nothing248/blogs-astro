---
title: "Dataform使用手册"
filename: gcp-dataform-modeling-guide
summary: GCP Dataform 数据建模与转换指南。详述了核心 SQLX 语法（配置块、ref 依赖管理），阐述了其在数据血缘、增量更新表、质量断言（Assertions）及 JS 逻辑复用上的优势。提供了从 ODS 模拟数据到最终 30d 活跃标签的 SQLX 建模代码，并分析了结合原生与 Cloud Composer/Airflow 调度的任务生命周期。
tags:
  - dataform
  - bigquery
  - sqlx
  - data-lineage
  - incremental-load
aliases:
  - Dataform使用手册
  - SQLX开发规范
  - BigQuery建模工具
status: completed
date created: 星期日, 十二月 21日 2025, 11:05:28 上午
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

在 BigQuery 技术栈中，**Dataform** 是目前最推荐的建模与转换工具。它类似于软件开发中的 IDE，将 SQL 开发、版本控制（Git）和工作流编排集成在一起，非常适合逆向梳理并维护标签系统的任务。

以下是对 Dataform 的深度解析，重点放在它如何解决 **变更与维护复杂性** 的问题。

---

## 1. 一、 核心概念：SQLX

Dataform 的核心是 `.sqlx` 文件。它是在标准 SQL 的基础上增加了配置块（config block）和引用功能（js snippets）。

- **配置化 (Config)**：在文件头部定义表类型（table, view, incremental）、描述、标签等。
- **依赖管理 (ref)**：弃用传统的 `project.dataset.table` 硬编码，改用 `${ref("table_name")}`。这会自动构建 **数据血缘图 (Lineage)**。

---

## 2. 二、 针对你任务的四大优势

### 2.1. 自动化的数据血缘 (Data Lineage)

当从“标签逻辑”逆向梳理到“原始数据”时，Dataform 会自动生成可视化图谱。

- **维护便利性**：如果修改了底层 `dws_user_daily` 表的一个字段名，Dataform 会立刻标记出所有受影响的下游标签表，防止线上任务崩溃。

### 2.2. 增量更新逻辑 (Incremental Tables)

对于“单天统计量”的计算，Dataform 提供了极其简便的增量模式：

```sql
config {
  type: "incremental",
  protected: true,
  bigquery: {
    partitionBy: "event_date"
  }
}

SELECT 
  event_date,
  user_id,
  ARRAY_AGG(DISTINCT LOWER(platform)) as active_platforms
FROM ${ref("raw_oap_events")}
WHERE event_date = CURRENT_DATE()
-- Dataform 自动处理：只有在增量运行时才会执行 WHERE 逻辑
```

### 2.3. 数据质量检查 (Assertions)

可以直接在定义标签表的同时编写断言。例如：确保 `user_id` 不为空，或者 `active_platforms` 数组不全为空。

- **价值**：在标签产出前拦截错误数据，避免错误的业务指标误导决策。

### 2.4. 逻辑复用 (Includes/Javascript)

如果多个标签都要用到“转小写后判断平台”的逻辑，可以写一个 Javascript 函数：

```javascript
// 在 includes/utils.js 中定义
function clean_platform(col) {
  return `LOWER(TRIM(${col}))`;
}
```

然后在多个 SQLX 文件中调用。这极大地减少了重复代码（DRY 原则）。

---

## 3. 三、 Dataform 与现有技术栈的集成

在此场景下，架构应该如下演进：

1. **数据采集**：原始数据进入 BigQuery。
2. **数据建模 (Dataform)**：
   - 定义 `definitions/sources/`（声明原始数据源表）。
   - 定义 `definitions/intermediate/`（计算单天统计量指标的中间表）。
   - 定义 `definitions/labels/`（根据中间表计算 30d 活跃等最终标签表）。
3. **任务编排 (Composer)**：
   - 虽然 Dataform 提供了自带调度，但在复杂业务流程中，更推荐使用 **Cloud Composer (Airflow)** 触发 Dataform 运行。
   - 使用 `DataformCreateCompilationResultOperator` 确保每次运行的都是最新的 Git 代码快照。

---

## 4. 四、 demo 案例

- **数据初始化**

```sql
-- 创建原始事件表 (ODS 层)
CREATE OR REPLACE TABLE `your-project.[数据集X].form_test_event`
(
  event_date DATE OPTIONS(description="分区字段：事件日期"),
  user_id STRING,
  event_name STRING,
  context STRUCT<
    event_time_utc8 TIMESTAMP,
    platform STRING,
    device_id STRING
  >
)
PARTITION BY event_date
CLUSTER BY user_id;

-- 2. 插入模拟数据
INSERT INTO `your-project.[数据集X].form_test_event` (event_date, user_id, event_name, context)
VALUES
(DATE('2025-12-15'), 'user_A', 'app_open', STRUCT('2025-12-15 10:00:00 UTC', 'iOS', 'dev_1')),
(DATE('2025-12-16'), 'user_A', 'click', STRUCT('2025-12-16 11:00:00 UTC', 'android', 'dev_2')),
(DATE('2025-12-17'), 'user_B', 'app_open', STRUCT('2025-12-17 09:00:00 UTC', 'WEB', 'dev_3')),
(DATE('2025-12-18'), 'user_C', 'app_open', STRUCT('2025-12-18 12:00:00 UTC', 'Android', 'dev_4'));
```

- **定义数据源**

```javascript
declare({
  database: "your-project",
  schema: "your_dataset",
  name: "ods_oap_events",
});
```

- **定义中间数据**

```sql
config {
  type: "incremental",
  schema: "your_dataset",
  uniqueKey: ["event_date", "user_id"],
  bigquery: {
    partitionBy: "event_date",
    clusterBy: ["user_id"]
  },
  description: "用户每日活跃平台汇总表（逆向梳理的单天指标）"
}

SELECT
  event_date,
  user_id,
  -- 逆向梳理出的最少统计量：当天去重后的平台列表
  ARRAY_AGG(DISTINCT LOWER(context.platform)) AS active_platforms
FROM
  ${ref("ods_oap_events")}
WHERE
  -- 只有在增量运行时才过滤日期，全量运行时扫描全表
  ${when(incremental(), `event_date = CURRENT_DATE()`)}
GROUP BY
  1, 2
```

- **定义最终数据**

```sql
config {
  type: "table",
  schema: "yangxy_test",
  description: "用户活跃标签：过去30天是否打开过App"
}

WITH user_agg_30d AS (
  SELECT
    user_id,
    -- 第一步：先将 30 天内的所有小数组合并成一个大数组
    ARRAY_CONCAT_AGG(active_platforms) AS all_platforms_30d
  FROM
    ${ref("dws_user_platform_daily")}
  WHERE
    event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY
    1
)

SELECT
  user_id,
  -- 第二步：在 SELECT 中使用 EXISTS + UNNEST 处理聚合后的结果
  CASE 
    WHEN EXISTS(
      SELECT 1 
      FROM UNNEST(all_platforms_30d) AS p 
      WHERE p IN ('app', 'ios', 'android')
    ) THEN 1 
    ELSE 0 
  END AS app_active_status_30d
FROM
  user_agg_30d
```

---

## 5. 五、 发布、部署/调度

### 5.1. 任务发布 (Release Configurations)

在 Dataform 中，所编写的代码不能直接“运行”到生产环境，必须先经过 **发布（Release）**。它定义了代码如何“打包”。

- **编译变量**：可以设置在“生产环境”下，数据库 ID 改为 `prod-project`，而在“测试环境”下使用 `test-project`。
- **版本管理**：可以按固定周期（比如每小时）对 Git 分支进行一次快照采样，生成一个“编译结果”（Compilation Result）。
- **环境管理**：每个环境可以指向不同的 BigQuery Dataset 甚至不同的 GCP Project。

### 5.2. 任务调度 (Workflow Configurations)

调度决定了任务“什么时候跑”以及“跑哪些表”。

### 5.3. 内部调度 (Native Scheduler)

在 Dataform 控制台的 **Workflow Configurations** 中直接创建。

- **选择范围**：可以选择运行“全部表”，或者利用 **Tags** 运行特定标签（比如只跑 `tag:app_active` 相关的表）。
- **频率设置**：支持标准的 Crontab 表达式。

### 5.4. 外部调度 (Cloud Composer / Airflow)

对于复杂的企业级应用，通常由 **Composer** 触发 Dataform。

- **优势**：可以实现跨系统的依赖。例如：先跑 Python 脚本从外部拉取数据 -> 触发 Dataform 进行 BQ 转换 -> 转换完成后发送邮件通知。
- **实现方式**：使用 Airflow 的 `DataformCreateCompilationResultOperator` 和 `DataformCreateWorkflowInvocationOperator`。

---

### 5.5. 核心生命周期图解

1. **Develop**: 在 Workspace 编写 `.sqlx`。
2. **Commit/Push**: 将代码同步到 Git 仓库。
3. **Compile**: Dataform 将 SQL 逻辑转化为一张 **Directed Acyclic Graph (DAG)**。
4. **Invoke**: 执行 DAG。Dataform 会根据依赖顺序，依次向 BigQuery 发送 SQL Job。
