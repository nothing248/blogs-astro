---
title: "etcd集群"
filename: etcd-distributed-key-value-store
description: etcd是用Go语言编写的分布式一致性键值存储系统，广泛用作Kubernetes等分布式系统的元数据注册中心。本文覆盖etcd在Linux上的解压部署、Systemd服务脚本编写、数据持久化与自动压缩参数配置，以及利用etcdctl客户端进行集群成员管理和数据读写的命令行实操。
tags: [etcd, distributed-systems, key-value-store, raft]
aliases: [etcd集群, etcd安装, etcdctl使用]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:27 下午
date modified: 星期五, 六月 19日 2026, 11:58:58 中午
---

<!-- toc -->

## 1. 简介

一个用于存储分布式系统中最关键数据的分布式、可靠的键值存储

## 2. 安装

- 下载

```shell
mkdir /opt/software
cd /opt/software
ETCD_VERSION='3.5.4'
wget https://github.com/etcd-io/etcd/releases/download/v${ETCD_VERSION}/etcd-v${ETCD_VERSION}-linux-amd64.tar.gz
tar -xvf etcd-v${ETCD_VERSION}-linux-amd64.tar.gz
cd etcd-v${ETCD_VERSION}-linux-amd64
sudo cp -a etcd etcdctl /usr/bin/
```

- 配置

```yaml
# /etc/etcd/conf.yaml
# This is the configuration file for the etcd server.

# Human-readable name for this member.
name: 'etcd0'

# Path to the data directory.
data-dir: '/var/lib/etcd'

# Path to the dedicated wal directory.
wal-dir: '/var/lib/etcd'

# Number of committed transactions to trigger a snapshot to disk.
snapshot-count: 10000

# Time (in milliseconds) of a heartbeat interval.
heartbeat-interval: 100

# Time (in milliseconds) for an election to timeout.
election-timeout: 1000

# Raise alarms when backend size exceeds the given quota. 0 means use the
# default quota.
quota-backend-bytes: 0

# List of comma separated URLs to listen on for peer traffic.
listen-peer-urls: http://0.0.0.0:2380

# List of comma separated URLs to listen on for client traffic.
listen-client-urls: http://0.0.0.0:2379

# Maximum number of snapshot files to retain (0 is unlimited).
max-snapshots: 5

# Maximum number of wal files to retain (0 is unlimited).
max-wals: 5

# Comma-separated white list of origins for CORS (cross-origin resource sharing).
cors:

# List of this member's peer URLs to advertise to the rest of the cluster.
# The URLs needed to be a comma-separated list.
initial-advertise-peer-urls: http://192.168.56.104:2380

# List of this member's client URLs to advertise to the public.
# The URLs needed to be a comma-separated list.
advertise-client-urls: http://192.168.56.104:2379

# Discovery URL used to bootstrap the cluster.
discovery:

# Valid values include 'exit', 'proxy'
discovery-fallback: 'proxy'

# HTTP proxy to use for traffic to discovery service.
discovery-proxy:

# DNS domain used to bootstrap initial cluster.
discovery-srv:

# Comma separated string of initial cluster configuration for bootstrapping.
# Example: initial-cluster: "infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
initial-cluster: 'etcd0=http://192.168.56.104:2380'

# Initial cluster token for the etcd cluster during bootstrap.
initial-cluster-token: 'etcd-cluster'

# Initial cluster state ('new' or 'existing').
initial-cluster-state: 'new'

# Reject reconfiguration requests that would cause quorum loss.
strict-reconfig-check: false

# Enable runtime profiling data via HTTP server
enable-pprof: true

# Valid values include 'on', 'readonly', 'off'
proxy: 'off'

# Time (in milliseconds) an endpoint will be held in a failed state.
proxy-failure-wait: 5000

# Time (in milliseconds) of the endpoints refresh interval.
proxy-refresh-interval: 30000

# Time (in milliseconds) for a dial to timeout.
proxy-dial-timeout: 1000

# Time (in milliseconds) for a write to timeout.
proxy-write-timeout: 5000

# Time (in milliseconds) for a read to timeout.
proxy-read-timeout: 0

client-transport-security:
  # Path to the client server TLS cert file.
  cert-file:

  # Path to the client server TLS key file.
  key-file:

  # Enable client cert authentication.
  client-cert-auth: false

  # Path to the client server TLS trusted CA cert file.
  trusted-ca-file:

  # Client TLS using generated certificates
  auto-tls: false

peer-transport-security:
  # Path to the peer server TLS cert file.
  cert-file:

  # Path to the peer server TLS key file.
  key-file:

  # Enable peer client cert authentication.
  client-cert-auth: false

  # Path to the peer server TLS trusted CA cert file.
  trusted-ca-file:

  # Peer TLS using generated certificates.
  auto-tls: false

  # Allowed CN for inter peer authentication.
  allowed-cn:

  # Allowed TLS hostname for inter peer authentication.
  allowed-hostname:

# The validity period of the self-signed certificate, the unit is year.
self-signed-cert-validity: 1

# Enable debug-level logging for etcd.
log-level: debug

logger: zap

# Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
log-outputs: [stderr]

# Force to create a new one member cluster.
force-new-cluster: false

auto-compaction-mode: periodic
auto-compaction-retention: "1"

# Limit etcd to a specific set of tls cipher suites
cipher-suites: [
  TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
]

# Limit etcd to specific TLS protocol versions 
tls-min-version: 'TLS1.2'
tls-max-version: 'TLS1.3'
```

- 启动

```shell
/usr/bin/etcd --config-file /etc/etcd/conf.yaml
```

- systemd 配置

```text
# /etc/systemd/system/etcd.service
[Unit]
Description=etcd - Distributed Key Value Store
Documentation=https://etcd.io/docs
After=network.target
Wants=network-online.target
Requires=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/etcd --config-file /etc/etcd/conf.yaml
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

- systemd 管理

```shell
systemctl restart etcd
systemctl stop etcd
systemctl start etcd
systemctl status etcd
```

## 3. 使用

- Cli 存取数据

```shell
etcdctl put greeting "Hello, etcd"
etcdctl get greeting
etcdctl get "" --prefix --keys-only #获取所有的 key 值
```

## 4. 拓展信息

### 4.1. 出现 DNS IS Empty 错误

```shell
echo nameserver 8.8.8.8
```

### 4.2. 出现 open File 1024 错误

```shell
# /etc/security/limits.conf
root soft nofile 65535
root hard nofile 100000
yangxy soft nofile 65535
yangxy hard nofile 100000
```

> 注意：此处的用户信息最好不要使用*来代表所有用户，可能会出现配置不生效的问题

### 4.3. V2 Vs V3 版本

两个版本之间存在非常大的变动，API 等格式都不一致，请注意对应的版本

## 5. 参考资料

- [官方文档](https://etcd.io/)
