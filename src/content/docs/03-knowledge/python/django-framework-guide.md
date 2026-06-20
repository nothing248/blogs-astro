---
title: "Django基础教程"
filename: django-framework-guide
description: Django 框架全栈开发与 REST API 构建指南。详述了应用初始化、URL 注册、模版自定义过滤器和 ORM 增删改查。重点剖析了 Django REST Framework (DRF) 的 Serializer 字段自定义方法及 APIView/mixins 视图构建。同时补充了 drf-spectacular 生成 OpenAPI 文档的装饰器配置、django-admin 自定义指令编写及 populate 重入异常排查。
tags:
  - django
  - django-rest-framework
  - orm-migration
  - openapi-spec
  - custom-commands
aliases:
  - Django基础教程
  - DRF接口开发
  - Django自定义指令
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:22 上午
date modified: 星期二, 六月 16日 2026, 6:24:20 晚上
---

<!-- toc -->

## 1. 简介

Django 是一款高级的 Python Web 框架，旨在快速开发安全且可维护的网站。

## 2. 安装

```shell
pip install Django
pip install djangorestframework
```

## 3. 基础使用

### 3.1. 创建项目

```shell
django-admin startproject django-demo
```

### 3.2. 创建 APP

```shell
django-admin startapp first_app
```

### 3.3. 运行服务

```shell
django-admin runserver
python manage.py runserver
```

### 3.4. 使用视图

每一个视图表现为一个 Python 函数，必须返回一个 `HttpResponse` 对象或抛出 `Http404` 异常。

- **创建视图**：

```python
# first_app/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

- **定义 URL**：

```python
# first_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

- **注册 URL**：

```python
# django_demo/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

### 3.5. 使用模板

- **定义设置**：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True, # 自动查找各应用下的 templates 目录
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- **定义模板**：

```html
<!-- first_app/templates/first_app/index.html -->
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

> [!NOTE]
> 因为 Django 模板加载器会选择其搜索路径中第一个匹配的模板，所以建议在 `templates` 目录下再建一个与应用同名的子目录以避免冲突。

- **自定义模板过滤器/标签**：

```python
import datetime
from django import template

register = template.Library()

@register.filter # 自定义过滤器
def custom_prefix(value, prefix):
    """
    自定义列表添加前缀过滤器
    """
    return [f"{prefix}{item}" for item in value]

@register.simple_tag # 自定义标签
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
```

> [!IMPORTANT]
>
> - 必须在当前应用的根目录下创建一个名为 `templatetags` 的 Python 包（包含 `__init__.py`）。
> - 自定义过滤器的参数最多支持 2 个。

- **在视图中调用模板**：

```python
# first_app/views.py
from django.template import loader
from django.http import HttpResponse
from .models import Question

def custom_template(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('first_app/index.html') # 加载模板
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

### 3.6. 使用数据库

> [!WARNING]
> Django 3.2 之后的版本要求 MySQL 的版本不低于 8.0。

- **配置文件**：

```python
# django_demo/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_demo',
        'USER': 'root',
        'PASSWORD': 'example',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

- **注册应用**：

```python
# django_demo/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'first_app.apps.FirstAppConfig'
]
```

- **创建模型**：

```python
# first_app/models.py
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

- **激活并生成迁移文件**：

```shell
python manage.py makemigrations first_app
```

- **执行数据库迁移**：

```shell
# 查看执行迁移的 SQL 语句
python manage.py sqlmigrate first_app 0001
# 执行真实迁移
python manage.py migrate
```

- **增、删、改、查操作**：

```python
from django.utils import timezone
from first_app.models import Choice, Question

# 增
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save() # 写入数据库

# 查
Question.objects.all() # 查询所有记录
Question.objects.get(pub_date__year=timezone.now().year) # 根据时间字段查询单个记录
Question.objects.filter(question_text__startswith='What') # 根据前缀条件过滤查询
Question.objects.get(pk=1) # 主键查询
q.choice_set.all() # 关联外键查询

# 改
q.question_text = "What's up?"
q.save()

# 删
q.delete()
```

### 3.7. 应用调试

使用 Django 内置的 Shell 运行环境进行交互式调试：

```shell
python manage.py shell
```

### 3.8. 数据库迁移

对于全新或干净的数据库进行迁移，需要确保：

1. 本地生成的所有表结构能正确执行。
2. 原库中 `django_migrations` 表中的历史应用迁移记录也应同步导入。

### 3.9. 管理后台界面

- **创建超级管理员账户**：

```shell
python manage.py createsuperuser
```

> 本地启动后访问：`http://127.0.0.1:8000/admin`。

- **将应用模型注册到管理页面**：

