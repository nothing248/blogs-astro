---
title: "FreshRSS搭建"
filename: freshrss-self-hosted-rss
description: FreshRSS是优秀的开源自托管RSS聚合器。本文提供了基于Docker Compose的快速搭建方法，包含了MySQL与SQLite数据库选型、安全反向代理环境参数、基于WebSub协议的实时信息拉取配置，以及在多设备端同步订阅源的最佳实践，属于高效信息聚合的核心行动项。
tags: [freshrss, rss-aggregator, docker-compose, self-hosting]
aliases: [FreshRSS搭建, RSS聚合器, 自建阅读器]
status: completed
date created: 星期三, 六月 17日 2026, 11:51:40 晚上
date modified: 星期五, 六月 19日 2026, 11:59:17 中午
---

<!-- toc -->

## 1. 简介

**FreshRSS** 是一个免费、开源的自托管 RSS/Atom feed 聚合器，旨在为您提供一个私密且高效的阅读体验。与传统的在线 RSS 阅读器不同，FreshRSS 允许您将所有订阅源的数据存储在自己的服务器上，完全掌控您的信息流。它支持多种平台部署，其中 Docker 是最受欢迎且便捷的方式之一。

**为什么选择 FreshRSS？**

* **数据隐私与控制:** 您的所有订阅数据都存储在您的服务器上，无需担心第三方平台的数据政策或服务关闭。
* **高度可定制:** 提供丰富的配置选项，您可以根据个人喜好调整界面、阅读模式和数据刷新频率等。
* **多客户端支持:** 通过内置的 Google Reader API 兼容性，FreshRSS 可以与各种支持此 API 的移动和桌面 RSS 客户端无缝同步，实现多设备阅读体验。
* **去中心化:** 摆脱对单一服务提供商的依赖，构建您自己的信息聚合中心。
* **活跃的社区支持:** 拥有活跃的开源社区，不断有新功能开发和问题修复。
* **高性能:** 针对大量订阅源和文章进行了优化，提供流畅的阅读体验。

FreshRSS 不仅是一个简单的 RSS 阅读器，更是一个强大的信息管理工具，帮助您有效筛选和获取互联网上的最新资讯。

## 2. 安装

FreshRSS 的安装推荐使用 Docker Compose，这是一种用于定义和运行多容器 Docker 应用程序的工具。通过一个 `docker-compose.yml` 文件，您可以配置应用程序的所有服务（如 FreshRSS 容器、数据库容器等），并使用一个命令启动所有服务。

在开始之前，请确保您的服务器已安装 Docker 和 Docker Compose。您可以通过以下命令检查它们是否已安装：

```bash
docker --version
docker-compose --version
```

### 2.1. docker-compose.yml 配置

以下是一个用于部署 FreshRSS 的 `docker-compose.yml` 示例配置。此配置包含了 FreshRSS 服务本身，并定义了数据卷、网络以及重要的环境变量。根据您的需求，可能还需要额外的数据库服务（如 PostgreSQL 或 MySQL）。

