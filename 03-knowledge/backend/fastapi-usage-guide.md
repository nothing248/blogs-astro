---
title: "FastAPI教程"
filename: fastapi-usage-guide
summary: 介绍基于 OpenAPI 规范的高性能 Python API 框架 FastAPI。详细涵盖路径与查询参数的声明、请求体与 Pydantic 数据校验、自定义验证器、中间件、静态文件挂载、后台任务管理、多层级依赖注入以及 API 接口元数据管理。同时提供了基于 jose 库的 JWT 授权管理完整代码与自定义错误异常处理机制。
tags:
  - FastAPI
  - 依赖注入
  - 数据校验
  - JWT认证
  - API框架
aliases:
  - FastAPI教程
  - FastAPI鉴权机制
  - FastAPI依赖注入
status: completed
date created: 星期一, 十二月 10日 2025, 9:59:20 上午
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 简介

一个 python 的 API 框架

- 基于 OpenAPI 规范
- 自动生成文档
- 支持插件

## 2. 安装

```shell
pip install fastapi
```

## 3. 使用

### 3.1. 基础用法

- 编写代码

```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

- 运行服务

```shell
uvicorn main:app --reload
```

### 3.2. 参数

- 路径参数

```python
from enum import Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
@app.get("/items/{item_id}")
async def read_item(item_id: ModelName):
    return {"item_id": item_id}
```

> 1、如果指定类型、会自行的进行类型转化与类型校验
>
> 2、顺序相关
>
> 3、通过枚举来进行预设值
>
> 4、{item_id: path}可以匹配完整路径，否则只匹配指定级别路径

- 查询参数

```python
from typing import Union,List
@app.get("/items/")
async def read_item(*,skip: Union[List[int],None] = Query(default=None), limit: int):
    return fake_items_db[skip : skip + limit]
```

> 默认值设置为 None 为可选参数
>
> 多种类型可以使用 Union 进行指定
>
> 多个查询参数，默认值设置只能使用 Query 进行设置
>
> 使用*去除非默认在默认值后面定义的错误

- 请求体参数(body)

```python
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description:Union[str,None] = None
    price: list[float] = []
    tax: set[str] = set()
    images: Union[list[Image],None] = None
@app.post("/body_param",response_model=Item)
async def body_param(item:list[Item],importtance:Annotated[int,Body()]):
    return item
```

> 但请求参数使用 Body()进行声明
>
> 单请求参数使用 Body(embed = True)开启嵌套
>
> 支持嵌套
>
> 支持响应参数(可以排除默认、或者空值参数等)

- Cookie 参数

```python
from fastapi import Cookie
@app.get("/cookie_param")
async def cookie_param(token:Annotated[Union[str,None],Cookie()]=None):
    return {"message": f"cookie_param:{token}"}
```

- Header 参数

```python
from fastapi import Header
@app.get("/header_param")
async def header_param(token:Annotated[Union[str,None],Header()]=None):
    return {"message": f"header_param:{token}"}
```

- 表单参数

```python
from fastapi import Form
@app.post("/form_param/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

- 文件参数

```python
from fastapi import File, UploadFile
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

- 数据校验

```python
class Item(BaseModel):
    name: str
    description: Union[str,None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float,None] = None
@app.get("/param_validate/{path_param}")
async def param_validate(*,path_param:Union[int,None]=Path(ge=1),q:Union[str,None]=Query(default=None,min_length=2,title="测试元数据"),item:Annotated[Item,Body(embed=True)]):
    return {'message': f"path_param:{path_param} param_validate:{q}"}
```

> Query 适用于字符串 max_length, min_length, pattern
>
> Path 适用于数字 gt ge lt le
>
> Field 进行请求体检验

- 自定义数据校验

```python
from pydantic import BaseModel,validator
class Item(BaseModel):
    dimensions:str
    @validator("dimensions")
    def validate_dimensions_length(cls,dimensions):
        if(len(dimensions)>0):
            raise ValueError("Dimensions count cannot exceed 9")
        return dimensions
```

### 3.3. 路由管理

...

### 3.4. 中间件

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 3.5. 静态文件

```python
from fastapi.staticfiles import StaticFiles
# 挂载一个 静态文件应用
app.mount("/static",StaticFiles(directory="static"),name="static")
```

### 3.6. 数据库

...

### 3.7. 后台任务

```python
from typing import Union

from fastapi import BackgroundTasks, Depends, FastAPI
from typing_extensions import Annotated

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Union[str, None] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

```

### 3.8. 依赖注入

根据请求参数先运行依赖，分为全局依赖、路径依赖、参数依赖三种。并且支持层级依赖

```python
from fastapi import Cookie,Depends
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)]) # 全局依赖
def query_extractor(q: Union[str, None] = None):
    return q
def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q
@app.get("/items/",dependencies=[Depends(verify_token), Depends(verify_key)]) #路径依赖, 不返回结果
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
```

### 3.9. 元数据管理

提供更加友好的接口文档

```python
class Item(BaseModel): #Pydantic 层级
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
class Item(BaseModel): #Field 层级
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
async def update_item( #body 层级
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
```

### 3.10. 错误处理

- 返回错误

```python
from fastapi import HTTPException
items = {"foo": "The Foo Wrestlers"}
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

- 自定义异常处理

```python
from fastapi import Request
from fastapi.responses import JSONResponse
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

> RequestValidationError(请求验证异常)、StarletteHTTPException

### 3.11. 授权管理

```python
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

```

## 4. 部署

...

## 5. 拓展信息

- 建议 controller 与 Service 进行分开发管理

## 6. 参考资料

- [官方链接](https://fastapi.tiangolo.com/)