```python
# first_app/admin.py
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

---

## 4. 调试与高级应用

### 4.1. SimpleUI 后台美化

- **安装**：

```shell
pip install django-simpleui
```

### 4.2. Django REST Framework (DRF)

- **安装**：

```shell
pip install djangorestframework
```

- **全局配置**：

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10
}
```

- **数据序列化配置 (Serializers)**：

```python
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    answer = serializers.SerializerMethodField()
    
    def __init__(self, *args, custom_record_id=None, **kwargs):
        """支持动态传参初始化"""
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.custom_record_id = custom_record_id
        
    def get_answer(self, obj): 
        """使用自定义 SerializerMethodField 进行个性化序列化"""
        raws = RecordAndAnswer.objects.filter(question=obj.id, record=self.custom_record_id)
        ids = []
        instances = []
        for item in raws:
            if item.answer_id not in ids:
                instances.append(item.answer)
                ids.append(item.answer_id)
        return RecordAnswerSerializer(instances, many=True).data

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'answer')

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
```

- **视图配置 (Views)**：

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# 函数式 API 视图
@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    列出所有代码片段，或者创建一个新的代码片段。
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 类视图 (APIView)
class SnippetList(APIView): 
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 结合 Mixins 的通用视图
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

- **序列化应用方式**：

```python
# 序列化单条数据并转为 JSON 字节流
serializer = SnippetSerializer(snippet)
content = JSONRenderer().render(serializer.data)

# 反序列化 JSON 字节流并校验数据
import io
from rest_framework.parsers import JSONParser
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
serializer = SnippetSerializer(data=data)
```

### 4.3. Drf-spectacular 自动接口文档生成

- **在类视图中声明**：

```python
from rest_framework.views import APIView
from .serializers import CaptchaResSerializer

class CaptchaAPI(APIView):
    serializer_class = CaptchaResSerializer # 明确指定序列化器供文档生成器解析
    def get(self, request):
        pass
```

- **在函数视图中声明**：

```python
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

@extend_schema(responses={200: CaptchaResSerializer, 404: CaptchaResSerializer}, request=CaptchaResSerializer)
@api_view(['POST'])
def test_view(request):
    """
    测试视图的详细描述说明。
    """
    return Response({"message": "Hello, world!"})
```

- **自定义接口参数声明**：

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

@extend_schema(
    parameters=[
        OpenApiParameter(name='artist', description='Filter by artist', required=False, type=str),
        OpenApiParameter(
            name='release',
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            description='Filter by release date',
        ),
    ],
    responses={200: CaptchaResSerializer, 404: CaptchaResSerializer},
    request=CaptchaResSerializer,
    description='更详细的 API 覆盖描述。'
)
def post(request):
    pass
```

- **在 Serializer 级自定义字段展示**：

```python
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    exclude_fields=('image_url',), # 明确指定生成接口文档时需隐藏的内部字段
    examples = [
         OpenApiExample(
            'Valid example 1',
            summary='字段示例说明',
            description='更长的主体功能介绍',
            value={
                'songs': {'top10': True},
                'single': {'top10': True}
            },
            request_only=True,
            response_only=True,
        ),
    ]
)
class CaptchaResSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    key = serializers.CharField()
    image_url = serializers.CharField()
    users = UserSerializer(read_only=True, many=True)
    test = serializers.SerializerMethodField() # 注意：只读的 Method 字段默认不显示在 Request 文档中
    
    def get_test(self):
        return "test_field"
```

### 4.4. 注册自定义 django-admin 命令行

- **标准应用命令目录结构**：

```text
polls/
    __init__.py
    models.py
    management/
        __init__.py
        commands/
            __init__.py
            _private.py
            closepoll.py  # 自定义运行脚本名称
    tests.py
    views.py
```

- **编写的 `closepoll.py` 脚本内容**：

```python
from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll

class Command(BaseCommand):
    help = "关闭指定投票的投票功能"

    def add_arguments(self, parser):
        # 声明命令行参数
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for poll_id in options["poll_ids"]:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
            ) 
```

### 4.5. Django-celery-beat 异步定时任务

- **安装**：

```shell
pip install django-celery-beat
```

---

## 5. 拓展与常见错误排查

### 5.1. `populate() Isn't Reentrant` 异常解决

当在初始化过程中多次不当重载 apps 注册表时，可能会触发此并发重入机制异常。

- **修复方案**：
  定位到 Python 环境路径下的 `django/apps/registry.py`，将引发该错误的行替代并修复为：

```python
# 替换原 raise RuntimeError("populate() isn't reentrant") 为
self.app_configs = {}
```

---

## 6. 参考资料

- [Django 官方网站](https://www.djangoproject.com/)
- [Django Settings DATABASES 官方定义](https://docs.djangoproject.com/zh-hans/4.1/ref/settings/#std-setting-DATABASES)
- [Django REST Framework 官方中文翻译文档](https://q1mi.github.io/Django-REST-framework-documentation/)
