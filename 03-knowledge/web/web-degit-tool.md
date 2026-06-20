---
title: "degit项目模板拉取"
filename: web-degit-tool
description: 项目脚手架快速生成工具 degit 的实践指南。内容涵盖该工具的底层原理（通过下载 Tarball 避免拉取整个 Git 提交历史），并通过全局安装与 npx 免安装两种形式，展示了克隆指定分支、指定 tag、私有仓库和自定义输出目录的常用命令行指令及 degit.json 后置行为配置。
tags:
  - web
  - dev-tools
  - git
  - degit
  - scaffolding
aliases:
  - degit项目模板拉取
  - degit工具教程
  - Git无历史克隆
status: completed
date created: 星期五, 一月 23日 2026, 8:32:17 晚上
date modified: 星期二, 六月 16日 2026, 6:24:18 晚上
---

<!-- toc -->

## 1. 简介

`degit` 是一个由 Svelte 作者 Rich Harris 编写的命令行工具。它用于克隆 Git 仓库的最新状态快照，但 **不复制任何 Git 历史记录**（即不会生成 `.git` 目录）。这使得它非常适合用于拉取脚手架模板（Scaffolding）来快速初始化新项目，其运行速度远比执行标准的 `git clone` 更为高效。

> [!NOTE]
> `degit` 的底层机制是直接通过托管平台（GitHub、GitLab、Bitbucket 等）的 API 下载目标仓库的打包压缩文件（Tarball）并于本地解压，从而规避了完整的版本库历史下载。

## 2. 使用方法

### 2.1. 全局安装使用

可以通过 npm 在系统全局进行安装：

```shell
npm install -g degit
```

安装后，可以直接调用 `degit` 指令：

```shell
# 默认克隆 GitHub 仓库的默认分支到当前目录
degit github:user/repo

# 使用 SSH 连接方式
degit git@github.com:user/repo

# 使用 HTTPS 连接方式
degit https://github.com/user/repo

# 克隆指定分支 (如 dev) 并且输出到新建的 my-new-project 目录下
degit user/repo#dev my-new-project
```

### 2.2. 免安装使用 (使用 npx)

推荐直接使用 `npx` 临时下载并运行，避免全局依赖污染：

```shell
# 克隆 GitHub 仓库并指定输出文件夹
npx degit user/repo my-new-project

# 克隆 GitLab 平台项目
npx degit gitlab:user/repo my-new-project

# 克隆指定的 Tag (例如 v1.0.0)
npx degit user/repo#v1.0.0 my-new-project
```

## 3. 进阶配置与后置操作

`degit` 支持在模板项目的根目录下创建 `degit.json` 配置文件。在模版被成功拉取并解压后，会自动执行配置中的动作（例如删除或重命名特定文件）：

```json
{
  "actions": [
    {
      "type": "remove",
      "files": [
        "LICENSE.md",
        "README.md"
      ]
    }
  ]
}
```

## 4. 参考文档

- [degit GitHub 官方仓库](https://github.com/Rich-Harris/degit)
