---
title: "Xray安装"
filename: xray-core-proxy-deployment
summary: Xray Core作为V2Ray安全增强版的网络代理工具，具有极强的流量伪装能力。本文整理了Xray的快速自动化脚本安装方式，提供了一份包含日志输出重定向、多协议入站代理监听、以及使用路由分流实现网络流量按国家或域名路由的基础JSON配置文件模版。
tags: [xray-core, network-proxy, v2ray-fork, routing-rules]
aliases: [Xray安装, Xray配置, V2ray增强版]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:09:29 中午
---

<!-- toc -->

## 1. 简介

一个代理软件

## 2. 安装/更新

```shell
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh) install
```

## 3. 配置

目录配置文件目录在/usr/local/etc/xray/config.json

```text
{
    "log": {
        "loglevel": "error"
     //"error": "/usr/local/etc/xray/xray_error.log"    // 错误记录
    },
    "inbounds": [
        {
            "port": 2022, # 可以换成其他端口
            "protocol": "vless",
            "settings": {
                "clients": [
                    {
                        "id": "**", // 填写UUID，可以使用xray uuid生成
                        "level": 1
                    }
                ],
                "decryption": "none",
                "fallbacks": [
                    {
                        "dest":80 // 回落配置，可以直接转到其他网站，例如"www.baidu.com:80"
                    }
                ]
            },
            "streamSettings": {
                "network": "ws",
                "security": "tls",
                "tlsSettings": {
                    "alpn": [
                        "http/1.1"
                    ],
                    "certificates": [
                        {
                            "certificateFile": "/root/certs/example.com/fullchain.pem", // 换成你的证书，绝对路径
                            "keyFile": "/root/certs/example.com/key.pem" // 换成你的私钥，绝对路径
                        }
                    ]
                },
                "fingerprint": "chrome"
            }
        },
        {
            "port": 2024, // 可以换成其他端口
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": "**", // 填写UUID，可以使用xray uuid生成
                        "level": 1
                    }
                ]
            },
            "streamSettings": {
                "network": "ws",
                "tlsSettings": {
                    "alpn": [
                        "http/1.1"
                    ]
                },
                "wsSettings": {
                    "path": "/**"
                }
            },
            "sniffing": {
                "enabled": true, // 开启流量探测，用于分流或屏蔽 BT 协议。
                "destOverride": [ // 当流量为指定类型时，按其中包括的目标地址重置当前连接的目标。
                    "http",
                    "tls",
                    "quic"
                ]
            }
        },
        {
            "port": 2023, // 可以换成其他端口
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": "**", // 填写UUID，可以使用xray uuid生成
                        "level": 1
                    }
                ]
            },
            "streamSettings": {
                "network": "ws",
                "security": "tls",
                "tlsSettings": {
                    "alpn": [
                        "http/1.1"
                    ],
                    "certificates": [
                        {
                            "certificateFile": "/root/certs/example.com/fullchain.pem", // 换成你的证书，绝对路径
                            "keyFile": "/root/certs/example.com/key.pem" // 换成你的私钥，绝对路径
                        }
                    ]
                },
                "wsSettings": {
                    "path": "/**"
                }
            },
            "sniffing": {
                "enabled": true, // 开启流量探测，用于分流或屏蔽 BT 协议。
                "destOverride": [ // 当流量为指定类型时，按其中包括的目标地址重置当前连接的目标。
                    "http",
                    "tls",
                    "quic"
                ]
            }
        },
        {
          "tag": "naiveproxy_in",
          "port": 2025,
          "listen": "127.0.0.1",
          "protocol": "socks"
        }
    ],
    "outbounds": [
        {
            "protocol": "freedom"
        },
        { // 出站 路由标记示例。WARP WireGuard 双栈非全局路由分流
                "tag": "WARP_x",
                "protocol": "freedom",
                "streamSettings": {
                        "sockopt": {
                            "mark": 51888  // 路由标记
                        }
                    },
                "settings": {
                    "domainStrategy": "UseIP" // "UseIP"(双栈自适应)、”UseIPv4”(IPv4 优先)、”UseIPv4”(Pv6 优先)
                }
        },
        {
            "tag":"WARP_SOCK",
            "protocol":"socks",
            "settings":{
                "servers": [
                    {
                        "address": "127.0.0.1",
                        "port": 40000
                    }
                ],
                "domainStrategy": "UserIP"
            }
        }
    ],
    "routing":{
        "domainStrategy":"AsIs",
        "rules":[
            {
                "type":"field",
                "domain":[
                "domain:openai.com",
                "domain:ai.com",
                "geosite:netflix",
            "domain:netflix.com",
            "domain:netflix.net",
            "domain:nflximg.net",
            "domain:nflxvideo.net",
            "domain:nflxso.net",
            "domain:nflxext.com"
                ],
                "outboundTag":"WARP_SOCK"
            }
 ]
    }
}
```

## 4. 拓展信息

- http 代理服务与 http 请求不一致。所以直接通过 xray 配置的 http inbound 不可以直接处理 http 请求的。
- 权限问题  
无法打开证书文件
  - 修改/ect/systemd/system/xray.service 中的 user 为 root
  - 确保证书文件目录拥有执行 x 权限

## 5. 参考资料

- [官方链接](https://xtls.github.io/config/inbound.html#inboundobject)
- [Github 地址](https://github.com/XTLS/Xray-core)
- [Examle](https://github.com/XTLS/Xray-examples)
