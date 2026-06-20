---
title: "Supervisor进程管理"
filename: supervisor-setup-guide
description: Supervisor 进程守护管理工具的安装与配置指南。Supervisor 是基于 Python 研发的进程管理程序。本指南涵盖 CentOS 与 pip 安装手段，详细解析了 supervisord.conf 配置参数（含 Unix/HTTP socket、日志轮转、web管理与子配置文件包含），重点阐释了 [program:xx] 进程守护模块的启动参数定义，并汇总了 supervisorctl 的常用运维管理指令。
tags:
  - supervisor
  - process-manager
  - linux-administration
  - python-tool
aliases:
  - Supervisor进程管理
  - supervisord配置详解
  - supervisorctl常用命令
status: completed
date created: 星期二, 二月 25日 2025, 3:23:54 下午
date modified: 星期二, 六月 16日 2026, 6:24:21 晚上
---

<!-- toc -->

## 1. 简介

Supervisor 是一款使用 Python 开发的进程管理及守护工具，能够对单机进程进行方便的监控与管理。

## 2. 安装

- **CentOS 安装**

```shell
yum install supervisor
```

- **通过 pip 安装**

```shell
pip install supervisor
```

## 3. 配置文件

主要配置文件路径包括 `/etc/supervisord.conf`，常通过子配置文件目录 `/etc/supervisord.conf.d` 进行多应用管理。

```ini
[unix_http_server]
file=/tmp/supervisor.sock   ; UNIX socket 文件，supervisorctl 会使用
;chmod=0700                 ; socket文件的mode，默认是0700
;chown=nobody:nogroup       ; socket文件的owner，格式：uid:gid

;[inet_http_server]         ; HTTP服务器，提供web管理界面
;port=127.0.0.1:9001        ; Web管理后台运行的IP和端口，如果开放到公网，需要注意安全性
;username=user              ; 登录管理后台的用户名
;password=123               ; 登录管理后台的密码

[supervisord]
logfile=/tmp/supervisord.log ; 日志文件，默认是 $CWD/supervisord.log
logfile_maxbytes=50MB        ; 日志文件大小，超出会rotate，默认 50MB，如果设成0，表示不限制大小
logfile_backups=10           ; 日志文件保留备份数量默认10，设为0表示不备份
loglevel=info                ; 日志级别，默认info，其它: debug,warn,trace
pidfile=/tmp/supervisord.pid ; pid 文件
nodaemon=false               ; 是否在前台启动，默认是false，即以 daemon 的方式启动
minfds=1024                  ; 可以打开的文件描述符的最小值，默认 1024
minprocs=200                 ; 可以打开的进程数的最小值，默认 200

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; 通过UNIX socket连接supervisord，路径与unix_http_server部分的file一致
;serverurl=http://127.0.0.1:9001 ; 通过HTTP的方式连接supervisord

; 包含其它配置文件
[include]
files = relative/directory/*.ini    ; 可以指定一个或多个以.ini结束的配置文件

; [program:xx]是被管理的进程配置参数，xx是进程的名称
[program:xx]
command=/opt/apache-tomcat-8.0.35/bin/catalina.sh run  ; 程序启动命令
autostart=true       ; 在supervisord启动的时候也自动启动
startsecs=10         ; 启动10秒后没有异常退出，就表示进程正常启动了，默认为1秒
autorestart=true     ; 程序退出后自动重启,可选值：[unexpected,true,false]，默认为unexpected，表示进程意外杀死后才重启
startretries=3       ; 启动失败自动重试次数，默认是3
user=tomcat          ; 用哪个用户启动进程，默认是root
priority=999         ; 进程启动优先级，默认999，值小的优先启动
redirect_stderr=true ; 把stderr重定向到stdout，默认false
stdout_logfile_maxbytes=20MB  ; stdout 日志文件大小，默认50MB
stdout_logfile_backups = 20   ; stdout 日志文件备份数，默认是10
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile=/opt/apache-tomcat-8.0.35/logs/catalina.out
stopasgroup=false     ; 默认为false,进程被杀死时，是否向这个进程组发送stop信号，包括子进程
killasgroup=false     ; 默认为false，向进程组发送kill信号，包括子进程
```

---

## 4. 使用说明

### 4.1. 启动 supervisor

```shell
supervisord -c /etc/supervisord.conf
```

### 4.2. 管理命令

```shell
supervisorctl status        # 查看所有进程的状态
supervisorctl stop es       # 停止 es 进程
supervisorctl start es      # 启动 es 进程
supervisorctl restart es    # 重启 es 进程
supervisorctl update        # 配置文件修改后，重载并加载新的配置
supervisorctl reload        # 重新启动配置中的所有守护程序
```