```yaml
version: '3.8'

volumes:
  freshrss-data:
    # 用于持久化 FreshRSS 的数据，包括配置、数据库（如果使用 SQLite）、缓存、文章内容等。
    # 确保即使容器被删除或重建，数据也能得到保留。
  freshrss-extensions:
    # 用于持久化 FreshRSS 的扩展，方便您添加或管理插件。

networks:
  local:
    external: true
    # FreshRSS 容器将连接到名为 'local' 的现有外部网络。这在您已经有一个统一的 Docker 网络用于其他服务时非常有用，
    # 可以让 FreshRSS 与其他容器（如反向代理或数据库）进行通信。

services:
  freshrss:
    image: freshrss/freshrss:latest
    # 指定使用的 Docker 镜像。'freshrss/freshrss:latest' 会拉取最新稳定版本的 FreshRSS 镜像。
    # 如果需要特定版本或自定义构建，可以修改为其他标签或启用 'build' 部分。
    # # Optional build section if you want to build the image locally:
    # build:
    #   # Pick #latest (slow releases) or #edge (rolling release) or a specific release like #1.27.1
    #   context: https://github.com/FreshRSS/FreshRSS.git#latest
    #   dockerfile: Docker/Dockerfile-Alpine
    container_name: freshrss
    # 定义容器的名称，方便识别和管理。
    hostname: freshrss
    # 定义容器内部的主机名。
    restart: unless-stopped
    # 设置容器的重启策略。'unless-stopped' 表示除非手动停止容器，否则在容器退出时总是重启它。
    logging:
      options:
        max-size: 10m
        # 配置容器日志的最大大小，避免日志文件过大。
    volumes:
      - freshrss-data:/var/www/FreshRSS/data
      - freshrss-extensions:/var/www/FreshRSS/extensions
      # 将上面定义的 Docker 卷挂载到容器内部的相应路径，实现数据持久化。
    ports:
      - 8001:80
      # 将宿主机的 8001 端口映射到容器内部的 80 端口。这意味着您可以通过访问宿主机的 8001 端口来访问 FreshRSS 服务。
      # 如果您使用反向代理（推荐），这个端口可以是任意未被占用的端口，不对外暴露。
    networks:
      - local
      # 将 FreshRSS 容器连接到之前定义的 'local' 网络。
    environment:
      TZ: Asia/Shanghai
      # 设置容器的时区。
      CRON_MIN: '3,33'
      # 设置 FreshRSS 后台任务（如抓取 RSS 源）的运行频率，这里是每小时的第 3 分钟和第 33 分钟运行。
      TRUSTED_PROXY: 172.16.0.1/12 192.168.0.1/16
      # 如果使用反向代理（如 Nginx），需要配置可信代理的 IP 范围，以便 FreshRSS 正确获取客户端真实 IP。
      FRESHRSS_INSTALL: |- # 注意该服务的位置是在environment下
        --api-enabled
        --base-url ${BASE_URL}
        --db-base ${DB_BASE}
        --db-host ${DB_HOST}
        --db-password ${DB_PASSWORD}
        --db-type pgsql
        --db-user ${DB_USER}
        --default-user admin
        --language en
        # 这些是 FreshRSS 首次安装时使用的命令行参数。它们用于自动化安装过程，设置数据库连接、API 启用状态、
        # 默认管理员用户和语言等。请注意，这里的数据库类型是 pgsql，如果使用 SQLite，则无需配置。
      FRESHRSS_USER: |-
        --api-password ${ADMIN_API_PASSWORD}
        --email ${ADMIN_EMAIL}
        --language en
        --password ${ADMIN_PASSWORD}
        --user admin
        # 这些参数用于配置 FreshRSS 的默认管理员用户。包括 API 密码、邮箱、登录密码和用户名。
        # 这些变量的值通常通过 .env 文件来提供。
    # # Optional healthcheck section:
    # healthcheck:
    #   test: ["CMD", "cli/health.php"]
    #   timeout: 10s
    #   start_period: 60s
    #   start_interval: 11s
    #   interval: 75s
    #   retries: 3
    # 健康检查配置可以帮助 Docker 监控容器的运行状况，确保服务正常可用。
```

### 2.2. .env 环境变量配置

在 `docker-compose.yml` 同级目录下创建一个 `.env` 文件，用于存储敏感信息或常用配置变量。这些变量会在 Docker Compose 启动时被自动加载并注入到容器的环境中。以下是示例 `.env` 文件的详细解释：

