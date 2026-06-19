---
title: "Gitee-Go使用"
filename: gitee-go-cicd-pipeline
summary: Gitee Go是Gitee平台内置的CI/CD持续集成与构建工具。本文梳理了Gitee Go图形化流水线配置流程。详细说明了主机组的物理机与ECS导入、安装Gitee Go Runner客户端、设置凭证密钥管理、定义流水线构建与发布步骤的核心操作，助力国内团队实现代码托管与自动化部署。
tags: [gitee-go, cicd, devops, automation-pipeline]
aliases: [Gitee-Go使用, 流水线部署, Runner配置]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:23 下午
date modified: 星期五, 六月 19日 2026, 11:59:23 中午
---

<!-- toc -->

## 1. 简介

- 该工具对应是 gitee 的流水线功能，是 gitee 开放的 CI CD 工具，用于自动化部署

- gitee 提供了图形视图与代码视图两类编辑入口，可以根据需求进行配置。本文的以图形化界面配置介绍为主。代码编辑可以参考 [该链接](https://gitee.com/help/articles/4292#article-header0)

## 2. 配置流程

- 配置主机
  - 进入对应的组织或个人中心管理界面的主机管理入口，并新建主机组
  
  ![image-20230802195236696](http://qiniu.sxyxy.top/image-20230802195236696.png?image=image)
  - 添加主机
  
  ![image-20230802195356585](http://qiniu.sxyxy.top/image-20230802195356585.png?image=image)

  > 注意：
  >
  > 1. 主机组是组织与个人隔离的。即使是一个账户下的不同组织或个人配置的主机也是不共享的。
  > 2. 主机配置的命令行不需要上传对应的账户密码信息，而文件导入则需要
  > 3. 若需要同一台主机配置不同组织的适配，可以通过文件导入方式进行

- 配置流水线
  - 配置流水线基础信息(流水线名称与标识)
  - 配置触发事件
    - 一般配置实为特定分支 push 事件

    ![image-20230802195855433](http://qiniu.sxyxy.top/image-20230802195855433.png?image=image)
  - 配置任务信息
    - 根据需求配置阶段与任务

    ![image-20230802200156176](http://qiniu.sxyxy.top/image-20230802200156176.png?image=image)

## 3. 配置场景

- 1.主机直接拉取代码，并直接重启应用部署(一般用于静态站点的部署)
  - 选择工具中 shell 脚本任务类型

  ![image-20230802200437361](http://qiniu.sxyxy.top/image-20230802200437361.png?image=image)
  - 配置对应的 shell 脚本

  ![image-20230803104018313](http://qiniu.sxyxy.top/image-20230803104018313.png?image=image)

- 2.正常的代码构建，发布、部署流程
  - 配置构建任务(根据开发环境选择对应构建类型，此处以 node 作为演示)

  ![image-20230803105035921](http://qiniu.sxyxy.top/image-20230803105035921.png?image=image)
  - 配置发布任务(用于上传对应的构建物，方便后期版本回滚)

  ![image-20230803105837318](http://qiniu.sxyxy.top/image-20230803105837318.png?image=image)

  > 注意：
  >
  > 1. 此处有 **发布** 与 **上传制品** 两个发布任务选项。区别对应是将 gitte-go 中的制品库模块。上传制品会将构建物上传到待发布制品库，发布会将制品直接发布到十已发布制品库中

  ![image-20230803110328776](http://qiniu.sxyxy.top/image-20230803110328776.png?image=image)
  - 配置部署任务(根据环境类型选择不同的部署类型，此处以单机部署为例)

  ![image-20230803110636623](http://qiniu.sxyxy.top/image-20230803110636623.png?image=image)

## 4. 查看流水线日志

- 查看任务运行情况(通过流水线 > 构建历史查看对应的流水线触发情况与任务日志)

![image-20230803104816030](http://qiniu.sxyxy.top/image-20230803104816030.png?image=image)

## 5. 参考资料

- [官方链接](https://gitee.com/help/articles/4358)
