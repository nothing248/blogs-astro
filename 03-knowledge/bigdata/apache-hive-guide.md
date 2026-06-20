---
title: "Hive安装配置"
filename: apache-hive-guide
description: 介绍建立在 Hadoop 之上的数据仓库工具 Apache Hive 3.1.3 的部署流程。包含与 MySQL 数据库的连接驱动配置及同步表结构操作，详解了 HiveServer2 远程服务及 Metastore 服务（嵌入式与独立式）的架构差别与参数调整。最后给出了 beeline 客户端连接示例、HiveQL 交互命令以及 systemd 脚本。
tags:
  - Hive
  - 数据仓库
  - Metastore
  - HiveServer2
  - ETL组件
aliases:
  - Hive安装配置
  - Beeline客户端
  - Hive元数据管理
  - Metastore独立部署
status: completed
date created: 星期一, 五月 19日 2025, 2:05:19 下午
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

Hive 是建立在 Hadoop 上的数据仓库基础架构。它提供了一系列的工具，可以用来进行数据提取转化加载，可以简称为 ETL。

## 2. 安装

### 2.1. 基础安装

- 安装

```shell
wget https://dlcdn.apache.org/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz #下载时需要注意与 Hadoop 版本的兼容
mv apache-hive-3.1.3-bin.tar.gz /opt/software
cd /opt/software
tar -zxvf apache-hive-3.1.3-bin.tar.gz
mkdir /data/hadoop
# 环境变量
export HIVE_HOME=/opt/software/apache-hive-3.1.3-bin
export HIVE_CONF_DIR=/opt/software/apache-hive-3.1.3-bin/conf
export PATH=$HADOOP_HOME/sbin:HIVE_HOME/bin:$PATH
```

- 目录

```shell
mkdir /data/hive
mkdir /data/hive/querylog
mkdir /data/hive/scratchdir
mkdir /data/hive/resources
```

- hive-env.sh 配置

```
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HIVE_HOME=/opt/software/apache-hive-3.1.3-bin
export HADOOP_HOME=/opt/software/hadoop-3.3.6
export HADOOP_CONF_DIR=/opt/software/hadoop-3.3.6/etc/hadoop
```

- hive-site.xml 配置

```
<configuration>
    <property>
     <name>javax.jdo.option.ConnectionURL</name>
     <value>jdbc:mysql://127.0.0.1:3307/hive?serverTimezone=Asia/Shanghai</value>
    </property>
    <property>
     <name>javax.jdo.option.ConnectionDriverName</name>
     <value>com.mysql.cj.jdbc.Driver</value>
    </property>
    <property>
     <name>javax.jdo.option.ConnectionUserName</name>
     <value>root</value>
    </property>
    <property>
     <name>javax.jdo.option.ConnectionPassword</name>
     <value>example</value>
    </property>
    <property>
     <name>hive.querylog.location</name>
     <value>/data/hive/querylog</value>
    </property>
    <property>
     <name>hive.exec.local.scratchdir</name>
     <value>/data/hive/scratchdir</value>
    </property>
    <property>
     <name>hive.downloaded.resources.dir</name>
     <value>/data/hive/resources</value>
    </property>
</configuration>
```

- 初始化数据库

```shell
wget https://downloads.mysql.com/archives/get/p/3/file/mysql-connector-j-8.3.0.tar.gz # 下载与 mysql 版本对应的 connecotr
tar -zxvf mysql-connector-j-8.3.0.tar.gz
mv mysql-connector-j-8.3.0.jar /opt/software/apache-hive-3.1.3-bin/lib #添加 jar 包
schematool -dbType mysql -initSchema --verbose # 同步表结构 注意：需要先创建对应数据库
```

### 2.2. hiveserver2 服务

可以提供远程的 hive 服务

- hadoop core.xml 配置

```
<!-- 配置访问hadoop的权限，能够让hive访问到 -->
<property>
 <name>hadoop.proxyuser.root.hosts</name>
 <value>*</value>
</property>
<property>
 <name>hadoop.proxyuser.root.users</name>
 <value>*</value>
</property>
```

- hive-site.xml 配置

```
<property>
 <name>hive.server2.thrift.bind.host</name>
 <value>0.0.0.0</value>
</property>

<!-- 指定hiveserver2连接的端口号 -->
<property>
 <name>hive.server2.thrift.port</name>
 <value>10000</value>
</property>
<property>  
    <name>hive.server2.webui.host</name>  
    <value>0.0.0.0</value>  
    <description>The host address the HiveServer2 WebUI will listen on</description>  
</property>  
<property>  
    <name>hive.server2.webui.port</name>  
    <value>10002</value>  
</property>
```

- 启动服务

```shell
hive --service hiveserver2
```

- 连接服务

```shell
beeline -u jdbc:hive2://localhost:10000 -n root
```

### 2.3. Metastore 服务

嵌入式(每个 Hive CLI 都需要直接连接元数据库，当 Hive CLI 较多时，数据库压力会比较大。)/独立式(每个客户端都需要用户元数据库的读写权限，元数据库的安全得不到很好的保证。)

- 嵌入式配置

```
<configuration>
    <!-- jdbc连接的URL -->
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://hadoop001:3306/metastore?useSSL=false</value>
    </property>
    
    <!-- jdbc连接的Driver-->
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.jdbc.Driver</value>
    </property>
    
 <!-- jdbc连接的username-->
    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>root</value>
    </property>

    <!-- jdbc连接的password -->
    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>123456</value>
    </property>
</configuration>
```

- 独立式

```
<!-- 指定metastore服务的地址 -->
<property>
 <name>hive.metastore.uris</name>
 <value>thrift://localhost:9083</value>
</property>
<!--Attempting to reconnect (1 of 1) after 1s. getCurrentNotificatio错误-->
<property>
    <name>hive.metastore.event.db.notification.api.auth</name>
    <value>false</value>
</property>
```

- 启动服务

```shell
hive --service metastore
```

> 不需要集群部署，可以单独设备进行部署

## 3. 使用

- 直接使用

```shell
hive
show databases;
show tables;
create table stu(id int, name string);
insert into stu values(1,"ss");
select * from stu;
```

- hive2serve 服务

```shell
hive --service metastore
```

- metaserver 服务

```shell
hive --service hiveserver2
```

- 客户端

```shell
beeline -u jdbc:hive2://localhost:10000 -n root
```

- systemd

```
# /etc/systemd/system/hiveserver2.service
[Unit]
Description=Apache HiveServer2
After=network.target

[Service]
Environment=HIVE_CONF_DIR=/opt/software/apache-hive-3.1.3-bin/conf
ExecStart=/opt/software/apache-hive-3.1.3-bin/bin/hive --service hiveserver2
Restart=on-failure

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/hivemetastore.service
[Unit]
Description=Apache Hive Metastore
After=network.target

[Service]
Environment=HIVE_CONF_DIR=/opt/software/apache-hive-3.1.3-bin/conf
ExecStart=/opt/software/apache-hive-3.1.3-bin/bin/hive --service metastore
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

- 管理

```shell
systemctl start hivemetastore
systemctl start hiveserver2
systemctl stop hiveserver2
systemctl stop hiveserver2
```

> 注意需要先启动 MySQL 与 Hadoop

## 4. 拓展信息

...

## 5. 参考资料

- [官方链接](https://hive.apache.org/)
