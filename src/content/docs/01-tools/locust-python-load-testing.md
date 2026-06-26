---
title: "Locust压测"
filename: locust-python-load-testing
description: Locust是基于Python的现代化、分布式压力测试工具。本文讲解Locust安装步骤以及通过定义HttpUser任务编写SSE接口压测脚本的流程，展示了如何通过Web UI仪表盘进行压力启动、并发数动态调整、报错查看，以及压测报告与性能指标下载的完整操作。
tags: [locust, load-testing, performance, python]
aliases: [Locust压测, 性能测试, Python压测]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:27 下午
date modified: 星期一, 六月 22日 2026, 5:12:48 下午
---

<!-- toc -->

## 1. 简介

一个基于 python 的并发压力测试工具

- 随时停止
- 下载测试报告

## 2. 安装

```shell
pip install locust
```

## 3. 使用

- 编写普通 API 脚本

```python
from locust import HttpUser, task, between  
  
class APIUser(HttpUser):  
    wait_time = between(1, 30)  
  
    @task  
    def test_sse(self):  
        response = self.client.get("/test_path/?name=&page_number=1&page_size=10000&range_in=all",headers={"Authorization": "Token a997b320953eae1ce24a765ca7648d5ed1742546"})
```

- 编写 sse 调用脚本

```python
from locust import HttpUser, task, between  
  
class SSEUser(HttpUser):  
    wait_time = between(1, 120)  
    @task  
    def test_sse(self):  
        a = self.client.post("/sse/", data={  
            "qa_id": 1,  
            "answer": """测试""",  
            "is_last_question": False,  
        }, stream=True, headers={"Authorization": "Token a997b320953eae1ce24a765ca7648d5ed1742546"})  
        # print(a.text)        
        # for line in a.iter_lines():        
         #     if line:        
         #         print(line.decode('utf-8'))  # 打印 SSE 事件
```

- 启动服务

```
locust -f locust_sse.py
```

- web 页面配置并发
![](http://qiniu.sxyxy.top/20250307161858.png)

> Ramp up 代表用户平滑线性增加

## 4. 拓展信息

### 4.1. Wrk 命令行并发工具

- 编写参数文件

```lua
# test.lua
wrk.headers["authorization"] = "Token a997b320953eae1ce24a765ca7648d5ed1742546"                                                        wrk.method = "POST"                                                                                                                    wrk.body = '{"qa_id": 1}'                                                                                                              wrk.headers["Content-Type"] = "application/json"
```

- 测试命令

```shell
wrk -t10 -c200 -d30s --timeout 30 -s test.lua https://www.example.com/test/
```

### 4.2. Ab 命令行并发工具

- 编写参数文件

```txt
# test.txt
{                                                                                                                                      
    "qa_id": 1                                                                                                                         
}
```

- 测试命令

```shell
ab -c 2 -n 2 -p test.txt -T application/json -H "Authorization:Token a997b320953eae1ce24a765ca7648d5ed1742546" https://www.example.com/test/
```

## 5. 参考资料

- [官方文档](https://docs.locust.io/en/stable/quickstart.html)
- [Github 地址](https://github.com/locustio/locust)