```
BASE_URL=https://freshrss.example.com
# FreshRSS 服务的外部访问 URL。请将其替换为您的实际域名或 IP 地址及端口。这个URL非常重要，
# FreshRSS 内部会使用它来生成正确的链接和重定向，特别是在使用反向代理时。

ADMIN_EMAIL=exmaple@gmail.com
# FreshRSS 管理员用户的邮箱地址。

ADMIN_PASSWORD=pass
# FreshRSS 管理员用户的登录密码。请务必使用一个强密码，并避免在生产环境中使用 'pass' 这样的弱密码。

ADMIN_API_PASSWORD=pass
# FreshRSS 管理员用户的 API 密码。用于通过 Google Reader API 兼容的客户端访问 FreshRSS。同样，请使用强密码。

# Database credentials (not relevant if using default SQLite database)
DB_HOST=db
# 数据库服务的主机名或 IP 地址。如果您的数据库容器名为 'db' 且在同一个 Docker 网络中，则保持 'db'。
# 如果使用 SQLite（默认），则无需配置这些数据库凭据。

DB_BASE=freshrss
# 数据库名称。

DB_PASSWORD=example
# 数据库用户的密码。请替换为您的实际数据库密码。

DB_USER=admin
# 数据库用户的用户名。请替换为您的实际数据库用户名。

**重要提示:**

*   请务必将 `BASE_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_API_PASSWORD` 以及所有数据库凭据替换为您的实际值。特别是在生产环境中，使用强密码至关重要。
*   如果选择使用 SQLite 作为数据库（FreshRSS 默认支持），则 `DB_HOST`, `DB_BASE`, `DB_PASSWORD`, `DB_USER` 这些变量可以不配置，或者直接从 `docker-compose.yml` 中 `FRESHRSS_INSTALL` 部分移除 `--db-*` 相关的参数。
```

### 2.3. 反向代理配置 (Nginx)

为了提供更安全、更专业的访问方式，并能够使用自定义域名，强烈建议为 FreshRSS 配置反向代理。这里以 Nginx 为例进行说明。反向代理可以将外部请求转发到 FreshRSS 容器内部的端口，同时可以处理 SSL/TLS 加密、域名路由等。

将以下配置添加到您的 Nginx 配置中（通常位于 `/etc/nginx/sites-available/` 或 `/etc/nginx/conf.d/` 目录下，并创建软链接到 `sites-enabled/`）：

```conf
server {
 listen 80;
    server_name freshrss.example.com; # 替换为你的域名或 IP
    # 监听 80 端口，并指定你的域名。如果您的域名配置了 SSL/TLS，通常还会有一个监听 443 端口的 server 块。

 location / {
  proxy_pass http://127.0.0.1:8001;
  # 将所有到该域名的请求转发到本地的 8001 端口，即 FreshRSS 容器映射的宿主机端口。
  # 如果 FreshRSS 容器与 Nginx 部署在不同的 Docker 网络中，这里可能需要填写 FreshRSS 容器的内部 IP 或服务名。
  add_header X-Frame-Options SAMEORIGIN;
  # 防止点击劫持 (Clickjacking) 攻击，只允许同源的页面在 frame、iframe 或 object 中显示此页面。
  add_header X-XSS-Protection "1; mode=block";
  # 启用浏览器的 XSS 过滤功能，当检测到 XSS 攻击时，浏览器会阻止页面渲染。
  proxy_redirect off;
  # 禁用 Nginx 自动修改响应头中的 Location 字段，这通常由后端应用处理。
  proxy_buffering off;
  # 关闭代理缓冲，请求会直接发送到后端，响应也会立即返回给客户端。这对于需要实时更新的应用程序很有用。
  proxy_set_header Host $host;
  # 将原始请求的 Host 头传递给后端服务器，确保 FreshRSS 能够获取正确的域名信息。
  proxy_set_header X-Real-IP $remote_addr;
  # 将客户端的真实 IP 地址传递给后端服务器。FreshRSS 可以使用此信息进行日志记录或安全控制。
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  # 将客户端的真实 IP 地址以及所有经过的代理 IP 列表传递给后端服务器。
  proxy_set_header X-Forwarded-Proto $scheme;
  # 告知后端服务器客户端请求使用的协议（HTTP 或 HTTPS）。这对于后端应用生成正确的 URL 很重要。
  proxy_set_header X-Forwarded-Port $server_port;
  # 告知后端服务器客户端请求使用的端口。
  proxy_read_timeout 90;
  # 设置 Nginx 从后端服务器读取响应的超时时间为 90 秒。

  # Forward the Authorization header for the Google Reader API.
  proxy_set_header Authorization $http_authorization;
  # 转发 Authorization HTTP 头，这对于支持 Google Reader API 的客户端进行身份验证至关重要。
  proxy_pass_header Authorization;
  # 确保 Authorization 头从代理服务器传递到后端服务器。
 }
}
```

