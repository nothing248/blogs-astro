---
title: "禅道安装教程"
filename: zentao-pms-installation-guide
summary: 禅道（ZenTao）是一款专为敏捷开发团队设计的全生命周期项目管理软件。本文详细记录了在 Ubuntu 环境下基于 PHP 7.4 + Nginx + MySQL 的裸机安装步骤。内容涵盖了 FastCGI 接口配置、SSL 证书集成以及包含产品、项目、测试等核心模块的组织架构初始化建议，是企业内部构建研发协同系统的参考指南。
tags: [project-management, agile, zentao, php, server-admin]
aliases: [禅道安装教程]
status: completed
date created: 星期一, 九月 22日 2025, 5:12:53 下午
date modified: 星期五, 六月 19日 2026, 12:09:32 中午
---

<!-- toc -->

## 1. 简介

禅道（ZenTao）集产品管理、项目管理、质量管理、文档管理、组织管理和事务管理于一体。它基于敏捷开发方法论（Scrum），能够覆盖软件研发的全生命周期。

## 2. 部署流程 (LNMP 架构)

### 2.1. 环境依赖安装 (PHP 7.4)

```shell
sudo add-apt-repository ppa:ondrej/php
sudo apt update
sudo apt install php7.4 php7.4-fpm php7.4-mysql php7.4-curl php7.4-mbstring
```

### 2.2. 源码下载与解压

```shell
cd /opt/software
wget https://www.zentao.net/dl/zentao/20.4/ZenTaoPMS-20.4-php7.2_7.4.zip
unzip ZenTaoPMS-20.4-php7.2_7.4.zip -d zentaopms
```

### 2.3. Nginx 站点配置

```nginx
server {
    listen 443 ssl;
    server_name [你的域名];

    ssl_certificate /https/cert.crt;
    ssl_certificate_key /https/key.key;

    root /opt/software/zentaopms/www;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
    }
}
```

## 3. 系统初始化

1. **Web 安装**：访问 `https://[你的域名]/install.php` 按照向导连接数据库。
2. **组织管理**：
   - 建立部门与职位。
   - 分配用户权限。
3. **流程核心**：
   - **产品**：管理需求与计划。
   - **项目/执行**：管理任务与迭代。
   - **测试**：管理用例、Bug 与版本。

## 4. 拓展信息

### 4.1. 依赖组件

- **数据库**：MySQL/MariaDB。
- **解析器**：PHP (建议 7.2-7.4)。
- **Web 服务器**：Nginx 或 Apache。

## 5. 参考资料

- [禅道官方下载与安装文档](https://www.zentao.net/download/)
