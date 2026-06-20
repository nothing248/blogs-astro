---
title: "Mac效率工具"
filename: macos-utility-tools-configuration
description: macOS实用工具配置与故障诊断指南。本文整理了在Mac系统下常用的效率套件，例如Maccy剪贴板历史工具的命令行安装，以及基于Homebrew配置以优化开发体验的工具列表。适合需要进行Mac环境初始化、多显示器缩放优化和磁盘空间清理的开发者参考。
tags: [macos, productivity, maccy, brew]
aliases: [Mac效率工具, Maccy安装, Mac环境配置]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:33 上午
date modified: 星期五, 六月 19日 2026, 12:06:21 中午
---

<!-- toc -->

## 1. 简介

mac 相关信息

## 2. 工具

### 2.1. 粘贴板历史工具

[maccy](https://github.com/p0deje/Maccy?tab=readme-ov-file#install)

- 下载安装  
...
  
- 命令安装

```shell
brew install maccy
```

### 2.2. 硬盘清理

[maccleanx](https://cleanmymac.macpaw.com/20?campaign=cmmx_search_brand_us_en&ci=105095406&adgroupid=100331958853&adpos=&ck=cleanmymac%20x%20free&targetid=kwd-552206083562&match={if:e}&gnetwork=g&creative=680412491432&placement=&placecat=&accname=cmm&gad_source=1&gclid=CjwKCAjwg-24BhB_EiwA1ZOx8u6M9ISKpKoRF3tW6_gPJrSyi8HXo6NEgkiWHlBQmTGO9pGQomLQPxoCmloQAvD_BwE)

### 2.3. 手势工具

[bettertouchtool](https://macapp.org.cn/app/bettertouchtool/)

### 2.4. 清除 DNS

```
 dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

## 3. 拓展信息

### 3.1. 更新系统到指定版本

- [参考链接](https://support.apple.com/zh-cn/102662)

### 3.2. 破解软件平台

- macwk 第一个当属 macwk，经历过闭站后浴火重生，现在资源还比较少，但是质量都很高。网站无需登录也没有登录。基本上提供夸克云盘下载
- 佛系软件 资源很多，大部分来自 TNT team。下载无需登录，提供百度云盘和夸克云盘下载
- macked 资源很多，也有原创一手破解。无需登录，提供 123 云盘和百度网盘下载。登录网站可以直链下载，速度挺快，并且有问题在评论留言站长也会回复，非常不错
- xmac 资源很多，大部分来自 TNT team。无需登录，提供直链和 IPFS 下载
- appstorrent 俄罗斯的网站，资源很多，更新也很快。无需登录，直链下载。有些热门软件会受版权影响则不提供下载，但是可以去其他地方找~
- macserialjunkie 国外的论坛，时常会有一手破解资源。非常不错，可以作为兜底去逛逛。

### 3.3. 公共网络弹出认证页面受限

- 去除 DNS 设置
- 访问 captive.apple.com 进行尝试
- 重启电脑、确定网络时候连接成功

## 4. 参考资料
