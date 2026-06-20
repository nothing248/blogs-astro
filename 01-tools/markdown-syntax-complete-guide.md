---
title: "MD语法"
filename: markdown-syntax-complete-guide
description: Markdown是一种轻量级标记语言。本文汇总了Markdown的标准排版语法，包含标题、粗斜体、删除线、多级引用、表格、超链接和图片链接编写，并给出了嵌套代码块以防止格式坍塌的写法，适合用作Obsidian等知识库构建时的格式排版设计规范。
tags: [markdown, writing, formatting, obsidian]
aliases: [MD语法, Markdown格式, 排版规范]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:23 下午
date modified: 星期五, 六月 19日 2026, 12:06:23 中午
---

<!-- toc -->

## 1. 语法

### 1.1. 基础用法

```shell
# 标题

**加粗**

*加斜*

~~删除~~

> 引用
>
> 多段落引用

*** #分割线

![aaa](https://img95.699pic.com/photo/50046/5562.jpg_wh300.jpg "测试")

[超链接](https://img95.699pic.com/photo/50046/5562.jpg_wh300.jpg "图片")

单行代码

- 无序

1. 有序
    
    ``` shell
    function fun(){
      echo "这是一句非常牛逼的代码";
    }
    fun();
    ```
未缩进  
&ensp;&ensp;缩进  
&emsp;缩进   
不换行&nbsp;缩进

多级缩紧
- 内置H5页面的数据采集方案
    - 方案1</br>
        **实施方式**:  
        -   在同一个GA Property中创建Web Stream，并且将数据直接发送到Web Stream中。  
        **优势**:  
        -   可以在H5页面使用一套
        
表格

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

视频
<video id="video" controls="" preload="none" poster="封面">
      <source id="mp4" src="mp4格式视频" type="video/mp4">
</videos>

<iframe src="//player.bilibili.com/player.html?aid=771248706&bvid=BV1gr4y1L7Ho&cid=782238447&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
```

### 1.2. 其他用法说明

- 空白行用于分割段落
- 行尾添加两个以上空格或 \< br > 用于换行
- &符号使&amp; amp;

## 2. 样例

**加粗**

*加斜*

~~删除~~

> 引用
>
> 多段落引用

***

![aaa](https://img95.699pic.com/photo/50046/5562.jpg_wh300.jpg "测试")

[超链接](https://img95.699pic.com/photo/50046/5562.jpg_wh300.jpg "图片")

[相对引用](jupyter.md "图片")

单行代码

- 无序

1. 有序

```shell
function fun(){
  echo "这是一句非常牛逼的代码";
}
fun();
```

未缩进  
&ensp;&ensp; 缩进  
&emsp; 缩进
不换行&nbsp; 缩进

多级缩紧

- 内置 H5 页面的数据采集方案
  - 方案 1 </br>
      **实施方式**:
    - 在同一个 GA Property 中创建 Web Stream，并且将数据直接发送到 Web Stream 中。  
      **优势**:
    - 可以在 H5 页面使用一套

表格

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

视频  
<iframe src="//player.bilibili.com/player.html?aid=771248706&bvid=BV1gr4y1L7Ho&cid=782238447&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

## 3. 参考资料

- [文档](https://markdown.com.cn/basic-syntax/)
