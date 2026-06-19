---
status: completed
filename: linux-swap-partition-management-and-expansion
title: "Linux Swap"
summary: 本笔记记录了在 Linux 服务器物理内存不足时，通过手动创建 Swap 交换文件来缓解 OOM (Out Of Memory) 风险的完整操作流程。详细提供了利用 `dd` 命令分配磁盘空间、`mkswap` 格式化及 `swapon` 挂载执行的具体 Shell 指令。此外，附带了使用 `swapon -s` 验证当前交换区状态的快捷命令，是排查与解决由于高并发导致的进程被内核强杀问题的应急参考手册。
aliases: [Linux Swap, 交换分区, 虚拟内存, OOM 解决]
tags: [Linux, 运维, 性能优化, Swap, 内存管理, Shell]
date created: 星期一, 一月 12日 2026, 10:03:48 上午
date modified: 星期四, 六月 18日 2026, 12:25:00 晚上
---

<!-- toc -->

## 1. 核心定位

Linux **Swap (交换区)** 是物理磁盘上的一块保留空间。当物理内存 (RAM) 耗尽时，操作系统会将内存中不常用的数据页 (Pages) 临时写入 Swap，以腾出物理内存给更紧急的进程使用，从而防止出现 OOM (Out of Memory) 导致核心进程被内核强杀。

---

## 2. Swap 空间新增与挂载实战

如果云服务器默认没有分配 Swap，或者现有 Swap 空间不足，可以通过创建一个交换文件来动态扩容。

### 2.1. 创建并挂载交换文件

```bash
# 切换到通常用于挂载外部设备的目录
cd /mnt/
mkdir -p swap && cd swap

# 1. 划出物理磁盘空间 (此例为 1024MB = 1GB)
dd if=/dev/zero of=swapfile bs=1M count=1024

# 2. 安全赋权 (防止非 root 用户读取内存泄漏数据)
chmod 600 swapfile

# 3. 将文件格式化为 Linux Swap 专用格式
mkswap swapfile

# 4. 激活并挂载该 Swap 空间
swapon swapfile
```

### 2.2. 状态验证与监控

通过以下命令验证 Swap 空间是否已成功被系统纳管：

```bash
swapon -s
# 或者使用 free -h 查看全局内存状况
```

> [!tip] 持久化提示
> 上述 `swapon` 命令在服务器重启后会失效。若需永久挂载，必须将其写入 `/etc/fstab` 文件中（追加 `/mnt/swap/swapfile none swap sw 0 0`）。
