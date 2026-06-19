---
filename: antigravity-python-highlighting-issue
summary: Google 推出的 AI 优先 IDE Antigravity 由于基于 VS Code OSS 与 Open VSX 扩展市场，无法使用闭源且绑定微软官方市场的 Pylance 扩展，导致 Python 代码语义高亮失效（标识符全白）。本笔记记录了此故障的排查过程及解决方案，通过安装 BasedPyright 语言服务，修改 settings.json 关闭内置 Python 语言服务器并启用 BasedPyright，同时设置 typeCheckingMode 为 off 以关闭冗余的类型检查警告，成功恢复了代码语义高亮与补全功能。
tags: ["Antigravity", "Python", "VS-Code", "BasedPyright", "Syntax-Highlighting"]
aliases: ["Antigravity高亮失效", "BasedPyright配置", "VSCodeOSS踩坑"]
status: completed
title: "Antigravity高亮失效"
source: "https://medium.com/@wilson1999112/antigravity-%E8%AE%93-python-%E9%AB%98%E4%BA%AE%E6%B6%88%E5%A4%B1-%E6%88%91%E9%81%87%E5%88%B0%E7%9A%84%E5%9D%91%E8%88%87%E8%A7%A3%E6%B3%95-a80476e41e9d"
author:
  - "[[Wilson]]"
published: 2025-11-20
created: 2025-12-11
description: "Antigravity 讓 Python 高亮消失？我遇到的坑與解法 相信有很多人跟我一樣，對於這兩天 Google Gemini 3 發布以及 Antigravity 躍躍欲試。  結果一打開 Antigravity …"
date created: 星期日, 十二月 21日 2025, 11:05:25 上午
date modified: 星期五, 六月 19日 2026, 11:56:38 中午
---

<!-- toc -->

> [!info] 编者按
> 好的，根据您提供的博客内容和要求，我已经整理并优化了文档格式，以 **简体中文** 输出。

---

## 1. 🤖 Antigravity IDE Python 代码高亮故障排查与修复指南

### 1.1. 一、 Antigravity 简介及问题根源

#### 1.1.1. 💡 什么是 Antigravity？

Antigravity 是 Google 推出的一个 **“AI 优先 (AI-first)” 的 VS Code 变种**。它旨在将 Gemini 3 模型和多代理（multi-agent）工作流程直接集成到 IDE 中。

- **技术基础：** 基于 VS Code 开源版本（VS Code OSS）。
- **核心特色：**
  - 右侧有专门的 Agent 面板，支持多 Agent 协助完成代码修改、运行终端命令、打开浏览器等操作。
  - 内置 **Gemini 3**，支持在编辑器、终端和浏览器之间进行协作。
  - 扩展程序市场使用 **Open VSX**，而非微软官方 Marketplace。

#### 1.1.2. ❌ 踩坑原因：Pylance 的缺失

Antigravity 是 VS Code 的一个分支（fork），且使用了不同的扩展程序市场（Open VSX）。因此，许多用户习惯依赖的工具（如 Python 的 **Pylance**）无法原封不动地使用。

- **Pylance 状态：** 官方 VS Code 使用 `ms-python.vscode-pylance` 作为语言服务器。Pylance 是 **闭源** 扩展，且 **只在微软官方 Marketplace 发布**。
- **结果：** 基于 VS Code OSS + Open VSX 的 Antigravity **无法直接使用官方 Pylance**。虽然可以安装 `ms-python` 扩展，但它主要负责 lint 和工具集成，**真正负责“语义分析 + 高亮”的 Pylance 不在**。
- **问题现象：** Python 文件仅剩最基本的语法高亮，所有标识符（函数名、变量名、参数名等）被降级为 **"Other"**，显示为白色。

#### 1.1.3. 🧐 问题诊断：缺乏语义令牌 (Semantic Tokens)

通过 VS Code 的调试工具 `Developer: Inspect Editor Tokens and Scopes` 检查变数，发现缺少关键信息：

- `standard token type:` 显示为 `Other`。
- `textmate scopes:` 只有 `source.python` 等基础 scope。

这表明编辑器 **不知道** 被选中的是变数、函数还是类。在 VS Code 世界中，漂亮的代码高亮主要依靠 **语言服务器** 产生的 **语义令牌**。没有语言服务器，主题的高亮能力非常有限。

---

### 1.2. 二、 解决方案：使用 BasedPyright 替代 Pylance

