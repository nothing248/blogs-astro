---
title: "Crontab"
status: pending
filename: linux-crontab-scheduled-tasks-and-environment
aliases: [Crontab, 定时任务, Linux 环境执行]
tags: [Linux, Crontab, 运维, 定时任务, Shell]
date created: 星期二, 二月 25日 2025, 3:24:01 下午
date modified: 星期四, 六月 18日 2026, 11:45:00 晚上
---

<!-- toc -->

## 1. 待完善：Linux Crontab 定时任务

本笔记旨在记录 Linux 下定时任务工具 Crontab 的用法。
目前仅记录了一个核心排障提示：

- **环境变量问题**：Crontab 在后台执行时不会加载用户的完整环境变量。若需执行特定的 Python 环境脚本，必须使用 **绝对路径** 指向虚拟环境的 Python 解释器（例如：`/anaconda/envs/../python`），否则会导致依赖加载失败。
