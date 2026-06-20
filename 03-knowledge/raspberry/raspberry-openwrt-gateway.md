---
title: "树莓派5旁路由部署"
filename: raspberry-openwrt-gateway
description: 树莓派 5 上基于 Docker/Podman 部署 OpenWrt 旁路由的实操指南。内容涵盖通过 macvlan 驱动配置容器网络、导入官方 rootfs 镜像并以特权模式启动、静态 IP 初始化与 DNS/DHCP 服务调整。同时提供 LuCI、iStore 及 PassWall2 插件安装方案，并重点针对宿主机与容器互通及局域网断网等常见网络问题给出防火墙伪装与 rc.local 路由调优的避坑解决方案。
tags:
  - raspberry-pi
  - openwrt
  - docker
  - macvlan
  - homelab
aliases:
  - 树莓派5旁路由部署
  - Docker安装OpenWrt
  - Macvlan旁路由网络优化
status: completed
date created: 星期三, 四月 1日 2026, 11:01:52 晚上
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 前提条件

- 本文以 **树莓派 5** 运行官方系统为例。
- 宿主机已成功部署并运行 **Docker** 或 **Podman** 容器引擎。

## 2. 镜像下载与导入

```bash
cd /tmp
# 下载官方 AArch64/ARMv8 架构的 rootfs 镜像
wget https://archive.openwrt.org/releases/24.10.4/targets/armsr/armv8/openwrt-24.10.3-armsr-armv8-generic-ext4-rootfs.img.gz
# 解压镜像文件
gzip -d openwrt-24.10.3-armsr-armv8-generic-ext4-rootfs.img.gz
# 将镜像导入为 Docker 镜像 (此处若使用的是官方 rootfs 归档包，可直接 docker import)
docker import openwrt-24.10.3-armsr-armv8-generic-ext4-rootfs.img openwrt
```

## 3. 网络准备与容器运行

- **开启物理网卡混杂模式并创建 Macvlan 网络**

```bash
# 临时开启 eth0 网卡的混杂模式
ip link set eth0 promisc on

# 创建 Docker Macvlan 外部网络（请根据实际局域网网段修改 subnet 与 gateway）
docker network create -d macvlan --subnet=192.168.8.0/24 --gateway=192.168.8.1 -o parent=eth0 openwrt
```

- **创建 docker-compose.yml 配置文件**

```yaml
services:
  openwrt:
    image: openwrt
    container_name: openwrt-route
    restart: always
    privileged: true
    command: /sbin/init
    networks:
      - openwrt

networks:
  openwrt:
    external: true  # 声明使用上面手动创建的 macvlan 网络
```

- **启动并进入 OpenWrt 容器**

```bash
docker compose up -d
docker exec -it openwrt-route /bin/sh
```

## 4. OpenWrt 初始化设置

在容器内执行以下初始化操作：

- **修改 Root 密码**

```bash
passwd
```

- **配置静态 IP 路由信息**

编辑 `/etc/config/network` 配置文件，根据实际局域网规划静态 IP（例如配置为 `192.168.8.202`）：

```text
config interface 'loopback'
        option device 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
        option ula_prefix 'fd61:570b:366f::/48'

config device
        option name 'br-lan'
        option type 'bridge'
        list ports 'eth0'

config interface 'lan'
        option device 'br-lan'
        option proto 'static'
        option ipaddr '192.168.8.202'
        option netmask '255.255.255.0'
        option gateway '192.168.8.1'
        option dns '223.5.5.5'
        option ip6assign '60'
```

- **重启网络服务**

```bash
service network restart
```

- **调整基础服务组件**

```bash
# 更新并切换到完整版 dnsmasq 以支持进阶过滤规则
opkg update  
opkg remove dnsmasq  
opkg install dnsmasq-full
service dnsmasq status

# 停止容器内默认的 IPv6 DHCP (odhcpd) 服务，防止与主路由冲突
/etc/init.d/odhcpd stop  
/etc/init.d/odhcpd disable

# 修正时区设置
uci set system.@system[0].zonename='Asia/Shanghai'  
uci set system.@system[0].timezone='CST-8'  
uci commit system  
/etc/init.d/system restart
```

> [!TIP]
> 建议后续在 OpenWrt Web 界面中，将 NTP 服务器手动添加国内的阿里云授时服务 `ntp.aliyun.com`。

## 5. 常用软件与插件安装

### 5.1. LuCI Web 中文面板

```bash
cd /tmp
opkg install luci-compat  
opkg install luci-lib-ipkg
opkg install luci-i18n-base-zh-cn  
opkg install curl wget-ssl unzip

# 安装优秀的 Argon 质感主题与配置工具
wget --no-check-certificate https://github.com/jerrykuku/luci-theme-argon/releases/download/v2.3.2/luci-theme-argon_2.3.2-r20250207_all.ipk  
opkg install luci-theme-argon*.ipk  

wget --no-check-certificate -O luci-app-argon-config_0.9_all.ipk https://github.com/jerrykuku/luci-app-argon-config/releases/download/v0.9/luci-app-argon-config_0.9_all.ipk  
opkg install luci-app-argon-config*.ipk
```

