---
title: "Git基础操作"
filename: git-version-control-practices
summary: Git是行业标准的分布式版本控制系统。本文涵盖Git基础概念（工作区、暂存区、版本库）与命令行实用指南。包含全局和项目级用户配置管理、分支生命周期操作（创建、合并与删除）、日志格式化追踪、强推覆盖、撤销本地提交，以及凭证缓存清理等高频日常操作。
tags: [git, version-control, git-branching, command-line]
aliases: [Git基础操作, Git配置, 版本控制]
status: completed
date created: 星期二, 二月 10日 2026, 10:44:33 上午
date modified: 星期五, 六月 19日 2026, 11:59:21 中午
---

<!-- toc -->

## 1. 简介

版本管理工具

## 2. 概念

- 工作区  
- 暂存区
- 版本库

## 3. 使用

### 3.1. 配置

```shell
git config --global user.name "Your Name" #设置名称
git config --global user.email "email@example.com" #设置邮箱
git config  user.name "Your Name" #设置项目层级名称
git config  user.email "email@example.com" #设置项目层级邮箱
rm ~/.git-credentials # 清除用户缓存
git config --global credential.helper store
git config --global rerere.enabled true # 设置记录变更处理
```

> 注意：当一个用户权限被移除，git pull 可能失效，需要使用 rm ~/.git-credentials 移除用户缓存配置

### 3.2. 仓库管理

- 创建版本库

```shell
git init
```

- 克隆仓库

```shell
git clone http://... path
```

> path 指定克隆地址

- 远程仓库

```shell
git remote -v #查看远程仓库信息
git remote add origin http://.. #添加远程仓库
git remote remove origin #删除远程仓库
git remote show origin #查看远程分支跟踪情况
```

### 3.3. 修改管理

- 查看修改记录

```shell
git status
```

- 提交暂存区

```shell
add add READMD.md 提交单个文件
```

> 可以使用 . 来代替所有文件

- 提交版本库

```shell
git commit -m "comment"
```

- 对比修改

```shell
git diff HEAD -- README.md
```

> HEAD 代表当前分支的最新的版本记录、可以替换成 commint Id

- 撤销修改

```shell
git restore --staged README.md #撤销暂存区修改
git restore #撤销工作区修改
```

- 隐藏修改

```shell
git stash #存储修改内容
git stash list #查看存储内容
git stash pop #回滚存储内容
```

### 3.4. 补丁

```shell
git format-patch commit_id #创建针对具体的 commit_id 的补丁文件
git apply patch_file.patch #运用程序
```

> 补丁相当于是一个 git diff 文件。

### 3.5. 日志

- 查看版本日志

```shell
git log #仅到当前最新版本
git reflog #包含未来的版本记录
```

> git relog 一般用于恢复 git reset --hard 回滚的记录

### 3.6. 版本管理

- 回退版本

```shell
    git reset hard -- HEAD test
```

> 1、soft 模式 本地文件不会改变、并且会版本修改记录回退到暂存区
>
> 2、mixed 模式 本地文件不会改变、并且会版本修改记录回退到工作区
>
> 3、hard 模式 本地文件会改变、会滚动版本最新记录

### 3.7. 分支管理

- 查看分支

```shell
git branch -v #查看本地分支
git branch -vv #查看本地分支, 可以查看与远程分支的关联情况
git branch -a #查看所有分支、包含远程分支
```

- 创建分支

```shell
git branch dev_test #以当前分支创建分支
git checkout -b dev_test dev #以dev 分支为准创建 dev_test 分支，并且切换到 dev_test 分支上
```

- 切换分支

```shell
git checkout dev_test
```

- 删除分支

```shell
git branch --delete dev_test
```

- 合并分支

```shell
git merge dev #在当前分支上合并 dev 分，会生成一个 commit
git rebase dev #在当前分支上合并 dev 分，不会重新生成 commit，并且提交记录会合并成一个。
```

- 分支跟踪关系

```shell
git branch --set-upstream master origin/next
```

> 创建好分支跟踪关系之后，pull 与 push 可以省略仓库名称

- 拉取分支

```shell
git fetch origin master #只拉取分支，但是不合并分支
git pull origin master:master #拉取并且合并分支
```

> pull 命令模式使用的是 merge 可以通过--rebase 使用 rebase 方式

- 推送分支

```shell
git push origin master:master
git push origin :master  #等于删除远程分支
```

> 初次可以使用-u 参数来建立跟踪关系

## 4. 拓展信息

### 4.1. 开源证书信息

![](http://qiniu.sxyxy.top/20240108112902.png?image=image)

## 5. 参考资料

- [官方链接](https://git-scm.com/)
- [参考文档](https://www.yiibai.com/git/git_branch.html)
- [Github Graph API](https://docs.github.com/en/graphql)