**完成 Nginx 配置后：**

1. **测试配置:** 运行 `sudo nginx -t` 检查配置文件的语法是否有误。
2. **重载 Nginx:** 运行 `sudo systemctl reload nginx` (或 `sudo service nginx reload`) 使新配置生效。
3. **配置 SSL/TLS (推荐):** 如果您希望使用 HTTPS 访问 FreshRSS，需要为您的域名配置 SSL/TLS 证书。可以使用 Certbot 等工具免费获取 Let's Encrypt 证书并自动配置 Nginx。

## 3. 使用场景

### 3.1. 批量更新 RSSHub 链接

当您在使用 FreshRSS 订阅了大量 RSSHub 生成的链接时，如果 RSSHub 服务的地址发生变化（例如，从官方 `rsshub.app` 切换到您自建的 `rsshub` 容器），您可能需要批量更新 FreshRSS 数据库中的订阅链接。以下 SQL 语句可以在 FreshRSS 的数据库中执行，以实现这一目的。

**如何执行 SQL 语句？**

您可以通过多种方式执行这些 SQL 语句：

* **通过 FreshRSS 后台:** 如果您使用的是 SQLite 数据库，并且 FreshRSS 提供了数据库管理界面（通常在“配置”或“诊断”部分），您可能可以直接在那里执行 SQL。
* **直接进入 FreshRSS 容器:** 使用 `docker exec -it <freshrss_container_name> bash` 进入容器，然后使用数据库客户端（如 `psql` for PostgreSQL 或 `sqlite3` for SQLite）连接到数据库并执行。
* **通过独立的数据库管理工具:** 如果您使用外部数据库（如 PostgreSQL 或 MySQL），可以使用 Navicat、DBeaver 等工具连接到数据库并执行。

```sql
-- 1. 替换域名：
--   此语句将所有 FreshRSS_admin_feed 表中 URL 字段包含 'https://rsshub.app' 的链接，
--   替换为 'http://rsshub: 1200'。这通常用于将外部 RSSHub 服务切换到内部自建服务。
UPDATE freshrss_admin_feed SET url = REPLACE(url, 'https://rsshub.app', 'http://rsshub:1200') WHERE url LIKE '%rsshub.app%';

-- 2. 新增不带?的 query 参数：
--   如果您的 RSSHub 需要一个认证 key 作为查询参数，而有些现有链接已经包含其他查询参数（即 URL 中有 ''?''），
--   此语句会在现有参数后追加 '&key = hNppGJJokue7'。
UPDATE freshrss_admin_feed SET url = url || '&key=hNppGJJokue7' WHERE url LIKE '%rsshub:1200%' AND url LIKE '%?%';

-- 3. 新增带?的 query 参数：
--   如果您的 RSSHub 需要一个认证 key 作为查询参数，而有些现有链接尚未包含任何查询参数（即 URL 中没有 ''?''），
--   此语句会在 URL 后直接添加 '?key = hNppGJJokue7'。
UPDATE freshrss_admin_feed SET url = url || '?key=hNppGJJokue7' WHERE url LIKE '%rsshub:1200%' AND url NOT LIKE '%?%';
```

**执行前注意事项：**

* **备份数据库:** 在执行任何批量数据库操作之前，务必备份 FreshRSS 的数据库，以防意外发生。
* **替换 `key=hNppGJJokue7`:** 将 `hNppGJJokue7` 替换为您实际的 RSSHub 认证密钥。
* **替换 `http://rsshub:1200`:** 如果您的 RSSHub 服务地址不同，请替换为实际地址。注意，如果 FreshRSS 和 RSSHub 在同一个 Docker 网络中，可以使用服务名（如 `rsshub`）和容器内部端口。

