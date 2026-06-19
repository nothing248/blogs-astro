---
title: "Hadoop伪分布式配置"
filename: hadoop-deployment-guide
summary: 详解分布式大数据存储平台 Hadoop 3.3.6 在单机、伪分布式、分布式集群及客户端模式下的安装、配置与测试流程。提供核心配置文件（core-site.xml、hdfs-site.xml、mapred-site.xml、yarn-site.xml）及 workers 的参数定义，给出使用 HDFS dfs 客户端与 MapReduce WordCount 运行测试的步骤，并附带了 systemd 服务单元配置文件。
tags:
  - Hadoop
  - HDFS
  - YARN
  - 大数据部署
  - 资源调度
aliases:
  - Hadoop伪分布式配置
  - YARN集群搭建
  - HDFS管理指令
  - MapReduce测试
status: completed
date created: 星期一, 五月 19日 2025, 2:05:17 下午
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

一个 HDFS 分布式文件系统，一般用户大数据文件存储；一个 MapReduce 为海量的数据提供了计算能力

## 2. 安装

### 2.1. 单机

- 安装

```
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
mv hadoop-3.3.6.tar.gz /opt/software
cd /opt/software
tar -zxvf hadoop-3.3.6.tar.gz 
mkdir /data/hadoop
# 环境变量
export HADOOP_HOME=/opt/software/hadoop-3.3.6
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/pseudo_hadoop
export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$PATH
```

> 环境变量也可以在$HADOOP_HOME/etc/hadoop/hadoop-env.sh 配置

### 2.2. 伪分布式

- 配置主机
  - hostname
  - 环境变量
  - ssh 免密登录

- 安装

> 参考单机安装

- 目录

```shell
# 创建目录
mkdir /data/hadoop
mkdir /data/hadoop/name #namenode 存放目录
mkdir /data/hadoop/secondary #secondarynamenode 存放目录
mkdir /data/hadoop/data #datanode 数据存放目录
mkdir /data/hadoop/tmp #临时数据
mkdir /data/hadoop/log #日志数据
```

- hadoop-env.sh 配置

```
export HDFS_NAMENODE_USER="root"
export HDFS_DATANODE_USER="root"
export HDFS_SECONDARYNAMENODE_USER="root"
export YARN_RESOURCEMANAGER_USER="root"
export YARN_NODEMANAGER_USER="root"
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_LOG_DIR=/data/hadoop/log
```

- core-site.xml 配置

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://wsl:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/data/hadoop/tmp</value>
   </property>
   <!--  hive2serve需要-->
   <property> 
     <name>hadoop.proxyuser.root.hosts</name> 
     <value>*</value>
    </property>
    <property>
     <name>hadoop.proxyuser.root.groups</name>
     <value>*</value>
    </property>
</configuration>
```

- hdfs-site.xml 配置

```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
     <property>
        <name>dfs.namenode.name.dir</name>
        <value>/data/hadoop/name</value>
        <description>namenode临时文件所存放的目录</description>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/data/hadoop/secondary</value>
        <description>secondarynamenode临时文件所存放的目录</description>
    </property>
    <property>
        <name>dfs.namenode.checkpoint.dir</name>
        <value>/data/hadoop/data</value>
        <description>datanode临时文件所存放的目录</description>
    </property>
    <property>
        <name>dfs.namenode.http-address</name>
        <value>wsl:9870</value> 
        <description>hdfs web 地址</description>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>wsl:50090</value>
    </property>
</configuration>
```

- mapred-site.xml 配置

```
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
        <description>告诉hadoop以后MR(Map/Reduce)运行在YARN上</description>
    </property>
    <property>
        <name>mapreduce.admin.user.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
        <description>可以设置AM【AppMaster】端的环境变量，如果上面缺少配置，可能会造成mapreduce失败</description>
   </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
        <description>可以设置AM【AppMaster】端的环境变量，如果上面缺少配置，可能会造成mapreduce失败</description>
   </property>
</configuration>
```

- yarn-site.xml 配置

```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
        <description>nomenodeManager获取数据的方式是shuffle</description>
    </property>
    <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>0.0.0.0:8088</value>
        <description>配置 yarn 外部可访问，(外网IP:端口)</description>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
        <description>容器可能会覆盖的环境变量，而不是使用NodeManager的默认值</description>
    </property>
    <property>
       <name>yarn.nodemanager.vmem-check-enabled</name>
       <value>false</value>
        <description>关闭内存检测，虚拟机需要，不配会报错</description>
    </property>
