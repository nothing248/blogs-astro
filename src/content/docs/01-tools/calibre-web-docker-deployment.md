---
title: "个人图书馆部署"
filename: calibre-web-docker-deployment
description: Calibre-web 是一款基于 Web 的图书管理服务，旨在提供书籍预览、刮削、格式转换及管理功能。本笔记提供了使用 Docker Compose 部署 Calibre-web 及其自动化增强版（calibre-web-automated）的详细配置，包括环境变量设置、卷挂载（对接 Nextcloud 存储）及网络配置。它作为轻量级图书管理方案，有效补充了 Calibre 桌面端在 Web 端的访问与同步需求。
tags: ["Calibre-Web", "Docker", "Book-Management", "E-book", "Home-Lab"]
aliases: ["个人图书馆部署", "Calibre Web容器化", "图书自动化刮削"]
status: completed
date created: 星期四, 四月 2日 2026, 10:38:39 上午
date modified: 星期五, 六月 19日 2026, 11:58:12 中午
---

<!-- toc -->

## 1. 简介

**Calibre-web** 是一个开源的 Web 应用程序，为现有的 Calibre 图书库提供了一个整洁的浏览、搜索和下载界面。它支持多种电子书格式，能够自动刮削书籍元数据，并支持将图书发送到 Kindle 等设备，是构建个人图书馆的理想选择。

---

## 2. 安装部署

### 2.1. 标准版 Calibre-web (`docker-compose.yml`)

适用于已有 Calibre 数据库，仅需 Web 访问界面的场景。

```yaml
services:
  calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    container_name: calibre-web
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - DOCKER_MODS=linuxserver/mods:universal-calibre # 支持格式转换插件
    volumes:
      - ./config:/config
      - /path/to/books:/books # 指向你的 Calibre 书库目录
    ports:
      - 8083:8083
    restart: unless-stopped
```

### 2.2. 自动化增强版 (Calibre-web-automated)

适用于需要自动监控目录并导入书籍的场景。

```yml
    services:
      calibre-web-automated:
        image: crocodilestick/calibre-web-automated:latest
        container_name: calibre-web-automated
        environment:
          # Only change these if you know what you're doing
          - PUID=33
          - PGID=33
          # Edit to match your current timezone https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
          - TZ=Asia/Shanghai
          # Sets the listening port for the application. Defaults to 8083.
          # - CWA_PORT_OVERRIDE=8083
          # Hardcover API Key required for Hardcover as a Metadata Provider, get one here: https://docs.hardcover.app/api/getting-started/
          # - HARDCOVER_TOKEN=your_hardcover_api_key_here
          # If your library is on a network share (e.g., NFS/SMB), disables WAL and chown to reduce locking/permission issues,
          # and switches file watching to polling (more reliable on network mounts) instead of inotify.
          # Accepts: true/false (default: false)
          - NETWORK_SHARE_MODE=false
          # If you want to force polling mode regardless of share type, set CWA_WATCH_MODE=poll
          # - CWA_WATCH_MODE=poll
          # If running behind multiple proxies (e.g., Cloudflare Tunnel + reverse proxy), set the total number of proxies
          # This ensures proper IP detection for session protection and rate limiting (default: 1)
          # - TRUSTED_PROXY_COUNT=2
          # Skip the automatic library detection/mount at startup. When enabled, the auto-library service will not run.
          # Accepts: true/yes/1 to disable auto-mount (default: false)
          - DISABLE_LIBRARY_AUTOMOUNT=false
        volumes:
          # CW users migrating should stop their existing CW instance, make a copy of the config folder, and bind that here to carry over all of their user settings etc.
          - ./config:/config
          # This is an ingest dir, NOT a library one. Anything added here will be automatically added to your library according to the settings you have configured in CWA Settings page. All files placed here are REMOVED AFTER PROCESSING
          - /data/podman/graph/volumes/qbittorrent_qbittorrent_data/_data/Books:/cwa-book-ingest
          # If you don't have an existing library, CWA will automatically create one at the bind provided here
          - /data/podman/graph/volumes/nextcloud_nextcloud_data/_data/data/admin/files/Books/Library:/calibre-library
          # If you use calibre plugins, you can bind your plugins folder here to have CWA attempt to add them to it's workflow (WIP)
          # If you are starting with a fresh install, you also need to copy customize.py.json to the Calibre config volume above, in /path/to/config/folder/.config/calibre/customize.py.json, see the README for more info
          # - calibre_web_automated_data:/config/.config/calibre/plugins
        ports:
          # Change the first number to change the port you want to access the Web UI, not the second
          - 8083:8083
        # If you set CWA_PORT_OVERRIDE to a port below 1024, you may need to uncomment the following line:
        # cap_add:
        #   - NET_BIND_SERVICE
        networks:
          - local
        restart: unless-stopped
    
    networks:
      local:
        external: true
```

---

## 3. 核心功能与注意事项

- **元数据刮削**：支持通过 Google Books、Douban 等 API 自动获取封面和书籍详情。
- **格式转换**：通过启用 `universal-calibre` 扩展，可以在 Web 端实现 EPUB/MOBI/PDF 等格式的互转。
- **Kindle 推送**：配置 SMTP 后可实现一键推送图书至 Kindle 邮箱。

> [!warning] 提示
> Calibre-web 主要侧重于 **管理与分发**。若需进行复杂的电子书排版编辑或大规模格式修复，建议使用 Calibre 桌面版。

---

## 4. 参考资料

- [Calibre-web GitHub 项目](https://github.com/janeczku/calibre-web)
- [Calibre-web-automated 镜像说明](https://github.com/crocodilestick/calibre-web-automated)