### 3.2. PubsubHubbub

**PubSubHubbub**（现在通常被称为 **WebSub**）是一种用于互联网上内容发布的 **开放式、去中心化、基于 HTTP 的推送协议**。

它的核心目的是将传统的“拉取（Pull）”式内容更新机制，转变为“推送（Push）”式更新，从而实现近乎实时的信息发布和接收。

#### 3.2.1. 为什么需要它？

在传统的 RSS（Really Simple Syndication，简易信息聚合）或 Atom（一种用于 Web 内容发布的 XML 标准）订阅中，订阅者（例如 RSS 阅读器）需要定期去检查发布者的服务器是否有新内容。如果发布者更新频率不高，这种不断查询的行为会浪费大量的网络资源和计算能力，且会有明显的延迟。

#### 3.2.2. 它是如何工作的？

PubSubHubbub 引入了一个中介角色——**Hub（中心枢纽）**，其流程如下：

* **发布者（Publisher）：** 当有新内容发布时，发布者会向 Hub 发送一个通知，告知 Hub 哪个 Feed（信息源）更新了。
* **中心枢纽（Hub）：** Hub 接收到通知后，会主动地、立刻地将更新内容推送给所有已经订阅该 Feed 的订阅者。
* **订阅者（Subscriber）：** 订阅者不再需要轮询发布者，只需等待 Hub 将更新推送到其指定的 Webhook（网络钩子）地址即可。

### 3.3. RSS 订阅链接

FreshRSS 允许您为不同的分类或所有文章生成 RSS 订阅链接，这些链接可以用于其他 RSS 阅读器或服务进行订阅。这对于将 FreshRSS 作为 RSS 源管理中心，并通过其他客户端阅读的用户非常有用。

#### 3.3.1. 方案一：通过分类 ID 生成订阅链接

这种方法适用于您想要订阅 FreshRSS 中特定分类下的所有文章。您需要 FreshRSS 的 `BASE_URL`、您的管理员用户名、API Token 以及分类的 ID (`c_X`，其中 `X` 是分类的数字 ID)。

```
https://freshrss.example.com/i/?a=rss&user=admin&token=123&hours=168&&get=c_5 # 其中c_5 对应的是分类id
```

* **`https://freshrss.example.com`**: 您的 FreshRSS 部署的 `BASE_URL`。
* **`user=admin`**: 您的 FreshRSS 用户名，通常是 `admin`。
* **`token=123`**: 您的 FreshRSS 用户的 API Token。您可以在 FreshRSS 后台的 “`认证`” -> “`API`” 设置中找到或生成。
* **`hours=168`**: 可选参数，指定订阅源获取多少小时内的数据。`168` 小时等于 7 天。
* **`get=c_5`**: 关键参数，`c_5` 表示订阅 ID 为 `5` 的分类。您可以在 FreshRSS 后台的“`订阅源`”或“`分类`”管理页面中查看各个分类的 ID。例如，`c_all` 表示所有订阅源。

**如何获取分类 ID？**

在 FreshRSS 的 Web 界面中，当您点击某个分类时，浏览器地址栏的 URL 中会包含该分类的 ID (例如 `.../i/?c=5`)。取 `c=` 后面的数字即可。

#### 3.3.2. 方案二：使用自定义查询生成订阅链接

FreshRSS 提供了强大的自定义查询功能，您可以根据标签、关键词、是否已读等条件来过滤文章，并为这些自定义视图生成 RSS 订阅链接。这为您提供了极大的灵活性，可以创建高度定制化的信息流。

* **操作步骤：**
    1. 登录 FreshRSS 后台。
    2. 在左侧导航栏找到“`智能过滤器`”或“`过滤器`”部分。
    3. 创建一个新的智能过滤器，或者编辑现有过滤器。
    4. 定义您的过滤规则，例如包含特定标签、排除特定关键词、只显示未读文章等。
    5. 保存过滤器后，通常会在过滤器列表旁边或详情页面找到一个“`RSS`”图标或链接。点击它，即可获取该自定义查询的 RSS 订阅链接。该链接通常会包含一个 `filter` 参数来标识您的自定义过滤器。

