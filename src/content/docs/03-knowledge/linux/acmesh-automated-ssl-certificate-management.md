---
status: completed
filename: acmesh-automated-ssl-certificate-management
title: "Acme.sh 证书"
summary: 本笔记详述了基于 Shell 脚本的轻量级 ACME 协议客户端 Acme.sh 的高级部署与操作流程。全面梳理了在 Linux 系统上的安装配置方法（涵盖指定 Default CA），重点整理了利用云厂商 DNS API（如华为云、Cloudflare）自动添加 TXT 记录以完成域名所有权验证并签发泛域名证书的实战指令。此外，提供了通过 `install-cert` 钩子自动重启系统代理服务（如 systemctl restart nginx）以及强制续期证书的运维标准动作，是保障 Web 服务 HTTPS 链路高可用与免维护的核心脚本。
aliases: [Acme.sh 证书, Let's Encrypt 签发, 自动续期 SSL, DNS 验证证书]
tags: [Linux, 网络安全, SSL, HTTPS, Acme.sh, Let's Encrypt, Nginx, 自动化运维]
date created: 星期一, 一月 12日 2026, 10:03:44 上午
date modified: 星期四, 六月 18日 2026, 12:45:00 晚上
---

<!-- toc -->

## 1. 工具定位

**Acme.sh** 是一个完全用纯 Shell 脚本编写的 ACME 协议客户端。无需安装额外的 Python 环境或庞大的 certbot，即可自动从 Let's Encrypt、ZeroSSL 等证书颁发机构签发、安装并自动续期 HTTPS (SSL/TLS) 证书。

---

## 2. 基础部署与高级安装

### 2.1. 方案 A：一键基础安装

```bash
curl https://get.acme.sh | sh -s email=my@example.com
```

### 2.2. 方案 B：高度定制化安装 (推荐)

自定义所有证书缓存与配置的落盘目录，方便集中隔离管理：

```bash
git clone --depth 1 https://github.com/acmesh-official/acme.sh.git
cd acme.sh

# 挂载定制化路径与身份邮箱
./acme.sh --install -m example@gmail.com \
    --home ~/myacme \
    --config-home ~/myacme/data \
    --cert-home ~/mycerts \
    --accountemail "my@example.com" \
    --accountkey ~/myaccount.key \
    --accountconf ~/myaccount.conf \
    --useragent "this is my client."

# 将 acme.sh 注入终端环境变量
echo '. "/opt/software/acme.sh/acme.sh.env"' >> ~/.bashrc

# 强制切换默认 CA 机构为稳定的 Let's Encrypt (默认可能是 ZeroSSL)
./acme.sh --set-default-ca --server letsencrypt
```

---

## 3. 签发实战：基于 DNS API 自动认证

申请泛域名证书（如 `*.example.com`）必须使用 DNS 验证（通过向域名商自动插入 TXT 记录证明你对该域名的所有权）。

### 3.1. 场景 1：华为云 (Huawei Cloud)

首先在终端环境中注入云账号的 API Key/Secret 令牌：

```bash
export HUAWEICLOUD_Username="your_username"
export HUAWEICLOUD_Password="your_password"
export HUAWEICLOUD_DomainName="your_domain"

# 发起自动签发请求 (-d 参数可以叠加，涵盖根域与泛域名)
./acme.sh --issue --dns dns_huaweicloud -d example.com -d *.example.com
```

### 3.2. 场景 2：Cloudflare

```bash
export CF_Token="your_cf_api_token"  
export CF_Account_ID="your_account_id"

./acme.sh --issue --dns dns_cf -d example.com -d *.example.com
```

---

## 4. 运维挂载：安装证书至 Web 服务

> [!warning] 避坑指南
> 绝对不要直接配置 Nginx/Apache 去读取 Acme.sh 内部工作目录下的证书文件。内部文件结构随时会变。
> 必须使用 `install-cert` 命令将证书“拷贝”到你的指定 Web 服务器配置目录，并绑定 reload 重启命令。

```bash
./acme.sh --install-cert -d example.com \
    --cert-file      /root/certs/example.com/cert.pem \
    --key-file       /root/certs/example.com/key.pem \
    --fullchain-file /root/certs/example.com/fullchain.pem \
    --reloadcmd      "systemctl restart nginx"
```

*备注：Acme.sh 会记住这条 `install-cert` 指令。未来触发自动续期（Renew）完成后，它将自动再次执行拷贝操作，并触发最后一行 `reloadcmd` 以重启 Web 服务使新证书生效。*

## 5. 其他高频操作

**强制手动续期 (测试用)**：

```bash
acme.sh --renew -d example.com --force
```

## 6. 参考资料

- [Acme.sh 官方 GitHub 与集成指南](https://github.com/acmesh-official/acme.sh)
