---
title: "Apprise通知聚合"
filename: apprise-notification-aggregator
description: Apprise 是一款强大的跨平台通知聚合工具，支持通过统一的 API 接口向微信、电报、邮件等数十个平台发送通知。本笔记介绍了使用 Docker Compose 部署 Apprise 无状态服务的方法，提供了 Webhook 测试命令、基于 YAML 的多渠道标签配置实例，以及如何利用 Nginx/OpenResty 配置带身份验证的反向代理，解决了多平台通知推送的集中化管理与安全调用问题。
tags: ["Apprise", "Notification", "Webhook", "Docker", "DevOps"]
aliases: ["Apprise通知聚合", "多平台推送工具"]
status: completed
date created: 星期三, 四月 1日 2026, 11:59:24 晚上
date modified: 星期五, 六月 19日 2026, 11:57:19 中午
---

<!-- toc -->

## 1. 简介

**Apprise** 是一款功能强大的聚合通知工具，它允许开发者通过几乎所有的流行通知平台（如微信、Telegram、Discord、Slack、邮件、Gotify 等）发送消息。Apprise 的核心优势在于其统一的 URL 架构，使得集成多渠道通知变得极其简单。

---

## 2. 安装与部署

### 2.1. 使用 Docker Compose 部署

Apprise 可以作为一个无状态的 HTTP 服务运行，方便通过 API 调用。

```yaml
services:
  apprise:
    image: caronc/apprise
    container_name: apprise-app
    restart: always
    networks:
      - local
    ports:
      - "8000:8000"
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - ./config:/config
      - ./plugin:/plugin
      - apprise_data:/attach

networks:
  local:
    external: true

volumes:
  apprise_data:
```

### 2.2. 基础测试

可以使用 `uvx` 或 `apprise` 命令行工具测试 Webhook 推送（以企业微信机器人为例）：

```bash
# 企业微信 Webhook 示例
# https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key = 1aa5b28d-xxxx-xxxx-xxxx-xxxx
uvx apprise -vv -t "测试消息标题" -b "测试消息正文" "wecombot://1aa5b28d-xxxx-xxxx-xxxx-xxxx"
```

---

## 3. 配置与高级用法

### 3.1. 多渠道配置文件 (`config.yml`)

通过配置文件可以实现标签化管理，一次向多个渠道推送。

```yaml
version: 1
urls:
  - wecombot://1aa5b28d-xxxx-xxxx-xxxx-xxxx:
      tag:
        - wecom
        - info
  - mailto://user:pass@example.com:
      tag:
        - email
        - critical
```

### 3.2. Nginx 反向代理与安全认证

为了保护 API 接口，建议在 Nginx 层增加基础身份验证（Basic Auth）。

```nginx
# 生成密码文件
# printf "admin:$(openssl passwd -apr1 123)\n" > /path/to/passwd

server {
    listen 80;
    server_name push.example.com;

    location / {
        auth_basic "Restricted Access";
        auth_basic_user_file /usr/local/openresty/nginx/conf/passwd/pushpasswd;
        
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        client_max_body_size 10m;
    }
}
```

### 3.3. 接口调用示例

```bash
# 使用命令行工具
apprise --body="测试消息" apprise://admin:密码@push.example.com/self/?tags=all

# 使用 curl 发送 POST 请求
curl -X POST \
    -F "body=Hello Apprise" \
    -F "tags=wecom" \
    https://admin:密码@push.example.com/notify/self
```

---

## 4. 参考资料

- [Apprise 官方文档：配置指南](https://appriseit.com/getting-started/configuration/)
- [Apprise GitHub 项目](https://github.com/caronc/apprise)
