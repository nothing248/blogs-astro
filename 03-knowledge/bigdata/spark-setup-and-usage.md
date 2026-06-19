---
title: "Spark安装与配置指南"
filename: spark-setup-and-usage
summary: Apache Spark 是一款通用分布式数据处理框架。本指南详述了其多环境（Windows、单机、伪分布式、分布式集群）安装、PySpark 库集成与 Systemd 守护配置。重点提供了 PySpark 核心算子在 Map/List/Set 聚合、窗口函数及时间间隔计算等业务场景下的代码，并针对 OOM 内存溢出和 BigQuery 写入报错给出了优化与避坑建议。
tags:
  - spark
  - pyspark
  - cluster-setup
  - bigquery
aliases:
  - Spark安装与配置指南
  - PySpark使用示例
  - Spark大数据处理
status: completed
date created: 星期五, 十二月 5日 2025, 3:42:13 下午
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

Spark 是一个开源的通用大数据处理框架，最初由加州大学伯克利分校的 AMPLab 开发，后来成为 Apache 软件基金会的一个顶级项目。它提供了高效的数据处理能力，支持多种数据处理任务，包括批处理、实时流处理、机器学习和图形处理等。

## 2. 安装

### 2.1. Window 安装

- 下载  

```shell
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
mv spark-3.5.0-bin-hadoop3.tgz /opt/software
tar -zxvf spark-3.5.0-bin-hadoop3.tgz
```

- 下载 hadoop(winutil.exe)信息  
下载版本目录并且复制 C:\apps\opt\hadoop

> [!NOTE]
> 注意：仅 Windows 需要。

- 配置环境变量

```shell
SPARK_HOME  = C:\apps\opt\spark-3.5.0-bin-hadoop2.7
HADOOP_HOME = C:\apps\opt\hadoop
PYSPARK_PYTHON = "D:\miniconda\envs\py3.11.8\python.exe" #指定 worker 解析器，默认使用启动是的解释器
PYSPARK_DRIVER_PYTHON = "" #dirver 解析器, 默认使用启动是的解释器。需要与 worker 保持版本一致。
PYTHONPATH = "D:\spark-3.5.0-bin-hadoop3\python;D:\spark-3.5.0-bin-hadoop3\python\lib\py4j-0.10.9.7-src.zip;%PYTHONPATH%" # 指定解析器模块查找路径地址
PATH=%PATH%;%SPARK_HOME%\bin;%HADOOP_HOME%\bin
```

> [!WARNING]
> 注意：PYSPARK_PYTHON 解析器有版本限制。例如 spark-3.5.0-bin-hadoop2.7 要求 py3.11.8。

### 2.2. Pyspark 安装

```shell
pip install pyspark==3.5.0
```

### 2.3. 单机安装

- 安装

```shell
wget https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-without-hadoop.tgz #下载时需要注意与 Hadoop 版本的兼容
mv spark-3.5.2-bin-without-hadoop.tgz /opt/software
cd /opt/software
tar -zxvf spark-3.5.2-bin-without-hadoop.tgz
# 环境变量
export SPARK_HOME=/opt/software/spark-3.5.2-bin-without-hadoop
export SPARK_CONF_DIR=/opt/software/spark-3.5.2-bin-without-hadoop/conf
export PATH=$SPARK_HOME/bin:$PATH
```

- 目录

```shell
mkdir /data/spark
mkdir /data/spark/log #日志数据
```

- spark-env.sh 配置

```properties
export SPARK_DIST_CLASSPATH=$(/opt/software/hadoop-3.3.6/bin/hadoop classpath)
export SPARK_LOG_DIR=/data/spark/log
```

### 2.4. 伪分布式

- 安装

> 参考单机安装

- spark-env.sh 配置

```properties
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_HOME=/opt/software/hadoop-3.3.6
export HADOOP_CONF_DIR=/opt/software/hadoop-3.3.6/ect/pseudo_hadoop
export SPARK_HOME=/opt/software/spark-3.5.2-bin-without-hadoop
export SPARK_DIST_CLASSPATH=$(/opt/software/hadoop-3.3.6/bin/hadoop classpath)
export SPARK_LOG_DIR=/data/spark/log
```

- workers 配置

```text
wsl
```

