---
title: "GoogleTrends数据采集"
filename: google-trends-scraping-guide
description: 详细整理了自建 Google Trends (谷歌趋势) 数据抓取的两种技术方案：通过分析 embed widget API 的 NID 鉴权及 Token 签名进行间接模拟抓取，以及在 Python 中利用 pytrends 第三方封装库进行核心指标请求与代理防封锁的最佳实践，以解决自建爬虫频发的 HTTP 429 访问限制。
tags:
  - google-trends
  - pytrends
  - web-scraping
  - python-crawler
aliases:
  - GoogleTrends数据采集
  - pytrends库使用
  - 谷歌趋势API抓取
status: completed
date created: 星期日, 十二月 21日 2025, 11:05:26 上午
date modified: 星期五, 六月 19日 2026, 10:50:00 上午
---

<!-- toc -->

## 1. 直接模式

直接解析 Google 内部调用结构，并进行模拟。

### 1.1. 一、配置文件

```python
# gtparas.py
tokenurl = "https://trends.google.com/trends/api/explore"
tsurl = "https://trends.google.com/trends/api/widgetdata/multiline"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "trends.google.com",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

cookies = {
    "AEC": "[Cookie已隐藏]",
    # "CONSENT": "PENDING+772",
    "SOCS": "[Cookie已隐藏]",
    "NID": "[Cookie已隐藏]",
    "__utmc": "10102256",
    "__utmt": "1",
    "__utma": "10102256.1794775742.1743474273.1743474290.1743489354.3",
    "__utmb": "10102256.3.10.1743489354",
    "__utmz": "10102256.1743474273.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "x-client-data": "CJK2yQEIorbJAQipncoBCNGgygEI7ZLLAQiTocsBCIWgzQEIusjNAQj+pc4BCMjRzgEIvNXOAQiu5M4BGJznzgE=",
}
```

### 1.2. 二、主代码

```python
import time
import requests
import json
import gtparas


def getoken(kw_list, daterange):
    token_payload = {
        "hl": "en-US",
        "tz": -480,
        "req": {"comparisonItem": [], "category": 0, "property": ""},
    }

    for kw in kw_list:
        keyword_payload = {"keyword": kw.lower(), "geo": "", "time": daterange}
        token_payload["req"]["comparisonItem"].append(keyword_payload)
    token_payload["req"] = json.dumps(token_payload["req"])

    con = requests.post(
        gtparas.tokenurl,
        headers=gtparas.headers,
        cookies=gtparas.cookies,
        params=token_payload,
    )

    # print(con.text)

    widgets = json.loads(con.text[5:])["widgets"]
    print("*************")
    print(widgets)
    print("*************")
    reqparas = recordtokens(widgets)
    return reqparas


def recordtokens(widgets):
    reqparas = ""
    with open("toknes.txt", "a") as f:
        for widget in widgets:
            if "token" in widget.keys() and "request" in widget.keys():
                del widget["helpDialog"]
                f.write(str(widget) + ",\n")
            if widget["id"] == "TIMESERIES":
                reqparas = widget
    return reqparas


def fetchdata(kw_list, daterange):
    reqparas = getoken(kw_list, daterange)
    time.sleep(3)
    params = {
        "hl": "en-US",
        "tz": -480,
        "req": json.dumps(reqparas["request"]),
        "token": reqparas["token"],
    }

    con = requests.get(
        gtparas.tsurl, headers=gtparas.headers, cookies=gtparas.cookies, params=params
    )

    req_json = json.loads(con.text[5:])

    return req_json


if __name__ == "__main__":
    kw_list = ["Blockchain"]
    daterange = "2020-01-01 2020-12-31"
    req_json = fetchdata(kw_list, daterange)
    print(req_json)
```

