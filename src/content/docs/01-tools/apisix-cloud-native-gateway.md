---
title: "Apache APISIX"
filename: apisix-cloud-native-gateway
summary: Apache APISIX 是一款高性能、云原生的开源 API 网关，基于 Nginx 和 etcd 实现。本笔记详细记录了 APISIX 的裸机安装步骤、核心配置文件（config.yaml）详解、服务管理命令以及通过 Admin API 进行路由验证的方法。同时涵盖了 Elasticsearch Logger 插件的配置、手动安装外部插件的流程，以及 APISIX Dashboard 的编译与部署方案，解决了 API 流量管理、监控及插件扩展的核心需求。
tags: ["APISIX", "API-Gateway", "Cloud-Native", "Nginx", "Etcd"]
aliases: ["Apache APISIX", "APISIX网关", "云原生网关"]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:55 上午
date modified: 星期五, 六月 19日 2026, 11:57:14 中午
---

<!-- toc -->

## 1. 简介

**Apache APISIX** 是一款高性能、可扩展的云原生 API 网关。它不仅提供了传统的负载均衡、动态路由、身份验证等功能，还支持动态配置和丰富的插件扩展，能够满足现代微服务架构对流量管理的复杂需求。APISIX 基于 Nginx 和 etcd 开发，确保了极高的性能和配置的实时同步。

---

## 2. 安装与配置

### 2.1. APISIX 核心安装 (裸机)

在 Debian/Ubuntu 环境下，可以通过以下步骤进行安装：

```shell
# 添加 APISIX 软件源
wget -O - http://repos.apiseven.com/pubkey.gpg | sudo apt-key add -
echo "deb http://repos.apiseven.com/packages/debian bullseye main" | sudo tee /etc/apt/sources.list.d/apisix.list
sudo apt update

# 安装指定版本的 APISIX
sudo apt install -y apisix=3.8.0-0

# 初始化配置
sudo apisix init
```

### 2.2. 核心配置文件 (`config.yaml`)

配置文件通常位于 `/usr/local/apisix/conf/config.yaml`。以下是一个典型的配置示例，包含 etcd 连接和 Prometheus 监控：

```yaml
apisix:
  node_listen: 9080 # HTTP 入口监听端口
  ssl:
    listen:
      - port: 9443
        enable_http2: true
deployment:
  role: traditional
  role_traditional:
    config_provider: etcd
  admin:
    admin_key:
      - name: admin
        key: [ADMIN_KEY_已隐藏] # 生产环境请务必修改此密钥
        role: admin
  etcd:
     host:
       - http://[IP_已隐藏]:2379 # 替换为实际的 etcd 地址
plugin_attr:
  prometheus:
    export_uri: /apisix/prometheus/metrics

    enable_export_server: true
    export_addr:
      ip: 0.0.0.0
      port: 9091
```

### 2.3. 服务管理

```shell
# 使用 systemd 管理
systemctl start apisix
systemctl restart apisix
systemctl stop apisix
systemctl status apisix

# 或使用 apisix 命令直接操作
sudo apisix start
```

---

## 3. 路由管理与插件配置

### 3.1. 路由验证示例

通过 Admin API 创建一个简单的路由，将流量转发至 `httpbin.org`：

```shell
curl -i "http://127.0.0.1:9180/apisix/admin/routes" \
-H 'X-API-KEY: [ADMIN_KEY_已隐藏]' -X PUT -d '
{
  "id": "getting-started-ip",
  "uri": "/ip",
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "httpbin.org:80": 1
    }
  }
}'

# 验证路由
curl "http://127.0.0.1:9080/ip"
```

### 3.2. 配置 Elasticsearch Logger 插件

