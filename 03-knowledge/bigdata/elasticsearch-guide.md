---
title: "ES教程"
filename: elasticsearch-guide
description: 介绍基于 Lucene 的分布式搜索引擎 Elasticsearch (ES)。详解倒排索引（词典与倒排文件）、主副分片恢复、节点发现机制及集群读写流程。提供了在 Linux 环境下的下载、Ik 分词插件安装、系统虚拟内存调优、elasticsearch.yml 详细参数设置及 systemd 服务管理配置。此外，还汇总了索引映射配置与文档的 RESTful API 基础及高级 DSL 操作。
tags:
  - Elasticsearch
  - 倒排索引
  - 搜索引擎
  - 分片机制
  - 运维调优
aliases:
  - ES教程
  - 全文搜索原理
  - 倒排表与词典
  - ES运维手册
status: completed
date created: 星期三, 十二月 10日 2025, 6:20:40 晚上
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

一个 JAVA 编写的基于 Lucene 的搜索引擎(封装 Lucene 的复杂性、提供 RESTful API 操作)。支持分布式部署，

## 2. 原理

### 2.1. 概念

- 集群
- 节点
- 索引
- 文档
- 分片
- 主分片
- 副本分片
- 分片恢复
- 索引缓冲区
- 传输模块
- 网关模块
- 节点发现模块
- 线程池

### 2.2. 存储结构