> [!TIP]
> `start-all.sh` 命令启动时发现环境变量丢失。可以修改 `start-workers` 中 `"${SPARK_HOME}/sbin/workers.sh" cd "${SPARK_HOME}" ; "${SPARK_HOME}/sbin/start-worker.sh" "spark://$SPARK_MASTER_HOST:$SPARK_MASTER_PORT"`（去除了 `\`）。

### 2.5. 分布式安装

- 安装

> 参考单机安装

- spark-env.sh 配置

> 参考伪分布式

- workers 配置

```text
slave1
slave2
slave3
```

### 2.6. 客户端

```shell
spark-shell --master spark://slave1:7077
```

> [!WARNING]
> 注意: 尽量保持客户端与服务端的版本一致。

## 3. 核心概念

### 3.1. 核心组件

| **组件名称** | **描述** | **主要用途** |
| :--- | :--- | :--- |
| **Spark Core** | Spark 的核心执行引擎，包括调度、内存管理、容错和与存储系统（如 HDFS、S3）的交互。它定义了 **RDD** API。 | 任务执行和数据抽象 |
| **Spark SQL** | 用于处理结构化和半结构化数据的模块。它允许用户使用 SQL 或 HiveQL 进行查询，并提供了 **DataFrame** API。 | 交互式查询、数据分析 |
| **Spark Streaming** | 用于处理实时流数据的模块，可以将流数据分解为一系列微批次（micro-batches）进行处理。 | 实时数据处理、日志分析 |
| **MLlib** | 一个可扩展的机器学习库，包含常见的学习算法和工具，如分类、回归、聚类和协同过滤。 | 机器学习模型训练与部署 |
| **GraphX** | 用于图（Graph）并行计算的 API 和库，可用于社交网络分析、路径查找等。 | 图计算和图分析 |

### 3.2. 核心概念

- Cluster Manager/Worker Node
- spark application
- DAG/惰性求值
- driver/excutor
- stage/task
- 宽依赖/窄依赖
- Transformation/action
- 分区/shuffle
- rdd/dataframe/datasets

## 4. 使用

### 4.1. 维护

- 启动

```shell
./sbin/start_all.sh
```

- 单机测试

```shell
spark-shell --master local[*]
```

- 分布式测试

```shell
curl http://wsl:8081
```

- 分布式测试

```shell
curl http://slave1:8081
```

- systemd

```ini
[Unit]
Description=Spark Service
After=network.target

[Service]
Type=forking
Environment=HADOOP_HOME=/opt/software/hadoop-3.3.6
Environment=JAVA_HOME=/opt/software/jdk1.8.0_351
Environment=HADOOP_CONF_DIR=/opt/software/hadoop-3.3.6/etc/pseudo_hadoop
Environment=SPARK_CONF_DIR=/opt/software/spark-3.5.2-bin-without-hadoop/pseudo_conf
ExecStart=/opt/software/spark-3.5.2-bin-without-hadoop/sbin/start-all.sh
ExecStop=/opt/software/spark-3.5.2-bin-without-hadoop/sbin/stop-all.sh
Restart=on-failure
RestartSec=5
RemainAfterExit=yes # 注意该选项必须设置为true

[Install]
WantedBy=multi-user.target 
```

- 管理

```shell
systemctl start spark
systemctl status spark
systemctl stop spark
```

### 4.2. 场景

- 初始化

```python
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
conf = SparkConf(). \
        setAppName(f"demo"). \
        set("spark.jars","lib\\spark-3.5-bigquery-0.37.0.jar"). \ # 该库是用于链接 Bigquery 库
        set("viewsEnabled", 'true'). \
        set("parentProject","gcp_project_id").\
        set("credentialsFile", "E:\\projects\\python\\user_tag_management_service\\conf\\gcp_server_account.json")
spark = SparkSession.builder. \
    config(conf=conf).getOrCreate()
```

- 统计 map

```python
from pyspark.sql.types import MapType, StringType, LongType
device_map_df = device_df.groupBy('one_id','device_category').agg(F.count(F.lit(1)).alias('device_category_count'))
device_map_df = device_map_df.groupBy("one_id").agg(F.collect_list(F.create_map("device_category", "device_category_count")).alias("device_category_map_list"))
device_map_df = device_map_df.withColumn('device_category_map',F.reduce('device_category_map_list', F.lit(F.create_map([])).cast(MapType(StringType(), LongType())), lambda acc,x: F.map_concat(acc,x)))
device_map_df = device_map_df.select('one_id','device_category_map')
device_map_df.head(20)
```

- 统计 list

```python
window = Window.partitionBy('one_id').orderBy(F.desc('event_datetime'))
device_list_df = device_df.withColumn('device_category_list',F.collect_list('device_category').over(window))
device_list_df = device_list_df.groupBy(device_list_df.one_id).agg(F.max('device_category_list').alias('device_category_list'))
device_list_df.head(20)
```

> [!IMPORTANT]
> 注意：直接 orderby 之后的 groupby 不能确保顺序。确保顺序需要使用 window 的方式。

- 统计 set

```python
device_set_df = device_list_df.withColumn('device_category_set',F.array_distinct('device_category_list'))
device_set_df.head(20)
```

- 统计 last

```python
window = Window.partitionBy('one_id').orderBy(F.desc('event_datetime'))
device_last_df = device_df.withColumn('device_category_last',F.first('device_category',ignorenulls=True).over(window))
device_last_df.show()
```

- 统计第几条记录

```python
# 方式一
window = Window.partitionBy('one_id').orderBy(F.desc('event_datetime'))
device_top_df = device_df.withColumn("row_number",F.row_number().over(window))
device_top_df = device_top_df.filter(stage_last_df["row_number"] == 1) #过滤最后行 
device_top_df = device_top_df.groupBy("one_id").agg(F.max(col).alias(f"{self.pre}_{col}_last")) #可能会出现 event_datetime 相同，保持唯一性去最大值
device_top_df.show()

