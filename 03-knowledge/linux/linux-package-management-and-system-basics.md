---
title: "linux-basics"
filename: linux-package-management-and-system-basics
summary: 本文梳理了 Linux（以 Debian/Ubuntu 系列为主）系统管理的核心基础知识。详细阐述了 APT、dpkg 及源码编译安装（如 OpenSSL）的配置与操作规范；系统性整理了 Linux 环境初始化配置文件（如 profile 与 bashrc）的加载顺序、动静态链接库（.so/.a）机制及 ldconfig 共享管理；并记录了高频用户权限管理命令与老旧 Debian 发行版（Stretch 归档源 404）的源修复方案。
tags:
  - linux
  - debian
  - package-manager
  - apt
  - compilation
  - shared-library
aliases:
  - linux-basics
  - apt-sources
  - dpkg-commands
status: completed
---

<!-- toc -->

## 1. 软件管理

### 1.1. 软件管理工具分类

在主流 Linux 发行版中，软件管理工具分为两大阵营：

- **Debian 系列（如 Ubuntu、Debian）**：使用 `APT`（Advanced Package Tool）作为高级包管理器，`DPKG`（Debian Package）作为底层安装工具。
- **Red Hat 系列（如 RHEL、CentOS、Fedora）**：使用 `YUM` 或 `DNF` 作为高级包管理器，`RPM`（RPM Package Manager）作为底层安装工具。

### 1.2. APT 软件源配置

APT 的软件源配置文件主要位于 `/etc/apt/sources.list` 以及 `/etc/apt/sources.list.d/` 目录中。

配置格式解析：

```text
deb http://archive.ubuntu.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ bionic main restricted universe multiverse
```

- `deb`：代表预编译好的二进制软件包（`.deb`）。
- `deb-src`：代表软件的源代码包（适用于手动修改源码重新编译）。
- `http://archive.ubuntu.com/ubuntu/`：软件镜像源地址。
- `bionic`：目标发行版的代号名称（如 Ubuntu 18.04 为 `bionic`）。
- `main / restricted / universe / multiverse`：软件库组件：
  - `main`：官方支持的自由与开源软件。
  - `restricted`：官方支持的非完全自由软件（如专有驱动）。
  - `universe`：社区维护的自由与开源软件。
  - `multiverse`：非自由软件（受版权或法律限制）。

常用更新命令：

```shell
# 更新本地软件源的索引缓存
apt update

# 从特定软件源库组件安装软件包
apt install package-name
```

### 1.3. DPKG 常用命令

`dpkg` 是偏底层的包管理器，只负责安装和卸载本地的 `.deb` 包，**不能** 自动下载软件以及自动解析处理复杂的依赖关系。

```shell
dpkg -l | grep package       # 查看包是否已经安装在系统中
dpkg -i package.deb         # 手动安装本地 .deb 包（若遇依赖缺失可运行 apt-get install -f 修复）
dpkg -c package.deb         # 查看 .deb 包中包含的文件及目录列表
dpkg -I package.deb         # 查看并提取该安装包的元数据及配置信息
dpkg -r package             # 移除软件包（保留其配置文件）
dpkg -P package             # 完全清除软件包（包括配置文件）
dpkg -L package             # 列出该软件安装在系统中的所有文件清单路径
dpkg -s package             # 显示已安装软件包的详细状态与依赖关系
dpkg -S /path/to/file       # 逆向查询系统中的某个文件是由哪个软件包生成的
dpkg-reconfigure package    # 对已安装的软件进行重新初始化配置（前提是其采用了 debconf 管理）
```

### 1.4. APT 与 APT-GET 命令对比

`apt` 融合了 `apt-get` 与 `apt-cache` 的命令优势，具有更直观的进度条和简明的命令结构。

| 操作任务 | 传统命令 (`apt-get` / `apt-cache`) | 现代推荐命令 (`apt`) |
| :--- | :--- | :--- |
| **安装包** | `apt-get install [pkg]` | `apt install [pkg]` |
| **升级全部包** | `apt-get upgrade` | `apt upgrade` |
| **系统版本升级** | `apt-get dist-upgrade` | `apt full-upgrade` |
| **移除包** | `apt-get remove [pkg]` | `apt remove [pkg]` |
| **更新索引** | `apt-get update` | `apt update` |
| **列出已安装包** | N/A | `apt list --installed` |

---

## 2. 源码编译与安装

如果官方包管理器中没有所需版本的软件，通常可以通过手动下载源码包进行编译安装。以升级安全组件 **OpenSSL** 为例：

### 2.1. 编译安装步骤

```shell
# 进入源码推荐存放路径
cd /usr/local/src

# 下载并解压缩源码包
wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz
tar -zxvf openssl-1.1.1g.tar.gz
cd openssl-1.1.1g

# 配置编译参数，指定安装路径前缀，可选 --enable-shared 生成动态库
./configure --prefix=/usr/local/openssl --enable-shared

# 开始多线程编译并安装到指定路径
make -j$(nproc)
make install
```

### 2.2. 配置环境变量与软链接

编译完成后，需要将新编译的可执行文件和库文件暴露给系统：

