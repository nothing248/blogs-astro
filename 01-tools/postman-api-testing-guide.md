---
title: "Postman教程"
filename: postman-api-testing-guide
description: Postman 是一款广泛使用的 API 开发与测试工具。本文介绍了 Postman 的核心组织架构（Collection, Folder, Request）以及如何利用 JavaScript 编写自动化测试脚本。重点演示了通过 Collection Runner 进行批量及并发测试的流程，适用于提高 API 交付质量与集成测试效率。
tags: [postman, api-testing, qa, automated-testing, development-tools]
aliases: [Postman教程, 接口自动化测试, API管理工具]
status: completed
date created: 星期二, 二月 25日 2025, 3:24:25 下午
date modified: 星期五, 六月 19日 2026, 12:07:33 中午
---

<!-- toc -->

## 1. 简介

Postman 是目前最流行的 API 协同开发平台，支持请求调试、自动化测试、Mock 服务以及 API 监控。其数据会自动同步至云端账户，方便跨设备使用。

## 2. 核心组织概念

为了高效管理海量接口，Postman 采用了层级化的组织结构：

- **Collection (集合)**：接口的最高级容器，通常以项目或微服务为单位进行划分。支持导出与团队共享。
- **Folder (文件夹)**：用于在集合内部进行逻辑分组（如：用户模块、订单模块）。
- **Request (请求)**：具体的 API 接口定义，包含 URL、Header、Body 以及 Pre-request/Tests 脚本。

## 3. 自动化测试脚本

Postman 允许在 `Tests` 选项卡中使用 JavaScript 编写校验逻辑，确保响应结果符合预期。

### 3.1. 示例脚本

```javascript
// 验证状态码是否为 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// 验证响应体是否包含特定字符串
pm.test("Body matches string", function () {
    pm.expect(pm.response.text()).to.include("success");
});

// 验证 JSON 字段值
pm.test("Check user ID", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql(123);
});
```

## 4. 批量测试 (Collection Runner)

当需要一次性运行多个接口以验证完整业务流程时，可使用 Runner 功能：

1. **选择集合**：点击集合右侧的更多选项，选择 `Run collection`。
2. **配置运行参数**：
   - **Iterations (迭代次数)**：设置运行几轮。
   - **Delay (延迟)**：设置请求间的间隔时间。
   - **Data (数据文件)**：可导入 CSV 或 JSON 文件进行参数化测试。
3. **查看结果**：运行完成后，Postman 会提供直观的测试通过率报告。

## 5. 参考资料

- [Postman 官方文档](https://www.postman.com/)
- [Postman 测试脚本示例指南](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/)
