---
title: "setuptools使用手册"
filename: setuptools-setup-guide
description: Python 打包与分发工具 setuptools 使用指南。系统解析了 setup() 的元数据及外部依赖声明参数，对比了 setup.py 传统历史命令与 pyproject.toml、pip install、python -m build 等现代替代标准。提供了一个集成 Cython 扩展（Extension、cythonize 编译）和 NumPy 头文件引入的完整 setup.py 实例配置，并给出了规避 flat-layout 的目录排除方法。
tags: [setuptools, python-packaging, cython-compilation, numpy-integration, pyproject-toml]
aliases: [setuptools使用手册, setup.py配置参数, Cython编译配置]
status: completed
date created: 星期日, 十二月 21日 2025, 11:05:26 上午
date modified: 星期五, 六月 19日 2026, 2:49:03 下午
---

<!-- toc -->

## 1. 简介

**setuptools** 是 Python 社区中用于 **打包 (packaging)**、**分发 (distribution)** 和 **安装 (installation)** Python 项目的标准工具集。

## 2. 配置参数

### 2.1. setup() 核心配置参数表

| 参数 | 作用说明 | 常见配置示例值 |
| :--- | :--- | :--- |
| **`name`** | **包的发布名称**，在 PyPI 上的唯一标识。 | `'requests'` |
| **`version`** | **版本号**，推荐遵循 [语义化版本规范](https://semver.org/)（如 X.Y.Z）。 | `'1.0.5'` |
| **`description`** | **单行简短摘要介绍**。 | `'A short description'` |
| **`long_description`** | **详细说明**，常读取 `README.md` 的内容呈现。 | `open('README.md').read()` |
| **`url`** | **项目官方主页或 GitHub 托管仓库地址**。 | `'https://github.com/...'` |
| **`author`**, **`author_email`** | **作者信息** 与联系邮箱。 | `'Your Name'`, `'email@example.com'` |
| **`license`** | **开源协议声明**。 | `'MIT'`, `'GPLv3'` |
| **`packages`** | **需要被打包的子包目录列表**。通常使用 `setuptools.find_packages()` 自动扫描所有含 `__init__.py` 文件夹。 | `find_packages()` |
| **`py_modules`** | 如果项目非常简单仅包含 **单个 .py 文件**，则使用该参数声明。 | `['mymodule']` |
| **`install_requires`** | **生产环境依赖包列表**。用户 `pip install` 你的包时，依赖会被自动下载。 | `['pandas', 'jinja2>=3.0']` |
| **`python_requires`** | **项目所要求的 Python 解释器最低版本**。 | `'>=3.6'` |
| **`entry_points`** | **注册 CLI 终端命令或者是插件系统挂载点**。 | 见下文示例 |
| **`include_package_data`** | 是否打包 **非代码静态资源**，需配合 `MANIFEST.in` 使用。 | `True` |

### 2.2. 声明式配置 (Declarative Config)

这是 `setuptools` 推荐的配置进化方案：将元数据与外部配置静态化写入 `setup.cfg` 或 `pyproject.toml` 中，保证 `setup.py` 文件足够干净简洁：

```python
# setup.py 
from setuptools import setup 

setup()
```

### 2.3. 现代配置标准 (pyproject.toml)

遵循 **PEP 517/518** 标准的配置文件，旨在统一整个 Python 社区中打包（Setuptools、Poetry、Hatch）、格式化、Lint 工具的配置入口。

> [!tip]
> 现代 Python 打包标准强烈推荐使用 `pyproject.toml` 静态声明配置，以下是一个典型的配置样例：
> 
> ```toml
> [build-system]
> requires = ["setuptools>=61.0.0", "wheel"]
> build-backend = "setuptools.build_meta"
> 
> [project]
> name = "my_package"
> version = "0.1.0"
> description = "A sample Python package"
> readme = "README.md"
> requires-python = ">=3.7"
> license = {text = "MIT"}
> authors = [
>     {name = "Author Name", email = "author@example.com"}
> ]
> classifiers = [
>     "Programming Language :: Python :: 3",
>     "License :: OSI Approved :: MIT License",
> ]
> dependencies = [
>     "requests>=2.28.0",
>     "numpy>=1.20.0"
> ]
> 
> [project.urls]
> Homepage = "https://github.com/example/my_package"
> 
> [project.entry-points.console_scripts]
> my-cli = "my_package.cli:main"
> ```

---

## 3. 常用打包命令对比

| 传统历史命令 | 作用说明 | 现代替代标准命令 (推荐) |
| :--- | :--- | :--- |
| **`python setup.py install`** | 将项目直接安装到当前环境的 `site-packages` 下。 | **`pip install .`** |
| **`python setup.py sdist`** | 构建 **源码分发包**（生成 `.tar.gz` 压缩文件）。 | **`python -m build`** |
| **`python setup.py bdist_wheel`** | 构建 **二进制轮子包**（生成跨平台安装的 `.whl` 文件）。 | **`python -m build`** |
| **`python setup.py clean`** | 清理编译过程中生成的 build/dist 临时文件夹。 | 无标准命令，通常手动 rm 清理。 |
| **`python setup.py develop`** | 可编辑开发模式（本地代码修改立刻生效，无需重新打包）。 | **`pip install -e .`** |

---

## 4. 复杂项目打包编译实例 (Cython 与 NumPy 集成)

本示例展示了如何编译 Cython 核心扩展模块，并通过 `setuptools` 构建分发包。

```python
import numpy
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

# ----------------------------------------------------------------------
# 步骤 1: 定义需要编译的 Cython 扩展模块
# ----------------------------------------------------------------------

# 假设您的 Cython 源文件结构位于包名：[项目 X] 内
# name 参数定义了导入路径 (例如: import [项目 X].core)
extensions = [
    Extension(
        name="[项目X].core",
        # Cython 源码实际路径
        sources=["[项目X]/core.pyx"],
        # 若编译时需要链接系统数学库：libraries = ["m"]
        # 优化编译器指令：extra_compile_args = ["-O3"]
        
        # 必须传入包含的 NumPy 头文件路径以进行 C-API 交互
        include_dirs=[numpy.get_include()] 
    )
]

# ----------------------------------------------------------------------
# 步骤 2: 编写 setup 配置
# ----------------------------------------------------------------------

setup(
    name="[项目X]",
    version="0.1.0",
    description="A project with protected Cython modules for alerting.",
    author="Your Name",
    
    # 自动定位项目中的子包，并显式排查其他杂项文件夹，防止触发 flat-layout 命名冲突错误
    packages=find_packages(
        exclude=['logs', 'runs', 'temp', 'result', 'static', 'test', 'docs'] 
    ),
    
    # 交给 Cython 进行编译转化
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"}, # 指定支持 Python 3 语法
        quiet=True                                   # 简化终端编译输出
    ),
    
    include_dirs=[numpy.get_include()],
    
    # pip 安装当前包时，必须自动补齐的第三方依赖
    install_requires=[
        'numpy>=1.16',
    ],
    
    # 本地编译打包时（例如执行构建时）本身所需要的模块依赖
    setup_requires=[
        'Cython>=0.29',
        'numpy>=1.16'
    ],
    
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

## 5. 进阶打包设计指南与避坑建议

> [!important]
> 在执行 Python 混合项目（Cython/C/C++ 扩展）打包发布时，需要注意以下工程化避坑要点：
> 
> 1. **Flat-Layout 冲突规避**：在现代 Python 打包标准中，强烈建议将源代码置于 `src/` 目录下（即 `src-layout` 模式），以避免 setuptools 将 `tests` 或 `docs` 等外部文件夹打包发布，触发 flat-layout 构建冲突错误。
> 2. **三方库头文件定位**：像 NumPy、Pybind11 等第三方库，其 C-API 头文件路径是在本地构建环境动态确定的，因此在 `setup.py` 中直接写死路径会导致跨机器编译失败。必须使用如 `numpy.get_include()` 等动态发现机制在编译期引入。
> 3. **编译参数跨平台兼容**：如需使用 `-O3` 或 `/Ox` 等编译器优化指令，应在 `Extension` 的 `extra_compile_args` 参数中区分 GCC (Linux/macOS) 和 MSVC (Windows) 编译器，进行分支定义以确保编译链的跨平台兼容性。

## 6. 参考资料

- [setuptools 官方打包指南文档](https://setuptools.pypa.io/en/latest/userguide/index.html)

