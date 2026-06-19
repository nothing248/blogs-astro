---
title: "GoogleDriveAPI开发"
filename: google-drive-api-python
summary: Google Drive API 客户端开发指南。面向 Python SDK 详述了文件及文件夹的创建、复制、删除、移动和搜索操作。重点分析了 fields 过滤机制以及文件导出的两种实现方式：针对 10MB 以下文件使用 export_media 方法，而针对 10MB 以上的大文件，则提供了通过拼接 access_token 的 HTTP URL 绕过大小限制的原生下载方案。
tags:
  - google-drive-api
  - python-sdk
  - file-download
  - file-export
aliases:
  - GoogleDriveAPI开发
  - 谷歌云端硬盘API
  - Python操作GoogleDrive
status: completed
date created: 星期一, 九月 22日 2025, 5:12:48 下午
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

## 1. 简介

Google Drive 是一款 Google 提供的在线文件存储与共享服务。

## 2. API 使用方式

- **创建文件**

```python
from googleapiclient.http import MediaFileUpload

def create_file(self, name=None, file_path=None, file_metadata=None, fields=None):
    """
    创建文件
    """
    media = MediaFileUpload(file_path, mimetype='image/jpeg', resumable=True)
    file = self.service.files().create(body=file_metadata, media_body=media, fields=fields).execute()
    return file
```

- **创建文件夹**

```python
def create_dir(self, name=None, fields=None):
    """
    创建文件夹
    """
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = self.service.files().create(body=file_metadata, fields=fields).execute()
    return file
```

- **复制文件**

```python
def copy_file(self, file_id=None, fields=None):
    """
    复制文件
    """
    file = self.service.files().copy(fileId=file_id, fields=fields).execute()
    return file
```

- **删除文件**

```python
def remove_file(self, file_id=None, fields=None):
    """
    删除文件（注意：此操作是彻底删除，而非移动到回收站）
    """
    file = self.service.files().delete(fileId=file_id, fields=fields).execute()
    return file
```

- **获取文件**

```python
def get_file(self, file_id=None, fields=None):
    """
    获取文件元数据
    """
    file = self.service.files().get(fileId=file_id, fields=fields).execute()
    return file
```

- **查询文件**

```python
def search_file(self, query=None, fields=None):
    """
    查询文件，fields 示例: "files(parents,id,name)"
    """
    files = []
    page_token = None
    while True:
        response = self.service.files().list(q=query, fields=fields, pageToken=page_token).execute()
        for file in response.get('files', []):
            print(f'Found file: {file.get("name")}, {file.get("id")}, {file.get("parents")}')
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files
```

> [!NOTE]
> 查询字符串的具体用法可以参考 [官方查询条件定义](https://developers.google.com/drive/api/guides/ref-search-terms?hl=zh-cn)。

- **下载文件**

```python
import urllib.request

slide_url = f"https://docs.google.com/presentation/d/{file_id}"
url = f"https://docs.google.com/presentation/d/{file_id}/export/pptx?access_token={self.credentials.token}"
urllib.request.urlretrieve(url, save_path)

return slide_url
```

> [!WARNING]
> 该下载 URL 中 `access_token` 参数不能为空，否则会报错。

- **更新文件**

```python
def update_file(self, file_id=None, file_metadata=None, fields=None):
    """
    更新文件元数据
    """
    file = self.service.files().update(fileId=file_id, body=file_metadata, fields=fields).execute()
    return file
```

- **移动文件**

```python
def move_file(self, file_id, folder_id, old_folder_id, fields=None):
    """
    移动文件（实质是通过修改父级目录实现）
    """
    file = self.service.files().update(
        fileId=file_id, 
        addParents=folder_id,
        removeParents=old_folder_id,
        fields=fields
    ).execute()
    return file.get('id', None), file.get('parents', None)
```

- **导出文件**

```python
import io
from googleapiclient.http import MediaIoBaseDownload

def export_file(self, file_id, mime_type):
    """
    导出文档内容
    """
    request = self.service.files().export_media(fileId=file_id, mimeType=mime_type)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f'Download {int(status.progress() * 100)}%.')

    return file.getvalue()
```

> [!WARNING]
> 官方 `export_media` 方法在导出 Google 文档时默认有 10MB 的大小限制。如果文件大小超出此限制，请改用上文“下载文件”部分中的直接 URL 拼接下载方案。

---

## 3. 注意

- **返回文件的特定字段**：可以通过 `fields` 参数指定返回字段。
  - 默认返回 `id`, `name`, `mimeType`。
  - 语法：`,` 代表分割选择；`/` 表示嵌套字段；`*` 代表通配符；`()` 代表一组子选择器。具体可 [参考官方字段参数文档](https://developers.google.com/drive/api/guides/fields-parameter?hl=zh-cn)。

---

## 4. 限制

- 接口仅存在频率限制，详细可 [参考频率控制官方说明](https://developers.google.com/drive/api/guides/limits?hl=zh-cn)。

---

## 5. 参考资料

- [官方链接](https://developers.google.com/drive/api/guides/about-sdk?hl=zh-cn)
- [API 链接](https://googleapis.github.io/google-api-python-client/docs/dyn/drivelabels_v2.html)
- [支持的 MIME 类型](https://developers.google.com/drive/api/guides/mime-types?hl=zh-cn)
- [支持导出的 MIME 类型](https://developers.google.com/drive/api/guides/ref-export-formats?hl=zh-cn)
