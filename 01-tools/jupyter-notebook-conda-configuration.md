---
title: "Jupyter安装"
filename: jupyter-notebook-conda-configuration
summary: Jupyter Notebook是广泛用于数据分析和算法测试的交互式计算环境。本文介绍在Anaconda环境中通过conda安装Jupyter的步骤，罗列了通过命令行参数临时设置工作目录的命令，并提供生成全局配置文件修改notebook_dir的永久路径配置，以实现启动路径固定。
tags: [jupyter-notebook, conda, data-science, configuration]
aliases: [Jupyter安装, Conda配置, 工作目录设置]
status: completed
date created: 星期一, 一月 12日 2026, 10:03:55 上午
date modified: 星期五, 六月 19日 2026, 12:05:36 中午
---

<!-- toc -->

## 1. 使用记录

- 安装

```shell
conda install jupyter notebook
```

- 在指定目录启动 jupyter
  - 临时启动

  ```shell
  jupyter notebook --notebook-dir='D://demo' #临时
  ```

  - 永久配置

  ```shell
  jupyter notebook --generate-config
  vim ~/.jupyter/jupyter_notebook_config.py
  c.NotebookApp.notebook_dir #配置该参数
  ```

- 关联 conda 环境
  - 方式一

  ```shell
  #在安装 jupyter notebook 的目录中执行
  conda install nb_conda #nb_conda 必须保证 python 版本小于 3.9(20230828), 建议使用 3.8 版本
  ```

  - 方式二(手动添加)

  ```shell
  activate des_dev #进入目标环境
  conda install ipykernel # #安装 ipykernel
  jupyter kernelspec list #查看 kenel
  jupyter kernelspec remove kernel_name #删除 kernel
  python -m ipykernel install --user --name <env_name> --display-name "<notebook_name>" #安装内核
  ```

- 管理 ipykernel 环境

```shell
jupyter kernelspec list #查看
jupyter kernelspec remove kernel_name #删除
```

## 2. Jupyterhub

一个支持多用户管理的 jupyter 工具

- 安装

```shell
python3 -m pip install jupyterhub
python3 -m pip install jupyter
python3 -m pip install nb_conda_kernel #某些时候子环境中的 nb_conda 会不生效，在 jupyterhub 环境下安装该依赖进行尝试(具体的查看 jupyterhub 的运行日志)
npm install -g configurable-http-proxy
```

- 设置白名单

```shell
c.Authenticator.allowed_users = {'yangxy'}
```

- 设置管理员

```shell
c.Authenticator.admin_users = {'yangxy'}
c.Authenticator.allow_all = True  #允许所有登录 
```

- ipython 脚本保持环境变量

```shell
c.Spawner.env_keep = ['JAVA_HOME','SPARK_HOME','PATH', 'PYTHONPATH', 'CONDA_ROOT', 'CONDA_DEFAULT_ENV', 'VIRTUAL_ENV', 'LANG', 'LC_ALL', 'JUPYTERHUB_SINGLEUSER_APP']
```

- 设置不活跃自动关闭

```
pip install jupyterhub-idle-culler
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': [
            'python3',
            '-m', 'jupyterhub_idle_culler',
            '--timeout=86400',  # 超时时间，以秒为单位
            '--cull-every=1800',  # 每隔多少秒检查一次
            '--concurrency=10',  # 并发数量
            '--cull-connected', #添加该选项则即使激活也会关闭，不添加该选择则会空间超时关闭
        ],
    }
]
```

- 关联 conda 环境

```shell
conda create -n myenv ipython nb_conda 
```

## 3. Notebook

- shell 命令格式

```python
!shell
```

- 魔术命令
  - 示例

  ```python
  % command #只针对单行有效
  %% commad #针对 cell 有效
  ```

  - 针对 google vertex AI 中的 Bigquery 魔法命令

  ```python
  %% bigqeury data #进行查询并且输出 data 的 dataframe
  select ...
  ```

## 4. 参考链接

- [jupyterhub](https://jupyterhub.readthedocs.io/en/stable/tutorial/index.html#installation)
- [参考文档](https://gist.github.com/tanbro/a94bfa4a552381f599e7e6b551ccadcf?permalink_comment_id=3867931)
