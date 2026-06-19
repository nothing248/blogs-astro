---
title: "MinIO安装与配置指南"
filename: minio-setup-guide
summary: MinIO 是基于 Go 语言的高性能分布式对象存储系统。本指南针对私有化部署需求，详细阐述了单机及集群两种架构的部署方案，包含磁盘挂载、Systemd 守护进程配置、Nginx 反向代理与负载均衡设置、以及命令行客户端 mc 的管理操作。旨在协助运维人员构建具备高可用性、强扩展性的私有云存储平台。
tags:
  - minio
  - object-storage
  - cluster-deployment
  - nginx
aliases:
  - MinIO安装与配置指南
  - MinIO集群部署
  - 私有化对象存储
status: completed
date created: 星期一, 五月 19日 2025, 2:05:18 下午
date modified: 星期二, 六月 16日 2026, 6:24:23 晚上
---

<!-- toc -->

## 1. 简介

MinIO 是一款开源的基于 Go 语言发开的高性能、分布式的对象存储系统。可以作为一个私有化的对象存储部署方案。

## 2. 安装

### 2.1. 单机部署

- 安装

```shell
# 服务器
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/
# 客户端
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/mc
```

- 配置 systemd

```ini
[Unit]
Description=MinIO
Documentation=https://min.io/docs/minio/linux/index.html
Wants=network-online.target
After=network-online.target
AssertFileIsExecutable=/usr/local/bin/minio

[Service]
WorkingDirectory=/usr/local

#User=minio-user
#Group=minio-user
#ProtectProc=invisible

EnvironmentFile=/etc/minio/env
ExecStartPre=/bin/bash -c "if [ -z \"${MINIO_VOLUMES}\" ]; then echo \"Variable MINIO_VOLUMES not set in /etc/default/minio\"; exit 1; fi"
ExecStart=/usr/local/bin/minio server $MINIO_OPTS $MINIO_VOLUMES

# MinIO RELEASE.2023-05-04T21-44-30Z adds support for Type=notify (https://www.freedesktop.org/software/systemd/man/systemd.service.html#Type=)
# This may improve systemctl setups where other services use `After=minio.server`
# Uncomment the line to enable the functionality
# Type=notify

# Let systemd restart this service always
Restart=always

# Specifies the maximum file descriptor number that can be opened by this process
LimitNOFILE=65536

# Specifies the maximum number of threads this process can create
TasksMax=infinity

# Disable timeout logic and wait until process is stopped
TimeoutStopSec=infinity
SendSIGKILL=no

[Install]
WantedBy=multi-user.target

# Built for ${project.name}-${project.version} (${project.name})
```

- 配置环境变量

```env
# MINIO_ROOT_USER and MINIO_ROOT_PASSWORD sets the root account for the MinIO server.
# This user has unrestricted permissions to perform S3 and administrative API operations on any resource in the deployment.
# Omit to use the default values 'minioadmin:minioadmin'.
# MinIO recommends setting non-default values as a best practice, regardless of environment

MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=example

# MINIO_VOLUMES sets the storage volume or path to use for the MinIO server.

MINIO_VOLUMES="/data/minio"

# MINIO_OPTS sets any additional commandline options to pass to the MinIO server.
# For example, `--console-address :9001` sets the MinIO Console listen port
MINIO_OPTS="--console-address :9001"

MINIO_BROWSER_REDIRECT_URL="https://minio.example.com/minio/ui"
```

- nginx 配置

```nginx
server {
    listen 443 ssl;
    server_name minio.example.com;  # 替换为您的服务器IP或域名

    ssl_certificate /opt/software/gogs/custom/https/cert.crt;
    ssl_certificate_key /opt/software/gogs/custom/https/key.key;

    location / {
        proxy_pass http://127.0.0.1:9000;  # 后端服务地址
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        real_ip_header X-Real-IP;

        proxy_connect_timeout 300;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

     location /minio/ui/ {
          rewrite ^/minio/ui/(.*) /$1 break;
          proxy_set_header Host $http_host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_set_header X-NginX-Proxy true;

          # This is necessary to pass the correct IP to be hashed
          real_ip_header X-Real-IP;

          proxy_connect_timeout 300;

          # To support websockets in MinIO versions released after January 2023
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          # Some environments may encounter CORS errors (Kubernetes + Nginx Ingress)
          # Uncomment the following line to set the Origin request to an empty string
          # proxy_set_header Origin '';

          chunked_transfer_encoding off;

          proxy_pass http://127.0.0.1:9001; # This uses the upstream directive definition to load balance
   }
}
```

