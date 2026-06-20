---
title: "SingBox配置"
filename: sing-box-universal-proxy-client
description: sing-box是新一代高性能通用代理软件与核心网络工具。本文涵盖sing-box在Ubuntu环境下的安装，提供一份包含日志等级控制、出站规则路由、安全DNS分流等基础配置信息的JSON配置模版，帮助用户理解和实现自定义智能路由及复杂的网络流量转发。
tags: [sing-box, universal-proxy, dns-routing, network-infrastructure]
aliases: [SingBox配置, 新型代理软件, 出站路由分流]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:55 上午
date modified: 星期五, 六月 19日 2026, 12:08:41 中午
---

<!-- toc -->

## 1. 简介

一个代理软件

## 2. 安装

- 安装

```shell
bash <(curl -fsSL https://sing-box.app/deb-install.sh)
```

## 3. 配置

- 配置参考

```json
# /etc/sing-box/config.json
{
  "log": {
    "disabled": false,
    "level": "error",
    "output": "/var/log/singbox.log",
    "timestamp": true
  },
  "dns": {},
  "ntp": {},
  "inbounds": [
    {
      "type": "naive",
      "listen": "::",
      "listen_port": 4001,
      "users": [
        {
          "username": "yxy",
          "password": "upFrrqjK5g"
        }
      ],
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      },
      "tag": "naive_in_old"
    },
    {
      "type": "vmess",
      "tag": "vmess_in_old",
      "listen": "::",
      "listen_port": 4002,
      "users": [
        {
          "uuid": "85b3a1c7-4670-438b-b971-4dbbed3a6c02",
          "alterId": 0
        }
      ],
      "transport": {
        "type": "ws",
        "path": "/85b3a1c7-4670-438b-b971-4dbbed3a6c02",
        "max_early_data": 2048,
        "early_data_header_name": "Sec-WebSocket-Protocol"
      },
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      }
    },
    {
      "type": "vless",
      "tag": "vless_in_old",
      "listen": "::",
      "listen_port": 4003,
      "users": [
        {
          "uuid": "85b3a1c7-4670-438b-b971-4dbbed3a6c02"
        }
      ],
      "transport": {
        "type": "ws",
        "path": "/85b3a1c7-4670-438b-b971-4dbbed3a6c02",
        "max_early_data": 2048,
        "early_data_header_name": "Sec-WebSocket-Protocol"
      },
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      }
    },
    {
      "type": "hysteria2",
      "tag": "hysteria2_in_old",
      "listen": "::",
      "listen_port": 4004,
      "up_mbps": 100,
      "down_mbps": 20,
      "users": [
        {
          "password": "upFrrqjK5g"
        }
      ],
      "tls": {
        "enabled": true,
        "alpn": [
          "h3"
        ],
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      }
    },
    {
      "type": "hysteria",
      "tag": "hysteria_in_old",
      "listen": "::",
      "listen_port": 4006,
      "up_mbps": 100,
      "down_mbps": 20,
      "users": [
        {
          "auth_str": "upFrrqjK5g"
        }
      ],
      "tls": {
        "enabled": true,
        "alpn": [
          "h3"
        ],
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      }
    },
    {
      "type": "trojan",
      "tag": "trojan_in_old",
      "listen": "::",
      "listen_port": 4005,
      "users": [
        {
          "password": "upFrrqjK5g"
        }
      ],
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      },
      "multiplex": {
        "enabled": true
      }
    },
    {
      "type": "naive",
      "listen": "::",
      "listen_port": 5001,
      "users": [
        {
          "username": "tm",
          "password": "pk8G6k9aTGt73d"
        }
      ],
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      },
      "tag": "naive_in"
    },
    {
      "type": "vmess",
      "tag": "vmess_in",
      "listen": "::",
      "listen_port": 5002,
      "users": [
        {
          "uuid": "acd09fff-3904-480a-a312-8a9a9b1aaf44",
          "alterId": 0
        }
      ],
      "transport": {
        "type": "ws",
        "path": "/demo-account",
        "max_early_data": 2048,
        "early_data_header_name": "Sec-WebSocket-Protocol"
      },
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      }
    },
    {
      "type": "vless",
      "tag": "vless_in",
      "listen": "::",
      "listen_port": 5003,
      "users": [
        {
          "uuid": "acd09fff-3904-480a-a312-8a9a9b1aaf44",
          "flow": "xtls-rprx-vision"
        }
      ],
      "tls": {
        "enabled": true,
        "server_name": "www.microsoft.com",
        "reality": {
          "enabled": true,
          "handshake": {
            "server": "www.microsoft.com",
            "server_port": 443
          },
          "private_key": "cAo_sswHagnOKA-VFDek44lvn6b8oU3kaNl2ESgSM1Y",
          "short_id": [
            ""
          ]
        }
      }
    },
    {
      "type": "hysteria2",
      "tag": "hysteria2_in",
      "listen": "::",
      "listen_port": 5004,
      "up_mbps": 100,
      "down_mbps": 20,
      "users": [
        {
          "password": "fV2Qk6tvtB7Mnd2V"
        }
      ],
      "tls": {
        "enabled": true,
        "alpn": [
          "h3"
        ],
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      }
    },
    {
      "type": "trojan",
      "tag": "trojan_in",
      "listen": "::",
      "listen_port": 5005,
      "users": [
        {
          "password": "BNZije223r3Hmd4D"
        }
      ],
      "tls": {
        "enabled": true,
        "certificate_path": "/usr/local/ssl/fullchain.cer",
        "key_path": "/usr/local/ssl/best.key"
      },
      "multiplex": {
        "enabled": true
      }
    }
  ],
  "endpoints": [],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct_out"
    },
    {
      "type": "socks",
      "tag": "socks_out",
      "server": "signa-vm1.proxy.truemetrics.cn",
      "server_port": 5006,
      "version": "5",
      "username": "tm",
      "password": "chumai2026"
    }
  ],
  "route": {
    "rules": [
      {
        "domain_keyword": [
          "openai",
          "chatgpt",
          "gemini",
          "claude",
          "groq",
          "generativeai",
          "generativelanguage",
          "alkalimakersuite-pa.clients6"
        ],
        "outbound": "socks_out"
      }
    ],
    "final": "direct_out"
  },
  "experimental": {}
}
```

## 4. 管理

```bash
systemclt status sing-box
systemclt start sing-box
systemclt stop sing-box
systemclt restart sing-box
```

## 5. 参考资料

- [官方链接](https://sing-box.sagernet.org/configuration/inbound/naive/)
