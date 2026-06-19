---
title: "Borg备份指南"
filename: borgbackup-deduplicated-backup-guide
summary: BorgBackup 是一款高效的开源去重加密备份软件。本笔记系统梳理了其核心特性（块级去重、高效压缩及客户端 AES-256 加密）、常用操作指令（初始化仓库、创建与恢复备份、FUSE 挂载），并重点详解了自动化配置前端 borgmatic 的 YAML 声明式配置、保留策略与数据库备份，提供了开箱即用的 Linux 定时自动备份工作流。
tags: ["BorgBackup", "Borgmatic", "Backup-Tools", "Linux-Sysadmin", "Data-Security"]
aliases: ["Borg备份指南", "borgmatic配置", "Linux自动备份"]
status: completed
date created: 星期二, 三月 10日 2026, 11:13:46 上午
date modified: 星期五, 六月 19日 2026, 11:58:08 中午
---

<!-- toc -->

## 1. 什么是 BorgBackup？

BorgBackup 是一款支持 **去重（Deduplication）**、**压缩** 和 **身份验证加密** 的归档程序。它的核心目标是提供一种高效且安全的方法来备份数据。

### 1.1. 核心特性

1. **高度去重 (Data Deduplication)：**
   这是它的杀手锏。它只存储更改的内容。例如：你备份一个 10GB 的虚拟机镜像，第二天只改了 10MB 数据，再次备份时，Borg 只会增加这 10MB 的存储占用。
2. **高效压缩：**
   支持多种压缩算法（如 `lz4` 追求速度，`zstd` 追求压缩率）。
3. **安全性 (加密)：**
   所有数据都可以在客户端进行 **AES-256** 加密。这意味着即使你的备份服务器被黑，黑客也无法读取你的备份内容。
4. **离线与远程备份：**
   可以通过 SSH 备份到远程服务器，且对带宽要求极低（因为只传输去重后的增量部分）。

### 1.2. 基本概念

理解 Borg 的操作逻辑，需要明白以下层级：

- **存储库 (Repository)：** 存放备份数据的总仓库（一个目录或远程服务器路径）。
- **归档 (Archive)：** 仓库里的某一次具体备份（例如 `Monday-Backup`）。
- **区块 (Chunks)：** Borg 会将文件切成小块，通过哈希值对比来实现去重。

---

## 2. 常用操作指南

### 2.1. 初始化仓库

在使用之前，你需要创建一个加密仓库：

```bash
# 初始化一个本地仓库，并使用密码加密
borg init --encryption=repokey /path/to/repo
```

### 2.2. 创建备份 (Create)

将 `/home/user/data` 备份到仓库中，并命名为 `my-backup`：

```bash
borg create --stats --progress /path/to/repo::my-backup /home/user/data
```

### 2.3. 列出与恢复 (List & Extract)

- **查看所有备份：** `borg list /path/to/repo`
- **恢复某个归档：**

```bash
# 进入一个空目录执行
borg extract /path/to/repo::my-backup
```

### 2.4. 挂载备份 (Mount)

> [!tip] 最酷的功能：本地文件系统挂载
> 你可以像挂载 U 盘一样，直接把备份仓库挂载成一个本地文件系统，直接用文件管理器进去找文件：
>
> ```bash
> mkdir /tmp/mountpoint
> borg mount /path/to/repo /tmp/mountpoint
> # 用完后卸载
> borg umount /tmp/mountpoint
> ```

---

## 3. Borgmatic

既然你已经了解了 **Borg** 是引擎，而 **borgmatic** 是驾驶员，那么深入使用 `borgmatic` 的核心就在于如何配置那个 **YAML 文件** 以及如何管理日常任务。

以下是 `borgmatic` 的实战使用全指南。

---

### 3.1. 安装与初始化

首先，确保你已经安装了 `borg`，然后安装 `borgmatic`：

```bash
# Ubuntu/Debian
sudo apt install borgmatic

# 或者通过 pip 安装最新版
pip install --user --upgrade borgmatic
```

#### 3.1.1. 生成示例配置文件

`borgmatic` 依赖一个 YAML 配置文件（通常位于 `/etc/borgmatic/config.yaml` 或 `~/.config/borgmatic/config.yaml`）。

```bash
# 生成一个带注释的完整示例文件
generate-borgmatic-config
```

---

### 3.2. 核心配置详解 (Config.yaml)

一个典型的生产环境配置文件通常包含以下四个部分：

#### 3.2.1. 存储位置 (Location)

定义备份谁，备份到哪。

```yaml
location:
    # 待备份的本地目录
    source_directories:
        - /home/user/documents
        - /var/www/html
        - /etc
    
    # 备份目的地（本地磁盘或远程 SSH 服务器）
    repositories:
        - /mnt/backup_disk/my_repo
        - user@remote-server.com:main_repo
    
    # 排除不需要的文件
    exclude_patterns:
        - '*.tmp'
        - '*/.cache'
        - '/home/*/.local/share/Trash'
```

#### 3.2.2. 存储策略 (Storage)

定义如何加密和压缩。

```yaml
storage:
    # 对应 borg init 的加密模式
    encryption_passphrase: "你的复杂密码"
    # 压缩算法：lz4 速度最快，zstd 压缩率更高
    compression: zstd,3
    # 远程备份时使用的 SSH 命令
    ssh_command: ssh -i ~/.ssh/id_rsa
```

#### 3.2.3. 保留策略 (Retention)

这是 `borgmatic` 最省心的地方，自动清理旧备份。