# 方式二
window = Window.partitionBy('one_id').orderBy(F.desc('event_datetime'))
top2_df = top2_df.withColumn('device_category_top',F.nth_value(F.col(col),1,ignoreNulls=True).over(window))
top2_df = top2_df.groupBy("one_id").agg(F.max('device_category_top').alias('device_category_top'))
top2_df.show()
```

- 统计时间间隔

```python
interval_df = device_df.withColumn("event_timestamp", F.unix_timestamp(F.col("event_datetime"), "yyyy-MM-dd HH:mm:ss").cast("timestamp")) #转化为时间戳格式 
window = Window.partitionBy('one_id').orderBy("event_timestamp")
interval_df = interval_df.withColumn("last_timestamp", F.lead("event_timestamp",1).over(window))
interval_df = interval_df.withColumn("time_interval", (F.col("last_timestamp").cast("long") - F.col("event_timestamp").cast("long")))
interval_df = interval_df.filter(F.col('time_interval').isNotNull())
interval_df = interval_df.groupby('one_id').agg(F.collect_list("time_interval").alias("time_intervals"),F.max('event_datetime').alias('pre_event_date'))
interval_df.show()
```

- 统计比率

```python
business_df = business_df.withColumn('last_365days_refund_amount_percentage', F.coalesce(F.col('last_days365_refund_amount_sum'),F.lit(0.0)) / F.coalesce(F.col('last_days365_order_sum'),F.lit(0.0)))
business_df.show()
```

- 统计是否大于平均值

```python
business_df = business_df.withColumn('last_365days_is_above_exchange_rate_average', F.when(F.col('last_365days_refund_amount_percentage')>business_df.select(F.mean("last_365days_refund_amount_percentage")).collect()[0][0],'是').otherwise('否'))
business_df.show()
```

- 转化列值

```python
def convert_map(key):
    return {
        "desktop":"de",
        "mobile":"mo"
    }.get(key,None)
# 注册 udf 函数
convert_map_udf = F.udf(convert_map,StringType())
convert_map_df = device_category_map_list.withColumn('convert_device_category_max',convert_map_udf('device_category_max'))
convert_map_df.show()
```

- 合并 map

```python
device_map_df = union_df.groupBy("one_id").agg(F.collect_list("device_category_map").alias("device_category_map_list"))
device_map_df = device_map_df.withColumn('device_category_map',F.reduce('device_category_map_list', F.lit(F.create_map([])).cast(MapType(StringType(), LongType())), lambda acc,x: F.map_zip_with(acc, x, lambda k, v1, v2: F.when(F.isnull(v1),v2).otherwise(F.when(F.isnull(v2),v1).otherwise(v1 + v2)))))
device_map_df = device_map_df.select('one_id','device_category_map')
device_map_df.show()
```

- 合并 list

```python
window = Window.partitionBy('one_id').orderBy(F.desc('event_datetime'))
device_list_df = union_df.withColumn('device_category_list_list',F.collect_list('device_category_set').over(window))
device_list_df = device_list_df.groupBy(device_list_df.one_id).agg(F.max('device_category_list_list').alias('device_category_list_list'))
device_list_df = device_list_df.withColumn('device_category_set',F.reduce('device_category_list_list', F.lit([]).cast(ArrayType(StringType())), lambda acc,x: F.concat(acc,x))) # 不去重
device_list_df.show()
```

- 合并 set

```python
window = Window.partitionBy('one_id').orderBy(F.desc('event_datetime'))
device_list_df = union_df.withColumn('device_category_list_list',F.collect_list('device_category_set').over(window))
device_list_df = device_list_df.groupBy(device_list_df.one_id).agg(F.max('device_category_list_list').alias('device_category_list_list'))
device_list_df = device_list_df.withColumn('device_category_set',F.reduce('device_category_list_list', F.lit([]).cast(ArrayType(StringType())), lambda acc,x: F.array_union(acc,x))) # 去重
device_list_df.show()
```

- join 多个 dataframe

```python
from functools import reduce
new_dfs = [base_df,device_merge_df]
new_df = reduce(lambda df1, df2: df1.join(df2, on="one_id", how="inner"), new_dfs)
new_df.show()
```

### 4.3. 经验

- 同行数指标统计，使用 withColumn 行进行处理。
- 行压缩统计，尽量使用 withColumn 进行处理，其次考虑使用 join。

## 5. 拓展信息

### 5.1. OOM 错误

- 分步使用 persist 持久化, count 算子解决该问题。
- 尽量减少 join 的使用。

### 5.2. Bigquery 写入

- 持久化写入报错 -- 去除持久化。
- 表结构变动 overwrite 写入报错 -- 先删除原来的表。

## 6. 参考资料

- [官方链接](https://spark.apache.org/)
- [winutil.exe 地址](https://github.com/steveloughran/winutils/blob/master/hadoop-3.0.0/bin/winutils.exe)
- [Bigquery Spark](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)
