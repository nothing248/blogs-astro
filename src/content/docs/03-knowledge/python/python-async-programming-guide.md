---
title: "Python协程与异步IO"
filename: python-async-programming-guide
description: Python 异步编程与高性能 Web 服务器配置指南。系统解析了生成器（yield/send/yield from）、Asyncio 异步库、Aiohttp 框架及 Gevent 等协程库的机制与代码。对比分析了 Gunicorn、uWSGI 与 Uvicorn 的配置参数，并深度论述了“Gunicorn + Uvicorn Worker”的多核高可用模式与直接运行 Uvicorn 在生产部署上的优劣。
tags:
  - python-coroutine
  - async-programming
  - uvicorn
  - gunicorn
  - web-server
aliases:
  - Python协程与异步IO
  - Gunicorn与Uvicorn部署
  - 生成器与yield-from
status: completed
date created: 星期三, 十二月 10日 2025, 6:20:41 晚上
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

## 1. 简介

协程（Coroutine）一般用于处理异步 I/O 操作。因为协程是在单线程之内进行并发任务调度，所以相较于多线程，它能够显著减少线程上下文切换带来的系统开销。

## 2. 生成器

生成器是实现协程的基石，主要用于暂停和恢复函数的执行。

### 2.1. 生成器的创建

- **生成器表达式**：

```python
g = (x * x for x in range(10))
```

- **生成器函数**：使用 `yield` 关键字。

```python
def generate_next_test():
    print('step 1')
    yield 1
    return 5
g = generate_next_test()
next(g)  # 输出 step 1 并返回 1
```

> [!WARNING]
> 对已迭代完毕的生成器再次调用 `next(g)` 会引发 `StopIteration` 错误。

### 2.2. 生成器使用

- **`next(g)` 方法**：

```python
f = fib(6)
next(f)  
```

- **`g.send(value)` 方法**：

```python
def average_gen():
    total = 0
    count = 1
    average = 0
    while True:
        new_num = yield average
        if new_num is None:
            break
        count += 1
        total += new_num
        average = total / count

    # 每一个 return 语句都会导致当前协程结束
    return total, count, average

calc_average = average_gen()
next(calc_average)            # 激活生成器，或使用 calc_average.send(None)
print(calc_average.send(10))  # 打印：10.0
```

> [!IMPORTANT]
> 第一次激活生成器时，必须使用 `next(g)` 语句或 `g.send(None)`。不能直接在第一次发送非 `None` 值，因为此时生成器还未启动，没有 `yield` 语句能够接收该值。

### 2.3. 高级用法

- **`yield from` 表达式**：

```python
def average_gen():
    total = 0
    count = 0
    average = 0
    while True:
        print("start average_gen")
        new_num = yield average
        if new_num is None:
            break
        count += 1
        total += new_num
        average = total / count

    return total, count, average

# 委托生成器
def proxy_gen():
    while True:
        print("start proxy_gen")
        # 只有子生成器退出（触发 return）时，yield from 左侧的变量才会被赋值并恢复执行
        total, count, average = yield from average_gen()
        print("计算完毕！！\n总共传入 {} 个数值， 总和：{}，平均数：{}".format(count, total, average))

# 调用方
def main():
    calc_average = proxy_gen()
    next(calc_average)            # 预激协程
    print(calc_average.send(10))  # 打印：10.0
    print(calc_average.send(20))  # 打印：15.0
    print(calc_average.send(30))  # 打印：20.0
    calc_average.send(None)       # 结束协程
    # 如果在此处再次调用 send，将会自动重新创建一个子生成器实例
```

> [!NOTE]
>
> - `yield from` 能够自动代理并传递子生成器内部可能抛出的异常。
> - `yield from` 语句修饰生成器时，会自动执行一次隐式的 `next()` 激活操作。

---

## 3. Asyncio

Asyncio 是 Python 标准库中提供的异步 I/O 框架，内置支持了 **TCP、UDP、SSL 等多种网络传输协议**。

- **安装**：

```shell
pip install asyncio
```

- **基本使用示例**：

```python
import threading
import asyncio

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.current_thread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.current_thread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

---

## 4. Aiohttp

Aiohttp 是一个基于 asyncio 实现的高性能异步 HTTP 框架，适用于高并发的 Web 服务或爬虫开发。

- **安装**：

```shell
pip install aiohttp
```

- **Web 服务器示例**：

```python
import asyncio
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
```

---

## 5. Greenlet

Greenlet 是一个底层的轻量级协程库，允许开发者手动控制代码段的跳转与切换。

- **安装**：

```shell
pip install greenlet
```

- **使用**：

```python
from greenlet import greenlet

