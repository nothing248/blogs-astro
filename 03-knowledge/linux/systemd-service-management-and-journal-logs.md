---
status: completed
filename: systemd-service-management-and-journal-logs
title: "Systemd 配置"
description: 本笔记深度解析了 Linux 现代初始化与服务管理器 Systemd 的核心配置。针对 `.service` 配置文件，提供了 Caddy 及 Supervisor 的实战 Unit 模板；详细剖析了 `Type` 属性中 `simple` 与 `forking` 的启动流派差异，以及 `KillMode` (control-group vs mixed vs process) 决定进程树销毁粒度的核心逻辑。此外，总结了清理 `journalctl` 冗余系统日志以释放内存的速查指令，是进阶服务器运维的必读参考。
aliases: [Systemd 配置, systemctl 守护进程, KillMode, forking 模式]
tags: [Linux, 运维部署, Systemd, 进程管理, 守护进程, 日志管理]
date created: 星期一, 十二月 1日 2025, 9:59:22 上午
date modified: 星期四, 六月 18日 2026, 12:25:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Systemd** 是现今大多主流 Linux 发行版的默认初始化系统（init）与系统和服务管理器。它通过 `.service` Unit 文件来管理各种后台守护进程的启动、重启、依赖树及销毁逻辑。

---

## 2. 标准服务配置模板 (`.service`)

一般存放于 `/etc/systemd/system/` 目录下。

### 2.1. 示例 1: 托管 Caddy (前端代理)

```ini
[Unit]
Description=Caddy Proxy Service

[Service]
User=root
# 前台阻塞式运行 (默认 Type=simple)
ExecStart=/usr/bin/caddy run --config /usr/local/etc/Caddyfile
ExecRestart=/usr/bin/caddy reload --config /usr/local/etc/Caddyfile
ExecStop=/usr/bin/caddy stop

[Install]
WantedBy=multi-user.target
```

### 2.2. 示例 2: 托管 Supervisor (进程管理池)

```ini
[Unit]
Description=Supervisor daemon
 
[Service]
User=root
Type=forking  # 必须声明为 forking，因为该指令会在后台派生新进程
ExecStart=/opt/miniconda/envs/audit/bin/supervisord -c /etc/supervisord.conf
ExecStop=/opt/miniconda/envs/audit/bin/supervisorctl shutdown
ExecReload=/opt/miniconda/envs/audit/bin/supervisorctl reload
KillMode=process
Restart=on-failure
RestartSec=42s
 
[Install]
WantedBy=multi-user.target
```

---

## 3. 核心配置属性深度解析

### 3.1. `Type`：启动流派判定

决定 systemd 如何判断该服务是否已“成功启动”。

- **`simple` (默认)**：systemd 认为被 `ExecStart` 唤起的那个原始进程就是主进程。只要该进程不退出，服务就一直处于 running 状态。
- **`forking`**：专为传统的 Unix 守护进程设计。这类程序启动后，会立刻 `fork()` 出一个后台子进程去干活，然后主进程（父进程）自行退出。systemd 看到父进程退出后，会去追踪子进程作为服务主体（通常需配合 `PIDFile` 选项）。

### 3.2. `KillMode`：进程组屠杀策略

决定在执行 `systemctl stop` 时，systemd 如何向目标发送停止信号。

- **`control-group` (默认)**：暴力模式。连锅端掉该 Control Group 中的 **所有剩余子进程**。
- **`mixed`**：优雅模式。先向主进程发送 `SIGTERM` 祈求它自己清理退出；如果超时未响应，再向它派生的所有子进程发送无可阻挡的 `SIGKILL` 强制剿灭。
- **`process`**：只终止主进程。适用于主进程用来“孵化”某些独立后台进程，且你希望主服务挂掉后，那些后台干活的进程能继续存活。
- **`none`**：systemd 不主动发送任何 Kill 信号，完全依赖程序的 `ExecStop` 脚本自己料理后事。

---

## 4. 日志管理与资源释放 (`journalctl`)

Systemd 原生集成了 `journald` 来接管所有服务的控制台输出。如果不加限制，它可能会吃掉巨大的磁盘空间与内存映射。

**释放日志空间的紧急指令**：

```bash
# 1. 强制将还在内存缓冲区中的日志刷入磁盘
journalctl --flush 

# 2. 按体积清理：仅保留最新的 100MB 日志，其余丢弃
journalctl --vacuum-size=100M 

# 3. 按时间清理：仅保留最近 2 小时内的日志
journalctl --vacuum-time=2h 
```

*日常优化：修改 `/etc/systemd/journald.conf` 中的 `SystemMaxUse` 参数持久化限制体积。*

## 5. 参考资料

- [阮一峰：Systemd 教程与命令全解](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)
