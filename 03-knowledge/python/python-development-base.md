---
title: "Python基础开发指南"
filename: python-development-base
description: Python 开发环境部署与包管理指南。详述了 Python 源码编译、Venv、Pip, Conda 的配置，给出了解决 Conda 环境下 Pip 路径失配的 site.py 修改步骤。对比了 Poetry 依赖解析与 Pipx 独立工具管理，总结了 Classmethod、Property、Dataclass 常用装饰器、邮件与文件处理模块，以及 PyInstaller 与 Nuitka 分发分包方案。
tags:
  - python
  - package-management
  - poetry
  - conda
  - software-distribution
aliases:
  - Python基础开发指南
  - Poetry环境配置
  - Python装饰器用法
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:25 上午
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

## 1. 源码编译安装 Python

### 1.1. 安装依赖

```shell
yum -y zlib* gcc libffi-devel
```

### 1.2. 下载安装包

```shell
wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz
```

### 1.3. 编译安装

```shell
mkdir /usr/local/python3
mv Python-3.9.13.tgz /usr/local/python3
cd /usr/local/python3
tar -zxvf Python-3.9.13.tgz 
cd Python-3.9.13
./configure --with-ssl
make
make install
```

### 1.4. 建立软连接

```shell
ln -s /usr/python/bin/python3 /usr/bin/python3
ln -s /usr/python/bin/pip3 /usr/bin/pip3
```

> [!WARNING]
> 注意：Python 3.7 之后，要求系统的 OpenSSL 版本大于 1.1。

---

## 2. Venv 虚拟环境使用

```shell
apt install python3.11-venv # 安装 venv 模块
cd project_path
python -m venv .
source bin/activate
python app.py 
pip install pandas # 安装项目依赖
```

- **部署调用运行命令示例**：

```shell
$project_path/bin/python $project_path/main/app.py
```

---

## 3. Pip 包管理工具

### 3.1. 安装

```shell
apt install python3-pip # Ubuntu 环境安装
```

### 3.2. 配置国内源

- **永久全局配置**

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

- **临时指定源配置**

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib
```

### 3.3. 常用命令

```shell
pip install google-analytics-admin # 安装
pip install --upgrade google-analytics-admin # 升级
pip list # 查看已安装列表
```

### 3.4. Conda 环境中 Pip install 的安装路径错位问题

- **问题描述**：
  在切换到指定 Conda 虚拟环境后，执行 `pip --version` 却发现 Pip 实际指向的路径并未关联到当前虚拟环境。
  ![](http://qiniu.sxyxy.top/20230830145522.png?image=image)

- **解决方法**：

```shell
conda activate env # 切换到目标环境
python -m site --help # 查看 site.py 配置文件路径
vim $path/site.py # 编辑 site.py 配置文件，并修改配置内容
```

  ![](http://qiniu.sxyxy.top/20230830145327.png?image=image)
  ![](http://qiniu.sxyxy.top/20230830145355.png?image=image)

---

## 4. Conda 环境管理

### 4.1. 查看 Conda 信息

```shell
conda info
```

### 4.2. Windows 环境变量配置参考

```text
D:\miniconda
D:\miniconda\Library\bin
D:\miniconda\Scripts
```

### 4.3. 初始化 Conda 终端

```shell
conda init 
```

### 4.4. 指定虚拟环境安装路径

```shell
vim ~/.condarc
# 添加以下配置内容以指定虚拟环境存放路径
envs_dirs:
  - D:\miniconda\envs
```

> [!WARNING]
> 注意：确保当前用户对上述配置的目录拥有足够的读写权限。

### 4.5. 配置 Conda 国内源

```shell
conda config --set show_channel_urls yes # 生成默认 .condarc 文件
vim ~/.condarc
```

在配置文件中添加清华镜像源：

```yaml
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

重置并清除缓存索引：

```shell
conda clean -i
```

### 4.6. 基本包管理

```shell
conda list 
conda install package_name
```

---

## 5. Poetry 依赖管理

Poetry 是一款现代的 Python 依赖管理与打包发布程序。相比 Conda 可以减少非必须包的打包，相比 Pip 拥有更强的依赖树解析功能，有效避免版本冲突导致的环境崩溃问题。

- 支持针对生产（Production）、开发（Development）等多环境进行分组隔离管理。
- 更好地支持自定义私有镜像源。

### 5.1. 安装方式

- **macOS / Linux / WSL**

```shell
curl -sSL https://install.python-poetry.org | python3 -
curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/software/poetry python3 - # 指定安装目录
```

- **Windows (PowerShell)**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 5.2. 常用命令

```shell
poetry completions bash >> ~/.bash_completion # 自动补全
poetry init # 交互式初始化已有项目
poetry new project_name # 创建一个全新的项目脚手架
poetry config --list # 查看当前全局配置
poetry config cache-dir "D:\poetry_env" # 修改缓存与虚拟环境路径
poetry env use $python_path # 指定当前项目关联的 Python 解析器
poetry env list # 查看当前项目所有的虚拟环境
poetry env info # 查看当前激活的虚拟环境信息
poetry env remove env_name # 删除指定虚拟环境
poetry add requests # 添加依赖并自动安装
poetry add requests --group dev # 添加到开发环境依赖组
poetry install # 自动解析并安装 pyproject.toml 声明的全部依赖
poetry install --no-dev # 仅安装生产环境依赖，部署时常用
poetry update # 更新全部依赖包版本
poetry show -t # 以树状结构查看当前已安装的依赖树
```

### 5.3. 配置国内源

- **命令行方式**

```shell
poetry source add aliyun https://mirrors.aliyun.com/pypi/simple/
```

