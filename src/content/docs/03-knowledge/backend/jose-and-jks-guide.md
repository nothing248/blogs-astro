---
title: "JWS与JWE"
filename: jose-and-jks-guide
summary: 介绍 JOSE（JSON Web 签名和加密）安全传输协议族，涵盖 JWS、JWE、JWK、JWKS 和 JWA 等核心组件及密钥轮换工作流。对比了 Python 库 jwcrypto 与 josepy 的异同。同时，详解了 Java KeyStore (JKS) 的存储格式与 Java 读取密钥的实现，并汇总了使用 keytool 生成密钥、列出信息、导出证书及通过 OpenSSL 导出 PEM 私钥的常用运维指令。
tags:
  - JOSE协议
  - JKS
  - 密钥管理
  - 加密与签名
  - keytool
aliases:
  - JWS与JWE
  - Java密钥库
  - JWKS密钥轮换
  - PEM私钥导出
status: completed
date created: 星期一, 十二月 10日 2025, 9:59:23 上午
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 简介

JOSE (JavaScript Object Signing and Encryption) 是一套 IETF 标准，用于安全地传输数据。 它定义了一组基于 JSON 的安全协议，用于对数据进行签名、加密和密钥管理。 JOSE 旨在简化 Web 应用程序、API 和其他应用中的安全实现，并提供互操作性。

## 2. 概念

- **JWS (JSON Web Signature)：** 用于对 JSON 数据进行数字签名，以保证数据的完整性和来源可信性。
- **JWE (JSON Web Encryption)：** 用于对 JSON 数据进行加密，以保护数据的机密性。
- **JWK (JSON Web Key)：** 用于表示密钥的 JSON 对象，支持对称密钥和非对称密钥。
- **JWKS (JSON Web Key Set)：** 包含一组 JWK 的 JSON 对象，用于密钥轮换和多密钥支持。
- **JWA (JSON Web Algorithms)：** 定义了 JOSE 中使用的各种算法，包括签名算法、加密算法和密钥 Agreement 算法等。

## 3. 流程

1. **服务提供方生成密钥对：** 服务提供方生成用于签名的私钥和公钥，并将公钥封装到 JWK 对象中。
2. **服务提供方发布 JWKS 端点：** 服务提供方创建一个 JWKS 端点，将包含公钥的 JWK 对象发布到该端点。
3. **客户端获取 JWKS：** 客户端从服务提供方的 JWKS 端点获取 JWK 对象。
4. **服务提供方生成 JWS：** 服务提供方使用私钥对数据进行签名，生成 JWS 对象。
5. **服务提供方将 JWS 发送给客户端：** 服务提供方将 JWS 对象发送给客户端。
6. **客户端验证 JWS：** 客户端使用从 JWKS 端点获取的公钥验证 JWS 对象的签名，确认数据的有效性和可信度。

## 4. 使用

### 4.1. Python

```python

```

### 4.2. JAVA

```java
import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.Certificate;

public class JKSExample {

    public static void main(String[] args) throws Exception {
        // 1. 加载 JKS 文件
        String keystoreFile = "mykeystore.jks";
        String keystorePass = "mypassword";
        String alias = "mykey";

        KeyStore keyStore = KeyStore.getInstance("JKS");
        try (FileInputStream fis = new FileInputStream(keystoreFile)) {
            keyStore.load(fis, keystorePass.toCharArray());
        }

        // 2. 获取私钥
        PrivateKey privateKey = (PrivateKey) keyStore.getKey(alias, keystorePass.toCharArray());
        System.out.println("Private Key: " + privateKey);

        // 3. 获取证书
        Certificate certificate = keyStore.getCertificate(alias);
        System.out.println("Certificate: " + certificate);

        // 4. 获取可信证书
        Certificate caCert = keyStore.getCertificate("cacert"); // 假设有别名为 cacert 的可信证书
        if (caCert != null){
            System.out.println("CA Certificate: " + caCert);
        }

    }
}
```

## 5. 拓展信息

### 5.1. python 中的 jwcrypto、josepy 区别

```
- 实现方式： jwcrypto 是纯 Python 实现，不依赖 OpenSSL，而 josepy 则依赖于 cryptography 库。
- 设计目标： jwcrypto 旨在提供高性能和安全性，而 josepy 则更注重易用性和扩展性。
- 应用场景： jwcrypto 适用于需要高性能和安全性的场景，例如 API 安全、身份验证等。 josepy 适用于需要易用性和扩展性的场景，例如 ACME 客户端开发。
- ACME 支持： josepy 专门为 ACME 协议设计，提供了 ACME 协议相关的 API。
- 更新频率： josepy 的更新频率可能较低，因为它主要服务于 Let's Encrypt 项目。
```

