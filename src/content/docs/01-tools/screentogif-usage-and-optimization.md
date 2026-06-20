---
title: "ScreenToGif教程"
filename: screentogif-usage-and-optimization
description: ScreenToGif 是一款开源、免费且功能极其强大的 Windows 屏幕录制与 GIF 编辑工具。本文简要介绍了其核心功能，包括屏幕/摄像头/白板录制，并针对 GIF 格式体积过大的痛点提供了实战优化建议（如针对长视频转为 WebP 或 MP4 格式）。是开发者演示、教程制作的得力助手。
tags: [screentogif, gif-recorder, windows-tools, image-editing, open-source]
aliases: [ScreenToGif教程, 动态图制作工具]
status: completed
date created: 星期一, 五月 19日 2025, 2:05:28 下午
date modified: 星期五, 六月 19日 2026, 12:08:25 中午
---

<!-- toc -->

## 1. 简介

ScreenToGif 是一款集录制、编辑于一体的开源软件。它不仅可以录制屏幕、摄像头，还内置了一个功能丰富的编辑器，允许用户对录制后的每一帧进行精细化调整。

## 2. 核心特性

- **多模式录制**：支持屏幕区域录制、摄像头录制以及手绘白板录制。
- **内置编辑器**：支持删除帧、调整帧率、添加文本、绘制箭头、模糊敏感信息（打码）等。
- **FFmpeg 集成**：支持调用 FFmpeg 导出为视频格式，提供更高的压缩比。
- **完全免费**：无广告、无水印、完全开源。

## 3. 进阶技巧：解决 GIF 体积过大问题

GIF 格式本质上是非压缩的位图序列，对于长视频非常不友好。

> [!warning] **优化建议**
>
> - **控制时长**：如果录制内容超过 15-20 秒，生成的 GIF 体积通常会达到数十 MB，不建议用于网页展示。
> - **减少帧率**：在编辑器中删除不必要的重复帧，或将帧率降低至 10-15 FPS。
> - **使用 WebP**：ScreenToGif 支持导出为 **WebP** 格式，在画质接近的情况下，体积通常只有 GIF 的 1/3。
> - **导出 MP4**：对于长演示，直接导出为 MP4 视频是更好的选择。

## 4. 参考资料

- [ScreenToGif 官方网站](https://www.screentogif.com/)
- [ScreenToGif GitHub 仓库](https://github.com/NickeManarin/ScreenToGif)
