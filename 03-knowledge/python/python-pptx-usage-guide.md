---
title: "python-pptx使用手册"
filename: python-pptx-usage-guide
description: Python python-pptx 库操纵 PowerPoint 文档指南。系统解析了 Presentation、Slide、Shape 和 Run 的层级对象模型。针对文本框（清除填充、字号样式）、图片（Cm/Emu单位定位插入、批量删除防错乱）、表格单元格以及柱状/条形图表数据替换与颜色填充，提供了完整的 Python 封装类方法及避坑经验。
tags:
  - python-pptx
  - ppt-generation
  - automation
  - office-automation
aliases:
  - python-pptx使用手册
  - Python生成PPT图表
  - PPTX格式解析
status: completed
date created: 星期二, 二月 25日 2025, 3:23:52 下午
date modified: 星期二, 六月 16日 2026, 6:24:19 晚上
---

<!-- toc -->

## 1. 简介

`python-pptx` 是一个功能强大的 Python 库，用于程序化地创建和修改 Microsoft PowerPoint (.pptx) 演示文稿文件。

## 2. 概念

- **Presentation**：代表整个 PPTX 演示文稿文件。
- **slide**：代表每一页独立的幻灯片。
- **slide_master**：幻灯片母版。用于统一配置幻灯片基本结构，如页脚、Logo 标识和统一的背景样式等。
- **slide_layout**：预设的幻灯片页面版式布局。
- **shape**：幻灯片中的各种图形元素（如文本框、图片、图表或自定义形状）。
- **paragraph**：文本框内部的段落对象。
- **run**：段落内部具有相同字符格式的具体文本片段，可用于细粒度地设置字符级格式。

---

## 3. 常用操作

```python
from pptx import Presentation

prs = Presentation()            # 创建一个空白的演示文稿
prs = Presentation("test.pptx") # 打开一个已有的演示文稿
slide = prs.slides[0]           # 获取第一页幻灯片

slide_id = slide.slide_id 
slide_by_id = prs.slides.get_slide(slide_id)

shape = slide.shapes[0]         # 获取页面上的第一个图形元素
shape_type = shape.shape_type   # 获取该图形的类型枚举
shape_idx = slide.shapes.index(shape)
shape_elem = shape.element      # 获取底层的 XML 元素对象

shape_elem.getparent().remove(shape_elem) # 删除该图形元素

prs.save("test_result.pptx")    # 存储并保存到指定路径
```

### 3.1. 文本操作

```python
shape.has_text_frame                        # 判定图形是否包含文本框
text_frame = shape.text_frame               # 获取文本框对象
paragraph = text_frame.paragraphs[0]        # 获取文本框的第一个段落
paragraph.clear()                           # 清空段落中的所有文本
paragraph.text = "Hello World"              # 直接填充文本（会采用 PPTX 默认的字体格式）
paragraph.alignment = PP_ALIGN.CENTER       # 设置段落对齐方式

run = paragraph.runs[0]                     # 获取或添加具体的文本块对象
run.text = "样式文本"
run.font.name = "Arial"                     # 设置字体名称
run.font.bold = True                        # 开启加粗
run.font.italic = False                     # 关闭斜体
run.font.color.rgb = RGBColor(255, 0, 0)    # 设置字体颜色
run.font.size = Pt(24)                      # 设置字号大小 (Pt 单位)
```

- **文本批量填充与格式化样例**：

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

def fill_text(self):
    """
    根据配置项批量填充并格式化 PPT 中的文本
    """
    for key in self.process_data["text"]:
        keys = [int(item) for item in key.split("-")]
        slide = self.prs.slides.get(keys[0])
        shape = slide.shapes[keys[1]]
        paragraph = shape.text_frame.paragraphs[keys[2]]
        paragraph.clear()  # 清除已有文本

        for item in self.process_data["text"][key]["runs"]:
            run = paragraph.add_run()
            if item.get("text"):
                run.text = item.get("text")

            # 读取应用字符级样式配置
            run.font.name = item["style"].get("font_name") if item["style"].get("font_name") else self.process_data["text"][key]["style"].get("font_name")
            run.font.bold = item["style"].get("font_bold") if item["style"].get("font_bold") else self.process_data["text"][key]["style"].get("font_bold")
            run.font.italic = item["style"].get("font_italic") if item["style"].get("font_italic") else self.process_data["text"][key]["style"].get("font_italic")
            run.font.color.rgb = RGBColor(*item["style"].get("font_color")) if item["style"].get("font_color") else RGBColor(*self.process_data["text"][key]["style"].get("font_color", (0, 0, 0)))
            run.font.size = Pt(item["style"].get("font_size")) if item["style"].get("font_size") else Pt(self.process_data["text"][key]["style"].get("font_size"))

        paragraph.alignment = self.process_data["text"][key]["style"].get("alignment")
