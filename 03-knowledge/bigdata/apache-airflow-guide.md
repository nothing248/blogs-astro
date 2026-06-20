---
title: "Apache Airflow教程"
filename: apache-airflow-guide
description: 介绍 Apache Airflow 工作流调度平台在本地环境下的安装与配置，提供使用 uv 编译安装、配置 PostgreSQL 数据库持久化及初始化管理员角色的完整步骤。同时，系统整理了 Airflow 最常见的算子（Core、DB/Warehouse、Transfer、Sensors 和云原生 K8s/Docker 算子）的使用场景与技术优势。
tags:
  - Airflow
  - 工作流调度
  - 算子设计
  - 数据管道
  - 自动化运维
aliases:
  - Apache Airflow教程
  - Airflow算子详解
  - 任务流调度
  - Airflow安装配置
status: completed
date created: 星期五, 十二月 26日 2025, 7:08:04 晚上
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 简介

## 2. 本地安装

### 2.1. 安装

```shell
export AIRFLOW_HOME=~/airflow

AIRFLOW_VERSION=3.1.3

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 3.0.0 with python 3.10: https://raw.githubusercontent.com/apache/airflow/constraints-3.1.3/constraints-3.10.txt

uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# 适配 pg 数据库
uv pip install psycopg2-binary
uv pip install apache-airflow-providers-postgres
uv pip install apache-airflow-providers-fab
```

- 试运行

```shell
source .venv/bin/activate
airflow standalone 
```

> 试运行完之后会在目录内产生 airflow.cfg 配置文件

- 配置

```
# airflow.cfg

# 配置端口号
port = 8888

# 配置数据库
sql_alchemy_conn = postgresql+psycopg2://postgres:password@127.0.0.1:5432/airflow

# 配置认证方式
auth_manager = airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
```

- 初始化

```shell
source .venv/bin/activate
airflow db migrate
airflow users create \
    --username admin \
    --firstname test \
    --lastname tm \
    --role Admin \
    --email admin@exmaple.com
```

## 3. 核心 Operator

Airflow 的 Operator 可以分为三大类：**核心算子（Core）**、**传输算子（Transfer）** 和 **社区/提供者算子（Providers）**。以下是各领域最常见的算子详解：

---

### 3.1. 最基础的核心算子 (Core Operators)

这些算子内置在 Airflow 核心包中，适用于最常见的通用任务。

- **`BashOperator`**：执行 Bash 命令或脚本。
  - _用途_：运行 Shell 脚本、安装依赖、简单的文件操作。
- **`PythonOperator`**：调用任意的 Python 函数。
  - _用途_：执行自定义的 Python 逻辑，这是灵活性最高的算子。
- **`EmailOperator`**：发送电子邮件。
  - _用途_：任务完成或失败时通知干系人。

---

### 3.2. 数据库与数据仓库算子 (DB/Warehouse)

用于与各种数据库交互，通常需要配合 `Connection` 使用。

- **`SQLExecuteQueryOperator`** (Airflow 2.5+)：通用的 SQL 执行算子，替代了旧版的 `PostgresOperator`、`MySqlOperator` 等。
- **`BigQueryInsertJobOperator`**：在 Google BigQuery 中运行查询或加载任务。
- **`SnowflakeOperator`**：在 Snowflake 数据仓库中执行 SQL。
- **`JdbcOperator`**：通过 JDBC 驱动连接任何支持的数据库。

---

### 3.3. 数据传输算子 (Transfer Operators)

专门用于在不同的系统之间“搬运”数据。

- **`S3ToRedshiftOperator`**：将数据从 AWS S3 加载到 Redshift。
- **`GCSToBigQueryOperator`**：将数据从 Google Cloud Storage 导入到 BigQuery。
- **`LocalFilesystemToGCSOperator`**：将本地文件上传到云端存储。

---

### 3.4. 传感器算子 (Sensors)

这是一种特殊的 Operator，它会 **持续轮询**，直到某个条件满足（如文件出现）才继续执行后续任务。

- **`FileSensor`**：等待指定路径下的文件出现。
- **`ExternalTaskSensor`**：等待另一个 DAG 或任务运行成功（跨 DAG 依赖）。
- **`HttpSensor`**：检查某个 API 接口是否返回正确的响应。
- **`SqlSensor`**：轮询数据库，直到某条 SQL 语句返回结果。

---

### 3.5. 云原生与容器算子 (Modern/Cloud Native)

在现代架构中，为了解决依赖冲突，常将逻辑封装在容器中运行。

- **`DockerOperator`**：在 Docker 容器中运行任务。
- **`KubernetesPodOperator`**：在 K8s 集群中动态创建一个 Pod 来运行任务（生产环境大规模任务的首选）。
  - _优点_：环境隔离最彻底，资源分配最灵活。
- **`SageMakerTrainOperator`**：在 AWS SageMaker 上启动机器学习训练任务。

---

## 4. 参考文档

- [官方文档](https://airflow.apache.org/docs/)