def func1():
    print(1)      # 第 1 步: 输出 1
    gr2.switch()  # 第 2 步: 手动切换到 func2 执行
    print(2)      # 第 5 步: 输出 2
    gr2.switch()  # 第 6 步: 再次切换回 func2

def func2():
    print(3)      # 第 3 步: 输出 3
    gr1.switch()  # 第 4 步: 手动切换回 func1 执行
    print(4)      # 第 7 步: 输出 4

gr1 = greenlet(func1)
gr2 = greenlet(func2)
gr1.switch()      # 第 0 步: 激活并启动 func1
```

---

## 6. Gevent

Gevent 是一个基于 Greenlet 封装的协程网络库，通过 Monkey Patch 技术实现同步阻塞代码的异步非阻塞化运行。

- **安装**：

```shell
pip install gevent
```

- **使用**：

```python
import gevent

def foo():
    print('Running in foo')
    gevent.sleep(2)
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    gevent.sleep(1)
    print('Implicit context switch back to bar')

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar)
])
```

---

## 7. Eventlet

Eventlet 是一个高度可定制的异步并发库，在原理上与 Gevent 类似，也是对 Greenlet 库进行了封装。

- **安装**：

```shell
pip install eventlet
```

- **使用**：

```python
import eventlet

def test(x):
    print(f'Greenthread test Num:{x}')
    eventlet.greenthread.sleep(1)
    return x

def test1(y):
    print(f'Greenthread test1 Num:{y}')
    return y

x = eventlet.spawn(test, 1)
y = eventlet.spawn(test1, 2)
x.wait()  # 等待协程执行完毕并返回结果
```

---

## 8. 常见的 Python Web 服务器

### 8.1. Gunicorn

Gunicorn 是一款基于 Python 开发的高性能 WSGI HTTP 服务器，广泛用于生产环境的 Web 应用部署。

- **安装**：

```shell
pip install gunicorn
```

- **项目配置示例 (`gunicorn_config.py`)**：

```python
import multiprocessing

