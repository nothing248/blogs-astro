---
title: "redis-guide"
filename: redis-installation-and-eviction-policies
summary: 本文记录了高并发键值缓存数据库 Redis 在 Linux 系统的 apt 安装与 systemd 服务管理。系统性整理了包括 noeviction、volatile-* 和 allkeys-* 等 8 种核心内存淘汰机制，并分别给出了通过配置文件与 Docker Compose 部署时设置最大内存限制（maxmemory）及内存回收策略（maxmemory-policy）的配置实例。
tags:
  - redis
  - cache
  - database
  - linux-service
  - docker-compose
aliases:
  - redis-guide
  - redis-eviction-policies
  - redis-installation
status: completed
---

<!-- toc -->

## 1. 简介

**Redis**（Remote Dictionary Server）是一个开源的、高性能的内存键值数据库。它支持多种数据结构（如字符串、哈希、列表、集合、有序集合等），通常被广泛用作缓存服务器、消息队列以及分布式锁。

## 2. 安装

### 2.1. Linux (Debian/Ubuntu) 安装

可以通过系统默认包管理器快速安装 Redis 服务端：

```shell
apt update
apt install redis-server
```

### 2.2. Docker 部署

通过 Docker 快速启动 Redis，可以前往 [Docker Hub Redis 官方页面](https://hub.docker.com/_/redis) 获取详细信息。

### 2.3. 图形化管理客户端 (Windows/macOS/Linux)

推荐使用开源好用的 [Another Redis Desktop Manager](https://github.com/qishibo/AnotherRedisDesktopManager/releases)。

## 3. 基础配置

在 Redis 配置文件 `/etc/redis/redis.conf` 中可以自定义端口和访问密码：

```text
port 6380
requirepass [密码已隐藏]
```

> [!WARNING]
> 请避免在生产环境中使用过于简单的密码。在修改配置后需要重启 Redis 服务。

## 4. 服务管理

在 Linux 系统中，使用 `systemd` 对 Redis 服务进行管理：

```shell
systemctl status redis-server    # 查看服务状态
systemctl stop redis-server      # 停止服务
systemctl start redis-server     # 启动服务
systemctl restart redis-server   # 重启服务
```

## 5. 典型应用场景

- **缓存**：减轻关系型数据库压力，加快读取速度。
- **会话存储 (Session Storage)**：存储分布式 Web 应用的用户 Session 状态。
- **分布式锁**：利用 `SETNX` 或 Redisson 框架实现跨进程的分布式锁。
- **速率限制器 (Rate Limiter)**：实现接口的滑动窗口或令牌桶限流。
- **排行榜**：使用 ZSET（有序集合）结构轻松维护实时更新的排行榜。

## 6. 内存淘汰策略 (Eviction Policies)

当 Redis 的内存占用达到最大上限时，它会触发内存淘汰策略以释放空间。这些策略可以分为：**不淘汰**、**针对所有 Key** (`allkeys-*`) 和 **针对设置了过期时间 (TTL) 的 Key** (`volatile-*`) 三大类。

### 6.1. 不淘汰策略 (No Eviction)

| **策略名称** | **淘汰逻辑** | **适用场景** |
| :--- | :--- | :--- |
| **`noeviction`** | **不淘汰任何数据。** 达到内存上限后，任何试图写入新数据的命令（如 `SET`, `LPUSH` 等）都会直接报错并返回错误提示，但读命令（如 `GET`）仍可正常执行。 | 适用于数据绝对不能丢失的核心计算/存储场景，通常不作为纯缓存的配置。 |

### 6.2. 针对设置了过期时间的 Key 的策略 (`volatile-*`)

此类策略只会淘汰 **那些设置了 TTL 且尚未过期的 Key**。

| **策略名称** | **淘汰逻辑 (仅针对设置了 TTL 的 Key)** | **适用场景** |
| :--- | :--- | :--- |
| **`volatile-lru`** | 淘汰 **最近最少使用** (Least Recently Used) 的 Key。 | 只有部分数据需要设置过期，且 Key 的访问频率具备明显的时间热度关联。 |
| **`volatile-lfu`** | 淘汰 **最不经常使用** (Least Frequently Used) 的 Key。 | 数据访问频率分化明显，希望基于总体的访问次数而非最近一次访问时间进行筛选。 |
| **`volatile-ttl`** | 淘汰 **剩余生存时间最短** (Time To Live) 的 Key。 | 优先回收即将自然失效的 Key。 |
| **`volatile-random`** | **随机** 选择 Key 进行淘汰。 | 对缓存命中率无特定高要求，追求最简易低耗的淘汰操作。 |

### 6.3. 针对所有 Key 的策略 (`allkeys-*`)

此类策略在淘汰时会扫描 **Redis 数据库中所有的 Key**（无论其是否设置了过期时间）。

| **策略名称** | **淘汰逻辑 (针对所有 Key)** | **适用场景** |
| :--- | :--- | :--- |
| **`allkeys-lru`** | 淘汰数据库中 **最近最少使用** (LRU) 的 Key。 | 最通用的缓存策略。当 Redis **纯粹用作通用缓存** 时首选此配置。 |
| **`allkeys-lfu`** | 淘汰数据库中 **最不经常使用** (LFU) 的 Key。 | 规避 LRU 对冷热转换数据清理不够及时的弊端（例如，在某时间段爆火随后变冷的 Key 不会被 LRU 及时淘汰，而 LFU 能够基于频次将其移除）。 |
| **`allkeys-random`** | **随机** 选择任意 Key 进行淘汰。 | 适用于读写数据分布均匀，无需特殊热点策略的场景。 |

---

## 7. 策略配置实例

### 7.1. 配置文件修改

编辑 `/etc/redis/redis.conf`，根据服务器规格设置最大内存并指定淘汰策略（默认是不淘汰的 `noeviction`）：

```text
# 设置最大可用内存为 1GB
maxmemory 1gb

# 设置淘汰策略为全局 LRU
maxmemory-policy allkeys-lru
```

### 7.2. Docker Compose 部署配置

在 `docker-compose.yml` 中，可以通过命令行参数直接注入内存限制和淘汰策略：

```yaml
version: '3.8'

services:
  redis:
    image: redis:latest
    container_name: my_redis_cache
    ports:
      - "6379:6379"
    # 通过 command 传入配置参数参数
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    # volumes:
    #   - ./redis-data:/data
```

## 8. 参考资料

- [Redis 官方网站](https://redis.io/)
