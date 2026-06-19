---
title: "Git基础操作"
filename: git-version-control-practices
summary: Git是行业标准的分布式版本控制系统。本文涵盖Git基础概念（工作区、暂存区、版本库）与命令行实用指南。包含全局和项目级用户配置管理、分支生命周期操作（创建、合并与删除）、日志格式化追踪、强推覆盖、撤销本地提交，以及凭证缓存清理等高频日常操作。
tags: [git, version-control, git-branching, command-line]
aliases: [Git基础操作, Git配置, 版本控制]
status: completed
date created: 星期二, 二月 10日 2026, 10:44:33 上午
date modified: 星期五, 六月 19日 2026, 4:59:32 下午
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

## 4. Substree

git subtree 是 Git 官方推出的一种高级仓库管理工具。 [1, 2]
它允许你将一个独立的 Git 仓库（子仓库）作为子目录，完整地嵌入到另一个 Git 仓库（主仓库）中。不仅能引入文件，还能完美合并两者的 Commit 历史记录。 [3, 4]

### 4.1. 核心工作原理：为什么它能合并历史？

在传统的思维中，两个仓库的历史是平行的（比如主仓库有 A-B-C 连续的提交，子仓库有 X-Y-Z 连续的提交）。
当你执行 git subtree add 时，Git 会在后台做三件事：

   1. 拉取子仓库：把子仓库（你的 Obsidian 笔记）的所有历史记录和文件下载到本地。
   2. 改写路径：把子仓库中原本在根目录的文件，虚拟移动到主仓库指定的目录下（如 src/content/docs/），并把子仓库的 Commit 历史也同步按这个路径改写。
   3. 编织历史：在主仓库创造一个全新的合并节点（Merge Commit）。此时，两个仓库的历史交织在了一起。你在主仓库运行 git log，就能同时看到主仓库和子仓库的所有历史 Commit。 

### 4.2. 核心命令详解

#### 4.2.1. 首次吸入子仓库 (Git sUbtree aDd)

```
git subtree add --prefix=src/content/docs <https://github.com> main --squash
```

- --prefix=src/content/docs：指定子仓库在主仓库里存放的目标文件夹位置。
- <https://github.com...：子仓库的远程地址。> [11]
- main：你要拉取子仓库的哪个分支。
- --squash（可选但强烈推荐）：
- 不加 --squash：会把子仓库过去的成百上千条 Commit 原封不动地全部塞进主仓库的历史树里。你的主仓库历史会变得非常长。
  - 加上 --squash：会把子仓库过去的所有 Commit 压缩聚拢成一个单一的 Commit 塞进来。不过不用担心，子仓库原本的详细历史并不会丢失，它会被安全地保存在一个隐藏的特殊分支中，未来拆分时依然可以完整还原。 [12, 13, 14, 15, 16]

#### 4.2.2. 从原仓库拉取更新 (Git sUbtree pUll)

如果你偶尔在旧的独立笔记仓库里写了东西，并推到了旧 GitHub 上，你想同步到现在的 Astro 博客里：

```shell
git subtree pull --prefix=src/content/docs <https://github.com> main --squash
```

- 这会自动把旧仓库的新文章同步到博客的 docs 目录下。

#### 4.2.3. 把修改推回原仓库 (Git sUbtree pUsh)

如果你在 Astro 博客的 src/content/docs 目录下写了新笔记，你想把这些修改同步回你原来的独立笔记仓库：

```
git subtree push --prefix=src/content/docs <https://github.com> main
```

- Git 会非常聪明地只筛选出发生在 src/content/docs 目录下的修改，并把它们打包推回你的独立笔记仓库。

#### 4.2.4. 随时随地完美拆分 (Git sUbtree sPlit)

Subtree 是“可逆”的。如果某天你不想用 Astro 了，想要拿回带历史记录的纯笔记仓库：

```
git subtree split --prefix=src/content/docs -b my-perfect-notes
```

------------------------------

## 5. Submodule

git submodule（子模块）是 Git 官方提供的另一种跨仓库管理方案。 
如果说 git subtree 是“把子仓库作为真实文件直接吸入并熔断”，那么 git submodule 则完全相反——它选择“只记录一个指针，保持绝对的独立与边界”。 

### 5.1. 核心工作原理：它到底是怎么记录的？

当你使用 git submodule 将你的 Obsidian 笔记仓库嵌入到 Astro 博客仓库中时，主仓库（博客）的本地文件夹里虽然能看到笔记文件，但 GitHub 上的主仓库里其实没有任何一个真实的 Markdown 文件。
Git 的底层是通过以下两样东西来维持这个引用的：

#### 5.1.1. .gitmodules 配置文件

在主仓库根目录下，会多出一个名为 .gitmodules 的文本文件，记录了子仓库的出生证明：

