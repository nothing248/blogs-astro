---
status: completed
filename: aliyun-ecs-maintenance-and-optimization
title: "阿里云服务器维护"
summary: 本笔记整理了针对阿里云 ECS 服务器的一系列深度运维与优化措施。内容涵盖 SSH 证书快速同步方案、系统安全/监控组件（云监控、安防插件、云助手）的停用与卸载方法，旨在降低资源占用并避免不必要的系统干预。此外，详细介绍了 Journald 日志滚动策略优化、Swap 虚拟内存的手动构建与持久化挂载步骤，以及利用 MTR 进行网络链路压测的实战技巧。
aliases: [阿里云服务器维护, ECS 性能调优, 停用云盾插件, Swap 虚拟内存配置]
tags: [阿里云, ECS, Linux 运维, 性能优化, 安全加固, Swap 配置, 系统日志, 运维脚本]
date created: 星期三, 四月 1日 2026, 11:29:58 晚上
date modified: 星期四, 六月 18日 2026, 8:45:00 晚上
---

<!-- toc -->

## 1. 证书管理与同步

快速实现多机互信：

```bash
ssh-keygen  
ssh-copy-id root@[Target_IP]  
# 自动扫描并添加已知主机指纹
ssh root@[Intermediate_IP] "ssh-keyscan [Final_IP] >> ~/.ssh/known_hosts"
```

---

## 2. 移除冗余云端控件 (精简系统)

> [!warning] 卸载前评估
> 停用云监控和防护插件将导致 Web 控制台无法显示实时监控数据及安全告警，请确认已具备替代方案。

### 2.1. A. 卸载云监控插件 (CloudMonitor)

```bash
bash /usr/local/cloudmonitor/cloudmonitorCtl.sh stop  
bash /usr/local/cloudmonitor/cloudmonitorCtl.sh uninstall  
rm -rf /usr/local/cloudmonitor
```

### 2.2. B. 卸载安防插件 (AliYunDun / Aegis)

```bash
wget "http://update2.aegis.aliyun.com/download/uninstall.sh" 
chmod +x uninstall.sh && ./uninstall.sh  
```

### 2.3. C. 停用云助手 (Assist-Daemon)

```bash
/usr/local/share/assist-daemon/assist_daemon --stop  
systemctl stop aliyun.service  
```

---

## 3. 系统日志滚动优化 (Journald)

防止日志占满磁盘，修改 `/etc/systemd/journald.conf`：

```ini
SystemMaxUse=500M      # 最大占用空间
SystemMaxFileSize=100M # 单个文件上限
MaxRetentionSec=1month # 保留时长
```

**生效管理**：

```bash
systemctl restart systemd-journald
```

---

## 4. Swap 虚拟内存实战配置

### 4.1. 第一步：创建并启用 Swap 文件

```bash
dd if=/dev/zero of=/mnt/swapfile bs=1M count=1024 # 1G 空间
mkswap /mnt/swapfile  
chmod 600 /mnt/swapfile
swapon /mnt/swapfile  
```

### 4.2. 第二步：持久化挂载

在 `/etc/fstab` 中追加：

```text
/mnt/swapfile none swap sw 0 0
```

### 4.3. 第三步：内核参数调优 (`/etc/sysctl.conf`)

```ini
vm.swappiness=60         # 积极使用 Swap 的倾向（0-100）
vm.vfs_cache_pressure=50 # 控制内核回收缓存的压力
```

**查看状态**：`swapon --show` 或 `free -h`。

---

## 5. 网络链路质量测试

- **基础测试**：`ping -c 50 www.google.com`
- **深度路径分析**：安装 `mtr` 实时查看每一跳的丢包率与延迟波动。

```bash
apt install mtr
mtr www.google.com
```
