---
title: "GitLab安装"
filename: gitlab-ce-self-hosted-installation
summary: GitLab CE是企业级私有代码仓库与协作平台。本文介绍在Debian/Ubuntu环境基于官方APT源和手动包下载部署GitLab的流程。详细罗列了默认目录、SMTP邮件通知配置、反向代理与SSL证书启用、以及配置变更后使用reconfigure和restart指令使设置生效的流程。
tags: [gitlab, self-hosting, gitlab-ce, smtp-config]
aliases: [GitLab安装, GitLab配置, 私有代码仓库]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:28 下午
date modified: 星期五, 六月 19日 2026, 11:59:26 中午
---

<!-- toc -->

## 1. 简介

## 2. 安装

- 安装依赖

```shell
apt-get install -y curl openssh-server ca-certificates tzdata perl 
```

- 安装

```shell
# 通过源安装
curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
apt install gitlab-ce
# 手动下载安装
wget https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/jammy/gitlab-ce_16.0.9-ce.0_amd64.deb
dpkg -i gitlab-ce_16.0.9-ce.0_amd64.deb
# 安装 gitlab runner
wget https://s3.dualstack.us-east-1.amazonaws.com/gitlab-runner-downloads/latest/binaries/gitlab-runner-linux-amd64
dpkg -i gitlab-runner-linux-amd64.deb
```

## 3. 配置

```
# /etc/gitlab/gitlab.rb
external_url 'http://example.com:8091' #配置外部链接

puma['listen'] = '0.0.0.0' #后端服务，直接访问没有静态文件
puma['port'] = 8080

gitlab_workhorse['listen_network'] = "tcp" #直接访问，不经过代理
gitlab_workhorse['listen_addr'] = "127.0.0.1:8091"

nginx['listen_port'] = 8888 #配置内置nginx启动端口

# 以下配置自己的mysql数据库而不是用内置的数据库
postgresql['enable'] = false #关闭内置postgresql数据库
gitlab_rails['db_adapter'] = "postgresql"
gitlab_rails['db_encoding'] = "utf8"
gitlab_rails['db_database'] = "gitlab"
gitlab_rails['db_username'] = "root"
gitlab_rails['db_password'] = "example"
gitlab_rails['db_host'] = "localhost"
gitlab_rails['db_port'] = 5433

# 以下配置自定的redis而不是用内置的redis
redis['enable'] = false
gitlab_rails['redis_host'] = "127.0.0.1"
gitlab_rails['redis_port'] = 6380
gitlab_rails['redis_password'] = "example"

# 以下配置自定的nginx而不是用内置的nginx
nginx['enable'] = false

# 配置ssh默认用户
user['username'] = "gitlab"
user['group'] = "gitlab"
gitlab_rails['gitlab_ssh_host'] = 'gitlab.wsl.sxyxy.top'
gitlab_rails['gitlab_ssh_user'] = 'gitlab'
```

## 4. 管理

```shell
gitlab-ctl reconfigure #基于配置文件重新配置 APP
gitlab-ctl start appName #缺省代表所有的服务
gitlab-ctl status appName
gitlab-ctl restart appName
gitlab-ctl service-list #查看所有的服务
gitlab-rake "gitlab:password:reset" #修改密码
# 管理
systemctl disable gitlab-runsvdir #gitlab
systemctl start gitlab-runsvdir #gitlab
systemctl stop gitlab-runsvdir #gitlab
systemctl restart gitlab-runsvdir #gitlab
systemctl enable gitlab-runsvdir #gitlab
systemctl disable gitlab-runner #runner
systemctl start gitlab-runner #runner
systemctl stop gitlab-runner #runner
systemctl restart gitlab-runner #runner
systemctl enable gitlab-runner #runner

gitlab-ctl cleanse #清空重来
rm -rf /opt/gitlanb #清除、然后重新安装
dkpg- i /opt/software/gitlab-ce_16.0.9-ce.0_amd64.deb
```

## 5. 使用

### 5.1. 用户组

...

### 5.2. 用户

...

### 5.3. 仓库

...

### 5.4. Runner

- 注册

```shell
gitlab-runner register  --url https://example.com  --token 123
```

- 配置 executor
  - Shell：在运行 GitLab Runner 的机器上直接使用 shell 命令运行作业。
  - Docker：在 Docker 容器中运行作业，提供了一种隔离的环境。
  - Docker Machine：在动态创建的 Docker 容器中运行作业，可以根据需求动态扩展。
  - Kubernetes：在 Kubernetes 集群中运行作业，适用于容器化应用的部署。
  - VirtualBox：在 VirtualBox 虚拟机中运行作业，适合需要虚拟化环境的情况。
  - Custom：允许用户定义自定义的执行器。
- 仓库配置 .gitlab-cli.yml 文件

```shell
stages:          # List of stages for jobs, and their order of execution
  - build
  - test
  - deploy

build-job:       # This job runs in the build stage, which runs first.
  stage: build
  tags:
    - test_new
  script:
    - echo "Compiling the code..."
    - echo "Compile complete."

unit-test-job:   # This job runs in the test stage.
  stage: test    # It only starts when the job in the build stage completes successfully.
  tags:
    - test_new
  script:
    - echo "Running unit tests... This will take about 60 seconds."
    - sleep 60
    - echo "Code coverage is 90%"

lint-test-job:   # This job also runs in the test stage.
  stage: test    # It can run at the same time as unit-test-job (in parallel).
  tags:
    - test_new
  script:
    - echo "Linting code... This will take about 10 seconds."
    - sleep 10
    - echo "No lint issues found."

deploy-job:      # This job runs in the deploy stage.
  stage: deploy  # It only runs when *both* jobs in the test stage complete successfully.
  tags:
    - test_new
  environment: production
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed."
```

- 命令使用

```shell
gitlab-runner register # 注册
gitlab-runner run #测试使用
gitlab-runner start
gitlab-runner status
gitlab-runner stop
gitlab-runner restart
gitlab-runner unregister --name <RUNNER_NAME> #取消注册
```

## 6. 拓展信息

### 6.1. CE 与 EE 的区别

CE 是社区版本，EE 是商业版本

### 6.2. GitLab 12.1 版本之后仅支持 postgresql 数据库

### 6.3. Wait for Logrotate Service Socket Gitlab 卡死

```shell
systemctl restart gitlab-runsvdir
gitlab-ctl reconfigure
```

### 6.4. 项目页面 500

```shell
gitlab-rake cache:clear #清理缓存
```

### 6.5. 当前依赖服务

- postgresql
- redis
- nginx(https 需要)
- runner(CI CD 需要)

## 7. 参考资料

- [官方文档](https://about.gitlab.com/install/#ubuntu)