</configuration>
```

- workers 配置

```
# etc/hadoop/workers
wsl
```

> 可以通过环境变量来控制不同的配置

### 2.3. 分布式部署

- 配置主机
  - hostname
  - 环境变量
  - ssh 免密登录

- 安装

> 参考单机安装

- 目录

```shell
# 创建目录
mkdir /data/hadoop
mkdir /data/hadoop/name #namenode 存放目录
mkdir /data/hadoop/secondary #secondarynamenode 存放目录
mkdir /data/hadoop/data #datanode 数据存放目录
mkdir /data/hadoop/tmp #临时数据
mkdir /data/hadoop/log #日志数据
```

- hadoop-env.sh 配置

```
export HDFS_NAMENODE_USER="root"
export HDFS_DATANODE_USER="root"
export HDFS_SECONDARYNAMENODE_USER="root"
export YARN_RESOURCEMANAGER_USER="root"
export YARN_NODEMANAGER_USER="root"
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_LOG_DIR=/data/hadoop/log
```

- core-site.xml 配置

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://slave1:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/data/hadoop/tmp</value>
   </property>
   <!--  hive2serve需要-->
   <property> 
     <name>hadoop.proxyuser.root.hosts</name> 
     <value>*</value>
    </property>
    <property>
     <name>hadoop.proxyuser.root.groups</name>
     <value>*</value>
    </property>
</configuration>
```

- hdfs-site.xml 配置

```
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/data/hadoop/name</value>
    <description>namenode临时文件所存放的目录</description>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/data/hadoop/secondary</value>
    <description>secondarynamenode临时文件所存放的目录</description>
  </property>
  <property>
    <name>dfs.namenode.checkpoint.dir</name>
    <value>/data/hadoop/data</value>
    <description>datanode临时文件所存放的目录</description>
  </property>
  <property>
    <name>dfs.namenode.http-address</name>
    <value>slave1:9870</value>
    <description>hdfs web 地址</description>
  </property>
  <property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>slave1:50090</value>
  </property>
</configuration>
```

- mapred-site.xml 配置

```
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
    <description>告诉hadoop以后MR(Map/Reduce)运行在YARN上</description>
  </property>
  <property>
    <name>mapreduce.admin.user.env</name>
    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    <description>可以设置AM【AppMaster】端的环境变量，如果上面缺少配置，可能会造成mapreduce失败</description>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    <description>可以设置AM【AppMaster】端的环境变量，如果上面缺少配置，可能会造成mapreduce失败</description>
  </property>
</configuration>
```

- yarn-site.xml 配置

```
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
    <description>nomenodeManager获取数据的方式是shuffle</description>
  </property>
  <property>
    <name>yarn.resourcemanager.webapp.address</name>
    <value>slave1:8088</value>
    <description>配置 yarn 外部可访问，(外网IP:端口)</description>
  </property>
  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    <description>容器可能会覆盖的环境变量，而不是使用NodeManager的默认值</description>
  </property>
  <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>slave1</value>
  </property>
  <property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
    <description>关闭内存检测，虚拟机需要，不配会报错</description>
  </property>
</configuration>
```

- workers 配置

```
# etc/hadoop/workers
slave1
slave2
slave3
```

### 2.4. 客户端

- 配置主机
  - hostname
  - 环境变量
  - ssh 免密登录

- 安装

> 参考单机安装

- 目录

```shell
# 创建目录
mkdir /data/hadoop
mkdir /data/hadoop/name #namenode 存放目录
mkdir /data/hadoop/secondary #secondarynamenode 存放目录
mkdir /data/hadoop/data #datanode 数据存放目录
mkdir /data/hadoop/tmp #临时数据
mkdir /data/hadoop/log #日志数据
```

- hadoop-env.sh 配置

```
export HDFS_NAMENODE_USER="root"
export HDFS_DATANODE_USER="root"
export HDFS_SECONDARYNAMENODE_USER="root"
export YARN_RESOURCEMANAGER_USER="root"
export YARN_NODEMANAGER_USER="root"
export JAVA_HOME=/opt/software/jdk1.8.0_351
export HADOOP_LOG_DIR=/data/hadoop/log
```

- core-site.xml 配置

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://slave1:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/data/hadoop/tmp</value>
   </property>
</configuration>
```

- hdfs-site.xml 配置

```
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>2</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/data/hadoop/name</value>
    <description>namenode临时文件所存放的目录</description>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/data/hadoop/secondary</value>
    <description>secondarynamenode临时文件所存放的目录</description>
  </property>
  <property>
    <name>dfs.namenode.checkpoint.dir</name>
    <value>/data/hadoop/data</value>
    <description>datanode临时文件所存放的目录</description>
  </property>
  <property>
    <name>dfs.namenode.http-address</name>
    <value>slave1:9870</value>
    <description>hdfs web 地址</description>
  </property>
  <property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>slave1:50090</value>
  </property>
