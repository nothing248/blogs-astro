---
title: "HBase安装教程"
filename: apache-hbase-guide
description: 详解分布式列式数据库 Apache HBase 2.6.0 的单机、伪分布式、分布式集群及客户端的部署步骤。提供核心配置文件（hbase-env.sh、hbase-site.xml、regionservers、backup-masters）的参数设置。同时，展示了使用 hbase shell 进行表创建（create）、插入（put）和获取（get）等数据交互命令，并附带了 systemd 服务配置文件。
tags:
  - HBase
  - NoSQL
  - 分布式数据库
  - HBase配置
  - 大数据组件
aliases:
  - HBase安装教程
  - HBase Shell操作
  - 列式存储数据库
  - HBase伪分布式搭建
status: completed
date created: 星期三, 十二月 10日 2025, 6:20:42 晚上
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

## 2. 安装

### 2.1. 单机安装

```shell
wget https://dlcdn.apache.org/hbase/2.6.0/hbase-2.6.0-bin.tar.gz #下载时需要注意与 Hadoop 版本的兼容
mv hbase-2.6.0-bin.tar.gz /opt/software
cd /opt/software
tar -zxvf hbase-2.6.0-bin.tar.gz
mkdir /data/hadoop
# 环境变量
export HBASE_HOME=/opt/software/hbase-2.6.0
export HBASE_CONF_DIR=/opt/software/hbase-2.6.0/conf
export PATH=$HBASE_HOME/bin:$PATH
```

- 目录

```shell
# 创建目录
mkdir /data/hbase
mkdir /data/hbase/log #日志数据
mkdir /data/hbase/tmp #日志数据
mkdir /data/hbase/data #日志数据
mkdir /data/hbase/zookeeper #日志数据
```

- hbase-env.sh 配置

```
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_HOME=/opt/software/hadoop-3.3.6
export HBASE_HOME=/opt/software/hbase-2.6.0
export HBASE_LOG_DIR=/data/hbase/log
```

- hbase-site.xml 配置

```xml
<configuration>
    <!-- 存储目录 这里的hdfs可以是单机版的-->
    <property>
        <name>hbase.rootdir</name>
        <value>file:////data/hbase/data</value>
        <description>The directory shared byregion servers.</description>
    </property>
    <property>
        <name>hbase.tmp.dir</name>
        <value>/data/hbase/tmp</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/data/hbase/zookeeper</value>
    </property>
    <!-- false是单机模式，true是分布式模式  -->
    <property>
        <name>hbase.cluster.distributed</name>
        <value>false</value>
    </property>
    <property>
        <name>hbase.unsafe.stream.capability.enforce</name>
        <value>false</value>
        <description>使用本地文件系统存储，不使用 HDFS 的情况下需要禁用此配置，设置为 false</description>
    </property>
</configuration>
```

## 3. 伪分布安装

- 安装

> 参考单机安装

- 目录

```shell
mkdir /data/hbase
mkdir /data/hbase/log #日志数据
mkdir /data/hbase/tmp #日志数据
mkdir /data/hbase/zookeeper_pseudo #日志数据
```

- hbase-env.sh 配置

```
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_HOME=/opt/software/hadoop-3.3.6
export HBASE_HOME=/opt/software/hbase-2.6.0
export HBASE_LOG_DIR=/data/hbase/log
export HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP="true" #解决object is not an instance of declaring class错误
export HBASE_MANAGES_ZK=false #是否使用内置的zookeeper
```

- hbase-site.xml 配置

```xml
<configuration>
    <!-- 存储目录 这里的hdfs可以是单机版的-->
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://wsl:9000/hbase</value>
        <description>The directory shared byregion servers.</description>
    </property>
    <property>
        <name>hbase.tmp.dir</name>
        <value>/data/hbase/tmp</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/data/hbase/zookeeper_pseudo</value>
    </property>
    <!-- false是单机模式，true是分布式模式  -->
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
<!--    以下是使用zookeeper配置-->
</configuration>
```

- regionservers

```
wsl
```

> 该方案必须启动 zookeeper

### 3.1. 分布式安装

- 安装  
...

> 参考单机安装

- 目录

```shell
mkdir /data/hbase
mkdir /data/hbase/log #日志数据
mkdir /data/hbase/tmp #日志数据
```

- hbase-env.sh 配置

```
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_HOME=/opt/software/hadoop-3.3.6
export HBASE_HOME=/opt/software/hbase-2.6.0
export HBASE_LOG_DIR=/data/hbase/log
export HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP="true" #解决object is not an instance of declaring class错误
export HBASE_MANAGES_ZK=false #是否使用内置的zookeeper
```

- hbase-site.xml 配置

```xml
<configuration>
    <property>
        <!-- 指定 hbase 以分布式集群的方式运行 -->
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <!-- 指定 hbase 在 HDFS 上的存储位置 -->
        <name>hbase.rootdir</name>
        <value>hdfs://slave1:9000/hbase</value>
    </property>
    <property>
        <name>hbase.tmp.dir</name>
        <value>/data/hbase/tmp</value>
    </property>
    <property>
        <!-- 指定 zookeeper 的地址-->
        <name>hbase.zookeeper.quorum</name>
        <value>slave1:2181,slave2:2181,slave3:2181</value>
    </property>
</configuration>
```

- regionservers

```
slave1
slave2
slave3
```

- backup-masters

```
slave2
```

## 4. 客户端配置

- hbase-site.xml 配置

```xml
<configuration>
    <property>
        <!-- 指定 zookeeper 的地址-->
        <name>hbase.zookeeper.quorum</name>
        <value>slave1:2181,slave2:2181,slave3:2181</value>
    </property>
</configuration>
```

## 5. 使用

- 服务启动

```shell
start-hbase.sh
```

- 单机测试

```shell
hbase shell
list #查看表
create 'users', 'info', 'data' #创建表
describe 'users' #描述表结构
put 'users', 'user1', 'info:name', 'Alice' #插入数据
get 'users', 'user1' #获取数据
exit #退出
```

- 伪分布式测试

```shell
hbase shell
list #查看表
create 'users_pes', 'info', 'data' #创建表
describe 'users_pes' #描述表结构
put 'users_pes', 'user1', 'info:name', 'Alice' #插入数据
get 'users_pes', 'user1' #获取数据
exit #退出
```

- 分布式

```shell
hbase shell
list #查看表
create 'users_dit', 'info', 'data' #创建表
describe 'users_dit' #描述表结构
put 'users_dit', 'user1', 'info:name', 'Alice' #插入数据
get 'users_dit', 'user1' #获取数据
exit #退出
```

- systemd

```
[Unit]
Description=hbase

[Service]
Type=forking
Environment="JAVA_HOME=/opt/software/jdk1.8.0_351"
Environment="HBASE_HOME=/opt/software/hbase-2.6.0"
ExecStart=/opt/software/hbase-2.6.0/bin/start-hbase.sh
ExecStop=/opt/software/hbase-2.6.0/bin/stop-hbase.sh

[Install]
WantedBy=multi-user.target
```

## 6. 拓展信息

### 6.1. 依赖服务

- hadoop
- zookeeper

## 7. 参考资料

- [官方链接](https://hbase.apache.org/)