### 3.4. CLI 工具：folocli

`folocli` 是一个由社区开发的命令行工具，旨在帮助用户更方便地管理 FreshRSS 订阅、文章和相关操作。它提供了一种通过终端与 FreshRSS 交互的方式，特别适合喜欢命令行操作、自动化脚本或者进行批量操作的用户。

**安装 folocli：**

`folocli` 通常通过 `npm` 或 `pnpm` 进行安装，确保您的系统已安装 Node.js 和 npm/pnpm。

```bash
pnpm install -g folocli@latest
# 或者使用 npm:
# npm install -g folocli@latest
```

安装完成后，您可以通过 `folo --help` 命令查看所有可用的命令和选项，了解其功能。

```bash
folo --help
```

**folocli 的常见用途：**

* **管理订阅源:** 添加、删除、列出订阅源。
* **管理文章:** 标记文章为已读/未读，星标文章，删除文章。
* **同步操作:** 手动触发 FreshRSS 的订阅源更新。
* **统计信息:** 获取 FreshRSS 的统计数据，如未读文章数量。
* **脚本自动化:** 将 `folocli` 命令集成到自动化脚本中，实现定时清理、状态报告等。

**示例用法 (假设已配置好 FreshRSS 的 API 访问):**

在使用 `folocli` 之前，您通常需要配置 FreshRSS 的 API 访问凭据 (URL, 用户名, API 密码)，这些可以通过 `folocli` 的配置命令或环境变量设置。

```bash
# 查看所有订阅源
folo list feeds

# 标记所有文章为已读
folo mark-read all

# 添加一个新的订阅源 (假设需要 FreshRSS 的 BASE_URL, 用户名, API 密码已配置)
# folo add feed "https://example.com/feed.xml" --title "Example Blog" --category "Tech"

# 触发所有订阅源的更新
folo update
```

`folocli` 极大地扩展了 FreshRSS 的使用场景，使其不仅仅局限于网页界面操作，为高级用户提供了更强大的控制能力。

## 4. 拓展

### 4.1. 在线聚合平台

除了自建 FreshRSS，市面上也有一些提供 RSS 聚合服务的在线平台。这些平台通常提供托管服务，方便用户无需自行部署即可享受 RSS 订阅功能，但可能在数据隐私和定制性方面有所限制。

* **RSS Mix:** 一个允许用户混合多个 RSS 源以创建新聚合源的工具。它不是一个完整的 RSS 阅读器，更像是一个 RSS 源的“搅拌器”或“合并器”，可以帮助用户创建更定制化的信息流。

### 4.2. 竞品对比

了解 FreshRSS 的竞品可以帮助您更好地评估其优缺点，并选择最适合您需求的 RSS 聚合器。以下是一些与 FreshRSS 功能类似的自托管 RSS 阅读器：

* **MiniFlux:** MiniFlux 是另一个轻量级、开源的 RSS/Atom 阅读器。它以简洁的用户界面、高性能和最小化的依赖性而闻名。与 FreshRSS 相比，MiniFlux 可能在功能上更专注于核心的 RSS 阅读体验，扩展性可能不如 FreshRSS 丰富，但其简洁的设计也吸引了一部分用户。
* **The Old Reader:** 这是一个模仿 Google Reader 经典界面的在线 RSS 阅读器，提供了类似社交分享的功能。它是一个托管服务，而非自托管，适合喜欢传统 RSS 阅读体验的用户。
* **Inoreader / Feedly:** 这些是功能强大的商业在线 RSS 阅读器，提供丰富的订阅管理、内容过滤、搜索、自动化和多平台同步功能。它们通常有免费版和付费高级版，适合对功能要求较高且不介意使用托管服务的用户。

### 4.3. 与 RSSHub 的区别

