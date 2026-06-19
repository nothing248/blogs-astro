# blogs-astro

基于 [Astro](https://astro.build) + [Starlight](https://starlight.astro.build) 构建的个人博客站点，通过 **Git Subtree** 将 [blogs-origin](https://github.com/nothing248/blogs-origin.git) 仓库中的 Markdown 文档引入，并自动发布到 **Cloudflare Pages**。

## 架构概览

```
blogs-origin (私有源文档仓库)
  └── *.md / 目录结构
        │
        │  push 触发 GitHub Actions (repository_dispatch)
        ▼
blogs-astro (本仓库)
  ├── .github/workflows/
  │   └── sync-from-origin.yml  # 自动同步工作流
  ├── astro.config.mjs          # Astro + Starlight 配置
  ├── src/
  │   ├── content/
  │   │   └── docs/             # ← subtree 挂载点 (来自 blogs-origin)
  │   └── content.config.ts
  ├── public/
  ├── package.json
  └── tsconfig.json
        │
        │  git push → Cloudflare Pages 自动构建
        ▼
  Cloudflare Pages (生产环境)
```

## 前置条件

- [Node.js](https://nodejs.org) >= 18
- [pnpm](https://pnpm.io)（推荐）或 npm
- Git

## 快速开始

```bash
# 1. 克隆本仓库
git clone https://github.com/nothing248/blogs-astro.git
cd blogs-astro

# 2. 安装依赖
pnpm install

# 3. 启动开发服务器
pnpm dev
# 访问 http://localhost:4321
```

## Git Subtree 工作流

本项目使用 `git subtree` 将 `blogs-origin` 仓库的内容挂载到 `src/content/docs/` 目录。

### 首次添加（已完成）

```bash
git subtree add --prefix=src/content/docs \
  https://github.com/nothing248/blogs-origin.git master --squash
```

### 拉取上游更新

当 `blogs-origin` 仓库有新的文档提交时，运行：

```bash
git subtree pull --prefix=src/content/docs \
  https://github.com/nothing248/blogs-origin.git master --squash
```

### 推送本地修改回上游（可选）

如果在本仓库中直接修改了 `src/content/docs/` 下的内容，可以推送回源仓库：

```bash
git subtree push --prefix=src/content/docs \
  https://github.com/nothing248/blogs-origin.git master
```

## 自动同步（CI/CD）

当向 `blogs-origin` 推送时，通过 GitHub Actions 自动触发本仓库的 subtree 同步，无需手动操作。

### 工作原理

1. `blogs-origin` 的 GitHub Actions 通过 `repository_dispatch` 事件通知 `blogs-astro`
2. `blogs-astro` 的同步工作流自动执行 `git subtree pull` 拉取最新文档内容
3. Cloudflare Pages 检测到 `blogs-astro` 有新提交，自动构建并部署

### 涉及的工作流文件

| 仓库 | 文件 | 作用 |
|:-----|:-----|:-----|
| blogs-astro | `.github/workflows/sync-from-origin.yml` | 接收 dispatch 事件，执行 subtree pull |
| blogs-origin | `.github/workflows/trigger-astro-sync.yml` | push 时发送 dispatch 事件到 blogs-astro |

### 配置要求

自动同步需要一个 **Fine-grained PAT**（Personal Access Token），用于：
- 在 `blogs-astro` 中读取私有仓库 `blogs-origin` 的内容
- 在 `blogs-origin` 中触发 `blogs-astro` 的 `repository_dispatch` 事件

#### 1. 创建 Fine-grained PAT

前往 [GitHub Settings > Fine-grained tokens](https://github.com/settings/tokens?type=beta) 创建 Token：

- **Repository access**: 选择 `blogs-origin` 和 `blogs-astro`
- **Permissions → Contents**: `Read and write`

#### 2. 配置 Secrets

| 仓库 | Secret 名称 | 用途 |
|:-----|:------------|:-----|
| blogs-astro | `BLOGS_ORIGIN_TOKEN` | 用于 subtree pull 时访问私有仓库 |
| blogs-origin | `BLOGS_ASTRO_DISPATCH_TOKEN` | 用于触发 blogs-astro 的工作流 |

#### 3. blogs-origin 触发工作流

在 `blogs-origin` 仓库中创建 `.github/workflows/trigger-astro-sync.yml`：

```yaml
name: Trigger blogs-astro sync

on:
  push:
    branches: [master]

jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger blogs-astro sync workflow
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.BLOGS_ASTRO_DISPATCH_TOKEN }}" \
            https://api.github.com/repos/nothing248/blogs-astro/dispatches \
            -d '{"event_type": "sync-blogs-origin"}'
```

### 手动触发同步

也可以在 [blogs-astro Actions 页面](https://github.com/nothing248/blogs-astro/actions) 手动触发 **Sync from blogs-origin** 工作流。

## Cloudflare Pages 部署

本项目配置为推送到 GitHub 后由 Cloudflare Pages 自动构建并部署。

### 部署配置

| 配置项       | 值               |
| :----------- | :--------------- |
| 构建命令     | `pnpm build`     |
| 输出目录     | `dist/`          |
| Node.js 版本 | `>= 18`         |

### 手动部署（可选）

```bash
# 构建生产版本
pnpm build

# 本地预览构建结果
pnpm preview
```

## 常用命令

| 命令                   | 说明                                       |
| :--------------------- | :----------------------------------------- |
| `pnpm install`         | 安装依赖                                   |
| `pnpm dev`             | 启动开发服务器（`localhost:4321`）          |
| `pnpm build`           | 构建生产版本到 `./dist/`                   |
| `pnpm preview`         | 本地预览生产构建                           |
| `pnpm astro ...`       | 运行 Astro CLI 命令                        |

## 技术栈

- **框架**: [Astro](https://astro.build) v6
- **文档主题**: [@astrojs/starlight](https://starlight.astro.build) v0.40
- **内容管理**: Git Subtree（从 `blogs-origin` 同步）
- **CI/CD**: GitHub Actions（自动同步 + 触发部署）
- **部署平台**: Cloudflare Pages
- **图片处理**: [sharp](https://sharp.pixelplumbing.com)

## 踩坑记录

在配置 GitHub Actions 自动同步过程中遇到了以下问题，记录备查。

### 1. 私有仓库认证 — `Repository not found`

**现象**：`git subtree pull` 报 `remote: Repository not found`，即使 URL 正确。

**原因**：`blogs-origin` 是私有仓库，GitHub Actions 默认的 `GITHUB_TOKEN` 只有当前仓库（`blogs-astro`）的权限，无法访问其他私有仓库。

**解决**：创建一个 Fine-grained PAT，授权访问 `blogs-origin` 和 `blogs-astro` 两个仓库，并配置为 Secret。

### 2. Token 嵌入 URL 方式无效

**现象**：将 Token 直接嵌入 `git subtree pull` 的 URL 中（`https://x-access-token:TOKEN@github.com/...`），仍然报 `Repository not found`。

**原因**：`git subtree pull` 内部调用 `git fetch`，不会正确传递 URL 中嵌入的认证信息。

**尝试的方案**：
```bash
# ❌ 方案 1：Token 嵌入 URL（subtree 内部 fetch 时丢失认证）
git subtree pull --prefix=src/content/docs \
  https://x-access-token:${TOKEN}@github.com/nothing248/blogs-origin.git master --squash

# ❌ 方案 2：git config url.insteadOf（被 checkout 的 credential 覆盖）
git config --global url."https://x-access-token:${TOKEN}@github.com/".insteadOf "https://github.com/"
```

### 3. `actions/checkout` 默认 Credential 覆盖

**现象**：API 验证 Token 通过（curl 返回 200），但 `git subtree pull` 仍然失败。

**原因**：`actions/checkout@v4` 默认 `persist-credentials: true`，会注入一个 **local** 级别的 credential helper（使用 `GITHUB_TOKEN`）。local 配置优先级高于 global，导致我们设置的 PAT 被覆盖。

**解决**：
```yaml
# 1. 禁用 checkout 默认的 credential
- uses: actions/checkout@v4
  with:
    persist-credentials: false

# 2. 使用 git-credentials 文件配置认证
- run: |
    git config --global credential.helper store
    echo "https://x-access-token:${TOKEN}@github.com" > ~/.git-credentials
```

## 许可证

MIT
