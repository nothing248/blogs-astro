# blogs-astro

基于 [Astro](https://astro.build) + [Starlight](https://starlight.astro.build) 构建的个人博客站点，通过 **Git Subtree** 将 [blogs-origin](https://github.com/nothing248/blogs-origin.git) 仓库中的 Markdown 文档引入，并自动发布到 **Cloudflare Pages**。

## 架构概览

```
blogs-origin (源文档仓库)
  └── *.md / 目录结构
        │
        │  git subtree add/pull
        ▼
blogs-astro (本仓库)
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
- **部署平台**: Cloudflare Pages
- **图片处理**: [sharp](https://sharp.pixelplumbing.com)

## 许可证

MIT
