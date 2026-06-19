---
status: completed
filename: pm2-nodejs-process-manager-guide
title: "PM2"
summary: 本笔记总结了 Node.js 生产环境标准的进程管理工具 PM2 的核心用法。涵盖了从基础的启动、监控（logs/list）、状态持久化（save/resurrect）到配置系统级开机自启（startup）的常用指令。重点提供了使用 `ecosystem.config.js` 配置文件进行应用声明式管控的模板代码，为实现 Node 服务的高可用守护与多实例集群部署 (Cluster Mode) 提供运维速查字典。
aliases: [PM2, Node 进程管理, ecosystem 配置]
tags: [Node.js, 运维部署, PM2, 进程管理, 守护进程, 前端工程化]
date created: 星期一, 五月 19日 2025, 2:05:22 下午
date modified: 星期四, 六月 18日 2026, 12:15:00 晚上
---

<!-- toc -->

## 1. 工具定位

**PM2** 是一款带有负载均衡功能的 Node.js 应用的进程管理器。它不仅能让 Node 脚本在后台持续运行（守护进程），还能提供性能监控、自动重启及支持多实例部署。

*安装指令*：`npm install pm2 -g`

---

## 2. 声明式配置：`ecosystem.config.js`

在生产环境中，强烈建议使用 ecosystem 配置文件来统一管理启动参数，而非在命令行拼写冗长的参数。

```javascript
// ecosystem.config.js 示例
module.exports = {
  apps: [
    {
      name: 'tm_nuxt_app',       // 进程别名，方便 pm2 管理
      script: 'npm',             // 执行脚本的解释器/入口
      args: 'start',             // 传递给 script 的参数 (相当于执行 npm start)
      
      // 高级选项 (被注释的部分)
      // exec_mode: 'cluster',   // 开启集群模式，最大化利用多核 CPU
      // instances: 'max',       // 启动的实例数量，'max' 会自动探测 CPU 核心数
      // watch: true,            // 监听文件变动，自动重启 (仅开发环境建议)
      // env: { NODE_ENV: "production" } // 注入环境变量
    }
  ]
}
```

---

## 3. 常用进程管理实战指令

### 3.1. 启动与查看

```bash
# 基于配置文件启动 (需在同级目录下执行)
pm2 start ecosystem.config.js

# 直接启动单个脚本
pm2 start test.py    # 甚至会自动调用对应的 python 解释器
pm2 start test.js --name "my-app" --watch

# 查看监控面板
pm2 list       # 查看所有进程的列表与状态
pm2 monit      # 实时终端仪表盘 (CPU/内存)
pm2 logs       # 查看所有或特定进程的聚合日志
```

### 3.2. 状态持久化与系统级开机自启

如果服务器重启，PM2 及其管理的进程会丢失。为了保证高可用，必须执行以下流程：

```bash
# 第一步：保存当前 PM2 正在托管的所有进程状态到 dump 文件
pm2 save

# 第二步：生成并配置系统层面的开机自启动脚本 (Systemd)
pm2 startup
# (执行该命令后，终端会输出一段需 sudo 执行的指令，请复制并执行它)

# 第三步 (故障恢复)：若需要手动从之前的保存点恢复进程树
pm2 resurrect
```

> [!tip] 取消自启
> 如果需要关闭 PM2 的开机自启行为，可执行 `pm2 unstartup`。通过 `systemctl status pm2-root` 可验证底层服务的驻留状态。