```
[submodule "src/content/docs"]
    path = src/content/docs
    url = https://github.com
```

这告诉 Git：“当有人来到 src/content/docs 这个目录时，请去这个 GitHub 链接找内容。”

#### 5.1.2. “Gitlink” 指针（版本锁）

这是子模块最核心的底层逻辑。主仓库在它的版本树里，只为子模块目录记录了一个 160 位的 SHA-1 提交哈希值（Commit ID）。

* 它就像一个精准的版本锁。主仓库硬编码记录着：“当前博客对应的笔记，必须严格停留在笔记仓库的 Commit X 这一刻。”
* 即使你在笔记仓库里提交了新的 Commit Y 和 Commit Z，只要你没有在主仓库“更新指针”，主仓库看到的依然永远是 Commit X 的旧内容。

### 5.2. 核心操作命令详解

由于子模块的“版本锁”机制，它的日常操作命令比普通 Git 要繁琐得多

#### 5.2.1. 首次添加子模块 (Git sUbmodule aDd)

```
git submodule add https://github.com src/content/docs
```

* 运行后，本地的 src/content/docs 会立刻下载你的笔记文件。
* 此时运行 git status，你会发现主仓库多了两个需要提交的东西：.gitmodules 文件和名为 src/content/docs 的新指针。你必须把它们 commit 并 push 到主仓库的 GitHub 上。

#### 5.2.2. 克隆带有子模块的仓库 (Git cLone --recursive)

如果你换了一台新电脑，直接 git clone 你的博客仓库，你会发现克隆下来的 src/content/docs 文件夹是完全空的！
因为默认克隆只会拉取主仓库的“指针”，不会自动下载子仓库。你必须使用以下命令：

##### 5.2.2.1. 方法 A：克隆时直接带上递归参数（一步到位）

```
git clone --recursive https://github.com
```

##### 5.2.2.2. 方法 B：如果已经克隆了主仓库，手动初始化并拉取子模块

```
git submodule init
git submodule update
```

#### 5.2.3. 日常同步与更新

如果你在原笔记仓库里写了新文章并推到了 GitHub，想让 Astro 博客也同步过去，你需要让主仓库的指针“往前走”：

- 在主仓库根目录下运行，让所有子模块拉取云端最新的提交并更新指针

```
git submodule update --remote --merge
```

- 或者，你也可以直接肉身走进 src/content/docs 目录（此时终端会切换到笔记仓库的环境），照常执行 git pull origin main，然后退回博客根目录，把主仓库产生的新指针变动 git commit 提交掉。

### 5.3. Submodule 与 Subtree 的本质区别

虽然 Submodule 听起来边界感很强、很干净，但在你搭建 Obsidian + Cloudflare Pages 博客 的场景下，它有几个致命的痛点：

| 维度 [7, 8, 9, 10, 11] | git submodule (子模块) | git subtree (子树) |
|---|---|---|
| 云端构建友好度 | 极差。Cloudflare 在云端编译你的网页时，如果你的笔记仓库是 Private（私有） 的，Cloudflare 会因为没有访问你子模块的权限而直接报错、构建失败。 | 极佳。因为文件在第一步合并时就已经实打实存在于主仓库里了，Cloudflare 傻瓜式读取。 |
| 日常更新心智负担 | 极高。在 Obsidian 里改了字，你得先在子目录 git push 一次；然后退回主目录再 git commit 更新一次指针并 git push 一次。漏掉一步，博客就不会更新。 | 极低。合并后完全融为一体，打开 GitHub Desktop 像对待普通文件夹一样一键 Commit & Push 即可。 |
| 代码冲突风险 | 经常遇到 Submodule head detached（指针游离）或者指针冲突报错，对不熟悉 Git 底层的用户来说如同灾难。 | 只有在两边修改同一个文件时才会冲突，处理方式和普通冲突完全一致。 |

------------------------------

### 5.4. 什么时候应该用 Submodule？

既然它这么繁琐，为什么 Git 官方还要保留它？因为它在大厂的大型模块化开发中不可替代：

* 公共库依赖：比如你开发了 10 个不同的软件（主仓库），它们都依赖同一个底层核心算法库（子仓库）。当你修改了算法库，你肯定不希望这 10 个软件的历史记录全部被 subtree 搞得一团糟。此时用 Submodule 挂载是最完美的。
* 严苛的权限隔离：某些核心代码只能高管看，普通员工只能看主壳代码。用 Submodule 可以做到主仓库公开、子仓库加密。 

## 6. 拓展信息

### 6.1.1. 开源证书信息

![](http://qiniu.sxyxy.top/20240108112902.png?image=image)

## 6.2. 参考资料

- [官方链接](https://git-scm.com/)
- [参考文档](https://www.yiibai.com/git/git_branch.html)
- [Github Graph API](https://docs.github.com/en/graphql)
