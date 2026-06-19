---
filename: markdown-linting-tools
title: Markdown格式规范指南
aliases: ["Markdown格式规范", "文档格式化工具", "MarkdownLinter", "ObsidianLinter"]
tags: ["markdown", "linter", "Obsidian", "工具", "文档格式", "自动化", "markdownlint", "markdown-toc", "Number Headings"]
status: completed
summary: 本笔记详细介绍了Markdown文档格式化与结构优化的多种工具及实践方法。核心内容涵盖了命令行工具 `markdownlint-cli` 及其定制化配置（如禁用特定规则MD013、MD033），以保持一致的代码风格；同时探讨了 `markdown-toc` 工具如何自动化生成内嵌目录，以及 Obsidian 插件 `Number Headings` 在标题编号方面的应用。此指南旨在提升Markdown笔记的可读性、维护性及RAG检索友好度，尤其适用于Obsidian用户进行高效知识管理。
date created: 星期五, 六月 19日 2026, 2:08:41 下午
date modified: 星期五, 六月 19日 2026, 4:44:12 下午
---

<!-- toc -->

## 1. 简介

本指南旨在介绍一系列用于保持 Markdown 文档格式一致性、提升可读性与结构化的工具。通过合理运用这些工具，可以确保个人知识库（PKM）中的笔记符合规范，并增强其在大模型语义检索（RAG）场景下的可发现性。

## 2. Markdownlint

**Markdownlint** 是一个强大的 Markdown 风格检查器（linter），它能帮助你发现并修正文档中不符合规范的格式问题。

### 2.1. 安装

使用 `npm` 进行全局安装，方便在任何项目中使用：

```shell
npm install -g markdownlint-cli
```

### 2.2. 配置 (`.markdownlint.jsonc`)

通过创建配置文件来定制化 `markdownlint` 的检查规则，以适应个人或团队的写作习惯和 Obsidian 的特性。以下是一个推荐的配置示例：

```json
{
    "default": true,
    "MD013": false, // 关闭行字数限制 (Line length)
    "MD033": false, // 允许使用内联 HTML (Inline HTML)
    "MD041": false, // 不强制第一行是 H1 (First line in file should be a top-level heading)
    "MD025": false, // 允许存在多个一级标题 (Multiple top-level headings in the same document)
    "MD040": false, // 允许围栏代码块不指定语言 (Fenced code blocks should have a language specified)
    "MD045": false, // 允许图片没有替代文本（alt text） (Images should have alternate text (alt text))
    "MD036": false, // 允许使用粗体或斜体作为标题 (Emphasis used instead of headings)
    // "MD056": false, // 允许表格各行的列数不一致 (Table row spans) - 通常建议开启以保持表格规范
    "MD060": false, // 允许表格各列的宽度/对齐样式不一致 (Table column widths) - 通常建议开启以保持表格规范
    "MD024": false, // 允许存在多个内容相同的标题 (Multiple headings with the same content)
    "MD028": false, // 允许引用块内存在空行，特别适用于 Obsidian 的 Callout 样式 (Blank line at the end of a block quote)
    "MD007": {
        "indent": 2
    } // 设置列表缩进为 2 个空格，匹配 Obsidian 的默认缩进习惯
}
```

> [!info] 配置说明
> 上述配置旨在平衡 Markdown 的规范性和 Obsidian 用户的灵活性。例如，关闭 `MD028` 对于使用 Callouts (引用块) 的用户来说非常有用。`MD007` 的缩进设置应与你的 Obsidian 编辑器设置保持一致。

### 2.3. 使用

在命令行中执行 `markdownlint`，可以对指定文件或目录进行检查和自动修复：

```shell
markdownlint "**/*.md" --fix --ignore ".obsidian/**"
```

> [!note] 命令参数
> 
> - `**/*.md`：匹配当前目录下所有 `.md` 文件及其子目录。
> - `--fix`：尝试自动修复发现的问题。
> - `--ignore ".obsidian/**"`：忽略 `.obsidian` 配置文件夹内的文件，避免误修改。

### 2.4. 与 Obsidian 集成

- **Markdownlint 插件**: Obsidian 社区插件市场中可以直接安装 `markdownlint` 插件，它能实时检查并提示格式问题，主要侧重于内容本身的优化。
- **Linter 插件**: 配合 Obsidian 的 `Linter` 插件，可以实现对 YAML Front Matter 等高级内容的自动化优化和格式统一。

## 3. Markdown-toc

**Markdown-toc** 是一个用于基于 Markdown 文件内的占位符自动生成内嵌目录（Table of Contents, TOC）的工具。

### 3.1. 安装

通过 `npm` 全局安装 `markdown-toc`：

```shell
npm install -g markdown-toc
```

### 3.2. 内容预填充示例

在你的 Markdown 文件中，使用 `<!-- toc -->` 注释作为 TOC 的占位符：

```md
---
title: "我的文章标题"
---

# 顶层标题 (可选，如果MD041未关闭)

<!-- toc -->

## 一级标题
### 二级标题
## 另一个一级标题
```

### 3.3. 使用

在命令行中执行 `markdown-toc` 命令，它会自动查找 `<!-- toc -->` 占位符并生成目录：

```shell
markdown-toc -i test.md
```

> [!tip] `-i` 参数
> `-i` (in-place) 参数表示直接在原文件中插入生成的 TOC。

## 4. Number Headings 插件

**Number Headings** 是一个 Obsidian 社区插件，用于自动为笔记中的标题添加编号。

### 4.1. 功能简介

该插件可以实时或手动为所有 H1 到 H6 标题添加 `1.`, `1.1.`, `1.1.1.` 这样的层级编号，非常适合技术文档或报告的编写。

### 4.2. 注意事项

> [!warning] 适用场景限制
> `Number Headings` 插件主要适用于**单个文件**的标题编号管理。如果你需要处理大量文件并统一管理标题编号，或者在发布到外部平台时需要保留编号，建议考虑**自定义脚本**来实现更灵活和批量化的编号方案。

## 5. TOC (Table of Contents)

目录（Table of Contents, TOC）是文档结构的重要组成部分，它以层级化的方式展示文档的主要标题和子标题，为读者提供快速导航和概览。在 Markdown 文档中，TOC 通常由文档中的各级标题自动生成，是文档内容索引和导航的核心元素。

- **快速概览与导航**: 读者可以通过 TOC 迅速了解文档的整体框架和涵盖的主题，并快速跳转到感兴趣的章节，大大提升阅读效率。
- **结构化理解**: 清晰的 TOC 有助于读者理解内容之间的逻辑关系和层级结构，从而更好地消化和吸收信息。
- **提升用户体验**: 对于长文档，TOC 是必不可少的导航工具，能够显著改善用户体验。
