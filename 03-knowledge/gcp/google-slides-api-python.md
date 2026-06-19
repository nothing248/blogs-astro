---
title: "GoogleSlidesAPI开发"
filename: google-slides-api-python
summary: Google Slides API 的 Python 开发与集成指南。详述了幻灯片的核心概念与原生 API，重点给用了批量交互的封装代码，涵盖元素复制/删除、占位符替换（解决 OSS 下载模式导致的 404 错误）、添加超链接以及修改文字颜色、边框和背景的实现。最后指出了导出为 PPTX 时图表保留的局限性与规避策略。
tags:
  - google-slides-api
  - python-sdk
  - batch-update
  - placeholders
aliases:
  - GoogleSlidesAPI开发
  - 谷歌幻灯片API
  - Python生成PPT
status: completed
date created: 星期五, 十二月 26日 2025, 7:08:04 晚上
date modified: 星期二, 六月 16日 2026, 6:24:22 晚上
---

<!-- toc -->

## 1. 简介

Google Slides 是 Google 提供的在线演示文稿程序，可以通过 API 动态生成和修改文档。

## 2. 概念

- **presentation**：PPT 演示文稿文档。
- **slide**：代表每一页幻灯片。
- **notesMaster**：备注页面信息。
- **layouts**：幻灯片布局模板。
- **masters**：母版信息。

## 3. API 使用方式

### 3.1. 原生 API

- **创建文档**

```python
response = self.service.presentations().create(body=body).execute()
```

> [!NOTE]
> 该接口只能创建空白文档，除 `presentationId` 外，传入的其他初始化参数都会被忽略。

- **更改文档**

