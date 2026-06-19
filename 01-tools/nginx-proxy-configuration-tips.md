---
title: "Nginx配置技巧"
filename: nginx-proxy-configuration-tips
summary: Nginx 是一款高性能的 HTTP 和反向代理服务器。本文整理了 Nginx 的实用配置技巧，包括如何通过 location 正则匹配解决 Vue 项目中的三方平台（如百度云 API）跨域限制问题，以及如何通过后缀名限制（如拒绝 PDF 访问）增强服务器的安全性。适用于需要精细化控制请求转发与安全过滤的场景。
tags: [nginx, reverse-proxy, cors, web-security, devops]
aliases: [Nginx配置技巧, Nginx反向代理]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:30 下午
date modified: 星期五, 六月 19日 2026, 12:06:44 中午
---

<!-- toc -->

## 1. 简介

Nginx 是一个高性能的 HTTP 反向代理服务器，也可用作负载均衡器、邮件代理服务器和通用 TCP/UDP 代理服务器。它以稳定性、丰富的功能集、简单的配置文件和低资源占用而闻名。

## 2. 实战配置技巧

### 2.1. 解决跨域限制 (CORS)

在前端开发（如 Vue 项目）中，经常需要代理特定的 API 请求以绕过同源策略。

```nginx
# 匹配以 /baidu 开头的路径
location ~ ^/(baidu)/.* {
   # 去掉路径中的 /baidu 前缀
   rewrite  ^.+baidu/?(.*)$ /$1 break;
   
   include  uwsgi_params;
   
   # 代理到具体的第三方 API 地址
   proxy_pass https://aip.baidubce.com; 
   
   # 建议增加以下头部以透传真实信息
   proxy_set_header Host aip.baidubce.com;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### 2.2. 请求过滤与安全限制

可以通过 `location` 指令配合正则，禁止用户访问特定类型的文件。

```nginx
# 限制所有 PDF 文件的访问
location ~* \.(pdf)$ {
  deny all;
}

# 限制敏感目录（如 .git）
location ~ /\.git {
  deny all;
}
```

## 3. 性能优化建议

- **开启 Gzip 压缩**：减小传输体积。
- **配置缓存控制**：设置 `Expires` 或 `Cache-Control` 头部，利用浏览器缓存。
- **开启 Keep-alive**：减少 TCP 握手开销。

## 4. 参考资料

- [Nginx 官方文档](http://nginx.org/en/docs/)
- [Nginx 核心指令详解 (中文)](https://www.nginx.com/resources/wiki/)