由于 Pylance 不可用，最佳替代方案是使用 **BasedPyright**，它是一个可在 Open VSX 上运行并提供语义高亮的开源项目。

- **BasedPyright 简介：** 它是从 Pyright 分叉（fork）出来的项目，专门用于弥补 VS Code 分支缺少 Pylance 的缺陷。

#### 1.2.1. Step 1：安装 BasedPyright 扩展

1. 在 Antigravity 中，点击左侧的 **Extensions**（积木图标），或使用快捷键 `Cmd + Shift + X`.
2. 搜索：`BasedPyright`.
3. 找到发布者为 **`DetachHead`** 的扩展，点击 **Install**.
4. 安装完成后，建议 **重启** Antigravity.

> [!warning] 避坑提示
> 请勿混淆其他类似的扩展，如 `Cursor Pyright` 或 `Windsurf Pyright`。

#### 1.2.2. Step 2：启用 BasedPyright 并关闭内置语言服务器

为了避免冲突，需要明确告诉编辑器使用 BasedPyright，并关闭内置的 Python 语言服务器。

1. 打开 `settings.json`：`Cmd + Shift + P` → `Preferences: Open User Settings (JSON)`.
2. 在最外层 `{ ... }` 中添加或修改以下配置：

Code snippet

```
{
    // 关掉内置 Python 语言服务器，避免互相冲突
    "python.languageServer": "None",

    // 确保 BasedPyright 的语言服务已启用
    "basedpyright. ": false
}
```

1. 保存配置，并关闭所有 `.py` 文件，重新打开一个 Python 文件.

#### 1.2.3. Step 3：确认代码高亮恢复

此时，您应该会看到函数名、变量名、参数名重新显示为不同的颜色。

- 如果再次用 `Inspect Editor Tokens and Scopes` 检查，您会看到新增一行：`semantic token type: variable` 或 `function` 等。
- 这表明 BasedPyright 已成功接管语言服务器的工作。

---

### 1.3. 三、 警告爆炸解决方案：关闭型别检查

在高亮恢复后，您可能会遇到大量黄色的底线警告，例如 `Type of “source_path” is unknown`。这是因为 BasedPyright 正在 **认真执行型别检查**。

为了先将 IDE 用顺，可以暂时关闭型别检查，但保留语义分析功能。

#### 1.3.1. Step 4：关闭 BasedPyright 的型别检查

在同一个 `settings.json` 中，继续添加以下配置：

Code snippet

```json
{
    "python.languageServer": "None",
    "basedpyright.disableLanguageServices": false,

    // 1. 关掉型别检查，只保留语义高亮、跳转、补全
    "basedpyright.analysis.typeCheckingMode": "off",

    // 2. 可选：关掉一些 Inlay Hints，让界面更简洁
    "basedpyright.analysis.inlayHints.variableTypes": false,
    "basedpyright.analysis.inlayHints.functionReturnTypes": false,
    "basedpyright.analysis.inlayHints.genericTypes": false
}
```

- `typeCheckingMode: "off"` 会保留 BasedPyright 的代码解析能力（颜色、跳转、补全），但会 **几乎消除型别错误和警告**。
- 保存后，警告将瞬间消失，仅剩下其他 linter（如 Ruff）真正报告的问题.

#### 1.3.2. ✅ 快速总结清单

如果您遇到 **“Python 代码全部变白”** 的问题，请按以下步骤操作：

1. 确认只有 Python 高亮失效，其他语言（如 TS/JS）正常.
2. 检查变数是否显示为 `standard token type: Other`，确认语言服务器未启动.
3. 在 Extensions 中安装 **BasedPyright**（发布者：DetachHead）.
4. 在 `settings.json` 中配置：

    ```json
    "python.languageServer": "None",
    "basedpyright.disableLanguageServices": false
    ```

5. （可选）若要关闭警告，添加：

    ```json
    "basedpyright.analysis.typeCheckingMode": "off"
    ```

6. 重启 Antigravity，重开 Python 文件，即可恢复高亮和提示功能.

---

### 1.4. 四、 结语

Antigravity 是 Google 用于展示 **“Gemini 3 + AI 代理协作”** 愿景的早期 AI-first IDE。但由于它是 VS Code 分支并采用 Open VSX 市场，必然会在扩展兼容性上产生摩擦。得益于 **BasedPyright** 这类开源替代品，用户在体验 AI-first IDE 的同时，仍能保持正常的 Python 开发环境.
