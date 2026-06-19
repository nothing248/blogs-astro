---
title: "Logstash"
status: pending
filename: logstash-data-collection-pipeline
aliases: [Logstash, 日志收集]
tags: [大数据, ELK, 日志处理, 数据流水线, Logstash]
date created: 星期三, 十二月 10日 2025, 6:20:41 晚上
date modified: 星期四, 六月 18日 2026, 10:25:00 晚上
---

<!-- toc -->

## 1. 待完善：Logstash 数据收集引擎

本笔记旨在记录 Elastic Stack (ELK) 中的数据收集与过滤组件 Logstash。目前仅包含基础的二进制包下载命令。后续需补充其 Input（输入）、Filter（过滤清洗，如 Grok 正则）及 Output（输出至 ES/Kafka）的核心配置。

```bash
# 基础下载指令
wget https://artifacts.elastic.co/downloads/logstash/logstash-8.17.3-linux-x86_64.tar.gz
tar -zxvf logstash-8.17.3-linux-x86_64.tar.gz
```