### 2.2. 集群部署

- 安装

```shell
# 服务器
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/
# 客户端
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/mc
```

- 挂载 driver

```shell
apt install parted xfsprogs
# 创建分区
parted /dev/sdb --script mkpart primary xfs 0% 10GB
parted /dev/sdb --script mkpart primary xfs 10G 100%
# 格式化文件系统
mkfs.xfs /dev/sdb1
mkfs.xfs /dev/sdb2
# 挂载文件
mount -t xfs /dev/sdb1 /mnt/minio1
mount -t xfs /dev/sdb2 /mnt/minio2
# 初始化挂载 /etc/fstab
/dev/sdb1 /mnt/minio1 xfs defaults 0 0
/dev/sdb2 /mnt/minio2 xfs defaults 0 0
```

> [!WARNING]
> 注意：此处的 driver 必须单独挂载磁盘而不能配置目录信息。建议文件系统使用 **xfs** 格式。

- systemd 配置

> 参考单机部署部分。

- 环境配置

```env
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=[密码已隐藏]
            
# MINIO_VOLUMES sets the storage volume or path to use for the MinIO server.
            
MINIO_VOLUMES="http://slave{1...3}:9000/mnt/minio{1...2}"
            
# MINIO_OPTS sets any additional commandline options to pass to the MinIO server.
# For example, `--console-address :9001` sets the MinIO Console listen port
MINIO_OPTS="--console-address :9001"

MINIO_BROWSER_REDIRECT_URL="https://minio.example.com/minio/ui"
```

- nginx 配置

```nginx
upstream minio_server {
    least_conn;
    server slave1:9000;
    server slave2:9000;
    server slave3:9000;
}

upstream minio_console {
    ip_hash;
    server slave1:9001;
    server slave2:9001;
    server slave3:9001;
}


server {
    listen 443 ssl;
    server_name minio.example.com;  # 替换为您的服务器IP或域名

    ssl_certificate /opt/software/gogs/custom/https/cert.crt;
    ssl_certificate_key /opt/software/gogs/custom/https/key.key;

    location / {
        proxy_pass http://minio_server;  # 后端服务地址
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        real_ip_header X-Real-IP;

        proxy_connect_timeout 300;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

     location /minio/ui/ {
          rewrite ^/minio/ui/(.*) /$1 break;
          proxy_set_header Host $http_host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_set_header X-NginX-Proxy true;

          # This is necessary to pass the correct IP to be hashed
          real_ip_header X-Real-IP;

          proxy_connect_timeout 300;

          # To support websockets in MinIO versions released after January 2023
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          # Some environments may encounter CORS errors (Kubernetes + Nginx Ingress)
          # Uncomment the following line to set the Origin request to an empty string
          # proxy_set_header Origin '';

          chunked_transfer_encoding off;

          proxy_pass http://minio_console; # This uses the upstream directive definition to load balance
   }
}
```

## 3. 使用

### 3.1. 管理

- 服务端

```shell
minio server /data/minio --console-address :9001 # 启动服务
```

- systemd

```shell
systemctl status minio
systemctl start minio
systemctl stop minio
systemctl restart minio
```

- 客户端

```shell
curl http://127.0.0.1:9001 # 访问 web 页面
mc alias set local http://127.0.0.1:9000 minioadmin minioadmin # 注册链接 
mc admin info local # 查看信息
```

## 4. 拓展信息

...

## 5. 参考资料

- [官方文档](https://min.io/docs/minio/kubernetes/upstream/index.html?ref=docs-redirect)
