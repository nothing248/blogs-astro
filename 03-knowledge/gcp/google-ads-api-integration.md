---
title: "GoogleAdsAPI使用指南"
filename: google-ads-api-integration
description: Google Ads API 解决方案指南。详述了客户端库安装，并针对 OAuth2.0 凭证和 Service Account（基于 Google Workspace 网域授权）两种授权机制提供了配置步骤与 Python 初始化代码。重点展示了利用 GoogleAdsService 执行广告活动检索的具体实例，并总结了经理/客户账户分类、Developer Token 绑定限制与调试经验。
tags:
  - google-ads-api
  - oauth2
  - service-account
  - google-workspace
  - python-sdk
aliases:
  - GoogleAdsAPI使用指南
  - AdsDeveloperToken配置
  - GoogleAdsService调用
status: completed
date created: 星期一, 五月 19日 2025, 2:05:20 下午
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

## 1. 简介

Google Ads 是 Google 的一个广告投放工具，本指南提供 Google Ads API 的使用与集成解决方案。

## 2. 安装

```shell
pip install google-ads
```

## 3. 授权

### 3.1. OAuth2.0

- 在 GCP 项目中创建 OAuth2.0 Client 授权信息（可以使用 desktop 类型）：  
  ![](http://qiniu.sxyxy.top/20231204143148.png?image=image)

- 在 Ads 经理账户（需要正式账户）中创建 Developer Token：  
  ![](http://qiniu.sxyxy.top/20231204143450.png?image=image)

  > [!WARNING]
  > 注意：
  > 1. 确定访问权限级别是否正确。
  > 2. 注册上面创的 GCP 是否已经与其他 Token 相关联、如果关联则请重新创建 GCP 项目。

- 获取对应的 Ads 账户 ID 信息：  
  ![](http://qiniu.sxyxy.top/20231204144001.png?image=image)  

  > 一般需获取 **Manager Account ID**、**Account ID**。

- 授权并且初始化客户端：

```python
import os
from google.ads.googleads.client import GoogleAdsClient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

client_account_path = "client_account.json"  # GCP 生成的授权文件
client_accountbat_path = "client_account.bat"  # 授权缓存路径
scope = ["https://www.googleapis.com/auth/adwords"]  # 授权范围

manager_account_id = ""  # 经理账户 ID
developer_token = ""  # Ads 生成的 developer token 信息

if os.path.exists(client_accountbat_path):
    credentials = Credentials.from_authorized_user_file(client_accountbat_path, scope)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_account_path, scope)
            credentials = flow.run_local_server(port=0)
            with open(client_accountbat_path, 'w') as token:
                token.write(credentials.to_json())
                
client = GoogleAdsClient(credentials=credentials, developer_token=developer_token, login_customer_id=manager_account_id)
```

> [!NOTE]
> 其中的 `manager_account_id` 可以与生成 Token 的 Manager Account 不一致。

- 授权效果展示：

  ![](http://qiniu.sxyxy.top/20231219113346.png?image=image)

### 3.2. Server Account

- 在 GCP 项目中创建 Server Account 授权信息：  
  ![](http://qiniu.sxyxy.top/20231204145219.png?image=image)

- 注册 Google Workspace：
  ![](http://qiniu.sxyxy.top/20231219160909.png?image=image)

- 取消 Workspace 服务订阅：
  ![](http://qiniu.sxyxy.top/20231219161313.png?image=image)

- 验证 Workspace 网域：
  ![](http://qiniu.sxyxy.top/20231219161506.png?image=image)

- Google Workspace 添加对应服务账户：  
  ![](http://qiniu.sxyxy.top/20231204145928.png?image=image)

  > [!IMPORTANT]
  > - 新增 server account 网域验证必须使用 Workspace 的 admin 账户。
  > - 但是获取对应 Email 的可以不是 admin 账户、只要同一个 workspace 账户即可。

- 将 Email 分配到对应的 Google Ads 账户：
  ![](http://qiniu.sxyxy.top/20231204153755.png?image=image)

- 在 Ads 经理账户（需要正式账户）中创建 Developer Token：  
  ![](http://qiniu.sxyxy.top/20231204143450.png?image=image)

  > [!WARNING]
  > 注意：
  > 1. 确定访问权限级别是否正确。
  > 2. 注册上面创的 GCP 是否已经与其他 Token 相关联、如果关联则请重新创建 GCP 项目。

- 获取对应的 Ads 账户 ID 信息：  
  ![](http://qiniu.sxyxy.top/20231204144001.png?image=image)

  > 一般需获取 **Manager Account ID**、**Account ID**。

- 授权并且初始化客户端：

```python
from google.ads.googleads.client import GoogleAdsClient

server_account_path = "server_account.json"  # GCP 生成的授权文件
scope = ["https://www.googleapis.com/auth/adwords"]  # 授权范围

manager_account_id = ""  # 经理账户 ID
developer_token = ""  # Ads 生成的 developer token 信息
workspace_email = ""

credentials = {
    "developer_token": developer_token, 
    "json_key_file_path": server_account_path,
    "impersonated_email": workspace_email,
    "login_customer_id": manager_account_id,
    "use_proto_plus": False
}
client = GoogleAdsClient.load_from_dict(credentials)
```

> [!NOTE]
> 其中的 `manager_account_id` 可以与生成 Token 的 Manager Account 不一致。

## 4. 使用

- 获取对应服务类型：

```python
ga_service = client.get_service("GoogleAdsService")
```

- 调取 API：

```python
account_id = ""  # ads 账户 ID
stream = ga_service.search_stream(customer_id=account_id, query="select campaign.name from campaign")
for batch in stream:
    for row in batch.results:
        print(
            f"Campaign with ID {row.campaign.id} and name "
            f'"{row.campaign.name}" was found.'
        )
```

> [!CAUTION]
> 如果发生 **DEVELOPER_TOKEN_PROHIBITED** 错误，则代表 GCP 授权项目与 Ads 的 developer token 不匹配，需要重新生成 GCP 项目并授权。

## 5. 拓展信息

- **账户分类**
  - **账户结构**
    - **经理账户**：可以创建多个客户账户；并且只有经理账户可以创建 Developer Token。
    - **客户账户**：用于真实的广告投放。
  - **账户类型**
    - **正式账户**：可以投放广告；并且 Developer Token 只有基础类型与标准类型可以调取该账户类型 API，测试类型不可以调取。
    - **测试账户**：不可以投放广告；并且 Developer Token 基础类型、标准类型和测试类型都可以调取该账户类型 API。
- **Developer Token**
  - **分类**
    - **测试**：只可以调取测试账户。
    - **基础**：可以调取所有类型账户，有额度限制。
    - **标准**：可以调取所有类型账户，没有额度限制。

    > [!NOTE]
    > 申请提升账户类型时需要填写表单；并且请注意 Token 有 **用途限制**。

  - **限制**
    - 每个 Token 会在第一个请求中与 GCP 授权项目（生成 OAuth2.0 或者 Server Account 的项目）进行绑定，并且该绑定是永久的。**如果重新生成了 Token，则该 GCP 必须重新创建（一个 Token 可以对应多个 GCP 项目）**。

## 6. 参考资料

- [官方链接](https://developers.google.com/google-ads/api/docs/start)
- [Ads Token 权限用途](https://developers.google.com/google-ads/api/docs/access-levels?hl=zh-cn#applying_for_basic_access)
- [Ads 状态码链接](https://developers.google.com/google-ads/api/docs/common-errors?hl=zh-cn#authorizationerror)
- [Ads API GitHub](https://github.com/googleads/google-ads-python/blob/main/examples/remarketing/add_customer_match_user_list.py)
- [Ads 目标客户创建](https://developers.google.com/google-ads/api/docs/remarketing/audience-segments/customer-match/get-started?hl=zh-cn#add-user)
