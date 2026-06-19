---
status: completed
filename: gcp-api-authentication-python-sdk
title: "GCP 鉴权"
summary: 本笔记记录了在 Python 环境下调用 Google Cloud Platform (GCP) 各种数据 API 的基础授权流程。详细区分了基于浏览器弹窗的 OAuth 2.0 用户端授权（支持 Token 缓存与自动刷新）与基于服务账号密钥文件 (Service Account Key) 的服务端鉴权。并列举了使用 Google API Python Client (Discovery) 及现代 Cloud Client Libraries 连接 Search Console、GA4、BigQuery 等核心数据服务的初始化代码片段，是开发 GCP 数据通道的认证脚手架字典。
aliases: [GCP 鉴权, Google API Python 客户端, 服务账号认证]
tags: [GCP, 鉴权, OAuth2, Service Account, Python, BigQuery, GA4, 后端开发]
date created: 星期一, 五月 19日 2025, 2:05:18 下午
date modified: 星期四, 六月 18日 2026, 10:45:00 晚上
---

<!-- toc -->

## 1. 鉴权模式概览

调用 GCP 接口需先获取用户凭证 (Credentials)。根据使用场景，主要分为 **客户端授权 (OAuth2.0)** 和 **服务端系统级授权 (Service Account)**。

---

## 2. 客户端终端鉴权 (OAuth 2.0)

适用于需要代表具体用户操作其个人数据的场景。代码包含自动换取和持久化缓存机制：

```python
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_oauth_credentials(client_account_path, client_accountbat_path, scope):
    credentials = None
    # 1. 尝试从本地缓存加载已授权的 Token
    if os.path.exists(client_accountbat_path):
        credentials = Credentials.from_authorized_user_file(client_accountbat_path)
    
    # 2. 如果无凭证或凭证已失效
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            # 刷新过期 Token
            credentials.refresh(Request())
        else:
            # 弹出浏览器走 Oauth2 登录授权流
            flow = InstalledAppFlow.from_client_secrets_file(client_account_path, scope)
            credentials = flow.run_local_server(port=0)
            
        # 3. 将新获取的有效 Token 写入本地缓存以备下次使用
        with open(client_accountbat_path, 'w') as token:
            token.write(credentials.to_json())
            
    return credentials
```

---

## 3. 服务端无头鉴权 (Service Account)

适用于后端系统直接拉取或推送数据，无需人工干预。

> [!warning] Token 刷新注意
> 默认通过文件获取的凭证对象并无立即向 Google 请求底层 Token。在传递给某些旧版 SDK 前，可能需要手动执行 `refresh`。

```python
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def get_service_account_credentials(service_account_path, scopes):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_path, 
        scopes=scopes
    )
    # 手动触发刷新以获取实际请求用的 Token
    auth_request = Request()
    credentials.refresh(auth_request)
    return credentials
```

---

## 4. Google 各核心 API 客户端初始化速查

获取到 `credentials` 后，可注入并实例化各类服务的客户端对象。

### 4.1. A. 使用传统的 Discovery 客户端

适用于部分较旧的 API：

```python
from googleapiclient.discovery import build

# Google Search Console
client_gsc = build("searchconsole", "v1", credentials=credentials)
# Google Analytics (UA - v3)
client_ua = build("analytics", "v3", credentials=credentials)
# Google Analytics Reporting (v4)
client_ga_rep = build("analyticsreporting", "v4", credentials=credentials)
# Google Slides & Drive
client_slides = build("slides", "v1", credentials=credentials)
client_drive = build("drive", "v3", credentials=credentials)
```

### 4.2. B. 使用现代 Cloud Client Libraries

适用于 GCP 的核心云服务：

```python
# Google Analytics 4 (GA4) Admin API
from google.analytics.admin import AnalyticsAdminServiceClient
client_ga4_admin = AnalyticsAdminServiceClient(credentials=credentials)

# Google Analytics 4 (GA4) Data API
from google.analytics.data_v1beta import BetaAnalyticsDataClient
client_ga4_data = BetaAnalyticsDataClient(credentials=credentials)

# Google BigQuery
from google.cloud import bigquery
client_bq = bigquery.Client(credentials=credentials, project="your_project_id", location="US")

# Google Cloud Storage (GCS)
from google.cloud import storage
client_gcs = storage.Client(credentials=credentials, project="your_project_id")
```