```

### 3.2. 图片操作

```python
shape.shape_type == MSO_SHAPE_TYPE.PICTURE  # 判定该图形元素是否为图片
pic = shape.image                           # 获取图片对象
pic_bytes = pic.blob                        # 获取图片底层的二进制数据流
slide.shapes.add_picture(file_path, left, top, width, height)
```

> [!WARNING]
>
> - `add_picture` 方法在插入新图片时会动态改变当前 Slide 中 `shapes` 的索引。为了防止由于索引错乱导致定位失败，建议在对同一个 Slide 处理时，先统一进行图片批量添加操作，最后再统一执行旧占位图形的批量删除。
> - `add_picture` 插入的图片数据仅支持本地文件路径或者是内存中的二进制流，不支持直接传入 HTTP 图片网络链接。

- **替换图片元素样例**：

```python
from pptx.util import Cm, Emu

def fill_picture(self):
    """
    根据配置项批量替换幻灯片中的图片占位元素
    """
    elements = []
    for key in self.process_data["image"]:
        keys = [int(item) for item in key.split("-")]
        slide = self.prs.slides.get(keys[0])
        shape = slide.shapes[keys[1]]
        e = shape.element
        
        # 尺寸换算配置
        top = Cm(self.process_data["image"][key]["top"]) if "top" in self.process_data["image"][key] else Emu(shape.top)
        left = Cm(self.process_data["image"][key]["left"]) if "left" in self.process_data["image"][key] else Emu(shape.left)
        width = Cm(self.process_data["image"][key]["width"]) if "width" in self.process_data["image"][key] else Emu(shape.width)
        height = Cm(self.process_data["image"][key]["height"]) if "height" in self.process_data["image"][key] else Emu(shape.height)
        
        # 将新图片以相同的物理坐标插入到幻灯片中
        slide.shapes.add_picture(self.process_data["image"][key]["path"], left, top, width, height)
        
        # 记录待删除的旧图片 XML 节点
        elements.append(e)
        
    # 统一移除旧节点，规避索引偏移
    for e in elements:
        e.getparent().remove(e)
```

### 3.3. 表格操作

```python
shape.has_table                             # 判定当前图形是否为表格
table = shape.table                         # 获取表格对象
rows_count = len(table.rows)
cols_count = len(table.columns)
cell = table.cell(row_index, col_index)     # 定位单元格
cell.text_frame.text = "单元格数据"           # 填充文本

# 底层删除行节点
table._tbl.remove(table.rows[row_index]._tr)
```

> [!NOTE]
> 表格的行（Row）和列（Column）对象本身不支持直接设置独立的背景颜色或文本样式。所有的文本、大小及背景渲染等属性均需向下深入定位到具体的单元格（Cell）对象中进行配置设置。

- **表格数据填充样例**：

```python
def fill_table(self):
    """
    批量向表格中填充文本数据并保持预设的排版字体样式
    """
    for key in self.process_data["table"]:
        keys = [int(item) for item in key.split("-")]
        slide = self.prs.slides.get(keys[0])
        shape = slide.shapes[keys[1]]

        for row_index, row in enumerate(self.process_data["table"][key]["cells"]):
            for col_index, cell_runs in enumerate(row):
                paragraph = shape.table.cell(row_index, col_index).text_frame.paragraphs[0]
                paragraph.clear()
                
                for run_content in cell_runs:
                    run = paragraph.add_run()
                    if run_content.get("text"):
                        run.text = run_content.get("text")
                    
                    # 应用字符级细粒度样式
                    run.font.name = run_content["style"].get("font_name") if run_content["style"].get("font_name") else self.process_data["table"][key]["style"].get("font_name")
                    run.font.bold = run_content["style"].get("font_bold") if run_content["style"].get("font_bold") else self.process_data["table"][key]["style"].get("font_bold")
                    run.font.italic = run_content["style"].get("font_italic") if run_content["style"].get("font_italic") else self.process_data["table"][key]["style"].get("font_italic")
                    run.font.color.rgb = RGBColor(*run_content["style"].get("font_color")) if run_content["style"].get("font_color") else RGBColor(*self.process_data["table"][key]["style"].get("font_color", (0, 0, 0)))
                    run.font.size = Pt(run_content["style"].get("font_size")) if run_content["style"].get("font_size") else Pt(self.process_data["table"][key]["style"].get("font_size"))

                paragraph.alignment = self.process_data["table"][key]["style"].get("alignment")
