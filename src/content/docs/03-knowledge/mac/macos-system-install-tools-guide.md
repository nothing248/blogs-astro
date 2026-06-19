---
title: "macOS系统管理"
filename: macos-system-install-tools-guide
summary: macOS 系统升级与指定开发工具安装的实用配置指南。解决用户仅需升级指定 macOS 版本而非最新版的问题，以及如何离线/命令行安装 Xcode Command Line Tools 与 Homebrew。核心步骤包括利用 Apple 官方技术支持检索下载特定 OS、通过终端指令部署基础开发工具链，以及配置国内加速镜像源。
tags:
  - macos
  - system-install
  - xcode-tools
  - system-config
aliases:
  - macOS系统管理
  - macOS升级
  - macOS开发工具安装
status: completed
date created: 星期一, 十二月 22日 2025, 12:28:23 凌晨
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

## 1. 简介

本指南整理了 macOS 系统指定版本升级/降级的操作流程，以及常用开发者基础工具链（如 Xcode Command Line Tools、Homebrew 软件包管理器等）的安装与配置方法，旨在帮助开发者快速搭建一个稳定且可控的 macOS 工作环境。

---

## 2. 系统安装指定版本

有些小伙伴可能会跟我一样，不希望直接升级到最新的 macOS Beta 版本或当前主推的最新正式版，而是想要将系统往上升级一个特定版本（例如从 Big Sur 升级到 Monterey，或从 Monterey 升级到 Ventura）。我们可以按照以下步骤进行安全地获取和操作：

1. **获取官方下载链接**：
   在 Apple 网站的 Apple - 技术支持 - 搜索 (中国) 中，搜索指定的系统版本做下载。
   官方入口网址：[support.apple.com/zh-cn/HT211683](https://support.apple.com/zh-cn/HT211683)（该页面会列出所有旧版本 macOS 的 App Store 直接跳转链接）。
2. **下载与获取安装包**：
   选择指定版本（例如 macOS Ventura），点击跳转打开 App Store 进行获取。下载完成后，安装程序将自动下载至你的 `/Applications`（应用程序）文件夹中，文件名为 `Install macOS [Version Name].app`。
3. **（可选）制作可引导的 macOS 启动安装器（U 盘启动盘）**：
   如果你需要对多台设备进行安装，或者需要抹盘全新安装，可以使用 U 盘制作启动盘。
   - 准备一个 16GB 或更大容量的 U 盘，并在磁盘工具中将其抹掉，格式化为“Mac OS 扩展（日志式）”，命名为 `MyVolume`。
   - 打开终端，执行以下命令（以 macOS Monterey 为例）：

     ```shell
     sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
     ```

   - 输入管理员密码并按回车，根据提示输入 `Y` 确认，等待写入完成。
4. **进入恢复模式进行安装**：
   - **Apple Silicon (M 系列芯片)**：关机后，长按电源按钮直到出现“正在载入启动选项”，选择“选项”并点击“继续”。
   - **Intel 芯片**：关机后，重新开机并立即按住 `Command (⌘) + R` 键，直到看到 Apple 标志或旋转的地球。
   - 在恢复模式下，可选择“安装 macOS”或使用“磁盘工具”抹盘后通过 U 盘启动盘进行系统安装。

## 3. 安装指定工具

在完成系统安装后，我们需要快速安装最核心的基础开发组件。

### 3.1. Xcode Command Line Tools（命令行开发者工具）

这是编译 C/C++ 代码、运行 Git 以及执行许多基础脚本所必需的底层组件。

- **在线安装**：
  打开终端，运行以下命令：

  ```shell
  xcode-select --install
  ```

  此时系统会弹出一个窗口，提示你需要安装该工具，点击“安装”并同意许可协议，系统将自动从 Apple 服务器下载并安装。
- **离线手动安装**：
  若遇到网络下载极慢或报错，可前往 Apple 开发者门户网站手动检索下载 `.dmg` 文件安装包：
  [developer.apple.com/download/all/](https://developer.apple.com/download/all/) (搜索 "Command Line Tools")。
- **验证安装**：
  在终端中输入：

  ```shell
  xcode-select -p
  # 应输出类似：/Library/Developer/CommandLineTools
  gcc --version
  ```

### 3.2. Homebrew（包管理器）

Homebrew 是 macOS 上不可或缺的软件包管理工具，用于安装各类终端实用工具和应用软件。

- **官方脚本安装**：

  ```shell
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

- **国内镜像源加速安装（防止网络超时）**：
  如果官方源下载慢，推荐使用科大或清华大学提供的学术镜像源。终端运行以下一键脚本：

  ```shell
  /bin/bash -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
  ```

- **配置环境变量**：
  对于 M 系列芯片的 Mac，Homebrew 默认安装在 `/opt/homebrew` 目录下，需要在 `~/.zshrc` 中配置环境路径：

  ```shell
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
  source ~/.zshrc
  ```

- **常用命令**：
  - 更新 Homebrew：`brew update`
  - 安装工具：`brew install wget`
  - 安装桌面应用：`brew install --cask visual-studio-code`

## 4. 参考资料

- [系统页面（下载旧版 macOS）](https://support.apple.com/zh-cn/102662)
- [开发页面（Apple 开发者资源检索）](https://developer.apple.com/cn/search/?q=command%20line%20tools)
- [Homebrew 官方网站](https://brew.sh/zh-cn/)
