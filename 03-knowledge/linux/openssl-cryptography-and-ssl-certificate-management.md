---
status: completed
filename: openssl-cryptography-and-ssl-certificate-management
title: "OpenSSL 命令"
summary: 本笔记记录了强大的开源安全加密库 OpenSSL 的常用运维指令。详细覆盖了从文本/文件级 MD5 数据摘要生成（含加盐处理），到基于 RSA 算法非对称密钥对（公私钥）的创建。重点梳理了构建自签名证书体系的全链路操作：生成根 CA、签发包含 SAN（多域名备用名称）扩展的 CSR 请求，以及最终签署 `.crt` 服务端证书的流程，是搭建内网 HTTPS 测试环境或进行数据防篡改校验的基础字典。
aliases: [OpenSSL 命令, 生成 SSL 证书, 自签名证书, 生成 RSA 密钥]
tags: [Linux, 网络安全, SSL, 密码学, OpenSSL, 证书管理, HTTPS]
date created: 星期二, 二月 25日 2025, 3:24:01 下午
date modified: 星期四, 六月 18日 2026, 12:55:00 晚上
---

<!-- toc -->

## 1. 工具定位

**OpenSSL** 是一个稳健、功能齐全的开源加密库和工具包，实现了 SSL 及 TLS 协议，并提供了包括数据摘要、对称/非对称加密及完整的 X.509 数字证书管理能力。

---

## 2. 数据摘要与密码散列

通常用于校验文件完整性或生成单向密码哈希。

```bash
# 生成文件的 MD5 摘要
openssl dgst -md5 target_file.txt

# 生成字符串摘要 (注意 echo 必须加 -n 防止换行符污染哈希结果)
echo -n "admin123" | openssl md5

# 使用特定盐值生成系统密码
openssl passwd -1 -in password_file.txt -salt myRandomSalt
```

---

## 3. 非对称加密：RSA 密钥对生成

```bash
# 生成 2048 位的 RSA 强私钥
openssl genrsa -out rsa_private.key 2048 

# 从私钥中提取分离出对应的公钥
openssl rsa -in rsa_private.key -pubout -out rsa_public.key
```

---

## 4. 证书探查与系统信任注入

**探查现有证书细节**：

```bash
# 检查证书有效期
openssl x509 -enddate -noout -in /path/to/server.crt 
# 查看证书完整载荷与颁发信息
openssl x509 -text -noout -in /path/to/server.crt 
```

**将内网证书注入 Linux 系统根信任区 (以 Ubuntu 为例)**：

```bash
sudo cp ca.crt /usr/local/share/ca-certificates/my_internal_ca.crt
sudo update-ca-certificates
```

---

## 5. 实战：生成包含 SAN 的自制 SSL 证书

在现代浏览器（如 Chrome）中，传统的单一 CN（公用名）已被弃用，必须在证书的 **SAN (Subject Alternative Name)** 扩展中声明所有关联的域名，否则会被拦截拦截为“不安全”。

### 5.1. Step A: 建立自签的根 CA (Certificate Authority)

```bash
# 1. 生成 CA 自己的私钥
openssl genrsa -out ca.key 2048 

# 2. 生成长效期 (100 年) 的根证书 (CRT)
openssl req -sha256 -new -x509 -days 36500 -key ca.key -out ca.crt \
    -subj "/C=CN/ST=GD/L=SZ/O=MyCompany/OU=IT/CN=MyInternalRootCA" 
```

### 5.2. Step B: 颁发服务端业务证书

```bash
# 1. 生成服务端私钥
openssl genrsa -out server.key 2048 

# 2. 生成证书签名请求 (CSR)，同时在请求中挂载多域名 SAN 扩展
openssl req -new -sha256 -key server.key -out server.csr \
    -subj "/C=CN/ST=GD/L=SZ/O=MyCompany/OU=IT/CN=wsl.domain.com" \
    -reqexts SAN -config <(cat /etc/pki/tls/openssl.cnf \
        <(printf "\n[SAN]\nsubjectAltName=DNS:*.wsl.domain.com,DNS:wsl.domain.com"))

# 3. 使用自建的 CA 证书与私钥，正式签署业务证书
openssl ca -in server.csr -days 36500 -md sha256 -keyfile ca.key -cert ca.crt \
    -extensions SAN -config <(cat /etc/pki/tls/openssl.cnf \
        <(printf "\n[SAN]\nsubjectAltName=DNS:*.wsl.domain.com,DNS:wsl.domain.com")) \
    -out server.crt
```

> [!warning] 数据库索引错误修复
> 若在执行签署时触发 `unable to open '/etc/pki/CA/index.txt'` 等追踪库相关错误，需手动重置 OpenSSL 的签发追踪库：
>
> ```bash
> mkdir -p /etc/pki/CA
> touch /etc/pki/CA/index.txt
> echo 00 > /etc/pki/CA/serial
> ```