- **效果分析**
  
  ![](http://qiniu.sxyxy.top/20250811111358.png)

> [!WARNING]
> 存在数据不一致的问题。

## 2. 间接模式

间接解析 embed 组件的 API 结构，并进行模拟。

### 2.1. 一、获取请求参数信息

通过浏览器网络抓包获取 embed API 发出的请求：

```shell
curl https://trends.google.com/trends/embed/explore/TIMESERIES?req={"comparisonItem":[{"keyword":"Honor","geo":""}],"category":0,"property":""}&tz=-480
```

### 2.2. 二、获取数据

使用模拟的 GET 请求爬取具体趋势数据：

```shell
wget --no-check-certificate --quiet \
  --method GET \
  --timeout=0 \
  --header 'Cookie: NID=[Cookie已隐藏]' \
   'https://trends.google.com/trends/api/widgetdata/multiline?req={"time": "2020-01-01 2020-12-31", "resolution": "WEEK", "locale": "en-US",
     "comparisonItem": [
         {
             "geo": {},
             "complexKeywordsRestriction": {
                 "keyword": [
                     {
                         "type": "BROAD",
                         "value": "Honor"
                     }
                 ]
             }
         }
     ],
     "requestOptions": {
         "property": "",
         "backend": "IZG",
         "category": 0
     },

     "userConfig": {
         "userType": "USER_TYPE_EMBED_OVER_QUOTA"
     }
 }&token=APP6_UEAAAAAaJquYECS38PTX_E0JsPqsLVcn7TBjkNv&tz=-480'
```

> [!TIP]
> 注意：可以解析 **获取请求参数信息 API** 的 Cookie 信息 (NID)，并在 **获取数据** 时进行携带。

---

## 3. 最佳替代实践：使用 PyTrends 第三方库

对于大规模的 Google Trends 数据抓取，在 Python 环境中推荐使用成熟的第三方封装库 `pytrends`，它已封装好底层的 Cookie 交互及 Token 获取逻辑：

### 3.1. 核心代码示例

```python
from pytrends.request import TrendReq

# 初始化请求对象，可设置语言 (hl) 与时区偏移 (tz)
pytrends = TrendReq(hl='en-US', tz=360)

# 构建搜索载荷 (关键字列表、分类及时间跨度)
kw_list = ["Blockchain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

# 1. 获取随时间变化的兴趣度数据
interest_over_time_df = pytrends.interest_over_time()
print(interest_over_time_df.head())

# 2. 获取地区层面的兴趣度分布
interest_by_region_df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
print(interest_by_region_df.head(10))
```

### 3.2. 爬虫防限流与代理设置

由于 Google Trends API 严格限制高频请求（常返回 `HTTP 429 Too Many Requests`），强烈建议配置代理池以避免 IP 被封锁：

```python
# 初始化时绑定代理服务器
pytrends = TrendReq(hl='en-US', tz=360, proxies=['https://127.0.0.1:7890'])
```

## 4. 高频抓取工程化防限流建议 (Anti-Scraping Strategy)

> [!warning]
> Google Trends API 的风控机制极度严格。在企业级高频抓取场景中，除代理 IP 轮载外，还必须配合执行以下防御策略：
>
> 1. **请求退避设计 (Backoff Retry)**：当检测到 HTTP 状态码为 429 时，必须自动执行指数级退避（Exponential Backoff）重试。首次等待 5 秒，之后翻倍，直至等待 60 秒。这不仅能保护 IP 权重，还能确保整个抓取流水线的长效高可用。
> 2. **请求抖动引入 (Jitter)**：在不同关键词抓取请求的间隔期中，切忌使用固定休眠（如 `time.sleep(3)`）。推荐引入 `-1.5` 到 `+1.5` 秒的随机波动时间戳扰动（Jitter），模拟真人用户的访问行为。
> 3. **会话持久化与状态更新**：NID Cookie 的生命周期非常短暂，需要定期利用 `TrendReq` 或 `requests.Session` 自动检测并刷新。当 Cookie 失效时，流水线必须能够自动抛出警示并阻塞，防止向接口发送大量无 Cookie 鉴权的垃圾请求。

## 5. 参考资料

- [pytrends 官方 GitHub 仓库与文档](https://github.com/generalodesign/pytrends)
