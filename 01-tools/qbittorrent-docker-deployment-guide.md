---
title: "qBittorrent安装"
filename: qbittorrent-docker-deployment-guide
description: qBittorrent 是一款开源且轻量级的 BitTorrent 客户端。本文介绍了使用 Docker Compose 部署 qBittorrent 的详细步骤，包括 Web UI 端口配置、初次登录密码获取及密码遗忘后的重置方法。同时探讨了公网 IP 对下载速度的影响以及 PT（私有）站点的基本概念，是家庭影音中心必备的下载工具指南。
tags: [qbittorrent, bittorrent, docker, download-manager, self-hosted]
aliases: [qBittorrent安装, BT下载工具, 磁力链接下载]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:07:50 中午
---

<!-- toc -->

## 1. 简介

qBittorrent 是一款基于 Qt 库和 libtorrent-rasterbar 开发的开源下载软件，以其简洁的界面、低资源占用和强大的功能（如搜索、RSS、Web 控制台）成为替代迅雷等闭源软件的首选。

## 2. 部署指南 (Docker Compose)

推荐使用 LinuxServer.io 维护的镜像，其配置灵活且更新及时。

```yaml
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - WEBUI_PORT=8088
      - TORRENTING_PORT=6881
    volumes:
      - ./config:/config
      - /mnt/data/downloads:/downloads # 映射下载目录
    ports:
      - 8088:8088
      - 6881:6881
      - 6881:6881/udp
    networks:
      - media_network
    restart: unless-stopped
    
networks:
  media_network:
    external: true
```

## 3. 账户与安全管理

### 3.1. 获取初始密码

在新版本中，默认密码是随机生成的，可以通过查看容器日志获取：

```bash
docker logs qbittorrent | grep "The WebUI password is"
```

### 3.2. 重置密码

如果忘记了 WebUI 密码且无法通过日志找回，可以采取以下“暴力”方案：

- **方案 A**：删除配置文件重置（会丢失部分设置）：

  ```bash
  rm config/qBittorrent/qBittorrent.conf
  ```

- **方案 B**：手动编辑 `qBittorrent.conf`，找到 `WebUI\Password_PBKDF2` 行并删除，重启容器后会恢复默认弱密码或重新生成。

## 4. 进阶技巧：BT 与 PT

- **BT (Public)**：公开种子，人人可下。在没有公网 IP 的情况下，速度可能较慢。
- **PT (Private Tracker)**：私有资源站。有严格的分享率要求（上传量需达到下载量的一定比例），通常能跑满带宽，适合高质量影视资源收集。
- **端口映射**：为了获得最佳上传/下载速度，**强烈建议** 在路由器上开启 `6881` 端口的 TCP/UDP 转发。

## 5. 参考资料

- [qBittorrent 官方网站](https://www.qbittorrent.org/)
- [LinuxServer.io qBittorrent 文档](https://docs.linuxserver.io/images/docker-qbittorrent/)
