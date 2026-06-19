---
title: "Django异步与SSE"
filename: django-async-and-sse-practices
summary: 介绍 Python 后端框架 Django 在异步（视图、中间件、ORM）场景下的技术方案。重点解决 PostgreSQL 数据库 intervalstyle 识别异常与连接池泄露问题，提供了异常捕获自动释放连接的数据库中间件代码。此外，针对大模型长连接响应，详细给出了“多线程队列”和“httpx-sse 异步转发”两种 SSE 流式数据传输的最佳实践。
tags:
  - Django
  - 异步编程
  - 连接池管理
  - SSE流式转发
  - PostgreSQL
aliases:
  - Django异步与SSE
  - 数据库连接泄露解决
  - httpx-sse流式传输
status: completed
date created: 星期一, 五月 19日 2025, 2:05:17 下午
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 简介

一个 Python 的后端服务框架

## 2. 异步

- 异步视图
- 异步中间件
- 异步 ORM

## 3. 拓展信息

### 3.1. Pg 数据 intervalstyle 识别问题

某些场景下 django 的时间间隔会出现识别问题, 需要将 pg 数据的的 intervalstyle 识别形式修改的 postgres 格式

### 3.2. Pg 连接池泄露问题

某些场景下连接没有正确释放到连接池, 导致获取连接超时失败.通过中间件手动进行释放处理

```python
# settings.py
MIDDLEWARE = [  
 ...
    'tm_common.exception_middleware.DatabaseConnectionReleaseMiddleware',  # 异常捕获自动释放连接池  件  
]


DATABASES = {  
    "default": {  
        'ENGINE': "django.db.backends.postgresql",  
        'NAME': os.getenv("DB_DATABASE"),  
        'USER': os.getenv("DB_USER"),  
        'PASSWORD': os.getenv("DB_PASSWORD"),  
        'HOST': os.getenv("DB_HOST", "localhost"),  
        'PORT': os.getenv("DB_PORT", 5432),  
        "OPTIONS": {  
            "pool": {  
                # "min_size": 5,  
                "max_size":int(os.getenv("DB_POOL_MAX_SIZE",4))  
            }  
        },  
    },  
}
```

```python
#exception_middleware.py
from django.db import close_old_connections, connection  
from django.utils.deprecation import MiddlewareMixin  
import logging  
  
logger = logging.getLogger(__name__)  
  
  
class DatabaseConnectionReleaseMiddleware(MiddlewareMixin):  
    """  
    有报错自动释放连接到连接池  
    """    def process_exception(self, request, exception):  
        logger.debug("发生异常。正在释放数据库连接。")  
        close_old_connections()  
        logger.debug(f"释放后的连接状态: {connection.connection}")  
        return None
```

### 3.3. SSE 异步转发解决方案

- 方案一: 多线程队列

```python
async def async_get_zhipuai_answer_stream_old(  
        user_id: str,  
        message: list[dict[str, str]],  
        keep_stable: bool = True,  
        llm_api_key: str = "GET-API-KEY-FROM-SITE",  
        llm_model_name: str = "glm-4-plus",  
) -> Generator[ZhipuAIResponse, None, None]:  
    """  
    使用智谱AI的流式输出方法获取答案。  
  
    参数:  
    - user_id: 用户ID，用于标识用户。  
    - message: 消息列表，包含用户与AI的对话历史。  
    - keep_stable: 是否保持输出稳定，默认为True。  
    - llm_api_key: AI模型的API密钥，默认为"GET-API-KEY-FROM-SITE"。  
    - llm_model_name: AI模型名称，默认为"glm-4-plus"。  
  
    返回:  
    - 一个生成器，用于流式输出AI的回答。  
    """    # 创建队列  
    q = queue.Queue()  
  
    # 创建智谱 AI 客户端  
    client = _create_zhipuai_client(llm_api_key)  
    # 生成请求 ID  
    request_id = get_request_uuid(user_id)  
  
    # 准备请求参数  
    request_params = _get_common_request_params(  
        user_id=user_id,  
        request_id=request_id,  
        message=message,  
        keep_stable=keep_stable,  
        llm_model_name=llm_model_name,  
        stream=True  
    )  
    def fetch_data(q,request_params): # 获取数据  
        # 创建流式响应  
        try:  
            stream = client.chat.completions.create(**request_params)  
            # 每次 yield 返回部分的数据  
            for chunk in stream:  
                if not chunk.choices:  
                    continue  
  
                delta_content = chunk.choices[0].delta.content  
                if delta_content:  
                    q.put({  
                        'response': chunk,  
                        'content': delta_content,  # 输出单次留结果，如果要输出所有连续结果，"".join(collected_messages),  
                        'prompt_tokens': chunk.usage.prompt_tokens if chunk.usage else 0,  # 初始化为 0  
                        'complete_tokens': chunk.usage.completion_tokens if chunk.usage else 0,  # 初始化为 0  
                        'total_tokens': chunk.usage.total_tokens if chunk.usage else 0,  # 初始化为 0  
                        'error': None  
                    })  
        except Exception as e:  
            logger.error(f"智谱API流式调用失败: {e}", exc_info=True)  
            q.put({  
                'response': None,  
                'content': "",  
                'prompt_tokens': 0,  
                'complete_tokens': 0,  
                'total_tokens': 0,  
                'error': str(e)  
            })  
        finally:  
            q.put(None)  
    try:  
        # 创建线程  
        thread = threading.Thread(target=fetch_data, args=(q, request_params))  
        thread.start()  
  
        while True:  
            content = await asyncio.to_thread(q.get)  # 从队列中获取数据  
            if content is None:  # 使用 None 作为结束信号  
                break  
            yield content  
  
        # 关闭线程  
        thread.join()  
    except Exception as e:  
        # 记录错误日志  
        logger.error(f"智谱API流式调用失败: {e}", exc_info=True)  
        # 返回错误信息  
        yield {  
            'response': None,  
            'content': "",  
            'prompt_tokens': 0,  
            'complete_tokens': 0,  
            'total_tokens': 0,  
            'error': str(e)  
        }
```