### 5.2. JKS

JKS (Java KeyStore) 是 Java 平台中用于存储密钥和证书的标准格式。 它可以被认为是 Java 的密钥和证书的容器，提供了一种安全的方式来管理用于加密、身份验证和授权的密钥和证书。

- 包含数据

```
- Key Entry (密钥条目): 包含一个私钥以及与该私钥关联的公钥证书链。 私钥用于加密、解密或签名，公钥证书用于验证身份。
- Trusted Certificate Entry (可信证书条目): 包含一个可信的公钥证书，通常是 CA (证书颁发机构) 的根证书或中间证书。 用于验证服务器或客户端证书的有效性。
- Secret Key Entry (秘密密钥条目): 包含一个对称密钥，例如用于 AES 或 DES 加密的密钥。 对称密钥用于加密和解密数据。
```

- keytools 解析

```shell
# 1. 生成密钥对
keytool -genkeypair -alias <alias> -keyalg <keyalg> -keysize <keysize> -sigalg <sigalg> -validity <validity> -keystore <keystore> -storepass <storepass>
# 参数信息
-genkeypair: (推荐) 生成密钥对，同时创建自签名证书。 -genkey 是旧版本命令，功能较少。
-alias <alias>: 指定密钥对的别名，用于在密钥库中标识该密钥对。 别名必须唯一。
-keyalg <keyalg>: 指定密钥算法。 常用的密钥算法包括 RSA (默认), DSA, EC (椭圆曲线)。
-keysize <keysize>: 指定密钥长度，单位为位。 RSA 密钥常用的长度包括 2048 位、3072 位和 4096 位。 EC 密钥常用的长度包括 256 位和 384 位。 密钥长度越长，安全性越高，但计算速度越慢。
-sigalg <sigalg>: 指定签名算法。 常用的签名算法包括 SHA256withRSA, SHA512withRSA, SHA256withECDSA 等。
-validity <validity>: 指定证书的有效期，单位为天。
-keystore <keystore>: 指定密钥库的文件名。 如果密钥库文件不存在，则会自动创建。
-storepass <storepass>: 指定密钥库的密码。 必须记住该密码，才能访问密钥库中的内容。
-keypass <keypass>: 指定密钥的密码。 如果不指定，则默认与 -storepass 相同。 建议为密钥设置单独的密码，提高安全性。
-dname <dname>: 指定证书的 Distinguished Name (DN)，包含证书所有者的信息，例如 CN (Common Name)、OU (Organizational Unit)、O (Organization)、L (Locality)、ST (State)、C (Country)。 可以使用 -dname "CN=example.com, OU=My Department, O=My Organization, L=My City, ST=My State, C=US" 格式指定 DN。
-ext <ext>: 指定证书扩展，例如 -ext san=dns:example.com,dns:www.example.com 可以为证书添加 Subject Alternative Name (SAN) 扩展，支持多个域名。

# 2. 列出密钥信息
keytool -list -v -keystore <keystore> -storepass <storepass>

-list: 列出密钥库中的所有条目。
-v: 显示详细信息。
-keystore <keystore>: 指定密钥库的文件名。
-storepass <storepass>: 指定密钥库的密码。

# 3. 导出证书
keytool -exportcert -alias <alias> -file <certificate_file> -keystore <keystore_file> -storepass <keystore_password>

- <alias>: 要导出证书的密钥对的别名。  
- <certificate_file>: 导出的证书文件的文件名 (例如 certificate.cer, certificate.pem)。
- <keystore_file>: 密钥库文件名 (例如 keystore.jks)。
- <keystore_password>: 密钥库的密码。

# 4. 导出 PEM 私钥
keytool -importkeystore -srckeystore keystore.jks -destkeystore temp.p12 -deststoretype PKCS12 -srcstorepass example -srcalias test-dja -destkeypass example -deststorepass example1 
openssl pkcs12 -in temp.p12 -out private_key.pem -nodes -passin pass:example1 
rm temp.p12 # 删除临时文件

- <src_keystore>: 源 JKS 密钥库文件名。
- <dest_keystore>: 目标 PKCS12 密钥库文件名。
- <deststoretype>: 指定目标密钥库类型为 PKCS12。
- <src_storepass>: 源 JKS 密钥库的密码。
- <dest_storepass>: 目标 PKCS12 密钥库的密码。
- <alias>: 要导出的密钥对的别名，如果不指定，默认导出所有
```