```shell
curl -i "http://127.0.0.1:9180/apisix/admin/routes/2" \
-H "X-API-KEY: [ADMIN_KEY_已隐藏]" -X PUT -d '  
{  
"plugins":{  
 "elasticsearch-logger":{  
  "endpoint_addr":"http://[IP_已隐藏]:9200",  
  "field":{ "index":"services", "type":"collector" },  
  "auth":{ "username":"elastic", "password":"[PASSWORD_已隐藏]" },  
  "ssl_verify":false,  
  "batch_max_size":1000,  
  "name":"elasticsearch-logger"  
  }
 },  
 "upstream":{  
  "type":"roundrobin",  
  "nodes":{ "httpbin.org:80": 1 }  
 }, 
 "uri":"/ip"  
}'
# 获取日志
curl https://192.168.56.1:9200/services/_search -u elastic:example --insecure
```

### 3.3. Apisix 手动安装插件

1. github 查找插件 <https://github.com/apache/apisix#>
2. 上传到指定目录 /usr/local/apisix/apisix/plugins
3. 配置开启插件

```yml
# /usr/local/apisix/conf/config.yml
plugins:                                                             
  - ai-proxy
```

### 3.4. Apisix Dashboard

- 安装

```shell
git clone -b release/3.0 https://github.com/apache/apisix-dashboard.git && cd apisix-dashboard 
make build
mkdir -p /usr/local/apisix-dashboard
cp -rf ./output/* /usr/local/apisix-dashboard
```

- 配置

```yaml
#/usr/local/apisix-dashboard/conf/conf.yaml
conf:
  security:
    access_control_allow_origin: "http://httpbin.org"
    access_control_allow_credentials: true          # support using custom cors configration
    access_control_allow_headers: "Authorization"
    access_control-allow_methods: "*"
    x_frame_options: "deny"
    content_security_policy: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-src localhost:3000"  # You can set frame-src to provide content for your grafana panel.
```

- systemd 配置

```text
# /usr/lib/systemd/system/apisix-dashboard.service
[Unit]
Description=apisix-dashboard
After=network-online.target

[Service]
WorkingDirectory=/usr/local/apisix-dashboard
ExecStart=/usr/local/apisix-dashboard/manager-api -c /usr/local/apisix-dashboard/conf/conf.yaml
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 4. 拓展信息与常见问题

- **etcd 依赖**：APISIX 强依赖 etcd 进行配置存储，启动前请确保 etcd 服务可用。
- **证书管理**：建议通过 Admin API 上传 SSL 证书，以避免 Dashboard 某些版本中可能存在的证书编码兼容性问题。
- **默认端口说明**：
  - `9080`: HTTP 业务流量入口
  - `9443`: HTTPS 业务流量入口
  - `9180`: 管理端 Admin API 接口

### 4.1. Dashboard 编译与常见问题

- **编译前置要求**：
  在安装和编译 Dashboard 前，请确保系统中已安装 `Node.js` (版本推荐 `14.*`)、`Yarn`、`Go` 和 `APISIX`。

- **Web 编译证书错误**：
  若在执行 `web build` 时遇到证书错误，可以采用以下两种方式之一解决：
  - 修改 `web/package.json` 中的 `build` 命令：

    ```json
    "build": "yarn copy-folder monaco-editor ./public/ && NODE_OPTIONS=--max_old_space_size=4096 NODE_OPTIONS=--openssl-legacy-provider umi build"
    ```

  - 或者删除 `web/yarn.lock` 文件并重新生成。

- **Web 编译 mjs 错误**：
  若在执行 `web build` 时遇到 `.mjs` 相关的编译错误，请修改 `web/conf/conf.ts` 中的 `chainWebpack` 方法，添加对 `.mjs` 文件的处理规则：

  ```typescript
  chainWebpack(conf) {
    // ....other config
    conf.module
      .rule('mjs$')
      .test(/\.mjs$/)
      .include
        .add(/node_modules/)
        .end()
      .type('javascript/auto');
  }
  ```

---

## 5. 参考资料

- [Apache APISIX 官方文档](https://apisix.apache.org/)
- [APISIX GitHub 仓库](https://github.com/apache/apisix)