bind = '127.0.0.1:8000'                      # 监听地址与端口号
workers = multiprocessing.cpu_count() * 2 + 1 # 工作进程数，建议设置为核数的 2-4 倍
backlog = 2048                              # 服务器最大挂起连接数
worker_class = "gevent"                     # 工作模式，可选 sync, gevent, eventlet 等
worker_connections = 1000                   # 单个工作进程最大并发连接数（仅 gevent 等异步模式下生效）
daemon = False                              # 是否以守护进程方式后台运行
debug = True                                # 调试日志开关
proc_name = 'gunicorn_demo'                 # 进程名称前缀
pidfile = './log/gunicorn.pid'              # PID 存放文件
errorlog = './log/gunicorn.log'             # 错误日志存放文件
```

- **部署运行命令**：

```shell
gunicorn -c gunicorn_config.py gunicorn_demo:app
```

### 8.2. uWSGI

uWSGI 是一款高性能的应用服务器，它完整实现了 WSGI 规范，并支持其自定义的 uwsgi 通信协议。

- **安装**：

```shell
pip install uwsgitop  # 安装 uWSGI 性能监控工具或直接安装 uwsgi 核心
```

- **项目配置示例 (`uwsgi.ini`)**：

```ini
[uwsgi]
chdir=/home/[张三]/web/flask/mysite/
home=/home/[张三]/web/flask/mysite/.env
module=hello                                 # 入口 Python 文件名
callable=app                                 # 应用实例对象名
master=true
processes=2                                  # Worker 进程数
chmod-socket=666
logfile-chmod=644
uid=[张三]_web
gid=[张三]_web
procname-prefix-spaced=mysite                # 进程名称前缀
py-autoreload=1                              # 检测到代码修改自动重载
# http=0.0.0.0:8080                           # 调试使用的 HTTP 服务端口
vacuum=true                                  # 退出时清理 pid/sock 等残留临时文件
socket=%(chdir)/uwsgi/uwsgi.sock             # Nginx 反向代理通信的 Socket 路径
stats=%(chdir)/uwsgi/uwsgi.status            # 状态监控文件路径
pidfile=%(chdir)/uwsgi/uwsgi.pid             # PID 控制文件路径
daemonize=%(chdir)/uwsgi/uwsgi.log           # 守护进程日志存放路径
```

- **运维常用控制指令**：

```shell
uwsgi --ini uwsgi.ini             # 启动服务
uwsgi --reload uwsgi.pid          # 平滑重启服务
uwsgi --stop uwsgi.pid            # 停止服务
```

### 8.3. Uvicorn

Uvicorn 是一款极速的、基于 uvloop 构建的现代 ASGI (异步网关) 服务器。

- **安装**：

```shell
pip install uvicorn
```

- **启动命令**：

```shell
uvicorn main:app --reload --host 192.168.1.100 --port 8001
```

---

## 9. 拓展信息

### 9.1. 网关接口协议 (CGI)

- 传统的 Web 服务器（如 Nginx、Apache）主要用于分发静态资源（如 HTML、图片）。当需要响应动态内容时，需要通过某种网关标准（CGI）与后台 **应用服务器**（如用 Python 编写的服务）进行数据流交互。

### 9.2. Web 服务协议演进

Web 协议包括 Web 服务器与 Web 框架之间的桥梁规约：

- **WSGI (Web Server Gateway Interface)**：Python 主流的同步 Web 服务标准，限制是无法支持长连接和 WebSocket 等新的双向通信协议。
- **uwsgi 协议**：uWSGI 服务器内部的高性能专有传输协议，通常用于与前端 Nginx 配合。
- **ASGI (Asynchronous Server Gateway Interface)**：WSGI 的异步继承者，支持异步处理、WebSocket 协议以及多通道通信。

### 9.3. Gunicorn + Uvicorn Worker 与 直接使用 Uvicorn 对比

#### 9.3.1. **Gunicorn + Uvicorn Worker 模式**

```shell
.venv/bin/python .venv/bin/gunicorn -w 9 -k uvicorn_worker.UvicornWorker brainnewlife.asgi:application -b 0.0.0.0:1820 --access-logfile -
```

在此模式中，**Gunicorn** 承担 **进程管理器 (Process Manager)** 职责，负责多核利用、守护进程状态监控与重启；**Uvicorn Worker** 仅作为 **ASGI 服务器实现**，专注于处理高性能的网络 I/O。

##### 9.3.1.1. **优势**

- **强悍的进程监控与可靠性**：支持平滑热重载（Graceful Reload），当任一工作进程意外崩溃或内存泄漏时，Master 进程能够瞬间恢复拉起新进程。
- **生产部署标准实践**：广泛应用于高并发、高可用的核心生产环境。
- **完善的监控集成**：日志系统及系统信号捕获集成成熟。

##### 9.3.1.2. **劣势**

- **架构略微复杂**：在容器（如 K8s）环境中多了一层进程管理器的抽象。

#### 9.3.2. **直接使用 Uvicorn 模式**

```shell
uvicorn brainnewlife.asgi:application --host 0.0.0.0 --port 1820 --workers 9
```

##### 9.3.2.1. **优势**

- **轻量且极简**：一行命令启动，开销小，非常适合微服务容器化（Docker）和本地开发环境。
- **多核进程原生支持**：新版 Uvicorn 已经支持通过 `--workers` 参数来实现类似的多核分摊。

##### 9.3.2.2. **劣势**

- **运维健壮性较弱**：相比于 Gunicorn 多年来在进程控制和异常回退上的积累，Uvicorn 本身的进程守护能力较薄弱。不推荐在无外层守护的物理机生产环境上直接裸跑单实例进程。

#### 9.3.3. **总结对比**

| **特性** | **Gunicorn + Uvicorn Worker** | **直接使用 Uvicorn (多 Worker)** |
| :--- | :--- | :--- |
| **核心角色** | Gunicorn (进程管理) + Uvicorn (I/O 网络) | Uvicorn 独立处理服务与多核调度 |
| **进程控制** | **极其强大**：成熟稳定，支持无缝热更、奔溃自愈。 | **一般**：支持多 Worker，但管理控制略粗糙。 |
| **部署复杂性** | 稍繁琐 | 极简单 |
| **适用场景** | 传统物理机或高稳定性要求的生产环境。 | 容器化部署（以单容器单进程为主）或测试开发。 |

---

## 10. 参考资料

- [廖雪峰 Python 协程教程](https://www.liaoxuefeng.com/wiki/1016959663602400/1017970488768640)
- [Asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)
- [Aiohttp 官方文档](https://docs.aiohttp.org/en/stable/)
- [Gunicorn 官方指南](https://gunicorn.org/#quickstart)
- [Gevent 协程网络库文档](http://www.gevent.org/)
- [Eventlet 协程库文档](https://eventlet.net/doc/)