```python
# requests 代表请求操作列表
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

> [!WARNING]
> `requests` 列表中的每个 request 字典只能包含一个对应的底层操作类型对象。

- **获取文档元数据**

```python
response = self.service.presentations().get(presentationId=file_id).execute()
```

- **获取指定 slide**

```python
response = self.service.presentations().pages().get(
    presentationId=file_id, 
    pageObjectId=page_id
).execute()
```

> [!WARNING]
> 该方式仅能获取页面本身信息，页面内部包含的具体子元素（如 Shapes、Images）无法通过此接口展开。

### 3.2. 封装 API

- **复制对象**

```python
copy_requests.append({
    "duplicateObject": {
        "objectId": self.slide_id_map[slide_template],
        "objectIds": item["slide_map"]
    }
})
```

> [!NOTE]
> `objectIds` 参数用于指定新生成对象与旧对象之间的 ID 映射关系，支持复制 slide 或页面级独立元素。

- **更新 slide 排序位置**

```python
position_requests.append({
    "updateSlidesPosition": {
        "slideObjectIds": [slide_template],
        "insertionIndex": int(index)
    }
})
```

- **删除对象**

```python
remove_requests.append({
    "deleteObject": {
        "objectId": item,
    }
})
```

- **替换文本占位符**  

```python
requests = []
for item in req:
    requests.append({
        'replaceAllText': {
            'containsText': {
                'text': item["placeholder"],
                'matchCase': True
            },
            "pageObjectIds": item["objectIds"],
            'replaceText': item["replaceText"]
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

> [!TIP]
> 此方法不仅可以替换文本框中的文字，还可以替换表格内的文本。占位符格式无硬性要求，建议使用 `{{placeholder}}` 格式以方便检索。

- **替换图片**

```python
requests = []
for item in req:
    requests.append({
        'replaceImage': {
            'imageReplaceMethod': item["replaceMethod"] if "replaceMethod" in item else "CENTER_INSIDE",  # 还支持 CENTER_CROP
            "imageObjectId": item["imageId"],
            'url': item["url"]
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

> [!WARNING]
> 替换图片时，图片源 URL 必须为直接预览模式（HTTP 响应头 `Content-Disposition` 为 `inline`），而不能是强行下载模式（常见于阿里云 OSS 等默认配置），否则 API 加载可能会报 404 无权限错误。

- **将文本框替换为图片**

```python
requests = []
for item in req:
    requests.append({
        "replaceAllShapesWithImage": {
            'containsText': {
                 'text': item["placeholder"],
                 'matchCase': True
             },
            "imageUrl": item["url"],
            "pageObjectIds": item["objectIds"],
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

> [!WARNING]
> 该操作只能替换标准的文字图形（Shape），不支持直接替换表格（Table）单元格内部的文本。

- **文本框添加超链接**

```python
requests = []
for item in req:
    requests.append({
        "updateTextStyle": {
            "objectId": item["objectId"],
            "textRange": {
                "startIndex": item["start_index"],
                "endIndex": item["end_index"],
                "type": "FIXED_RANGE"
            },
            "style": {
                "link": {
                    "pageObjectId": item['pageObjectId']
                }
            },
            "fields": "link",
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

- **表格单元格文本添加超链接**

```python
requests = []
for item in req:
    requests.append({
        "updateTextStyle": {
            "objectId": item["objectId"],
            "cellLocation": {
                "rowIndex": item["row_index"],
                "columnIndex": item["column_index"],
            },
            "style": {
                "link": {
                    "pageObjectId": item['pageObjectId']
                }
            },
            "fields": "link",
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

- **修改文本框内文本颜色**

```python
requests = []
for item in req:
    stage = {
        "updateTextStyle": {
            "objectId": item["objectId"],
            "style": {
                "foregroundColor": {
                    "opaqueColor": {
                        "themeColor": item["color"]
                    }
                }
            },
            "fields": "foregroundColor",
        }
    }
    if "start_index" in item:
        stage["updateTextStyle"]["textRange"] = {
            "startIndex": item["start_index"],
            "endIndex": item["end_index"],
            "type": "FIXED_RANGE"
        }
    requests.append(stage)
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

> [!TIP]
> 如果文本框内部文字的 Index 不固定，建议先通过空格填充来统一排版与 Index。颜色支持主题色与 RGB 两种方式，推荐使用主题色进行统一设计管理。

- **修改表格单元格内文本颜色**

```python
requests = []
for item in req:
    requests.append({
        "updateTextStyle": {
            "objectId": item["objectId"],
            "cellLocation": {
                "rowIndex": item["row_index"],
                "columnIndex": item["column_index"],
            },
            "style": {
                "foregroundColor": {
                    "opaqueColor": {
                        "themeColor": item["color"]
                    }
                }
            },
            "fields": "foregroundColor",
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

- **修改图形边框颜色**

```python
requests = []
for item in req:
    requests.append({
        "updateShapeProperties": {
            "objectId": item["objectId"],
            "shapeProperties": {
                "outline": {
                    "outlineFill": {
                        "solidFill": {
                            "color": {
                                "themeColor": item["color"]
                            }
                        }
                    }
                }
            },
            "fields": "outline.outlineFill.solidFill.color",
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

- **修改背景填充颜色**

```python
requests = []
for item in req:
    requests.append({
        "updateShapeProperties": {
            "objectId": item["objectId"],
            "shapeProperties": {
                "shapeBackgroundFill": {
                    "solidFill": {
                        "color": {
                            "themeColor": item["color"]
                        }
                    }
                }
            },
            "fields": "shapeBackgroundFill.solidFill.color",
        }
    })
response = self.service.presentations().batchUpdate(
    body={"requests": requests}, 
    presentationId=presentation_id
).execute()
```

---

## 4. 注意

- 新创建或复制的文档默认存储在 Google Drive 的根目录。如果需要整理结构，请使用 Google Drive API 进行目录更新。
- 在发送 `update` 请求时，可以指定 `revision_id` 进行乐观锁冲突控制。若不指定，系统默认基于最新版本合并提交。

---

## 5. 拓展信息

### 5.1. API 限制

- 仅存在调用频率限制，具体细节请 [参考频率限制官方文档](https://developers.google.com/slides/api/limits?hl=zh-cn)。

### 5.2. 图表操作限制

- 插入的 Slide 图表底层均依赖 Google Sheet 数据源，并在 Slide 中以静态图片形式渲染呈现。如果 Google Sheet 源数据更新，必须主动调用刷新接口重新渲染图片。
- 支持通过 API 替换特定 Shape 为指定 Google Sheet 的 Chart。
- **缺点**：将 Slide 导出并下载为 PPTX 格式时，图表会直接固化为静态图片格式，在本地 PowerPoint 中无法双击编辑数据。

> [!TIP]
> 如果直接在 Google Drive 中上传原生 PPTX 格式文件，可以保持图表的在线编辑与数据联动，但该模式将不支持使用 Google Slides API 进行程序化操纵修改。

### 5.3. 图片 URL 响应模式

- **预览模式**：`Content-Disposition: inline`，浏览器或 API 直接解析渲染。
- **下载模式**：`Content-Disposition: attachment`，浏览器打开直接下载。

---

## 6. 参考资料

- [官方文档](https://developers.google.com/slides/api/reference/rest?hl=zh-cn)
- [API 文档](https://googleapis.github.io/google-api-python-client/docs/dyn/slides_v1.html)
