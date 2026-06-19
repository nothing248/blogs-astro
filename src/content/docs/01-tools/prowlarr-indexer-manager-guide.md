---
title: "Prowlarr图床配置"
filename: prowlarr-indexer-manager-guide
summary: Prowlarr 是一款专为影音爱好者设计的开源索引管理工具（Indexer Manager），属于著名的“Arr”家族系列。它能够无缝聚合各种公共（Public）和私有（PT）资源站，并同步至 Sonarr, Radarr, Lidarr 等下游应用。本文提供了 Docker Compose 部署方案及核心环境变量配置，是搭建全自动化家庭影音中心的关键环节。
tags: [prowlarr, media-server, self-hosted, docker, pvr, automation]
aliases: [Prowlarr图床配置, PT索引管理, Arr家族工具]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:07:41 中午
---

<!-- toc -->

## 1. 简介

Prowlarr 是一款基于项目架构的索引器管理器，它是对 Jackett 的现代化替代。它支持对上百个公共和私有追踪器（Trackers/PT 站）进行统一管理，并能通过集成的 API 自动将索引器推送到你的影音自动化套件（如 Sonarr, Radarr 等）中，无需在每个应用中手动配置。

## 2. 部署指南 (Docker Compose)

使用 Docker 部署是目前最便捷的方式，建议配合反向代理或直接暴露端口访问。

```yaml
services:
  # 资源搜索与索引管理端：Prowlarr
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000  # 建议与宿主机用户 ID 一致
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - ./config:/config  # 持久化配置文件
    ports:
      - 9696:9696  # 默认访问端口
    networks:
      - media_network
    restart: unless-stopped

networks:
  media_network:
    external: true
```

## 3. 核心功能与工作流

1. **统一索引**：在一个界面配置所有的 PT 站（如 M-Team, HDSky）或 BT 站。
2. **自动同步**：配置好下载端后，Prowlarr 会自动同步索引器设置到 Radarr/Sonarr，确保存储库一致。
3. **统计分析**：提供每个索引器的查询成功率、响应时间等统计图表。
4. **代理支持**：内置代理设置，方便访问因地域限制无法连接的索引器。

## 4. 常见问题与技巧

- **PT 站认证**：大部分私有站需要填入 Cookie 或 Passkey，请务必在 Prowlarr 内部测试通过后再同步。
- **与 Jackett 区别**：Prowlarr 速度更快，UI 更现代化，且具备更强的自动化同步能力。

## 5. 参考资料

- [Prowlarr 官方 Wiki 文档](https://prowlarr.com/docs/)
- [Prowlarr GitHub 仓库](https://github.com/Prowlarr/Prowlarr)
- [LinuxServer.io Prowlarr 镜像说明](https://docs.linuxserver.io/images/docker-prowlarr/)
