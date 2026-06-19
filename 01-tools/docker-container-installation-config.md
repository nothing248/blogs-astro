---
title: "Docker安装"
filename: docker-container-installation-config
summary: Docker是基于操作系统的应用容器引擎。本文总结了在Windows和Linux（Ubuntu）平台部署Docker的实战要点。针对Windows下WSL2环境，提供了非C盘安装路径的避坑方案、镜像存储迁移步骤、以及阿里云代理和容器自动重启等常规Daemon配置文件优化建议。
tags: [docker, containerization, wsl2, devops]
aliases: [Docker安装, WSL2部署, Daemon配置]
status: completed
date created: 星期五, 十二月 5日 2025, 3:42:14 下午
date modified: 星期五, 六月 19日 2026, 11:58:42 中午
---

<!-- toc -->

## 1. 简介

一个容器服务

## 2. 安装

### 2.1. Windows

安装 docker-desktop 时可以使用 wsl, 来确保兼容性。

- 修改文件安装路径

```shell
"Docker Desktop Installer.exe" install --installation-dir="D:\docker\docker_desktop"
```

> 注意: 不要使用软连接的方式了，测试会报错。使用以上的路径安装方式既可以

- 开启 wsl 支持  
Settings > Resources > WSL Integration > 选择对应系统

- 配置镜像存储地址
地址：C:\Users\xxxxx\AppData\Local\Docker\wsl
  - data/ext4.vhdx 是被 docker-desktop-data 发行版使用，存放镜像
  - distro/ext4.vhdx 是被 docker-desktop 发行版使用，存放程序（内存占用小，根据需要，可以不用修改）

```shell
wsl --shutdown
wsl --export docker-desktop E:\Docker\wsl\docker-desktop\docker-desktop.tar
wsl --export docker-desktop-data E:\Docker\wsl\docker-desktop-data\docker-desktop-data.tar
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
wsl --import docker-desktop E:\Docker\wsl\docker-desktop E:\Docker\wsl\docker-desktop\docker-desktop.tar --version 2
wsl --import docker-desktop-data E:\Docker\wsl\docker-desktop-data E:\Docker\wsl\docker-desktop-data\docker-desktop-data.tar --version 2
```

### 2.2. Linux

- 获取源

```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

- 安装

```shell
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 3. 使用

### 3.1. 网络

- bridge  
它允许容器在同一主机上相互通信，同时也与主机网络进行交互
  - 默认网络：当你创建一个容器而不指定网络时，Docker 会将其连接到 bridge 网络。
  - 网络隔离：容器在 bridge 网络中是隔离的，容器之间只能通过指定的网络进行通信。
  - NAT：Bridge 网络使用网络地址转换（NAT）来管理容器与外部世界的通信。
  - IP 地址分配：Docker 会为每个连接到 bridge 网络的容器分配一个独特的 IP 地址。
  - DNS 解析：Docker 内置的 DNS 服务器可以帮助容器之间通过名称进行通信。

```shell
docker network create --subnet=192.168.1.0/24 --gateway=192.168.1.1 my_custom_bridge #创建网络
```

- macvlan  
是一种特殊的网络模式，允许你为 Docker 容器提供独立于主机网络环境的 MAC 地址。它使得容器能够像物理设备一样直接连接到网络，适用于需要直接与物理网络进行交互的场景。
  - 独立的 MAC 地址：每个容器可以拥有自己的 MAC 地址，这样它们在网络中表现得就像独立的网络设备。
  - 直接与物理网络通信：容器可以直接与网络中的其他设备通信，而无需通过 Docker 的 NAT（网络地址转换）层。
  - 支持 VLAN：支持 VLAN（虚拟局域网），可以实现网络隔离。
  - 与主机网络隔离：macvlan 网络的容器与主机的网络栈是隔离的，避免了主机与容器之间的网络干扰。

```shell
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  my_macvlan_network
```

> docker0 网卡是 Docker 引擎在主机上创建的一个虚拟网络接口。 它的作用是为 Docker 容器提供网络连接

### 3.2. 容器

```shell
docker run --rm -d -p 3306:3306 -e env --name mysql image:tag #运行容器
docker exec -it /bin/bash #在容器内运行命令
```

> 容器可以链接到多个网络内

### 3.3. 文件

```shell
docker cp container:/path/file /path/file
```

## 4. Docker-compose

### 4.1. 配置文件

```yaml
version: '3'
services:
  db:
    image: mysql:5.7
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    volumes:
      - './data:/var/lib/mysql'
      - './conf:/etc/mysql'
    ports:
      - '3306:3306'
    environment:
      MYSQL_ROOT_PASSWORD: example
    networks:
      - share

networks:
  share:
    external:
      name: share
```

> 宿主机上的映射目录不需要手动创建

### 4.2. 使用

```shell
docker-compose up -d
```

## 5. 拓展信息

### 5.1. 国内访问 docker Hub 出现问题

- 10810 端口挂载一个代理
- 因为 docker 是一个后台进程，需要单独配置

```shell
sudo -s
mkdir -p /etc/systemd/system/docker.service.d
vim /etc/systemd/system/docker.service.d/http-proxy.conf
# 以下为文件内容信息
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:10810"
Environment="HTTPS_PROXY=http://127.0.0.1:10810"
Environment="NO_PROXY=localhost,127.0.0.1"
systemctl daemon-reload
systemctl restart docker
```

### 5.2. 修改数据存储地址

```json
# /etc/docker/daemon.json

{ "data-root": "/mnt/data/docker" // 请将此路径替换为您的目标新目录 }
```

## 6. 参考资料

...
