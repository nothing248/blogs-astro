---
title: "ZooKeeper安装与配置指南"
filename: zookeeper-setup-guide
description: ZooKeeper 是一款开源的分布式应用程序协调服务，常用于分布式同步、命名服务、集群维护和分布式锁。本指南详细介绍了 ZooKeeper 在单机与多节点集群环境下的部署步骤与配置项，包括 myid 的设置、客户端连接管理指令，并提供了结合 Java 环境变量的 Systemd 守护进程配置文件以及 ZooInspector 可视化工具的使用方法。
tags:
  - zookeeper
  - cluster-setup
  - service-coordination
  - systemd
aliases:
  - ZooKeeper安装与配置指南
  - ZooKeeper集群搭建
  - ZooInspector使用
status: completed
date created: 星期三, 十二月 10日 2025, 6:20:41 晚上
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

ZooKeeper 是一个开源的分布式应用程序协调服务，是 Google 的 Chubby 一个开源的实现。

- 分布式同步
- 命名服务
- 集群维护
- 分布式锁

## 2. 概念

- Leader
- Follower
- Observer

## 3. 安装

### 3.1. 单机

- 安装

```shell
wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz
mv apache-zookeeper-3.8.4-bin.tar.gz /opt/software
cd /opt/software
tar -zxvf apache-zookeeper-3.8.4-bin.tar.gz
mkdir /data/zookeeper
# 环境变量
export ZOOKEEPER_HOME=/opt/software/apache-zookeeper-3.8.4-bin
export PATH=$ZOOKEEPER_HOME/bin:$PATH
```

- 配置

```properties
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/data/zookeeper
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1

## Metrics Providers
#
# https://prometheus.io Metrics Exporter
#metricsProvider.className=org.apache.zookeeper.metrics.prometheus.PrometheusMetricsProvider
#metricsProvider.httpHost=0.0.0.0
#metricsProvider.httpPort=7000
#metricsProvider.exportJvmInfo=true
```

### 3.2. 集群

- 安装

> 参考单机安装部分。

- 配置

```properties
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/data/zookeeper
# the port at which the clients will connect
clientPort=2181
# 配置集群
server.1=slave1:2888:3888
server.2=slave2:2888:3888
server.3=slave3:2888:3888
```

- myid

```shell
# 写入 myid 文件以标识当前节点
/opt/software/apache-zookeeper-3.8.4-bin/data/myid
1
```

> [!WARNING]
> 注意：myid 只能使用数字。

## 4. 使用

### 4.1. 服务端

```shell
zkServer.sh start
zkServer.sh start-foreground
zkServer.sh stop
zkServer.sh status
zkServer.sh restart
```

### 4.2. 客户端

```shell
zkCli.sh -server 127.0.0.1:2181
```

### 4.3. 管理

- systemd 配置

```ini
## 需要指明jdk环境变量和ZOO_LOG_DIR
#/etc/systemd/system/zookeeper.service
[Unit]
# 服务描述
Description=zookeeper
# 在网络服务启动后运行
After=network.target

[Service]
Type=forking
# jdk环境变量
Environment=JAVA_HOME=/opt/software/jdk1.8.0_351
# 启动命令
ExecStart=/opt/software/apache-zookeeper-3.8.4-bin/bin/zkServer.sh start
# 停止命令
ExecStop=/opt/software/apache-zookeeper-3.8.4-bin/bin/zkServer.sh stop
# 重载命令
ExecReload=/opt/software/apache-zookeeper-3.8.4-bin/bin/zkServer.sh restart

[Install]
WantedBy=multi-user.target
```

- 管理

```shell
systemctl daemon-reload
systemctl enable zookeeper
systemctl restart zookeeper
```

- 可视化工具

```shell
wget https://issues.apache.org/jira/secure/attachment/12436620/ZooInspector.zip
unzip ZooInspector.zip
java -jar zookeeper-dev-ZooInspector.jar  
```

![](http://qiniu.sxyxy.top/20240813170628.png)

## 5. 拓展信息

...

## 6. 参考资料

- [官方链接](https://zookeeper.apache.org/)
