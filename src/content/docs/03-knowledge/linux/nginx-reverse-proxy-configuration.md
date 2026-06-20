---
title: "nginx-guide"
filename: nginx-reverse-proxy-configuration
description: 本文记录了高性能 Web 服务器 Nginx 的基本配置方法，重点介绍 Location 匹配规则及反向代理（proxy_pass）的基础语法。包含代理至本地服务端口的配置示例，并附带 Location 匹配优先级的流程图解，以便开发者快速查阅与排查反向代理配置。
tags:
  - nginx
  - web-server
  - reverse-proxy
  - network
  - configuration
aliases:
  - nginx-guide
  - nginx-proxy
  - nginx-configuration
status: completed
---

<!-- toc -->

## 1. 简介

**Nginx** 是一个高性能的 HTTP 和反向代理 Web 服务器，同时也提供了 IMAP/POP3/SMTP 服务。其因具有占有内存少、并发能力强等特点，在云原生和互联网架构中得到了极其广泛的应用。

## 2. 核心配置示例

### 2.1. 反向代理配置

将匹配到的特定 URL 路由请求转发至后端应用服务器（例如本地的 8080 端口）：

```nginx
location /test1 {
    proxy_pass http://127.0.0.1:8080;
    
    # 常用请求头透传配置
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 2.2. 静态文件代理

配置静态资源根目录，支持高效的文件读取：

```nginx
location /static/ {
    alias /var/www/static/;
    expires 30d;
    access_log off;
}
```

### 2.3. WebSocket / WSS 配置

若需要支持 WebSocket 协议转发，需显式升级 Connection 和 Upgrade 请求头：

```nginx
location /ws {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

## 3. 拓展信息

### 3.1. Location 匹配规则与优先级

Nginx 依靠 `location` 指令匹配请求的 URI，以下是匹配规则的优先级顺序及原理图解：

1. `location = /uri`：精确匹配。
2. `location ^~ /uri`：前缀匹配，一旦匹配成功，停止往下搜索正则匹配。
3. `location ~ pattern`：区分大小写的正则匹配。
4. `location ~* pattern`：不区分大小写的正则匹配。
5. `location /uri`：通用前缀匹配。

![Location 匹配参数图解](http://qiniu.sxyxy.top/20241017111758.png)
