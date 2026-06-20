---
title: "Aliyun CLI"
filename: aliyun-cli-swas-guide
description: 介绍阿里云命令行工具（Aliyun CLI）在 MacOS 下的安装与配置流程，重点阐述了通过安装 `swas-open` 插件来管理阿里云轻量应用服务器（SWAS）实例的命令行操作。包括查询可用地域、创建实例、获取实例列表等实用命令，并附带了全球主要地域的 Endpoint 信息及官方 API 参考指南。
tags:
  - 阿里云
  - 命令行工具
  - 轻量应用服务器
  - 实例管理
  - 自动化运维
aliases:
  - Aliyun CLI
  - 阿里云命令行
  - 阿里云SWAS命令
status: completed
date created: 星期一, 五月 4日 2026, 3:30:19 下午
date modified: 星期二, 六月 16日 2026, 6:24:25 晚上
---

<!-- toc -->

## 1. 简介

Aliyun 平台的命令行工具

## 2. 按照

### 2.1. MacOS

```bash
brew install aliyun-cli
```

## 3. 使用

### 3.1. 配置

```bash
aliyun configure [--profile <PROFILE_NAME>] [--mode <AUTHENTICATE_MODE>]
```

### 3.2. 轻量级服务器

- 安装插件

```
aliyun plugin install --names aliyun-cli-swas-open
aliyun help swas-open
```

- 获取资源

```bash
aliyun swas-open list-regions --region-id cn-hangzhou
```

- 创建

```bash
aliyun swas-open create-instances \  
--region ap-northeast-1 \  
--biz-region-id ap-northeast-1 \  
--image-id e9363571cf2444aba422b17470285465 \  
--plan-id swas.s.c2m05s20b1.linux \  
--period 1 \  
--instance-name "test" \  
--auto-renew false
```

> 一定要带 `--region` ，否则会制定的区域无效。image-id 与 plan-id 在各个区域都是一致的

- 获取实例

```bash
aliyun swas-open list-instances \
    --region cn-hangzhou \
    --biz-region-id ap-northeast-1 \
    --page-size 10 \
    --page-number 1
```

- 取消订阅

> 无该 CLI

- 地域信息

```json
{
        "Regions": [
                {
                        "LocalName": "华北1（青岛）",
                        "RegionEndpoint": "swas.cn-qingdao.aliyuncs.com",
                        "RegionId": "cn-qingdao"
                },
                {
                        "LocalName": "华北2（北京）",
                        "RegionEndpoint": "swas.cn-beijing.aliyuncs.com",
                        "RegionId": "cn-beijing"
                },
                {
                        "LocalName": "华北3（张家口）",
                        "RegionEndpoint": "swas.cn-zhangjiakou.aliyuncs.com",
                        "RegionId": "cn-zhangjiakou"
                },
                {
                        "LocalName": "华北5（呼和浩特）",
                        "RegionEndpoint": "swas.cn-huhehaote.aliyuncs.com",
                        "RegionId": "cn-huhehaote"
                },
                {
                        "LocalName": "华东1（杭州）",
                        "RegionEndpoint": "swas.cn-hangzhou.aliyuncs.com",
                        "RegionId": "cn-hangzhou"
                },
                {
                        "LocalName": "华东2（上海）",
                        "RegionEndpoint": "swas.cn-shanghai.aliyuncs.com",
                        "RegionId": "cn-shanghai"
                },
                {
                        "LocalName": "华南1（深圳）",
                        "RegionEndpoint": "swas.cn-shenzhen.aliyuncs.com",
                        "RegionId": "cn-shenzhen"
                },
                {
                        "LocalName": "华南2（河源）",
                        "RegionEndpoint": "swas.cn-heyuan.aliyuncs.com",
                        "RegionId": "cn-heyuan"
                },
                {
                        "LocalName": "西南1（成都）",
                        "RegionEndpoint": "swas.cn-chengdu.aliyuncs.com",
                        "RegionId": "cn-chengdu"
                },
                {
                        "LocalName": "华南3（广州）",
                        "RegionEndpoint": "swas.cn-guangzhou.aliyuncs.com",
                        "RegionId": "cn-guangzhou"
                },
                {
                        "LocalName": "华北6（乌兰察布）",
                        "RegionEndpoint": "swas.cn-wulanchabu.aliyuncs.com",
                        "RegionId": "cn-wulanchabu"
                },
                {
                        "LocalName": "华东5 （南京）关停中",
                        "RegionEndpoint": "swas.cn-nanjing.aliyuncs.com",
                        "RegionId": "cn-nanjing"
                },
                {
                        "LocalName": "华东6（福州）关停中",
                        "RegionEndpoint": "swas.cn-fuzhou.aliyuncs.com",
                        "RegionId": "cn-fuzhou"
                },
                {
                        "LocalName": "华中1（武汉）",
                        "RegionEndpoint": "swas.cn-wuhan-lr.aliyuncs.com",
                        "RegionId": "cn-wuhan-lr"
                },
                {
                        "LocalName": "中国香港",
                        "RegionEndpoint": "swas.cn-hongkong.aliyuncs.com",
                        "RegionId": "cn-hongkong"
                },
                {
                        "LocalName": "新加坡",
                        "RegionEndpoint": "swas.ap-southeast-1.aliyuncs.com",
                        "RegionId": "ap-southeast-1"
                },
                {
                        "LocalName": "马来西亚（吉隆坡）",
                        "RegionEndpoint": "swas.ap-southeast-3.aliyuncs.com",
                        "RegionId": "ap-southeast-3"
                },
                {
                        "LocalName": "印度尼西亚（雅加达）",
                        "RegionEndpoint": "swas.ap-southeast-5.aliyuncs.com",
                        "RegionId": "ap-southeast-5"
                },
                {
                        "LocalName": "日本（东京）",
                        "RegionEndpoint": "swas.ap-northeast-1.aliyuncs.com",
                        "RegionId": "ap-northeast-1"
                },
                {
                        "LocalName": "美国（硅谷）",
                        "RegionEndpoint": "swas.us-west-1.aliyuncs.com",
                        "RegionId": "us-west-1"
                },
                {
                        "LocalName": "美国（弗吉尼亚）",
                        "RegionEndpoint": "swas.us-east-1.aliyuncs.com",
                        "RegionId": "us-east-1"
                },
                {
                        "LocalName": "德国（法兰克福）",
                        "RegionEndpoint": "swas.eu-central-1.aliyuncs.com",
                        "RegionId": "eu-central-1"
                },
                {
                        "LocalName": "英国（伦敦）",
                        "RegionEndpoint": "swas.eu-west-1.aliyuncs.com",
                        "RegionId": "eu-west-1"
                },
                {
                        "LocalName": "菲律宾（马尼拉）",
                        "RegionEndpoint": "swas.ap-southeast-6.aliyuncs.com",
                        "RegionId": "ap-southeast-6"
                },
                {
                        "LocalName": "泰国（曼谷）",
                        "RegionEndpoint": "swas.ap-southeast-7.aliyuncs.com",
                        "RegionId": "ap-southeast-7"
                },
                {
                        "LocalName": "韩国（首尔）",
                        "RegionEndpoint": "swas.ap-northeast-2.aliyuncs.com",
                        "RegionId": "ap-northeast-2"
                }
        ]
}
```

## 4. 参考资料

- [官方文档](https://help.aliyun.com/zh/cli/cloud-products-supporting-cli?spm=a2c4g.11186623.help-menu-29991.d_1_0.4c42ad1eIrAShX)
- [轻量级服务器 API 文档](https://api.aliyun.com/document/SWAS-OPEN/2020-06-01/CreateInstances)