```shell
# 备份系统旧版本的 bin 文件
mv /usr/bin/openssl /usr/bin/openssl.old

# 为新版本程序创建软链接
ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
ln -s /usr/local/openssl/include/openssl /usr/include/openssl

# 将新的动态链接库路径加入系统库搜寻配置文件中
echo "/usr/local/openssl/lib" >> /etc/ld.so.conf

# 刷新动态链接库缓存
ldconfig
```

---

## 3. 环境变量配置文件加载顺序

当用户登录系统或启动一个 Bash 交互会话时，Linux 会按照特定的顺序读取并加载一系列配置文件来初始化用户环境变量：

```text
1. /etc/profile              # 全局系统环境变量配置，对所有登录用户有效
2. /etc/profile.d/*.sh       # 全局系统辅助配置目录，被 /etc/profile 自动循环读取
3. /etc/bash.bashrc          # 全局交互式非登录 Shell 配置文件
4. /etc/bash_completion      # 全局命令行自动补全配置
5. ~/.profile                # 个人登录 Shell 配置，若存在 ~/.bash_profile 则可能不读取
6. ~/.bashrc                 # 个人交互式非登录 Shell 配置（最常用的个人变量与别名配置点）
7. ~/.bash_history           # 存储个人历史命令记录的文件
8. ~/.bash_logout            # 仅限普通用户退出登录时执行的清理脚本（root 用户默认不创建）
```

---

## 4. 类库文件管理与动态装载

类库是编译好的二进制代码，能被多个应用调用。主要保存在 `/usr/lib/` 或 `/lib/` 目录下。

- **动态链接库 (`.so` 后缀)**：Runtime Library。在程序运行时由内核动态链接载入内存，可跨程序共享，减少物理空间占用。
- **静态链接库 (`.a` 后缀)**：Static Library。在程序编译时直接被复制并打包进最终的可执行文件中，不依赖外部库运行，但体积偏大。

### 4.1. 动态链接库管理命令 `ldconfig`

- **工作原理**：`ldconfig` 会扫描系统默认路径（`/lib`、`/usr/lib`）以及 `/etc/ld.so.conf` 中列举的第三方动态链接库路径，扫描出可共享的共享库，并据此更新系统动态装载器（`ld.so`）所需要的高速链接缓存文件。
- **链接缓存**：默认输出为二进制的 `/etc/ld.so.cache`。系统运行程序时依靠此缓存快速定位所需的动态链接库。
- **使用时机**：通常在系统开机初始化时自动运行；但当系统手动安装了新的第三方链接库（如上述编译 OpenSSL 动态库）后，**必须手动运行一次 `ldconfig`** 强制刷新。

---

## 5. 常用基础命令

### 5.1. 用户管理与权限配置

```shell
# 创建一个新用户，-m 表示同步创建家目录，并指定默认 Shell 为 bash
sudo useradd -m -s /bin/bash username

# 修改指定用户的登录 Shell 解释器
sudo chsh -s /bin/bash username
```

若需要为指定用户赋予 `sudo` 临时系统管理权限，可以编辑配置文件：

```shell
sudo visudo
```

在文件中追加如下权限控制配置（`NOPASSWD` 表示该用户在使用 sudo 时无需输入自身密码）：

```text
username   ALL=(ALL:ALL) NOPASSWD: ALL
```

### 5.2. 系统版本与内核信息查询

```shell
uname -a               # 显示完整的系统架构、主机名以及正在运行的内核版本
cat /etc/os-release    # 打印操作系统的详细分发版本名称与版本代号
cat /proc/version      # 打印当前 Linux 内核编译的相关环境与编译器版本信息
```

### 5.3. 硬件温度监控

```shell
# 安装硬件传感器检测工具
apt install lm-sensors

# 交互式自动检测主板、CPU 的硬件温度传感器配置
sensors-detect

# 输出当前 CPU 核心及各个硬件温度参数
sensors
```

---

## 6. 经典案例排查

### 6.1. 解决 Debian Stretch 归档生命周期结束导致的 APT 更新失败

#### 6.1.1. 问题描述

由于 Debian Stretch (Debian 9.x) 版本较老，已进入官方生命周期终点（EOL）。此时使用 `apt update` 可能会遇到因安全软件仓库迁移下线引发的 404 错误：

```text
404  Not Found
E: The repository 'http://security.debian.org stretch/updates Release' does no longer have a Release file.
```

#### 6.1.2. 解决方案

需要将旧的软件源域名重定向至 Debian 的历史归档源（Archive Repositories）：

```shell
# 将默认的主包源地址 debian.org 替换为 archive.debian.org 归档地址
sudo sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list
sudo sed -i 's|security.debian.org|archive.debian.org/debian-security/|g' /etc/apt/sources.list

# 同步对拓展三方库 backports 的地址进行更新
sudo sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list.d/backports.list 2>/dev/null || true
sudo sed -i 's|security.debian.org|archive.debian.org/debian-security/|g' /etc/apt/sources.list.d/backports.list 2>/dev/null || true

# 重新运行更新与升级
apt update && apt upgrade -y
```