- **修改 pyproject.toml 方式**

```toml
[[tool.poetry.source]]
name = "aliyun"
url = "https://mirrors.aliyun.com/pypi/simple/"
```

---

## 6. Pipx 独立应用管理

Pipx 是一个用于在完全隔离的环境中安装和运行 Python 终端用户应用（例如 CLI 工具）的工具。

### 6.1. 安装

```shell
pip install pipx
```

### 6.2. 环境变量与命令

- **配置环境变量**

```shell
# pipx 路径配置
export PIPX_GLOBAL_HOME="/opt/software/pipx"
export PIPX_GLOBAL_BIN_DIR="/opt/software/pipx/bin"
export PIPX_GLOBAL_MAN_DIR="/opt/software/pipx/man"
export PATH=$PATH:/opt/software/pipx/bin
```

- **常用命令**

```shell
pipx install poetry # 在当前用户下隔离安装
pipx install poetry --global # 全局安装
pipx list # 查看安装的工具列表
```

> [!NOTE]
> 应用默认被隔离安装在 `$HOME/local/.bin`，Pipx 的元数据信息存储在 `$HOME/local/.pipxmd`。

---

## 7. 常见装饰器

- **`@staticmethod` (静态方法)**  
  定义一个与类和实例都无关的独立方法。

```python
class Dog():
    name = ""
    def call(self, arg=None):
        self.arg = arg
    
    @staticmethod
    def eat():
        print(Dog.name)
        dog = Dog() # 必须先手动实例化才能调用类内部的实例方法
        print(dog.call())
```

- **`@classmethod` (类方法)**  
  定义一个接收类对象作为第一个参数（通常是 `cls`）的方法。

```python
class Dog():
    name = ""
    def call(self, arg=None):
        self.arg = arg

    @classmethod
    def eat(cls): # 传递类对象
        print(cls.name)
        dog = cls() # 基于当前类模板动态实例化
        print(dog.call())
```

- **`@property` (属性化方法)**  
  将类内部的一个方法转化为只读属性。

```python
class Dog():
    @property
    def call(self):
        pass

dog = Dog()
dog.call # 直接作为属性调用，无需加括号
```

- **`@dataclass` (数据类)**  
  用于简化编写主要用于存放数据的类，自动生成 `__init__`、`__repr__` 等魔法方法。

```python
from dataclasses import dataclass

@dataclass
class Food:
    name: str
    unit_price: float
    stock: int = 0
    
    def stock_value(self) -> float:
        return self.stock * self.unit_price
```

---

## 8. 常见实用模块

- [python-pptx](python-pptx.md)：用于创建和修改 PowerPoint (.pptx) 演示文稿的 Python 库。
- [six](https://six.readthedocs.io/)：用于兼容 Python 2 和 Python 3 代码库的工具包。
- [mimetypes](https://docs.python.org/3/library/mimetypes.html)：解析文件 MIME 类型的标准库。
- [python-magic](https://pypi.org/project/python-magic/)：基于系统的 libmagic 开发，用于通过文件签名检测实际类型的 Python 接口。
- [pyftpdlib](https://pypi.org/project/pyftpdlib/)：基于异步 IO 编写的极速 FTP 服务器库。
- [uploadserver](https://pypi.org/project/uploadserver/)：支持 Web 浏览器上传、下载文件并提供简单鉴权验证的简易服务器。
- [email](https://docs.python.org/3/library/email.examples.html)：构造和处理电子邮件的标准库。

  > [!WARNING]
  > 在 email 库中设置 `From` 发件人字段时，必须与实际登录授权的发送邮箱地址保持完全一致，否则邮件可能会被主流收件箱拦截。

- **`http.server` (静态资源服务)**  
  在本地目录下快速拉起一个静态文件下载服务器。

```shell
python -m http.server 8080
```

- **`speedtest-cli` (网络测速)**

---

## 9. 软件发布与保护移交

### 9.1. 软件分发格式

- **tar.gz**：纯源码包。
- **wheel**：预编译分发格式，包含元数据、py 源码或已编译的 pyc 字节码。

### 9.2. 模块级混淆移交

- 使用 CPython 编译为底层系统的 **.so / .pyd** 机器码库文件。

### 9.3. 单一可执行程序分发

- **Pyinstaller**：打包为单文件，内部打包加密后的 .pyc 文件。
- **Nuitka**：将 Python 转换为 C++ 再编译为纯机器码，执行效率与安全性更高。

### 9.4. 源码保护授权

- **Pyarmor**：提供完善的混淆、加密以及运行授权证书（License）控制。

> [!TIP]
> 如果项目已经通过 Nuitka 等工具编译为二进制机器码，则不需要再单独使用 Pyarmor 进行代码混淆加密。

---

## 10. 参考资料

- [Python 官方网站](https://www.python.org/)
- [Python MRO 查找机制详解](https://www.cnblogs.com/poloyy/p/15226424.html)
- [Python 源码包下载地址](https://www.python.org/ftp/python/3.9.13/)
- [Poetry 官方文档](https://python-poetry.org/docs/)
- [Pipx 官方配置手册](https://pypa.github.io/pipx/#on-windows-install-via-pip-requires-pip-190-or-later)
- **国内常用镜像源**：
  - 镜像源一：`https://pypi.tuna.tsinghua.edu.cn/simple` (清华源)
  - 镜像源二：`http://mirrors.aliyun.com/pypi/simple/` (阿里云)
  - 镜像源三：`https://pypi.mirrors.ustc.edu.cn/simple/` (中科大)
  - 镜像源四：`http://pypi.douban.com/simple/` (豆瓣)
  - 镜像源五：`https://pypi.org/simple` (官方源)