</configuration>
```

- mapred-site.xml 配置

```
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
    <description>告诉hadoop以后MR(Map/Reduce)运行在YARN上</description>
  </property>
  <property>
    <name>mapreduce.admin.user.env</name>
    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    <description>可以设置AM【AppMaster】端的环境变量，如果上面缺少配置，可能会造成mapreduce失败</description>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    <description>可以设置AM【AppMaster】端的环境变量，如果上面缺少配置，可能会造成mapreduce失败</description>
  </property>
</configuration>
```

- yarn-site.xml 配置

```
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
    <description>nomenodeManager获取数据的方式是shuffle</description>
  </property>
  <property>
    <name>yarn.resourcemanager.webapp.address</name>
    <value>slave1:8088</value>
    <description>配置 yarn 外部可访问，(外网IP:端口)</description>
  </property>
  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    <description>容器可能会覆盖的环境变量，而不是使用NodeManager的默认值</description>
  </property>
  <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>slave1</value>
  </property>
  <property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
    <description>关闭内存检测，虚拟机需要，不配会报错</description>
  </property>
  <property>
    <name>yarn.application.classpath</name>
    <value>
    /opt/software/hadoop-3.3.6/etc/hadoop,
    /opt/software/hadoop-3.3.6/share/hadoop/common/*,
    /opt/software/hadoop-3.3.6/share/hadoop/common/lib/*,
    /opt/software/hadoop-3.3.6/share/hadoop/hdfs/*,
    /opt/software/hadoop-3.3.6/share/hadoop/hdfs/lib/*,
    /opt/software/hadoop-3.3.6/share/hadoop/mapreduce/*,
    /opt/software/hadoop-3.3.6/share/hadoop/mapreduce/lib/*,
    /opt/software/hadoop-3.3.6/share/hadoop/yarn/*,
    /opt/software/hadoop-3.3.6/share/hadoop/yarn/lib/*
    </value>
    <description>添加依赖</description>
  </property>
</configuration>
```

## 3. 使用

- 单机测试

```shell
cd /opt/software/hadoop-3.3.6
mkdir input
cp /etc/protocols ./input
hadoop jar /opt/software/hadoop-3.3.6/share/hadoop/mapreduce/sources/hadoop-mapreduce-examples-3.3.6-sources.jar org.apache.hadoop.examples.WordCount input output
```

- 伪分布式测试

```shell
hdfs namenode -format #格式化 hdfs 重新格式化需要删除/data/hadoop/tmp
start-all.sh # 启动集群
start-dfs.sh
start-yarn.sh
stop-all.sh 
jps #验证集群信息
curl http://wsl:9870 #HDFS 界面
curl http://wsl:8088 #YARN 界面 
```

- 分布式测试

```shell
hdfs namenode -format #格式化 hdfs 重新格式化需要删除/data/hadoop/tmp
start-all.sh # 启动集群
start-dfs.sh
start-yarn.sh
stop-all.sh 
jps #验证集群信息
curl http://slave1:9870 #HDFS 界面
curl http://slave1:8088 #YARN 界面 
```

- 客户端测试

```shell
hdfs dfs -rm -r /output #删除目录
hdfs dfs -mkdir /input #上传文件
hdfs dfs -put /input/hadoop-env.sh / #上传文件
hdfs dfs -ls /input #查看文件
hadoop jar /opt/software/hadoop-3.3.6/share/hadoop/mapreduce/sources/hadoop-mapreduce-examples-3.3.6-sources.jar org.apache.hadoop.examples.WordCount /input /output
```

- systemd

```shell
[Unit]
Description=Hadoop Service
After=network.target

[Service]
Type=forking
Environment=HADOOP_HOME=/opt/software/hadoop-3.3.6
Environment=JAVA_HOME=/opt/software/jdk1.8.0_351
Environment=HADOOP_CONF_DIR=/opt/software/hadoop-3.3.6/etc/pseudo_hadoop
ExecStart=/opt/software/hadoop-3.3.6/sbin/start-all.sh
ExecStop=/opt/software/hadoop-3.3.6/sbin/stop-all.sh
Restart=on-failure
RestartSec=5
RemainAfterExit=yes # 注意该选项必须设置为 true

[Install]
WantedBy=multi-user.target 
```

- 服务端  
...

- 客户端  
...

## 4. 拓展信息

## 5. 参考资料

- [官方链接](https://hadoop.apache.org/)
- [core-size.xml](https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-common/core-default.xml)
- [hdfs-size.xml](https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml)
- [mapred-site.xml](https://hadoop.apache.org/docs/r2.7.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml)
- [yarn-site.xml](https://hadoop.apache.org/docs/r2.7.3/hadoop-yarn/hadoop-yarn-common/yarn-default.xml)
