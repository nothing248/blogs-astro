---
title: "PicGo图床配置"
filename: picgo-image-hosting-setup
summary: PicGo 是一款开源的图片上传及图床管理工具，广泛应用于 Markdown 写作流中。本文详细介绍了如何配置 Gitee（通过插件）及七牛云作为图床。针对 Gitee 的防盗链限制及七牛云测试域名的有效期问题提供了避坑指南，旨在帮助用户构建一个高效、稳定的自动化图片上传工作流。
tags: [picgo, image-hosting, markdown, writing-tools, cloud-storage]
aliases: [PicGo图床配置, Gitee图床, 七牛云图床]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:30 下午
date modified: 星期五, 六月 19日 2026, 12:07:27 中午
---

<!-- toc -->

## 1. 简介

PicGo 是一款功能强大的开源图片上传工具，支持 macOS, Windows 和 Linux。它能够将本地图片或剪贴板图片一键上传到指定的云端存储空间（图床），并自动在剪贴板生成对应格式的链接（如 Markdown, HTML），极大提升了写作效率。

## 2. 方案一：配置 Gitee 图床 (适合个人笔记)

Gitee 提供免费的仓库空间，配合插件可作为简易图床使用。

### 2.1. Gitee 端配置

- 创建一个 **公有** 仓库（例如：`[USER]/images`）。
- 生成 **私人令牌 (Access Token)**：在设置中创建，请务必保存好生成的令牌。

### 2.2. PicGo 端配置

- **安装插件**：在 PicGo 插件设置中搜索并安装 `gitee-uploader`。
- **参数配置**：
  - `repo`: 仓库路径（格式为 `用户名/仓库名`）。
  - `token`: 填入刚才生成的私人令牌。
  - `path`: 图片存储路径（如 `img/`）。

> [!warning]
> **防盗链提醒**：Gitee 官方对图片外链有一定的频率限制和防盗链保护。如果你计划将笔记公开发布到大型平台，该方案可能会导致图片无法显示。

## 3. 方案二：配置七牛云图床 (适合长期稳定)

七牛云提供 10GB 的永久免费存储空间（标准存储），稳定性优于 Git 仓库。

### 3.1. 七牛云端配置

- 注册账户并完成实名认证。
- 创建 **对象存储 (Kodo)** Bucket，记录 `Bucket 名称`。
- 获取密钥：在个人中心找到 `AccessKey` 和 `SecretKey`。
- **存储区域**：根据创建 Bucket 时的选择记录对应区域（如 `z0` 代表华东）。

### 3.2. PicGo 端配置

- 选择内置的 `七牛图床` 选项。
- 填入 `AccessKey`, `SecretKey`, `Bucket` 及 `访问域名`。

> [!tip]
> **域名说明**：七牛云提供的测试域名有效期仅为 30 天。若要长期使用，**强烈建议** 绑定已备案的自定义域名，否则域名过期后图片链接将全部失效。

## 4. 参考资料

- [PicGo 官方文档](https://picgo.github.io/PicGo-Doc/zh/guide/)
- [PicGo GitHub Releases](https://github.com/Molunerfinn/PicGo/releases)
