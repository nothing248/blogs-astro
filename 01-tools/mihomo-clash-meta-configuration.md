---
title: "Mihomo安装"
filename: mihomo-clash-meta-configuration
description: Mihomo（前身Clash Meta）是内核级开源代理客户端。本文整理了Mihomo在Linux环境下的安装源与配套Web管理界面（如metacubexd、yacd）的对接方式，并提供了包含策略组锚点定义、节点过滤器映射、自定义规则集等核心字段的详细配置文件范本。
tags:
  - mihomo
  - clash-meta
  - proxy-client
  - network-routing
aliases:
  - Mihomo安装
  - ClashMeta配置
  - 代理内核
status: completed
date created: 星期一, 五月 19日 2025, 2:05:26 下午
date modified: 星期二, 六月 16日 2026, 6:24:15 晚上
---

<!-- toc -->

## 1. 简介

Clash Meta 最新版的开源项目

## 2. 安装

### 2.1. 应用

- [安装地址](https://wiki.metacubex.one/en/startup/)

### 2.2. Web 管理界面

- [metacubexd](https://github.com/MetaCubeX/metacubexd)
- [yacd](https://github.com/haishanh/yacd)

## 3. 配置文件

```
######### 锚点 start #######
# 策略组相关
pr: &pr {type: select, proxies: [默认,香港,台湾,日本,新加坡,美国,其它地区,全部节点,自动选择,直连]}

#这里是订阅更新和延迟测试相关的
p: &p {type: http, interval: 3600, health-check: {enable: true, url: https://www.gstatic.com/generate_204, interval: 300}}

######### 锚点 end #######

# url 里填写自己的订阅,名称不能重复
proxy-providers:
  provider1:
    <<: *p
    url: ""

  provider2:
    <<: *p
    url: ""

ipv6: true
allow-lan: true
mixed-port: 7890
unified-delay: false
tcp-concurrent: true
external-controller: 127.0.0.1:9090
external-ui: ui #此处指定的是管理页面所在的文件目录
external-ui-url: "https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip"

find-process-mode: strict
global-client-fingerprint: chrome

profile:
  store-selected: true
  store-fake-ip: true

sniffer:
  enable: true
  sniff:
    HTTP:
      ports: [80, 8080-8880]
      override-destination: true
    TLS:
      ports: [443, 8443]
    QUIC:
      ports: [443, 8443]
  skip-domain:
    - "Mijia Cloud"
tun:
  enable: true
  stack: mixed
  dns-hijack:
    - "any:53"
  auto-route: true
  auto-detect-interface: true

dns:
  enable: true
  listen: :1053
  ipv6: true
  enhanced-mode: fake-ip
  fake-ip-range: 28.0.0.1/8
  fake-ip-filter:
    - "*"
    - "+.lan"
    - "+.local"
  default-nameserver:
    - 223.5.5.5
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  proxy-server-nameserver:
    - https://doh.pub/dns-query
  nameserver-policy:
    "rule-set:cn_domain,private":
      - https://doh.pub/dns-query
      - https://dns.alidns.com/dns-query
    "rule-set:geolocation-!cn":
      - "https://dns.cloudflare.com/dns-query#dns"
      - "https://dns.google/dns-query#dns"
proxies:
- name: "直连"
  type: direct
  udp: true
proxy-groups:
  - {name: 默认, type: select, proxies: [自动选择, 直连, 香港, 台湾, 日本, 新加坡, 美国, 其它地区, 全部节点]}
  - {name: dns, type: select, proxies: [自动选择, 默认, 香港, 台湾, 日本, 新加坡, 美国, 其它地区, 全部节点]}
  - {name: Google, <<: *pr}
  - {name: Telegram, <<: *pr}
  - {name: Twitter, <<: *pr}
  - {name: Pixiv, <<: *pr}
  - {name: ehentai, <<: *pr}
  - {name: 哔哩哔哩, <<: *pr}
  - {name: 哔哩东南亚, <<: *pr}
  - {name: 巴哈姆特, <<: *pr}
  - {name: YouTube, <<: *pr}
  - {name: NETFLIX, <<: *pr}
  - {name: Spotify, <<: *pr}
  - {name: Github, <<: *pr}
  - {name: 国内, type: select, proxies: [直连, 默认, 香港, 台湾, 日本, 新加坡, 美国, 其它地区, 全部节点, 自动选择]}
  - {name: 其他, <<: *pr}

  #分隔,下面是地区分组
  - {name: 香港, type: select , include-all-providers: true, filter: "(?i)港|hk|hongkong|hong kong"}
  - {name: 台湾, type: select , include-all-providers: true, filter: "(?i)台|tw|taiwan"}
  - {name: 日本, type: select , include-all-providers: true, filter: "(?i)日|jp|japan"}
  - {name: 美国, type: select , include-all-providers: true, filter: "(?i)美|us|unitedstates|united states"}
  - {name: 新加坡, type: select , include-all-providers: true, filter: "(?i)(新|sg|singapore)"}
  - {name: 其它地区, type: select , include-all-providers: true, filter: "(?i)^(?!.*(?:🇭🇰|🇯🇵|🇺🇸|🇸🇬|🇨🇳|港|hk|hongkong|台|tw|taiwan|日|jp|japan|新|sg|singapore|美|us|unitedstates)).*"}
  - {name: 全部节点, type: select , include-all-providers: true}
  - {name: 自动选择, type: url-test, include-all-providers: true, tolerance: 10}

rules:
  - GEOIP,lan,直连,no-resolve
  - RULE-SET,biliintl_domain,哔哩东南亚
  - RULE-SET,ehentai_domain,ehentai
  - RULE-SET,github_domain,Github
  - RULE-SET,twitter_domain,Twitter
  - RULE-SET,youtube_domain,YouTube
  - RULE-SET,google_domain,Google
  - RULE-SET,telegram_domain,Telegram
  - RULE-SET,netflix_domain,NETFLIX
  - RULE-SET,bilibili_domain,哔哩哔哩
  - RULE-SET,bahamut_domain,巴哈姆特
  - RULE-SET,spotify_domain,Spotify
  - RULE-SET,pixiv_domain,Pixiv
  - RULE-SET,cn_domain,国内
  - RULE-SET,geolocation-!cn,其他

  - RULE-SET,google_ip,Google
  - RULE-SET,netflix_ip,NETFLIX
  - RULE-SET,telegram_ip,Telegram
  - RULE-SET,twitter_ip,Twitter
  - RULE-SET,cn_ip，国内
  - MATCH，其他

rule-anchor:
  ip: &ip {type: http, interval: 86400, behavior: ipcidr, format: yaml}
  domain: &domain {type: http, interval: 86400, behavior: domain, format: yaml}
rule-providers:
  private:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/private.yaml"
  cn_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.yaml"
  biliintl_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/biliintl.yaml"
  ehentai_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/ehentai.yaml"
  github_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/github.yaml"
  twitter_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitter.yaml"
  youtube_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.yaml"
  google_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google.yaml"
  telegram_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/telegram.yaml"
  netflix_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/netflix.yaml"
  bilibili_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/bilibili.yaml"
  bahamut_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/bahamut.yaml"
  spotify_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/spotify.yaml"
  pixiv_domain:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/pixiv.yaml"
  geolocation-!cn:
    <<: *domain
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/geolocation-!cn.yaml"

  cn_ip:
    <<: *ip
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.yaml"
  google_ip:
    <<: *ip
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/google.yaml"
  netflix_ip:
    <<: *ip
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/netflix.yaml"
  twitter_ip:
    <<: *ip
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/twitter.yaml"
  telegram_ip:
    <<: *ip
    url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/telegram.yaml"
```

> 配置 [参考文档](https://wiki.metacubex.one/en/faq/)
>
> 一些三方工具(例如：shellclash)会拆分配置文件，可能会导致配置文件中锚点不可用，需要注意。ß

## 4. 使用

### 4.1. 手动启动

```shell
mihomo -f config.yaml #指定文档
mihomo -s $mihomo_path #指定目录
```

### 4.2. 服务启动

使用所 systemd 服务

```
[Unit]
Description=mihomo Daemon, Another Clash Kernel.
After=network.target NetworkManager.service systemd-networkd.service iwd.service

[Service]
Type=simple
LimitNPROC=500
LimitNOFILE=1000000
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
Restart=always
ExecStartPre=/usr/bin/sleep 1s
ExecStart=/usr/local/bin/mihomo -d /etc/mihomo
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

## 5. 拓展信息

- 一些客户端可能兼容该版本的内核，需要注意，建议最好直接从官网上下载。

## 6. 参考资料

- [项目地址](https://github.com/MetaCubeX/mihomo)
- [官方地址](https://wiki.metacubex.one/en/)
