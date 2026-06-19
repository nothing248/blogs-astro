---
status: completed
filename: scrapy-python-web-scraping-framework-guide
title: "Scrapy 教程"
summary: 本笔记记录了 Python 生态中最经典的分布式异步网络爬虫框架 Scrapy 的基础用法。分为轻量级单脚本调用模式与重量级标准项目脚手架模式。详细梳理了利用 `start_requests` 生成初始抓取序列、在 `parse` 回调中使用 CSS/XPath 选择器提取目标节点数据，以及利用 `response.follow` 触发翻页动作的核心流程。同时提供了通过 Scrapy Shell 进行实时页面节点调试的实战指引。
aliases: [Scrapy 教程, Python 爬虫框架, Scrapy 爬虫]
tags: [Python, 爬虫, 数据采集, Scrapy, 自动化, 爬虫架构]
date created: 星期二, 二月 25日 2025, 3:24:04 下午
date modified: 星期五, 六月 19日 2026, 2:49:00 下午
---

<!-- toc -->

## 1. 框架定位

**Scrapy** 是一个为了爬取网站数据、提取结构性数据而编写的开源应用框架。它底层基于 Twisted 异步网络库，拥有极高的抓取并发能力，适用于构建复杂的爬虫体系和分布式数据采集系统。

*(安装依赖：`pip install scrapy`)*

---

## 2. 模式 A：轻量级单文件脚本

适用于简单的、无需复杂管道 (Pipeline) 处理的临时抓取任务。

**`quotes_spider.py` 示例**：

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # 框架默认入口，自动下发 GET 请求并进入 parse 回调
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",
    ]

    def parse(self, response):
        # 1. 业务抽取：使用内置的 CSS / XPath 选择器提炼数据
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        # 2. 翻页爬取：提取下一页链接，并自动推入调度队列
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

**终端执行并直接序列化落盘**：

```bash
scrapy runspider quotes_spider.py -o quotes.jsonl
```

---

## 3. 模式 B：标准工程化脚手架

适用于复杂的大型抓取任务，需配置防封禁（Downloader Middleware）、自动存库（Pipeline）等高阶行为。

### 3.1. 初始化框架

```bash
scrapy startproject quotes_demo
cd quotes_demo
```

### 3.2. 编写独立 Spider (`spiders/quotes_spider.py`)

演示如何手动控制初始请求的分发，以及将抓取的原始 HTML 落地。

```python
from pathlib import Path
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        """覆盖默认的 start_urls，支持灵活定制初始 headers 或 payload"""
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """将网页源码持久化保存"""
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
```

### 3.3. 运行工程级爬虫

```bash
# 执行名为 quotes 的爬虫任务
scrapy crawl quotes
```

---

## 4. 高阶调试神器：Scrapy Shell

在编写解析逻辑前，**强烈建议使用框架提供的 Shell 终端进行实时调试**。它会自动拉取页面，并把你直接放置在交互式环境中：

```bash
scrapy shell 'https://quotes.toscrape.com/page/1/'

# 进入交互式终端后，可直接测试选择器：
# >>> response.css('span.text:: text').getall()
# >>> quit() 
```

## 5. 拓展生态

- **动态页面内容抓取**：原生的 Scrapy 无法执行 JS 渲染。遇到 React/Vue 单页应用时，必须借助 `Splash` 中间件，或直接挂载 `Playwright` / `Selenium`。

## 6. 参考资料

- [Scrapy 官方全量英文文档](https://docs.scrapy.org/en/latest/)
- [Scrapy Cookbook 中文文档](https://scrapy-cookbook.readthedocs.io/zh-cn/latest/scrapy-12.html)