```yaml
retention:
    # 策略示例：保留最近 7 天的每天备份，最近 4 周的每周备份，最近 6 个月的每月备份
    keep_daily: 7
    keep_weekly: 4
    keep_monthly: 6
    # 必须设置前缀，防止误删其他来源的备份
    prefix: hostname-
```

#### 3.2.4. 数据库备份 (Databases)

无需手动执行 `mysqldump`。

```yaml
databases:
    - name: my_database_name
      type: postgresql
      username: postgres
```

---

### 3.3. 常用操作指令

配置完成后，所有的操作都变得非常简单：

| 操作 | 命令 | 备注 |
| :--- | :--- | :--- |
| **初始化仓库** | `borgmatic init --encryption repokey` | 仅需执行一次 |
| **执行备份** | `borgmatic` | 默认执行所有配置好的任务 |
| **清理旧备份** | `borgmatic prune` | 根据 retention 策略删除旧档 |
| **检查损坏** | `borgmatic check` | 验证仓库完整性 |
| **查看列表** | `borgmatic list` | 列出所有已有的备份存档 |
| **一键完成** | `borgmatic --create --prune --compact` | **推荐：** 备份+清理+回收空间 |

---

### 3.4. 自动化：定时任务 (Cron/Systemd)

你不需要手动运行备份。通常我们会设置 **Systemd Timer** 或 **Cron**。

#### 3.4.1. 使用 Systemd (推荐)

`borgmatic` 通常会附带 Systemd 单元文件。你可以启用它：

```bash
sudo systemctl enable --now borgmatic.timer
```

这会默认每天执行一次备份。

---

### 3.5. 进阶：如何恢复数据？

`borgmatic` 提供了方便的挂载功能，让你像找回 U 盘文件一样找回备份：

1. **挂载整个仓库**：

   ```bash
   mkdir /tmp/my_backup
   borgmatic mount --mount-point /tmp/my_backup
   ```

2. **拷贝你需要的文件**：
   直接使用 `cp` 命令从 `/tmp/my_backup` 拷走文件。
3. **卸载**：

   ```bash
   borgmatic umount --mount-point /tmp/my_backup
   borgmatic delete --archive ... # 删除
   ```

---

## 4. 拓展信息

### 4.1. Borg Vs 其他工具

| 特性 | BorgBackup | rsync / rclone | Restic |
| :--- | :--- | :--- | :--- |
| **去重** | **强项** (块级去重) | 无 (仅文件级同步) | 支持 |
| **加密** | 原生支持 | 需配合其他工具 | 原生支持 |
| **挂载** | 支持 (FUSE) | 不支持 | 支持 |
| **性能** | 极快，适合处理大量小文件 | 适合大文件同步 | 内存占用略高于 Borg |

### 4.2. Borgmatic

简单来说，**BorgBackup (简称 Borg)** 是一个强大的去中心化、去重备份工具，而 **borgmatic** 是 Borg 的“高级管家”或配置层，让 Borg 的使用变得更简单、更自动化。

#### 4.2.1. Borgmatic: 自动化助手

虽然 Borg 很强大，但如果你想实现“每天凌晨 2 点备份、备份前停止数据库、备份后清理旧数据、顺便检查备份完整性”，直接写 Borg 的 Shell 脚本会非常繁琐。**borgmatic** 就是为了解决这个问题而生的。

#### 4.2.2. 为什么需要 borgmatic？

- **声明式配置**：使用简单的 YAML 文件替代复杂的命令行参数。
- **多任务集成**：在一个配置文件里同时管理多个备份源和多个目的地。
- **数据库支持**：内置了对 MySQL, PostgreSQL, MongoDB 的支持（备份前自动 dump，备份后自动清理临时文件）。
- **自动清理 (Pruning)**：根据保留策略（如：保留最近 7 天，每周一个，每月一个）自动删除旧档案。
- **一致性检查**：自动运行 `borg check` 确保数据没损坏。
- **监控钩子**：备份成功或失败时发送通知（如 Healthchecks, PagerDuty 等）。

#### 4.2.3. 两者对比总结

| 特性 | BorgBackup (Borg) | borgmatic |
| :--- | :--- | :--- |
| **角色** | 核心工具（后端） | 封装工具（前端/驱动） |
| **操作方式** | 纯命令行，参数复杂 | 配置文件 (YAML) |
| **自动化** | 需自行编写脚本 | 原生支持定时、清理、检查 |
| **数据库备份** | 需手动导出 | 简单配置即可自动备份数据库 |
| **适用人群** | 开发者、高级系统管理员 | 追求高效、稳定的系统运维人员 |

---

## 5. 典型工作流示例 (使用 borgmatic)

如果你安装了 `borgmatic`，你的备份流程通常只需要两步：

### 5.1. 第一步：编写配置文件 `config.yaml`

```yaml
location:
    source_directories:
        - /home/user/data
        - /etc
    repositories:
        - user@remote-storage.com:repo
    database_backends:
        - postgresql

retention:
    keep_daily: 7
    keep_weekly: 4
    keep_monthly: 6

consistency:
    checks:
        - repository
        - archives
```

### 5.2. 第二步：运行备份

只需执行一行命令，或者将其加入 Cron 任务：

```bash
borgmatic --create --prune --compact
```

这条命令会自动：导出数据库 -> 执行加密备份 -> 删除过期旧备份 -> 整理磁盘空间。

---

> [!question] 部署场景确认
> 您是准备在个人服务器上部署备份系统，还是在公司生产环境中使用？如果需要，我可以为您提供一份针对特定场景（如备份 Docker 卷或数据库）的详细配置模板。

---

## 6. 参考文档

- [官方文档](https://www.borgbackup.org/)
- [vorta](https://vorta.borgbase.com/)
