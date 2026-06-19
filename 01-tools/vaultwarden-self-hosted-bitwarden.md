---
title: "Vaultwarden安装"
filename: vaultwarden-self-hosted-bitwarden
summary: Vaultwarden是使用Rust重写的轻量级Bitwarden服务器替代方案，大幅降低了系统资源消耗。本文介绍通过Docker Compose搭建Vaultwarden的方法，涵盖安全环境变量设置、WebSocket实时同步、Borgmatic与Cloudflare R2的异地数据安全备份及保留策略配置。
tags: [vaultwarden, bitwarden, self-hosting, data-backup]
aliases: [Vaultwarden安装, 密码管理, Borgmatic备份]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:09:05 中午
---

<!-- toc -->

## 1. 简介

一个开源的 Bitwarden 的替代方案

## 2. 安装

- 生成密码

```
openssl rand -base64 32
```

- docker-compose

```yml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    environment:
      - DOMAIN=https://vault.example.com # 替换为你的 Cloudflare 域名
      - SIGNUPS_ALLOWED=true                  # 注册完第一个账号后记得改回 false
      - ADMIN_TOKEN=ImR/v/pFFuBZGI7gpII/R45OYEdupS1R7XchFROdiKc=       # 访问 /admin 页面的密码
      - WEB_VAULT_ENABLED=true                # 启用网页端
      # 开启 WebSocket 通知（实时同步修改）
      - WEBSOCKET_ENABLED=true
      - SMTP_HOST=smtp.163.com
      - SMTP_FROM=example@163.com
      - SMTP_FROM_NAME=Vaultwarden
      - SMTP_PORT=465
      - SMTP_SECURITY=starttls
      - SMTP_USERNAME=example@163.com
      - SMTP_PASSWORD=WFU2e
    volumes:
      - ./data:/data
    ports:
      - "8880:8880"
    networks:
      - local
    restart: unless-stopped
    
networks:
  local:
    external: true
```

- 备份配置

```
# --- 全局参数 (不再嵌套在 location/storage 下) ---
source_directories:
    - /data/podman/composes/vaultwarden/data

repositories:
    - path: /mnt/ex_storage_1/backups/valutwarden

exclude_patterns:
    - '*.log'
    - 'db.sqlite3'
    - 'db.sqlite3-shm'
    - 'db.sqlite3-wal'

encryption_passphrase: "4tZ44vYPYIjZCnCxkiVgz1gupGGIMhpd2GlnKKdeivCooNHX"
compression: lz4
checkpoint_interval: 1800

# --- 保留策略 ---
keep_daily: 7
keep_weekly: 4
keep_monthly: 6

# --- 命令钩子 (使用新的 commands 语法) ---
commands:
    - before: action
      when: [ create ]
      run:
          - echo "开始备份 Vaultwarden 数据库..."
          - sqlite3 /data/podman/composes/vaultwarden/data/db.sqlite3 ".backup /data/podman/composes/vaultwarden/data/db.sqlite3.bak"

    - after: action
      when: [ create ]
      run:
          - rm /data/podman/composes/vaultwarden/data/db.sqlite3.bak
          - echo "本地备份完成，同步到 Cloudflare R2..."
          - rclone sync /mnt/ex_storage_1/backups/valutwarden r2:documents/vaultwarden --progress

    - after: error
      when: [ create, prune, compact, check ]
      run:
          - echo "备份任务发生错误，请检查日志！"

# --- 其他配置 ---
bootstrap: {}# --- 全局参数 (不再嵌套在 location/storage 下) ---
source_directories:
    - /data/podman/composes/vaultwarden/data

repositories:
    - path: /mnt/ex_storage_1/backups/valutwarden

exclude_patterns:
    - '*.log'
    - 'db.sqlite3'
    - 'db.sqlite3-shm'
    - 'db.sqlite3-wal'

encryption_passphrase: "4tZ44vYPYIjZCnCxkiVgz1gupGGIMhpd2GlnKKdeivCooNHX"
compression: lz4
checkpoint_interval: 1800

# --- 保留策略 ---
keep_daily: 7
keep_weekly: 4
keep_monthly: 6

# --- 命令钩子 (使用新的 commands 语法) ---
commands:
    - before: action
      when: [ create ]
      run:
          - echo "开始备份 Vaultwarden 数据库..."
          - sqlite3 /data/podman/composes/vaultwarden/data/db.sqlite3 ".backup /data/podman/composes/vaultwarden/data/db.sqlite3.bak"

    - after: action
      when: [ create ]
      run:
          - rm /data/podman/composes/vaultwarden/data/db.sqlite3.bak
          - echo "本地备份完成，同步到 Cloudflare R2..."
          - rclone sync /mnt/ex_storage_1/backups/valutwarden r2:documents/vaultwarden --progress

    - after: error
      when: [ create, prune, compact, check ]
      run:
          - echo "备份任务发生错误，请检查日志！"

# --- 其他配置 ---
bootstrap: {}
```

- 进行备份

```bash
# 安装备份环境
sudo apt update && sudo apt install borgbackup borgmatic -y
pip install --upgrade borgmatic --break-system-packages # 升级
apt install sqllite3 python3-pyfuse3 python3-llfuse # 确保环境没有问题

# 备份
borgmatic init --encryption repokey # 初始化
borgmatic --verbosity 1 # 手动备份

# 设置 crontab
0 3 * * * /usr/bin/borgmatic --syslog --verbosity 0
```

## 3. 拓展信息

### 3.1. 客户端

- 直接使用 Bitwarden 即可

## 4. 参考资料

- [Girhub](https://github.com/dani-garcia/vaultwarden)