- 方案二: httpx-sse

```python
def generate_token(apikey: str, exp_seconds: int):  
    try:  
        id, secret = apikey.split(".")  
    except Exception as e:  
        raise Exception("invalid apikey", e)  
  
    payload = {  
        "api_key": id,  
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,  
        "timestamp": int(round(time.time() * 1000)),  
    }  
  
    return jwt.encode(  
        payload,  
        secret,  
        algorithm="HS256",  
        headers={"alg": "HS256", "sign_type": "SIGN"},  
    )  
  
from httpx_sse import aconnect_sse  
async def async_get_zhipuai_answer_stream(  
        user_id: str,  
        message: list[dict[str, str]],  
        keep_stable: bool = True,  
        llm_api_key: str = "GET-API-KEY-FROM-SITE",  
        llm_model_name: str = "glm-4-plus",  
) -> Generator[ZhipuAIResponse, None, None]:  
    """  
    使用智谱AI的流式输出方法获取答案。  
  
    参数:  
    - user_id: 用户ID，用于标识用户。  
    - message: 消息列表，包含用户与AI的对话历史。  
    - keep_stable: 是否保持输出稳定，默认为True。  
    - llm_api_key: AI模型的API密钥，默认为"GET-API-KEY-FROM-SITE"。  
    - llm_model_name: AI模型名称，默认为"glm-4-plus"。  
  
    返回:  
    - 一个生成器，用于流式输出AI的回答。  
    """    # 生成请求头  
    headers = {  
        "Authorization": generate_token(llm_api_key, 600000),  
        "Content-Type": "application/json"  
    } #token 十分钟过期  
    # 生成请求 ID  
    request_id = get_request_uuid(user_id)  
    # 准备请求参数  
    request_params = _get_common_request_params(  
        user_id=user_id,  
        request_id=request_id,  
        message=message,  
        keep_stable=keep_stable,  
        llm_model_name=llm_model_name,  
        stream=True  
    )  
    # 创建智谱 AI 客户端  
    async with httpx.AsyncClient() as client: #修改为异步调用  
        try:  
            # stream = await client.post("https://open.bigmodel.cn/api/paas/v4/chat/completions", data = json.dumps(request_params), headers = headers, timeout = httpx.Timeout(timeout = 300.0, connect = 8.0))  
            async with aconnect_sse(client=client, method="post",  
                                    url="https://open.bigmodel.cn/api/paas/v4/chat/completions",  
                                    data=json.dumps(request_params), headers=headers,  
                                    timeout=httpx.Timeout(timeout=300.0, connect=8.0)) as sse:  
                # 用于收集流式返回的消息  
                collected_messages = []  
                async for line in sse.aiter_sse():  
                    value = line.data  
                    if not value or "choices" not in value:  
                        continue  
                    chunk = json.loads(value)  
  
                    delta_content = chunk["choices"][0]["delta"]["content"]  
                    if delta_content:  
                        collected_messages.append(delta_content)  
                    yield {  
                        'response': chunk,  
                        'content': delta_content,  # 输出单次留结果，如果要输出所有连续结果，"".join(collected_messages),  
                        'prompt_tokens': chunk["usage"].get("prompt_tokens") if chunk.get("usage") else 0,  # 初始化为 0  
                        'complete_tokens': chunk["usage"].get("completion_tokens") if chunk.get("usage") else 0,  # 初始化为 0  
                        'total_tokens': chunk["usage"].get("total_tokens") if chunk.get("usage") else 0,  # 初始化为 0  
                        'error': None  
                    }  
  
        except Exception as e:  
            # 记录错误日志  
            logger.error(f"智谱API流式调用失败: {e}", exc_info=True)  
            # 返回错误信息  
            yield {  
                'response': None,  
                'content': "",  
                'prompt_tokens': 0,  
                'complete_tokens': 0,  
                'total_tokens': 0,  
                'error': str(e)  
            }
```

## 4. 参考资料

- [httpx-sse](https://pypi.org/project/httpx-sse/)
- [psycopg](https://www.psycopg.org/psycopg3/docs/advanced/pool.html)