* RSSHub（内容生产者）： 它解决的是 “有没有” 的问题。它的唯一任务是数据转换。把原本没有 RSS 的万物（网页、APP、音频、视频）强行翻译成标准 RSS 格式。它本身不存储历史数据，也不记录你的阅读状态。
* RSS 聚合服务器（内容管理者）： 它解决的是 “好不好用” 的问题。它的唯一任务是状态同步与管理。它负责订阅 RSSHub 生产出来的链接，并全天候自动下载、保存内容，同时记录你每一篇文章是“已读”还是“未读”。￼

### 4.4. 高级设置

FreshRSS 提供了许多高级设置，允许用户根据自己的需求精细调整其行为。这些设置通常可以在 FreshRSS 后台的“`配置`”或“`系统`”菜单中找到。

* **增量更新 (Incremental Updates):**
  * **解释:** 增量更新是指 FreshRSS 在抓取订阅源时，只会下载自上次更新以来新增的文章，而不是重新下载整个 Feed。这显著减少了网络带宽和服务器资源的消耗，并加快了更新速度。
  * **配置:** FreshRSS 通常默认启用增量更新。您可以在“`配置`”->“`更新`”或类似部分查找相关选项，确保它已启用。

* **刷新频率 (Update Frequency):**
  * **解释:** 这决定了 FreshRSS 自动检查和抓取订阅源新内容的频率。根据订阅源的活跃程度，您可以设置不同的刷新频率。
  * **配置:** 在“`配置`”->“`更新`”中，您可以设置全局的默认刷新频率（例如，每 15 分钟、每小时）。对于单个订阅源，通常也可以在编辑订阅源时覆盖全局设置，为其指定更频繁或更不频繁的更新间隔。
  * **注意事项:** 过于频繁的刷新可能会给发布者的服务器带来不必要的负担，甚至可能导致您的 IP 被暂时屏蔽。请根据实际情况合理设置。

* **自动过期 (Automatic Purging):**
  * **解释:** 为了避免数据库过大和保持性能，FreshRSS 可以配置为自动删除旧文章或已读文章。这有助于管理存储空间。
  * **配置:** 在“`配置`”->“`清理`”或“`数据保留`”部分，您可以设置：
    * **保留天数:** 例如，只保留最近 30 天的文章。
    * **保留未读文章:** 即使文章已过期，如果它仍然是未读状态，可以选择不删除。
    * **保留星标文章:** 星标文章通常会被永久保留，除非您手动删除。确保此选项符合您的需求。

### 4.5. RSS 与 Google Reader API 协议

在 FreshRSS 的生态系统中，RSS/Atom 协议与 Google Reader API 协议扮演着不同的、但又相互协作的角色，共同提供了一个完善的信息聚合和阅读体验：

1. **后端内容获取 (RSS/Atom):**
    * **职责:** FreshRSS 服务器作为后端，其核心任务是使用标准的 RSS (Really Simple Syndication) 和 Atom 协议，定时从您订阅的各个信息源（如博客、新闻网站、RSSHub 实例）“拉取”最新的文章内容。
    * **机制:** 这是一种传统的“拉取”机制，FreshRSS 会按照您设定的刷新频率，主动访问这些 RSS/Atom Feed 的 URL，并将抓取到的新文章存储到其内部数据库中。

2. **多端同步与状态管理 (Google Reader API):**
    * **职责:** Google Reader API 是 FreshRSS 提供的一个兼容接口。它允许各种支持此 API 的第三方客户端（例如 Android 上的 FeedMe、macOS 上的 NetNewsWire 等）与 FreshRSS 服务器进行通信，实现阅读状态（已读/未读）、星标、订阅管理等信息的双向同步。
    * **机制:** 当您在移动设备上的客户端中阅读文章、将其标记为已读、或者取消订阅某个 Feed 时，客户端会通过 Google Reader API 将这些操作“推送”给 FreshRSS 服务器。FreshRSS 服务器接收到这些指令后，会更新其数据库中的相应状态，从而确保您的阅读进度在所有连接的设备上保持一致。

