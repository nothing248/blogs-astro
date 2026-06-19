---
title: "Docsify文档"
filename: docsify-lightweight-document-system
summary: Docsify是一款无需构建、直接在浏览器端解析Markdown的轻量级文档系统。本文详解通过NPM全局安装docsify-cli、项目初始化、_sidebar.md多级侧边栏路由以及嵌套目录README匹配逻辑，并分享了搜索插件、多主题样式及代码高亮插件的配置实践。
tags: [docsify, markdown, static-site, documentation]
aliases: [Docsify文档, 侧边栏配置, 静态站点生成]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:25 下午
date modified: 星期五, 六月 19日 2026, 11:58:50 中午
---

<!-- toc -->

## 1. 简介

一个轻量级的文档系统

## 2. 支持范围

- 解析 md 文件
- 支持兼容 vue
- 插件支持(搜索等)

## 3. 安装

```npm
npm install -g docsify-cli
```

## 4. 初始化

- 初始化项目(进入到对应目录)

```shell
docsify init ./docs
```

- 创建_sidebar.md 文件

```markdown
- 首页
    - [Index](/index)
- [尾页](/end)
  - [Index](/end/index)
```

> 注意: 如果嵌套路由需要可以直接查看，则需要对应目录中存在 README.md 文件

- 修改 index
  - 引入插件(按需求决定)

  ```html
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
  ```

  > 注意: 如果是 https 站点, 但是站点内容 需要加载 http 资源, 建议添加以下安全策略

  ```html
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
  ```

  - 配置选项

  ```js
  window.$docsify = {
        name: '',
        repo: '',
        loadSidebar:true, //开启侧边栏
        alias: { //防止侧边栏目录从顶部目录落入到内部目录
          '/.*/_sidebar.md': '/_sidebar.md'
        },
        subMaxLevel: 2, //侧边栏解析 md 文件中 header 最大层级,
        loadNavbar: true, // 开启导航
        search:{ //搜索配置
          placeholder:"搜索",
          noData:"没有数据"
        }
      }
  ```

## 5. 内容

- 在对应目录中创建 md 文件

> 代码块中的特殊符号会被编译

## 6. 运行项目

- 运行命令(进入到对应目录)

```shell
docsify serve
```

## 7. 生成 sitemap

当前没有插件支持直接生成 sitemap, 以下利用 python 脚本依赖_sidebar.md 进行手动生成

```python
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import re


page_regex = r"(.*).md$"
hostname = "https://blogs.service.sxyxy.top"
urlset = Element("urlset")
urlset.attrib["xmlns"] = "http://www.sitemaps.org/schemas/sitemap/0.9"

# 读取文件
with open("../_sidebar.md",'r',encoding='utf-8') as f:
    readme = f.read()
    html = markdown.markdown(readme)
    soup = BeautifulSoup(html,'html.parser')

    links = soup.find_all('a')
    for link in links:
        reg_result = re.match(page_regex,link['href'])
        if reg_result:
            url = SubElement(urlset, "url")
            print(reg_result.group(1))
            SubElement(url, "loc").text = f"{hostname}{reg_result.group(1)}"
            #SubElement(url, "lastmod").text = link ['title']
            #SubElement(url, "changefreq").text = ""
            #SubElement(url, "priority").text = ""


# 存储文件
xml_string = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
with open("../sitemap.xml", "w", encoding="utf-8") as f:
    f.write(xml_string)
```

## 8. 部署项目

- 直接静态部署

```nginx
server {
  listen 80;
  server_name  your.domain.com;

  location / {
    root /path/to/dir/of/docs/;
    try_files $uri /index.html;
    index index.html;
  }
}
```

- docker 部署

```dockerfile
  FROM node:latest
  LABEL description="A demo Dockerfile for build Docsify."
  WORKDIR /docs
  RUN npm install -g docsify-cli@latest
  EXPOSE 3000/tcp
  ENTRYPOINT docsify serve .
```

```shell
docker build -f Dockerfile -t docsify/demo .
```

```shell
docker run -itp 3000:3000 --name=docsify -v $(pwd):/docs docsify/demo
```

## 9. 参考资料

- [官方链接](https://docsify.js.org/#/quickstart)