### 5.2. iStore 软件中心

```bash
wget https://github.com/linkease/openwrt-app-actions/raw/main/applications/luci-app-systools/root/usr/share/systools/istore-reinstall.run  
chmod 755 istore-reinstall.run  
./istore-reinstall.run
```

### 5.3. PassWall2 网络代理插件

```bash
# 安装系统依赖
opkg install kmod-nft-socket  
opkg install kmod-nft-tproxy

# 导入 GPG 公钥并添加软件源
wget -O passwall.pub https://master.dl.sourceforge.net/project/openwrt-passwall-build/passwall.pub  
opkg-key add passwall.pub

read release arch << EOF  
$(. /etc/openwrt_release ; echo ${DISTRIB_RELEASE%.*} $DISTRIB_ARCH)  
EOF  

for feed in passwall_luci passwall_packages passwall2; do  
  echo "src/gz $feed https://master.dl.sourceforge.net/project/openwrt-passwall-build/releases/packages-$release/$arch/$feed" >> /etc/opkg/customfeeds.conf  
done

opkg update
opkg install luci-app-passwall2  
opkg install luci-i18n-passwall2-zh-cn
service passwall2 enable
```

> [!NOTE]
> 如果安装后在 Web 面板中操作“总开关”出现状态不同步、无效等情况，请尝试重启容器或 OpenWrt 系统。

## 6. 宿主机与容器互通优化

在 Docker Macvlan 模式下，出于安全隔离，**宿主机与容器默认是无法直接通信的**。若想让宿主机自身也能使用旁路由，需通过添加虚拟网桥进行通信中转。

- **配置宿主机 `/etc/rc.local` 脚本**

```bash
#!/bin/bash  
# 1. 开启物理网卡混杂模式
ip link set eth0 promisc on  
  
# 2. 创建宿主机专属的 macvlan 虚拟网卡并绑定到物理网卡
ip link add macvlan-bridge link eth0 type macvlan mode bridge  
ip addr add 192.168.8.203/24 dev macvlan-bridge  
ip link set macvlan-bridge up  
  
# 3. 指定宿主机访问容器 IP (192.168.8.202) 的路由规则走虚拟网卡
ip route add 192.168.8.202 dev macvlan-bridge  
  
# 4. 优先级路由：将系统默认网关指向旁路由，设置较低 Metric (10)
# 这样即便 192.168.8.1 的默认网关存在，系统也会优先通过旁路由出网
ip route add default via 192.168.8.202 dev macvlan-bridge metric 10  
  
exit 0
```

- **应用并激活 rc.local 服务**

```bash
chmod +x /etc/rc.local
systemctl restart rc-local
```

- **适配 DNS 服务走旁路由代理**

修改宿主机 `/etc/systemd/resolved.conf`：

```text
[Resolve]  
DNS=192.168.8.202  
FallbackDNS=192.168.8.1 114.114.114.114  
```

重启系统解析服务并清理缓存：

```bash
systemctl daemon-reload
systemctl restart systemd-resolved
resolvectl flush-caches  
resolvectl status
```

> [!WARNING]
> 大多数内置的无线网卡（wlan0）驱动不支持 macvlan 模式，此套旁路由方案一般只适用于有线物理网卡（如 eth0）。

## 7. 避坑与拓展信息

> [!CAUTION]
> **Docker Stop OpenWrt 导致宿主机重启**
> 在部分 Linux 内核上，停止 OpenWrt 容器可能会因为 macvlan 虚拟网络堆栈崩溃引发宿主机 Kernel Panic 重启。目前暂无完美软件修复方案，建议尽量保持旁路由常驻运行，避免频繁启停。

> [!IMPORTANT]
> **移动带宽下 114.114.114.114 无法连接**
> 部分地区移动运营商对 114.114.114.114 进行了限流或劫持，建议国内公共 DNS 优先配置为阿里 DNS（`223.5.5.5`）或腾讯 DNS（`119.29.29.29`）。

> [!NOTE]
> **局域网设备 Ping 不通旁路由**
> 请进入 PassWall2 后台的“高级配置”中，开启 **“劫持 ICMP (PING)”** 选项。

> [!NOTE]
> **局域网设备“内网通，外网不通”**
> 请确保在 OpenWrt 的“网络 -> 防火墙 -> 路由/NAT”设置中，开启 **“IP 动态伪装 (Masquerading)”**。

> [!NOTE]
> **局域网设备访问外网间歇性报 SSL 证书错误**
> 请在 PassWall2 过滤规则中开启 **FakeDNS** 模式，或者开启防火墙中的 **IP 动态伪装 (Masquerading)** 以修正数据包回程路由。

## 8. 参考资料

- [Docker 安装 OpenWrt 旁路由指南](https://lilith.pro/gijyutsu/2646)
- [OpenWrt 下 PassWall2 的配置实践](https://lilith.pro/gijyutsu/2646)
