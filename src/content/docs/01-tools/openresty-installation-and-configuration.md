---
title: "OpenResty安装"
filename: openresty-installation-and-configuration
summary: OpenResty 是一款基于 Nginx 与 Lua 的高性能 Web 平台。本文介绍了在 Ubuntu 环境下的标准安装流程及服务管理方法。重点探讨了 Nginx 配置文件中的复杂正则表达式应用（如环视断言），并详细解析了 Location 匹配优先级。同时通过实战示例展示了如何实现“拦截非指定后缀文件访问”的安全策略，适用于构建高性能、可编程的网关服务。
tags: [openresty, nginx, lua, api-gateway, web-server, regex]
aliases: [OpenResty安装, Nginx正则配置, 高性能网关]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:24 下午
date modified: 星期五, 六月 19日 2026, 12:07:12 中午
---

<!-- toc -->

## 1. 简介

OpenResty 是一个基于 Nginx 的全功能 Web 平台，它打包了标准的 Nginx 核心、许多高质量的 Lua 库、第三方模块以及大多数依赖项。它允许开发者在 Nginx 内部直接运行 Lua 脚本，从而构建极高并发的动态 Web 应用和网关。

## 2. 安装指南 (Ubuntu)

推荐使用官方包管理器进行安装以确保稳定性：

```shell
# 安装编译与网络依赖
sudo apt-get install libpcre3-dev libssl-dev perl make build-essential curl wget gnupg ca-certificates lsb-release

# 导入官方 GPG 密钥
wget -O - https://openresty.org/package/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/openresty.gpg

# 添加 APT 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/openresty.gpg] http://openresty.org/package/ubuntu $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/openresty.list > /dev/null

# 更新并安装
sudo apt-get update
sudo apt-get -y install openresty
```

## 3. 服务管理

OpenResty 安装后注册为 systemd 服务，使用以下命令管理：

```shell
sudo systemctl start openresty    # 启动
sudo systemctl restart openresty  # 重启
sudo systemctl stop openresty     # 停止
sudo systemctl status openresty   # 查看状态
```

## 4. 核心配置与进阶技巧

### 4.1. 结构化配置建议

建议将站点配置独立出来，保持主配置文件简洁：

```nginx
# /etc/openresty/nginx.conf
http {
    # 引入外部配置目录
    include /etc/openresty/conf.d/*.conf;
}
```

### 4.2. Location 匹配优先级

理解优先级是排查配置问题的关键：

| 修饰符 | 匹配类型 | 优先级 |
| :--- | :--- | :--- |
| `=` | 精确匹配 | 1 (最高) |
| `^~` | 最佳前缀匹配（不检查正则） | 2 |
| `~` / `~*` | 正则表达式匹配（区分/不区分大小写） | 3 |
| (无) | 普通前缀匹配 | 4 |

### 4.3. 复杂正则：环视断言 (Lookaround)

OpenResty 中的正则基于 PCRE，支持强大的环视断言。

- **`(?=...)` 正向先行断言**：后面必须跟着某内容。
- **`(?!...)` 负向先行断言**：后面不能跟着某内容。
- **`(?<=...)` 正向后行断言**：前面必须跟着某内容。
- **`(?<!...)` 负向后行断言**：前面不能跟着某内容。

> [!warning]
> **后行断言限制**：后行断言通常只支持固定长度的字符串，不能包含 `*` 或 `+` 等量词。

### 4.4. 实战示例：文件访问白名单

以下配置实现了“仅允许访问特定后缀文件，其他请求一律拦截”：

```nginx
server {
    listen 80;
    server_name blogs.example.com;
    root /var/www/blogs;

    # 1. 默认处理：支持 SPA 路由
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 2. 匹配不包含 "." 的纯路径
    location ~* ^\/[a-zA-Z0-9\/_\-]*$ {
        try_files $uri $uri/ /index.html;
    }

    # 3. 安全拦截：拒绝非白名单后缀的访问
    # 使用负向后行断言，排除 .md, .html, .ico
    location ~* .+(?<!\.md|html|ico)$ {
        deny all;
    }
}
```

## 5. 参考资料

- [OpenResty 官方网站 (中文)](https://openresty.org/cn/)
- [OpenResty GitHub 仓库](https://github.com/openresty/openresty)
