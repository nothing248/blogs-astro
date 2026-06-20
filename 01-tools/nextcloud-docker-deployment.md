---
title: "Nextcloud部署"
filename: nextcloud-docker-deployment
description: Nextcloud 是一款功能强大的开源私有云存储平台。本文详细介绍了使用 Docker Compose 部署 Nextcloud 的完整流程，包括集成 PostgreSQL 数据库、Redis 缓存以及环境变量配置。同时提供了常用管理命令（如重置密码、配置信任域名）和 CRON 定时任务设置，解决了非客户端手动上传文件无法自动识别的常见问题。
tags: [nextcloud, self-hosted, docker, cloud-storage, devops]
aliases: [Nextcloud部署, 私有云盘安装]
status: completed
date created: 星期三, 四月 1日 2026, 11:54:52 晚上
date modified: 星期五, 六月 19日 2026, 12:06:42 中午
---

<!-- toc -->

## 1. 简介

Nextcloud 是目前最流行的开源协作平台和个人云存储方案，支持文件同步、日历、联系人以及丰富的插件生态。

## 2. 安装与部署

推荐使用 Docker Compose 进行一键式部署，方便维护和升级。

### 2.1. Docker Compose 配置

```yaml
services:
  nextcloud-app:
    image: nextcloud:apache
    container_name: nextcloud-app
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    ports:
      - 8888:80
    environment:
      # 数据库配置 (PostgreSQL)
      - POSTGRES_HOST=db          # 外部 Postgres 的 IP 或域名
      - POSTGRES_DB=nextcloud      # 数据库名
      - POSTGRES_USER=[DB_USER]    # 数据库用户名
      - POSTGRES_PASSWORD=[DB_PASS] # 数据库密码
      
      # Redis 缓存配置
      - REDIS_HOST=redis          # 外部 Redis 的 IP 或域名
      #- REDIS_HOST_PASSWORD=[REDIS_PASS] # 如果 Redis 有密码则开启
      
      # 初始化管理员账户
      - NEXTCLOUD_ADMIN_USER=admin
      - NEXTCLOUD_ADMIN_PASSWORD=[ADMIN_PASSWORD]
      
      # 域名与协议配置
      - NEXTCLOUD_TRUSTED_DOMAINS=[nxcloud.example.com]
      - OVERWRITEHOST=[nxcloud.example.com]
      - OVERWRITEPROTOCOL=https
    networks:
      - nextcloud_network

volumes:
  nextcloud_data:

networks:
  nextcloud_network:
    external: true
```

## 3. 运维管理

Nextcloud 提供了强大的命令行工具 `occ`。在容器环境中，需通过 `docker exec` 调用。

### 3.1. 常用命令示例

```bash
# 重置管理员密码
docker exec -u www-data -it nextcloud-app php occ user:resetpassword admin  

# 列出所有用户
docker exec -u www-data -it nextcloud-app php occ user:list

# 查看当前已信任的域名
docker exec -u www-data -it nextcloud-app php occ config:system:get trusted_domains  

# 添加新的信任域名
docker exec -u www-data -it nextcloud-app php occ config:system:set trusted_domains 1 --value=127.0.0.1:8888  
docker exec -u www-data -it nextcloud-app php occ config:system:set trusted_domains 2 --value=[nxcloud.example.com]

# 手动触发文件扫描（适用于直接将文件放入宿主机 data 目录的情况）
docker exec -u www-data nextcloud-app php /var/www/html/occ files:scan --path="/admin/files/Books"
```

## 4. 定时任务 (CRON)

为了确保后台任务（如文件同步、预览图生成）能正常运行，建议在宿主机设置 crontab。

```cron
# 每 5 分钟执行一次 Nextcloud 后台任务
*/5 * * * * docker exec -u www-data nextcloud-app php -f /var/www/html/cron.php

# (可选) 定期扫描特定路径下的文件
*/5 * * * * docker exec -u www-data nextcloud-app php /var/www/html/occ files:scan --path="/admin/files/Books"
```

> [!tip]
> **文件同步注意**：直接通过文件系统（如 SFTP/Samba）上传到 Nextcloud 数据目录的文件不会自动显示在网页端，必须通过 `occ files:scan` 命令强制扫描。

## 5. 参考资料

- [Nextcloud 官方文档](https://docs.nextcloud.com/)
- [Docker Hub - Nextcloud](https://hub.docker.com/_/nextcloud)
