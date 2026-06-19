---
title: "Redmine 安装指南"
filename: redmine-project-management
summary: Redmine 是一款基于 Ruby on Rails 开发的开源项目管理工具，支持跨平台和多种数据库。本笔记详细介绍了在 Linux 环境下利用 RVM 管理 Ruby 版本，安装 Rails、Rake 及 Bundler 等核心依赖，并完成了 Redmine 5.1.3 的源码安装、数据库迁移及 Secret Token 生成。此外，还提供了结合 Passenger 模块与 Nginx 的生产环境部署配置示例。
tags: [Redmine, Project-Management, Ruby-on-Rails, Nginx, Passenger]
aliases: [Redmine 安装指南]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:30 上午
date modified: 星期五, 六月 19日 2026, 12:07:58 中午
---

<!-- toc -->

## 1. 简介

Redmine 是一款灵活的开源项目管理 Web 应用程序。它使用 Ruby on Rails 框架编写，支持跨平台、多数据库，并提供甘特图、日历、问题跟踪和维基等功能。

## 2. 安装步骤

### 2.1. 环境准备 (RVM & Ruby)

首先需要安装 RVM (Ruby Version Manager) 来管理 Ruby 版本，并安装指定版本的 Ruby。

```shell
# 安装 RVM
bash < <( curl -L https://get.rvm.io ) 
source /etc/profile.d/rvm.sh
# 配置自动激活
echo '[[ -s "/etc/profile.d/rvm" ]] && source "/etc/profile.d/rvm"' > /etc/profile 

# 安装 Ruby 3.2.0
rvm install 3.2.0

# 优化 Gem 更新源 (推荐国内镜像)
gem sources --remove https://rubygems.org/
gem sources -a https://mirrors.cloud.tencent.com/rubygems/
bundle config mirror.https://rubygems.org https://gems.ruby-china.com
```

### 2.2. 安装核心依赖

```shell
# 安装 Rails, Rake 和 Bundler
gem install rails -v '6.1.0'
gem install rake
gem install bundler
```

### 2.3. Redmine 源码安装与配置

```shell
# 拉取并解压项目
cd /opt/software
wget https://www.redmine.org/releases/redmine-5.1.3.tar.gz
tar -zxvf redmine-5.1.3.tar.gz
cd redmine-5.1.3

# 安装依赖项
bundle install --with development test

# 配置文件准备
mv config/database.yml.example config/database.yml
# 需编辑 config/database.yml 进行数据库连接配置

# 初始化系统
bundle exec rake generate_secret_token
RAILS_ENV=production bundle exec rake db:migrate # 必须一次性执行迁移
RAILS_ENV=production bundle exec rake redmine:load_default_data # 加载默认数据

# 临时启动测试
bundle exec rails server -e production
```

## 3. 数据库配置示例

在 `config/database.yml` 中配置 MySQL 连接信息：

```yaml
production:
  adapter: mysql2
  database: redmine
  host: localhost
  username: redmine
  password: "[PASSWORD]" 
  variables:
    transaction_isolation: "READ-COMMITTED" 
```

## 4. Nginx 与 Passenger 部署

为了在生产环境获得更好的性能，建议使用 Passenger 模块集成 Nginx。

### 4.1. 安装 Passenger 模块

```shell
apt-get install libcurl4-openssl-dev
gem install passenger
# 按照指引编译安装 Nginx 模块
passenger-install-nginx-module
```

### 4.2. Nginx 站点配置

```nginx
server {
    listen 443 ssl;
    server_name [DOMAIN]; # 替换为实际域名

    ssl_certificate [SSL_CERT_PATH];
    ssl_certificate_key [SSL_KEY_PATH];

    root /opt/software/redmine-5.1.3/public;
    index index.html index.htm;

    location / {
          try_files $uri/index.html $uri @app;
    }
    
    location @app {
        passenger_enabled on;
        passenger_app_env production;
    }

    # 静态资源缓存优化
    location ~ ^/(images|javascripts|stylesheets|favicon.ico) {
          expires max;
          add_header Cache-Control public;
    }
}
```

## 5. 运行环境依赖

- **编程语言**: Ruby (推荐通过 RVM 管理)
- **数据库**: MySQL / PostgreSQL
- **Web 服务**: Nginx + Passenger / Apache

## 6. 参考资料

- [Redmine 官方下载页](https://www.redmine.org/projects/redmine/wiki/Download)
- [Redmine 中文帮助手册](http://www.redmine.org.cn/manual)
- [RVM 官方网站](https://rvm.io/)

> [!tip] 提示
> 在执行 `db:migrate` 时，请确保环境变量 `RAILS_ENV=production` 正确设置，否则数据可能被写入开发环境数据库。
