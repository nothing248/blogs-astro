---
title: "Selenium自动化"
filename: selenium-automation-guide
summary: Selenium 是一个强大的 Web 自动化测试框架，支持多种浏览器和编程语言。本文介绍了 Selenium 的 Python 环境安装及基础配置。它是自动化测试、网页抓取和交互式脚本开发的核心工具，通常与各浏览器的 WebDriver 配合使用，用于执行复杂的网页交互逻辑。
tags: [automation, testing, selenium, python]
aliases: [Selenium自动化]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:24 下午
date modified: 星期五, 六月 19日 2026, 12:08:30 中午
---

<!-- toc -->

## 1. 简介

Selenium 是一个针对不同浏览器的站点自动化测试工具。它允许开发者编写脚本来模拟用户在浏览器中的操作，如点击按钮、填写表单、页面导航等。

## 2. 安装

### 2.1. Python 环境安装

通过 Python 的包管理工具 `pip` 可以快速安装 Selenium 库：

```shell
pip install selenium
```

> [!tip]
> 安装完成后，你还需要下载对应浏览器的驱动程序（如 ChromeDriver 或 GeckoDriver），并将其路径添加到系统环境变量中。

## 3. 核心功能

- **多浏览器支持**：支持 Chrome, Firefox, Edge, Safari 等主流浏览器。
- **多语言支持**：除了 Python，还支持 Java, C#, Ruby, JavaScript 等。
- **分布式测试**：可以通过 Selenium Grid 在多台机器上并行运行测试。

## 4. 参考资料

- [Selenium 官方文档](https://www.selenium.dev/documentation/)
- [Python Selenium 中文文档](https://python-selenium-zh.readthedocs.io/zh-cn/latest/1.%E5%AE%89%E8%A3%85/)
