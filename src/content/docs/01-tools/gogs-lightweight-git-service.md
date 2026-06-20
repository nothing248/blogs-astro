---
title: "Gogs安装"
filename: gogs-lightweight-git-service
description: Gogs是采用Go语言编写的极轻量级自建Git服务。本文介绍了在裸机（Linux）上部署Gogs的步骤。内容涵盖新建git运行用户、MySQL数据库表导入与配置文件设定，并阐述了利用守护程序使Gogs持续在后台稳定运行的方法，完美解决低资源服务器上的代码私有托管需求。
tags: [gogs, git-service, go-language, self-hosting]
aliases: [Gogs安装, 轻量级Git, Gogs配置]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 11:59:28 中午
---

<!-- toc -->

## 1. 简介

一个私有的 git 仓库

## 2. 安装

- 安装 mysql(非必须。可以使用 sqllite)  
参考 mysql 教程

- 安装 git(必须的)  
参考 git 教程

- 裸机安装 gogs

```shell
sudo -s
mkdir /opt/software
cd /opt/software
useradd -s /bin/bash -m git #创建用户
echo 'git ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers #添加免密登陆
su git
wget https://dl.gogs.io/0.13.0/gogs_0.13.0_linux_amd64.tar.gz
tar zxvf gogs_0.13.0_linux_amd64.tar.gz
cd gogs
```

## 3. 配置

```
#/opt/software/gogs/custom/conf/app.ini
BRAND_NAME = Gogs
RUN_USER   = git
RUN_MODE   = prod

[database]
TYPE     = mysql
HOST     = 127.0.0.1:3307
NAME     = gogs
SCHEMA   = public
USER     = root
PASSWORD = example
SSL_MODE = disable
PATH     = /opt/software/gogs/data/gogs.db

[repository]
ROOT           = /opt/software/gogs/gogs-repositories
DEFAULT_BRANCH = master

[server]
PROTOCOL = https #开启https
DOMAIN           = gogs.wsl.sxyxy.top
HTTP_PORT        = 3000
EXTERNAL_URL     = https://gogs.wsl.sxyxy.top:3000/
DISABLE_SSH      = false
SSH_PORT         = 22
SSH_ROOT_PATH = /home/git/.ssh #ssh地址
REWRITE_AUTHORIZED_KEYS_AT_START = true
START_SSH_SERVER = false #不建议开启，使用系统的服务即可
OFFLINE_MODE     = false 
USE_CERTIFICATE = true
CERT_FILE = custom/https/cert.crt
KEY_FILE = custom/https/key.key


[email]
ENABLED = true
HOST = smtp.163.com:456
FROM = example@163.com
USER = example@163.com
PASSWD = ***


[auth]
REQUIRE_EMAIL_CONFIRMATION  = true
DISABLE_REGISTRATION        = false
ENABLE_REGISTRATION_CAPTCHA = true
REQUIRE_SIGNIN_VIEW         = true

[user]
ENABLE_EMAIL_NOTIFICATION = true

[picture]
DISABLE_GRAVATAR        = false
ENABLE_FEDERATED_AVATAR = false

[session]
PROVIDER = file

[log]
MODE      = file
LEVEL     = Info
ROOT_PATH = /opt/software/gogs/log

[security]
INSTALL_LOCK = true
SECRET_KEY   = L9S3NQi7yhtdy9C
LOCAL_NETWORK_ALLOWLIST = "jenkins.example.com" #允许网络，woobhook推送到本地是可能需要
```

> 注意 github 上的配置文件分支

## 4. 配置开机自启动

```shell
# /etc/systemd/system/gogs.service
[Unit]
Description=Gogs
After=syslog.target
After=network.target
After=mariadb.service mysql.service mysqld.service postgresql.service memcached.service redis.service

[Service]
# Modify these two values and uncomment them if you have
# repos with lots of files and get an HTTP error 500 because
# of that
###
#LimitMEMLOCK = infinity
#LimitNOFILE = 65535
Type=simple
User=git
Group=git
WorkingDirectory=/opt/software/gogs
ExecStart=/opt/software/gogs/gogs web
Restart=always
Environment=USER=git HOME=/opt/software/gogs

# Some distributions may not support these hardening directives. If you cannot start the service due
# to an unknown option, comment out the ones not supported by your version of systemd.
ProtectSystem=full
PrivateDevices=yes
PrivateTmp=yes
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## 5. 管理服务

```shell
systemctl daemon-reload #重启 systemd 服务
systemctl restart gogs
systemctl status gogs
systemctl stop gogs
```

## 6. 开启 ssh 服务

- 安装

```shell
sudo -s
apt install openssh-server
```

- 配置

```
# /etc/ssh/sshd_config
Port = 23
```

- 服务

```shell
systemctl start ssh
systemctl status ssh
systemctl stop ssh
```

- 切换 ssh 默认用户

```
# 创建用户
useradd -s /bin/bash -m gogs
#修改源文件权限
chown -R gogs:gogs /opt/gogs 
# service文件
User=git
Group=git
Environment=USER=git HOME=/opt/software/gogs
# 配置文件
#/opt/software/gogs/custom/conf/app.ini
RUN_USER   = git

[server]
SSH_ROOT_PATH = /home/git/.ssh #ssh地址
# 重启服务
systemctl restart gogs

# 测试服务
git -T gogs
ssh -T gogs@exampel.com
```

- 配置 webhook

```shell
https://jenkins.exampl.com/gogs-webhook/?job=test
```

> job 对应的 query 参数需要 jenkins 的 job 配置保持一致，如果存在目录则 dir/test

## 7. 拓展信息

### 7.1. 出现邮件配置无效

参考指定配置文件版本进行配置，不同的配置文件配置参数可能不一致

### 7.2. 配置 ssl 无效

- 注意 PROTOCOL 参数使用设置为 https

### 7.3. 出现 crsf 非法

清除 cookie 之后重试

## 8. 参考资料

- [官方文档](https://gogs.io/)
- [配置文件](https://github.com/gogs/gogs/blob/main/conf/app.ini)
