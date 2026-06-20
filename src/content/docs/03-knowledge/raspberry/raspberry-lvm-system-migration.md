---
title: "树莓派LVM迁移指南"
filename: raspberry-lvm-system-migration
description: 树莓派系统全盘克隆至新 SSD 并启用 LVM（逻辑卷管理）的迁移指南。内容涵盖对目标盘手动分区、初始化逻辑卷（PV/VG/LV）、利用 rsync 保持权限同步系统数据，以及修改 fstab 与 cmdline.txt 引导配置。并详细说明了通过 chroot 进入挂载环境更新 initramfs 驱动镜像的避坑关键步骤。
tags:
  - raspberry-pi
  - lvm
  - system-migration
  - storage
  - rsync
aliases:
  - 树莓派LVM迁移指南
  - 树莓派全盘克隆SSD
  - 树莓派LVM搭建教程
status: completed
date created: 星期五, 二月 27日 2026, 7:15:51 晚上
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 核心逻辑

将树莓派运行中的系统直接“全盘迁移”到新磁盘（如从 SD 卡迁移到 SSD，或从旧 SSD 迁移到新 SSD）并在此过程中启用 LVM（逻辑卷管理）是优化存储性能和后期扩容的核心方案。

最稳妥的实施路径是：**先在目标盘上手动分区并建立 LVM，然后同步当前系统数据，最后配置并重构引导。**

> [!NOTE]
> 假设：
>
> - **源盘**：当前运行系统的磁盘（正在使用的 SD 卡或旧固态硬盘）。
> - **目标盘**：新接入待迁移的磁盘（在本文中假设识别为设备 `/dev/sdb`）。

---

## 2. 迁移步骤

### 2.1. 对目标盘进行手动分区

目标盘需要划分两个分区：一个 **FAT32 启动分区**（存放引导固件）和一个 **LVM 分区**（存放系统根目录及其他逻辑卷）。

使用 `fdisk` 对目标盘进行分区操作：

```bash
sudo fdisk /dev/sdb
```

在交互命令行中依次执行：

1. **创建启动分区**：输入 `n` -> `p` -> `1` -> 起始扇区回车默认 -> 结束扇区输入 `+512M`。
2. **创建 LVM 分区**：输入 `n` -> `p` -> `2` -> 起始扇区回车默认 -> 结束扇区回车默认（使用磁盘全部剩余空间）。
3. **修改分区类型**：
   - 输入 `t` -> 指定分区 `1` -> 输入十六进制代码 `c` (W95 FAT32 LBA)。
   - 输入 `t` -> 指定分区 `2` -> 输入十六进制代码 `31` (Linux LVM)。
4. **保存配置并退出**：输入 `w` 写入分区表。

---

### 2.2. 初始化 LVM

在新建的 Linux LVM 分区上初始化物理卷、卷组以及逻辑卷：

```bash
# 1. 将分区 /dev/sdb2 创建为物理卷 (PV)
sudo pvcreate /dev/sdb2

# 2. 创建名为 vg_system 的卷组 (VG)
sudo vgcreate vg_system /dev/sdb2

# 3. 在卷组中创建根目录逻辑卷 (LV)，可先分配 100G（后期可随时动态扩容）
sudo lvcreate -L 100G -n lv_root vg_system
```

---

### 2.3. 格式化与数据同步

将新分区进行格式化，并将源系统的文件内容完整、无损地“克隆”到 LVM 逻辑卷中。

- **格式化新分区**

```bash
# 格式化引导分区为 FAT32，并设置卷标
sudo mkfs.vfat -F 32 -n "boot-conf" /dev/sdb1

# 格式化逻辑卷根目录为 Ext4
sudo mkfs.ext4 /dev/vg_system/lv_root
```

- **挂载分区并同步文件系统**

```bash
# 创建挂载点
sudo mkdir -p /mnt/target_root
sudo mount /dev/vg_system/lv_root /mnt/target_root

# 挂载新引导分区到对应的 boot/firmware 目录中（适配树莓派新版目录结构）
sudo mount /dev/sdb1 /mnt/target_root/boot/firmware --mkdir

# 使用 rsync 完美同步所有文件及权限属性（排除系统动态虚拟目录与临时挂载点）
sudo rsync -axHAWXS --numeric-ids --info=progress2 \
  --exclude=/proc/* \
  --exclude=/sys/* \
  --exclude=/dev/* \
  --exclude=/run/* \
  --exclude=/tmp/* \
  --exclude=/mnt/* \
  --exclude=/lost+found \
  / /mnt/target_root/
```

---

### 2.4. 修正引导配置与 Initramfs 重构

这是 LVM 迁移中最容易出错的环节。必须显式告知内核启动引导的根目录位于 LVM 映射路径下，并且提前在 initramfs 引导镜像中加载 LVM 驱动。

- **修改目标系统的 fstab 挂载表**

编辑 `/mnt/target_root/etc/fstab`，将根路径 `/` 的挂载源配置修改为 LVM 映射器地址：

```text
/dev/mapper/vg_system-lv_root  /  ext4  defaults  0  1
```

- **修改目标系统的引导命令行**

编辑 `/mnt/target_root/boot/firmware/cmdline.txt`，修改其中的 `root=...` 参数，并增加启动延迟等待逻辑卷设备上线：

```text
root=/dev/mapper/vg_system-lv_root rootdelay=5
```

- **重构 Initramfs（关键避坑步骤）**

由于默认的树莓派启动镜像中不带 LVM 驱动模块，直接重启会导致内核无法挂载根路径而发生挂死（Panic）。需要通过 chroot 进入目标系统重建 initramfs：

```bash
# 绑定宿主机的虚拟系统目录到新系统根路径中
for i in /dev /dev/pts /proc /sys /run; do 
  sudo mount -B $i /mnt/target_root$i
done

# chroot 改变根目录进入新系统环境
sudo chroot /mnt/target_root

# 在目标环境中更新/生成包含 LVM 驱动的 initramfs 镜像
update-initramfs -u

# 退出 chroot 环境
exit
```

---

### 2.5. 测试启动

1. 安全卸载挂载的磁盘：`sudo umount -R /mnt/target_root`
2. 关闭树莓派电源，拔掉原系统磁盘（如 SD 卡）。
3. 确保目标 SSD 磁盘已妥善连接至树莓派的 USB 3.0 或 PCIe 接口。
4. 重新上电，启动并验证系统是否正常进入 LVM 根分区。

## 3. 拓展信息

> [!TIP]
> 成功进入 LVM 系统后，若有磁盘扩容需求，可随时通过 `lvextend -L +XG /dev/vg_system/lv_root` 配合 `resize2fs /dev/vg_system/lv_root` 在线扩展根分区的大小。