![](http://qiniu.sxyxy.top/20240118110614.png?image=image)

- 词条（Term）： 索引里面最小的存储 and 查询单元，对于英文来说是一个单词，对于中文来说一般指分词后的一个词。
- 词典（Term Dictionary）： 或字典，是词条 Term 的集合。搜索引擎的通常索引单位是单词，单词词典是由文档集合中出现过的所有单词构成的字符串集合，单词词典内每条索引项记载单词本身的一些信息以及指向“倒排列表”的指针。
- 倒排表（Post list）： 一个文档通常由多个词组成，倒排表记录的是某个词在哪些文档里出现过以及出现的位置。每条记录称为一个倒排项（Posting）。倒排表记录的不单是文档编号，还存储了词频等信息。
- 倒排文件（Inverted File）： 所有单词的倒排列表往往顺序地存储在磁盘的某个文件里，这个文件被称之为倒排文件，倒排文件是存储倒排索引的物理文件。

> 核心数据结构为词典于倒排文件。词典存储在内存中、到虚表存储在磁盘上

### 2.3. 集群

- 发现机制  
Zen Discovery(内置的默认发现模块)
  - 初始化  
    - 初始化投票配置
    - 选举主节点
    - 发现其他节点
    - 启动完毕
  - 更新
    - 预提交阶段
    - 正式提交
  - 心跳维护

  > 确保主候选节点一半以上正常

- 存储机制  
  - 分片
    - 分配
      - 感知(逻辑区域划分)
      - 过滤
    - 恢复
      - 本地存储恢复
      - 对等恢复
      - 快照恢复

    > 可以设置延迟恢复、或者设置条件恢复

  - 写入

  > 先主分片、副本分片、返回请求结果

- 查询机制
  - 查询
    - 携带路由
    - 不携带路由

  > 主分片和副本分片都可以

## 3. 安装

### 3.1. 下载

- es 安装

```shell
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.17.3-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.17.3-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-8.17.3-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-8.17.3-linux-x86_64.tar.gz
cd elasticsearch-8.17.3/ 
```

- ES-head 管理界面

```shell
# 可选
git clone git://github.com/mobz/elasticsearch-head.git
cd elasticsearch-head
npm install
npm run start
```

- 分词插件

```shell
.\bin\elasticsearch-plugin.bat install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.12.1/elasticsearch-analysis-ik-7.12.1.zip
```

> 可选，并且命令用于按爪个插件

## 4. 配置

- elasticsearch.yml ES 配置文件

```yaml
#配置 ES 的集群名称，默认值是 ES，建议改成与所存数据相关的名称，ES 会自动发现在同一网段下的集群名称相同的节点。
cluster.name：elasticsearch

#集群中的节点名，在同一个集群中不能重复。节点的名称一旦设置，就不能再改变了。当然，也可以设置成服务器的主机名称，例如 node.name:${HOSTNAME}。
node.nam： "node1"

#指定该节点是否有资格被选举成为 Master 节点，默认是 True，如果被设置为 True，则只是有资格成为 Master 节点，具体能否成为 Master 节点，需要通过选举产生。
noed.master：true

#指定该节点是否存储索引数据，默认为 True。数据的增、删、改、查都是在 Data 节点完成的。
node.data：true

#设置都索引分片个数，默认是 5 片。也可以在创建索引时设置该值，具体设置为多大都值要根据数据量的大小来定。如果数据量不大，则设置成 1 时效率最高。
index.number_of_shards：5

#设置默认的索引副本个数，默认为 1 个。副本数越多，集群的可用性越好，但是写索引时需要同步的数据越多。
index.number_of_replicas：1

#设置配置文件的存储路径，默认是 ES 目录下的 Conf 文件夹。建议使用默认值。
path.conf：/path/to/conf

#设置索引数据多存储路径，默认是 ES 根目录下的 Data 文件夹。切记不要使用默认值，因为若 ES 进行了升级，则有可能数据全部丢失。 可以用半角逗号隔开设置的多个存储路径，在多硬盘的服务器上设置多个存储路径是很有必要的。
path.data：/path/to/data1,/path/to/data2

#设置日志文件的存储路径，默认是 ES 根目录下的 Logs，建议修改到其他地方。
path.logs：/path/to/logs

#设置第三方插件的存放路径，默认是 ES 根目录下的 Plugins 文件夹。
path.plugins：/path/to/plugins

#设置为 True 时可锁住内存。因为当 JVM 开始 Swap 时，ES 的效率会降低，所以要保证它不 Swap。
bootstrap.mlockall：true

#设置本节点绑定的 IP 地址，IP 地址类型是 IPv4 或 IPv6，默认为 0.0.0.0。
network.bind_host：192.168.0.1

#设置其他节点和该节点交互的 IP 地址，如果不设置，则会进行自我判断。
network.publish_host：192.168.0.1

#用于同时设置 bind_host 和 publish_host 这两个参数。
network.host：192.168.0.1

#设置对外服务的 HTTP 端口，默认为 9200。ES 的节点需要配置两个端口号，一个对外提供服务的端口号，一个是集群内部使用的端口号。 http.port 设置的是对外提供服务的端口号。注意，如果在一个服务器上配置多个节点，则切记对端口号进行区分。
http.port：9200

#设置集群内部的节点间交互的 TCP 端口，默认是 9300。注意，如果在一个服务器配置多个节点，则切记对端口号进行区分。
transport.tcp.port：9300

#设置在节点间传输数据时是否压缩，默认为 False，不压缩。
transport.tcp.compress：true

#设置在选举 Master 节点时需要参与的最少的候选主节点数，默认为 1。如果使用默认值，则当网络不稳定时有可能会出现脑裂。 合理的数值为(master_eligible_nodes/2)+1，其中 master_eligible_nodes 表示集群中的候选主节点数。
discovery.zen.minimum_master_nodes：1

#设置在集群中自动发现其他节点时 Ping 连接的超时时间，默认为 3 秒。 在较差的网络环境下需要设置得大一点，防止因误判该节点的存活状态而导致分片的转移。
discovery.zen.ping.timeout：3s

xpack.security.enabled: false
xpack.security.enrollment.enabled: false
# Enable encryption for HTTP API client connections, such as Kibana, Logstash, and Agents
xpack.security.http.ssl:
 enabled: false
 #keystore.path: certs/http.p12
# Enable encryption and mutual authentication between cluster nodes
xpack.security.transport.ssl:
 enabled: false
    #verification_mode: certificate
 #keystore.path: certs/transport.p12
 #truststore.path: certs/transport.p12
```

> 初次启动不要配置 xpack 相关的配置, 会自动生成 config/certs 证书文件与配置信息

- log4j2.properties 日志配置文件

> 配置方式 API 临时生效 - API 永久生效 - 配置文件

- 配置密码

```shell
elasticsearch-setup-passwords interactive #首次启动
elasticsearch-reset-password -u kibana_system -i #重设内置用户 elastic 的密码 #kibana_system/elastic
curl -X GET "https://localhost:9200" -u elastic:43cba8QKqjuDV1CWD6bS --insecure
```

> elasticsearch-setup-passwords 不可用参考: <https://blog.csdn.net/lhrm0213/article/details/122468588>

- 环境变量

```shell
# elasticsearch
export ELASTICSEARCH_HOME=/opt/software/elasticsearch-8.17.3
export PATH=$ELASTICSEARCH_HOME/bin:$PATH
```

- 启动

```shell
.\bin\elasticsearch -d #后端运行
```

> 注意：es 不允许以 root 用户进行启动。

## 5. 管理

- systemd 配置

```
# /etc/systemd/system/elasticsearch.service
[Unit]
Description=Elasticsearch
After=network.target

[Service]
Type=forking
User=elastic
Group=elastic
WorkingDirectory=/opt/software/elasticsearch-8.17.3
ExecStart=/opt/software/elasticsearch-8.17.3/bin/elasticsearch -d
PrivateTmp=true
Restart=on-failure
LimitMEMLOCK=infinity
LimitNOFILE=65535
LimitNPROC=65535

[Install]
WantedBy=multi-user.target
```

- 管理命令

```shell
systemctl start elasticsearch
systemctl stop elasticsearch
systemctl restart elasticsearch
systemctl status elasticsearch
```

## 6. 使用

### 6.1. 映射

- 创建

```text
PUT mysougoulog
{
  "settings": {
    "number_of_shards": "5", #5个主分片，创建之后不可以修改
    "number_of_replicas": "1" #1个副本分片
  },
  "mappings": {
    "properties": {
      "userid": {
        "type": "text"
      }
    }
  }
}
```

- 修改配置

```text
PUT mysougoulog/_settings
{
  "settings": {
    "number_of_replicas": "2"
  }
}
```

- 查看

```text
GET mysougoulog/_mapping
```

- 修改

```text
PUT ignore-test
{
  "mappings": {
    "properties": {
      "age": {
        "type": "integer"
      },
      "born": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss",
        "ignore_malformed": true #汇率非法数据
      }
    }
  }
}
```

- 复制

```text
可以实现一个字段查询多个字段的效果
PUT copy-field
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "copy_to": "full_text"
      },
      "author": {
        "type": "text",
        "copy_to": "full_text"
      },
      "abstract": {
        "type": "text",
        "copy_to": "full_text"
      },
      "full_text": {
        "type": "text"
      }
    }
  }
}
```

> 1.支持的数据类型  
> ![](http://qiniu.sxyxy.top/20240122100931.png?image=image)
>
> - 文本类型: 默认会被分词
> - 关键字类型: 保存不经分析、处理的原始文本。一般用于精准查询
> - 对象类型
> - 数组类型
> - 二进制文件类型
>
> 1. 支持动态扩展的数据类型
> ![](http://qiniu.sxyxy.top/20240122152557.png?image=image)

### 6.2. 数据

- 查看集群节点

```shell
curl -X GET 'http://localhost:9200/_cat/nodes?v'
```

- 查看搜索索引

```shell
curl -X GET 'http://localhost:9200/_cat/indices?v'
```

- 新增索引

```text
PUT test-3-2-1
{
  "mappings": {
    "properties": {
      "id": {
        "type": "integer"
      },
      "sex": {
        "type": "boolean"
      },
      "name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "born": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "location": {
        "type": "geo_point"
      }
    }
  }
}
```

- 新增 doc

```text
POST test-3-2-1/_doc/1
{
  "id": "1",
  "sex": true,
  "name": "张三",
  "born": "2020-09-18 00:02:20",
  "location": {
    "lat": 41.12,
    "lon": -71.34
  }
}
```

> 1 代表主键(存在则覆盖、不存在默认创建，元数据_id 中)；_doc 代表索引类型

- 查

```text
GET test-3-2-1/_doc/1
```

- 改

```text
POST test-3-2-1/_update/1
{
  "doc": {
    "sex": false,
    "born": "2020-02-24 00:02:20"
  }
}
```

- 删

```text
DELETE test-3-2-1/_doc/1
```

- 查看某一个 doc

```shell
curl 'localhost:9200/accounts/1?pretty=true'
```

- 查看所有的 doc

```shell
curl http://localhost:9200/account/_search?size=1
```

### 6.3. 高级

- 并发控制(乐观锁)

## 7. 拓展信息

### 7.1. OLAP

Online Analytics Processing

### 7.2. 数据搜索

- 结构化数据
  - 直接使用现有的工具、例如 mysql 等
- 非结构化数据
  - 顺序扫描
  - 全文搜索

### 7.3. 虚拟内存限制过低

```shell
# max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

echo "vm.max_map_count=262144" >> /etc/sysctl.conf
sysctl -p
sysctl -a | grep vm.max_map_count
```

## 8. 参考资料

- [官方链接](https://www.elastic.co/cn/)
- [官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)
- [Lucene 开源的全文检索引擎工具包](https://lucene.apache.org/)，有支持的 python 版本 pyLucene
- [Kibana 实 ES 设计的开源的可视化分析平台](https://www.elastic.co/cn/kibana?utm_campaign=Google-B-RoAPJ-SG-Exact&utm_content=Brand-Core-Kibana&utm_source=google&utm_medium=cpc&device=c&utm_term=kibana&gad_source=1&gclid=Cj0KCQiAnrOtBhDIARIsAFsSe51mnSV6PdXEMYMh_6Ka8zFJ2ogekeeO7L5r1RWp6485fr1FikYzcgkaAmL0EALw_wcB)
- [Logstash 开源的实时流水线数据收集引擎](https://www.elastic.co/cn/logstash)
- [三方参考资料](https://segmentfault.com/a/1190000023080158)
