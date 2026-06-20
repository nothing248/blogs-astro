---
title: "Oxylabs代理"
filename: oxylabs-proxy-service-setup
description: Oxylabs作为企业级代理和数据采集方案提供商，支持庞大的住宅与数据中心代理。主要用于网页爬虫与地理位置模拟。通过cURL可配置国家代码及账号凭证以进行出口IP测试，返回地理位置、ASN运营商等结构化JSON数据，是企业级高防网络采集的成熟方案。
tags: [oxylabs, proxy-servers, web-scraping]
aliases: [Oxylabs代理, 住宅代理, 数据中心代理]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:29 上午
date modified: 星期五, 六月 19日 2026, 12:07:19 中午
---

<!-- toc -->

## 1. 简介

一个专门做的 ip 代理的服务商

## 2. 费用

![](http://qiniu.sxyxy.top/20250813114859.png)

## 3. 使用

```
curl 'https://ip.oxylabs.io/location' -U 'user-proxy_g8LvU-country-US:example' -x 'dc.oxylabs.io:8000'

{"ip":"93.115.200.156","providers":{"dbip":{"country":"US","asn":"AS203020","org_name":"HostRoyale Technologies Pvt Ltd","city":"Chicago","zip_code":"","time_zone":"","meta":"\u003ca href='https://db-ip.com'\u003eIP Geolocation by DB-IP\u003c/a\u003e"},"ip2location":{"country":"US","asn":"","org_name":"","city":"San Francisco","zip_code":"94199","time_zone":"-07:00","meta":"This site or product includes IP2Location LITE data available from \u003ca href=\"https://lite.ip2location.com\"\u003ehttps://lite.ip2location.com\u003c/a\u003e."},"ipinfo":{"country":"US","asn":"AS203020","org_name":"HostRoyale Technologies Pvt Ltd","city":"","zip_code":"","time_zone":"","meta":"\u003cp\u003eIP address data powered by \u003ca href=\"https://ipinfo.io\" \u003eIPinfo\u003c/a\u003e\u003c/p\u003e"},"maxmind":{"country":"US","asn":"AS203020","org_name":"HostRoyale Technologies Pvt Ltd","city":"San Francisco","zip_code":"","time_zone":"-07:00","meta":"This product includes GeoLite2 Data created by MaxMind, available from https://www.maxmind.com."}}
```

## 4. 拓展信息

- 支持 5 个免费的数据中心代理

## 5. 参考资料

- [官方文档](https://developers.oxylabs.io/documentation/cn/dai-li/zhu-zhai-dai-li-1)
- [官方链接](https://dashboard.oxylabs.io/)
