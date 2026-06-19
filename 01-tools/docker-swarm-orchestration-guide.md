---
title: "Docker Swarm集群指南"
filename: docker-swarm-orchestration-guide
summary: Docker Swarm 是 Docker 原生的容器集群管理工具，通过 Manager 和 Worker 节点实现服务的高可用与自动调度。本笔记解析了 Swarm 的核心概念（节点、服务、任务、堆栈），提供了集群初始化、节点加入、服务扩缩容及滚动更新的操作指南。同时涵盖了使用 Docker Stack 配合 YAML 配置文件进行多服务编排的实战方法，解决了容器化应用在生产环境中的批量管理与负载均衡需求。
tags: ["Docker", "Swarm", "Orchestration", "Clustering", "DevOps"]
aliases: ["Docker Swarm集群指南", "容器编排工具", "Docker Stack使用"]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:23 下午
date modified: 星期五, 六月 19日 2026, 11:58:45 中午
---

<!-- toc -->

## 1. 简介

**Docker Swarm** 是 Docker 官方提供的原生集群管理和编排工具。它将一组 Docker 主机转化为一个单一的、虚拟的 Docker 主机，使得开发者可以像管理单个容器一样管理大规模的容器集群。

---

## 2. 核心概念

- **管理器节点 (Manager Node)**：负责集群状态维护、任务调度及集群成员管理。建议生产环境配置奇数个管理器以实现高可用。
- **工作节点 (Worker Node)**：负责接收并执行来自管理器的任务（即运行容器）。
- **服务 (Service)**：定义了容器在集群中的期望状态（如副本数、网络、端口映射）。
- **任务 (Task)**：Swarm 调度的最小单元，通常对应一个运行中的容器。
- **堆栈 (Stack)**：通过 Compose 文件定义的一组关联服务，用于管理复杂的应用架构。

---

## 3. 集群管理实战

### 3.1. 初始化与加入集群

```shell
# 在主节点初始化集群
docker swarm init --advertise-addr <MANAGER_IP>:2377

# 查看加入集群所需的 Token (worker 或 manager)
docker swarm join-token worker

# 在子节点运行加入命令
docker swarm join --token <TOKEN> <MANAGER_IP>:2377

# 查看所有节点状态
docker node ls

# 提升节点到 manager 节点
docker node promote slave2

# 退出集群，如果是最后一个 manager 节点，则需要添加--force
docker swarm leave --force
```

### 3.2. 服务操作

```shell
#拉取镜像
docker pull kentalk/helloworld 

# 创建一个 3 副本的 Nginx 服务
docker service create --replicas 3 --name my-web -p 8080:80 nginx

# 服务扩缩容
docker service scale my-web=5

# 更新服务镜像
docker service update --image nginx:stable my-web

# 回滚操作
docker service rollback my-web
```

---

## 4. Docker Stack 编排

使用 `docker-stack.yml` 进行多服务部署。

```yaml
version: "3.8"
services:
  web:
    image: nginx:latest
    ports:
      - "8000:80"
    deploy:
      replicas: 3
      update_config: #配置滚动更新策略。
        parallelism: 1 #每次更新一个副本。
        delay: 10s #每次更新后等待 10 秒。
   rollback_config：
  parallelism: 1 #每次回滚一个副本。
        delay: 10s #每次回滚后等待 10 秒。
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
networks:
  default:
    name: my-stack-network
```

### 4.1. 部署命令

```shell
# 部署或更新堆栈
docker stack deploy --compose-file docker-stack.yml my-app-stack

# 查看堆栈
docker stack ls
# 查看堆栈任务
docker stack ps my-app-stack
# 删除堆栈
docker stack rm
```

---

## 5. 参考资料

- [Docker Swarm 官方文档](https://docs.docker.com/engine/swarm/)
- [Docker Stack 部署参考](https://docs.docker.com/engine/reference/commandline/stack_deploy/)