```

### 3.4. 图表操作

```python
shape.has_chart                             # 判定图形是否为数据图表
chart = shape.chart                         # 获取图表对象
chart_type = chart.chart_type               # 获取图表类型枚举值
chart.has_title = True                      # 是否渲染图表标题
series = chart.series[0]                    # 获取第一组数据序列
data_labels = series.data_labels            # 获取数据标签管理组件
data_labels.number_format = "0.0%"          # 格式化展示数据
```

- **图表数据替换与渲染颜色微调样例**：

```python
from pptx.chart.data import CategoryChartData, ChartData

def fill_chart(self):
    """
    修改图表背后的基础数据并重新渲染其样式颜色
    """
    for key in self.process_data["chart"]:
        keys = [int(item) for item in key.split("-")]
        slide = self.prs.slides.get(keys[0])
        shape = slide.shapes[keys[1]]

        # 根据图表类型构建替换数据包
        if self.process_data["chart"][key]["type"] == "bar":
            chart_data = CategoryChartData()
            for series_index, series in enumerate(self.process_data["chart"][key]["series"]):
                chart_data.categories = series["categories"]
                chart_data.add_series(f"series_{series_index}", series["data"], "0.0%")

        if self.process_data["chart"][key]["type"] == "ban":
            chart_data = ChartData()
            for series_index, series in enumerate(self.process_data["chart"][key]["series"]):
                chart_data.categories = series["categories"]
                chart_data.add_series(f"series_{series_index}", series["data"], "0.0%")

        # 触发数据底层重绘渲染
        shape.chart.replace_data(chart_data)

        # 重新应用自定义柱形/条形图的填充色彩
        for index, item in enumerate(self.process_data["chart"][key]["style"]["points"]):
            # 特别提示：在对个别 Point 设置颜色时，必须先显式调用 .solid() 声明纯色填充模式
            shape.chart.series[0].points[index].format.fill.solid()
            shape.chart.series[0].points[index].format.fill.fore_color.rgb = RGBColor(*item.get('fill_color', (127, 127, 127)))

        shape.chart.has_title = self.process_data["chart"][key]["style"].get("has_title", False)
```

> [!NOTE]
> 对于竖排系列的条形图，系统读取 `series` 列表中各数据维度的方向默认是从底部往上排列。

---

## 4. 拓展与使用技巧

### 4.1. 设置 PPTX 文件的默认文字字体

- **字体类型**：可通过在 Office PowerPoint 中切换到“视图 -> 幻灯片母版”，在母版全局设置中统一调整“字体”来锁定整套文件的字体。
- **图形文本格式**：新建一个文本框，调整其字体颜色、大小和边距等参数后，右键选择“设置为默认文本框”来统一当前演示文稿后续新建文本框的渲染样式。

---

## 5. 参考资料

- [python-pptx 官方 API 开发文档](https://python-pptx.readthedocs.io/en/latest/index.html#api)
- [微软官方在演示文稿中配置多母版教程](https://support.microsoft.com/zh-cn/office/%E5%9C%A8%E4%B8%80%E4%B8%AA%E6%BC%94%E7%A4%BA%E6%96%87%E7%A8%BF%E4%B8%AD%E4%BD%BF%E7%94%A8%E5%A4%9A%E4%B8%AA%E5%B9%BB%E7%81%AF%E7%89%87%E6%AF%8D%E7%89%88-dc684a1d-9d14-4ead-9bb5-2303d4fedba8)