**总结:**

* **RSS/Atom:** 是 FreshRSS 用来 **从外部获取内容** 的标准格式和协议。
* **Google Reader API:** 是 FreshRSS 用来 **与客户端应用进行通信并同步用户阅读状态** 的桥梁。

这两个协议互补协作，使得 FreshRSS 能够既作为一个强大的内容聚合后端，又能与丰富的客户端生态系统无缝集成，提供灵活多样的阅读方式。

### 4.6. 遇到的问题：反爬限制

在使用 FreshRSS 订阅某些网站的 RSS 源时，可能会遇到反爬机制导致的抓取失败。这通常表现为 FreshRSS 无法获取到最新的文章内容，或者在日志中显示抓取错误。

* **原因分析：**
  * **User-Agent 检测:** 很多网站会检测访问者的 User-Agent 字符串。如果检测到是爬虫或非浏览器请求，可能会拒绝服务。
  * **IP 限制/频率限制:** 某些网站会对来自同一 IP 地址的访问频率进行限制。如果 FreshRSS 频繁抓取，可能会被临时封禁。
  * **JavaScript 渲染:** 一些现代网站的内容是动态通过 JavaScript 渲染的，而 FreshRSS 默认只抓取原始 HTML。对于这类网站，传统的 RSS 抓取方式可能无法获取完整内容。
  * **CDN/WAF 阻拦:** 网站可能使用了 CDN 或 Web 应用防火墙 (WAF)，这些服务会识别并阻挡可疑的爬虫请求。

* **潜在解决方案：**
  * **调整抓取频率:** 尝试降低 FreshRSS 对特定订阅源的抓取频率，避免触发网站的频率限制。
  * **使用 RSSHub:** 对于反爬限制较严的网站，如果直接订阅困难，可以尝试通过 [[RSSHub]] 来生成 RSS 源。RSSHub 专门处理复杂网站的内容抓取，并将其转换为标准 RSS 格式。
  * **更换 IP 地址:** 如果是 IP 限制，更换 FreshRSS 服务器的出口 IP 可能会有帮助（但这通常涉及到更复杂的网络配置）。
  * **检查 FreshRSS 日志:** 详细查看 FreshRSS 的错误日志，通常能找到具体的错误信息，有助于诊断问题。

### 4.7. Folo 中订阅 FreshRSS 链接不更新问题

在使用 `folocli` 或其他客户端订阅 FreshRSS 提供的 RSS 链接时，有时会遇到链接不更新或无法获取新内容的问题。这可能涉及多个环节的配置问题。

* **问题描述：** 客户端（如 Folo）成功订阅了 FreshRSS 的 RSS 链接，但无法获取到 FreshRSS 后端抓取到的新文章。

* **尝试解决：通过 Nginx 覆写去除 query 参数 -> 无效**
  * **分析：** 尝试去除 URL 中的查询参数（例如 `?key=xxx`）来解决。这种方法可能基于的假设是，查询参数导致了缓存问题或者 Nginx 无法正确处理。
  * **结果：** 实验证明这种方法无效，表明问题可能不在于查询参数本身或者 Nginx 的 URL 覆写。

* 最终结论
  * 隔了一个晚上，发现可 nginc 代理日志中有抓取日志，但是平频率非常低，猜测 folo 的模式当前中心抓取机制，并且大的 rss 源会高频抓取+高级爬取等措施，而小的 rss 则是低频的

## 5. 参考资料

* [FreshRSS 官方文档](https://freshrss.github.io/FreshRSS/en/users/02_First_steps.html)
  * 这是获取 FreshRSS 最新、最权威信息的最佳来源，涵盖了安装、配置、使用和故障排除的各个方面。
* [FreshRSS GitHub 仓库](https://github.com/FreshRSS/FreshRSS)
  * 查看项目源码、提交问题、参与贡献或了解最新开发进展。
* [WebSub (原 PubSubHubbub) 规范](https://www.w3.org/TR/websub/)
  * 深入了解 WebSub 协议的工作原理及其优势。
