---
title: "语义化版本控制"
filename: semantic-versioning-guide
description: 语义化版本控制（SemVer）指南，详细阐述主版本号（MAJOR）、次版本号（MINOR）与修订号（PATCH）的递增规则。规定当发生不兼容的 API 变更、向下兼容的功能新增以及向下兼容的错误修复时对应的版本升级策略，并说明预发布版本及构建元数据的扩展标记方法，为软件发布和依赖管理提供标准化流程。
tags: [version-control, semver, best-practices, release-management, software-engineering]
aliases: [语义化版本控制, SemVer, 版本号规范, 语义化版本]
status: completed
date created: 星期日, 十二月 21日 2025, 11:05:29 上午
date modified: 星期五, 六月 19日 2026, 12:11:07 中午
---

<!-- toc -->

## 1. 语义化版本控制核心规则

语义化版本格式为：`MAJOR.MINOR.PATCH`（主版本号.次版本号.修订号），其版本号递增规则如下：

1. **主版本号 (MAJOR)：** 当你做了 **不兼容的 API 修改** 时递增。
2. **次版本号 (MINOR)：** 当你以 **向下兼容的方式新增了功能** 时递增。
3. **修订号 (PATCH)：** 当你做了 **向下兼容的错误修复 (Bug Fixes)** 时递增。

> [!note]
> 先行版本（Pre-release）及版本编译信息可以加在 `MAJOR.MINOR.PATCH` 的后面作为延伸（例如 `1.0.0-alpha`, `1.0.0-beta+exp.sha.5114f85`）。

---

## 2. 规则详解与使用建议

### 2.1. 主版本号 (MAJOR)

- 当 API 的公共接口发生破坏性变更（Breaking Changes），导致旧的依赖客户端无法直接升级时，必须递增 `MAJOR` 版本，并将 `MINOR` 和 `PATCH` 清零（例如从 `1.5.2` 升级到 `2.0.0`）。
- 在 `0.y.z` 阶段（即大版本号为 0），系统处于初始开发阶段，API 随时可能发生变化，此时的 `0.y.z` 变更不需要严格遵循 `MAJOR` 不兼容的规则。

### 2.2. 次版本号 (MINOR)

- 当引入了新的公共 API、弃用了某些旧 API（Deprecation），或者在内部代码中实现了显著的新功能，但 **确保现有 API 接口依旧保持兼容** 时，必须递增 `MINOR` 版本，并将 `PATCH` 清零（例如从 `1.5.2` 升级到 `1.6.0`）。

### 2.3. 修订号 (PATCH)

- 仅用于向下兼容的缺陷修复（Bug Fixes）。这指的是没有新增公共 API，也没有修改已有公共 API 的内部代码修正（例如从 `1.5.2` 升级到 `1.5.3`）。

---

## 3. 参考资料

- [SemVer 官方网站（中文）](https://semver.org/lang/zh-CN/)
- [SemVer Specification (English)](https://semver.org/)
