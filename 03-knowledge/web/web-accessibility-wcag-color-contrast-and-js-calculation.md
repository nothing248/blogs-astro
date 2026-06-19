---
status: completed
filename: web-accessibility-wcag-color-contrast-and-js-calculation
title: "颜色对比度"
summary: 本笔记深入探讨了 Web 无障碍设计中关于颜色对比度的核心标准。依据 WCAG 2.0 规范，解析了基于相对亮度而非色相的对比度计算原理，并详细列出了 A/AA/AAA 三个合规等级的阈值要求（如最佳 7:1，最低 4.5:1）。同时，提供了一套具有极高工程价值的纯 JavaScript 代码实现：包括通过 RGB 色值严密计算亮度的算法公式，以及递归向上遍历 DOM 树以获取元素真实且非透明背景色的底层脚本，为前端自动化 UI 走查提供技术支撑。
aliases: [颜色对比度, WCAG 颜色标准, 前端无障碍设计, JS 计算对比度]
tags: [前端开发, JavaScript, UI/UX, 无障碍设计, a11y, WCAG, 算法]
date created: 星期一, 五月 19日 2025, 2:05:16 下午
date modified: 星期四, 六月 18日 2026, 13:15:00 晚上
---

<!-- toc -->

## 1. 理论基石：为什么只关注“亮度”？

在 W3C (万维网联盟) 的无障碍阅读性能评估中，发现 **色调（Hue）和饱和度（Saturation）对易读性的影响微乎其微**。起决定性作用的是两者的 **相对亮度（Luminance）** 差异。只要亮度对比足够大，即使是存在严重色觉障碍（色盲）的人群也能清晰阅读。

### 1.1. 对比度等级规范 (WCAG 2.0)

对比度的取值范围在 1:1（完全相同，如白底白字）与 21:1（极限对比，如黑底白字）之间。

- **A 级**：对比度达到 `3:1`。（针对大号加粗字体可接受的最低极限）。
- **AA 级**：对比度达到 `4.5:1`。（常规文本的法定最低标准，可覆盖轻度视力损失人群）。
- **AAA 级**：对比度达到 `7:1`。（最高黄金标准，为严重视力受损者设计）。

---

## 2. 核心算法：纯 JS 实现亮度与对比度计算

计算公式严格遵循 W3C 的相对亮度标准方程。

```javascript
export default {
    /**
     * 第一步：计算 sRGB 色彩空间的相对亮度 (Luminance)
     */
    luminanace(r, g, b) {
        var a = [r, g, b].map(function (v) {
            v /= 255;
            // Gamma 校正与线性化处理
            return v <= 0.03928
                ? v / 12.92
                : Math.pow((v + 0.055) / 1.055, 2.4);
        });
        // 亮度权重：人眼对绿色最敏感，蓝色最迟钝
        return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
    },

    /**
     * 第二步：对比计算 (返回 1 ~ 21 之间的比值)
     */
    contrast(rgb1, rgb2) {
        // Hex 转换为 RGB 对象
        var result1 = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(rgb1);
        var result2 = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(rgb2);
        
        var rgb1Obj = result1 ? { r: parseInt(result1[1], 16), g: parseInt(result1[2], 16), b: parseInt(result1[3], 16)} : null;
        var rgb2Obj = result2 ? { r: parseInt(result2[1], 16), g: parseInt(result2[2], 16), b: parseInt(result2[3], 16)} : null;

        var lum1 = this.luminanace(rgb1Obj.r, rgb1Obj.g, rgb1Obj.b);
        var lum2 = this.luminanace(rgb2Obj.r, rgb2Obj.g, rgb2Obj.b);

        // 公式：(最亮色 + 0.05) / (最暗色 + 0.05)
        var brightest = Math.max(lum1, lum2);
        var darkest = Math.min(lum1, lum2);

        return (brightest + 0.05) / (darkest + 0.05);
    }
}

// 测试：纯白与纯黄的对比度极低，极难阅读
// console.log(contrast('#ffffff', '#ffff00')); // 输出: 1.0738...
```

---

## 3. 进阶：如何穿透 DOM 树获取元素“真实的背景色”

在复杂的 Web 页面中，元素的 `background-color` 可能是透明的（如 `rgba(0,0,0,0)` 或 `display:none`），此时肉眼看到的颜色其实是透出的 **父级或祖父辈节点的背景色**。必须递归查询。

```javascript
(function(WDS, undefined){
    // 获取经过浏览器最终渲染计算后的层叠样式
    function getStyle(elem, property){
        if(!elem || !property) return false;
        var value = elem.style[camelize(property)], css; 
        if(!value && document.defaultView && document.defaultView.getComputedStyle){
            css = document.defaultView.getComputedStyle(elem, null);
            value = css ? css.getPropertyValue(property) : null;
        }
        return [value, elem];
    }

    function camelize(str) {
        return str.replace(/-(\w)/g, function (strMatch, p1){ return p1.toUpperCase(); });
    }

    // 检测截获到的背景色是否具备视觉有效性
    function checkBgValue(elem){
        var value = getStyle(elem, 'background-color')[0];
        var hasColor = value ? true : false; 

        // 排除透明、不可见、未渲染的干扰节点
        if(value == "transparent" || value == "rgba(0, 0, 0, 0)"){
            hasColor = false;
        } else if(getStyle(elem, 'opacity')[0] == "0" || 
                  getStyle(elem, 'visibility')[0] == "hidden" || 
                  getStyle(elem, 'display')[0] == "none"){
            hasColor = false;
        }
        return hasColor;
    }

    // 递归向上追溯真实的非透明视觉背景色
    function getRealBg(elem){
        if(checkBgValue(elem)){
            return getStyle(elem, 'background-color')[0];
        } else if(elem != document.documentElement){
            // 如果自身没颜色，找老子要颜色
            return getRealBg(elem.parentNode);
        }
        return ''; // 追溯到顶依然没有
    }

    WDS.getRealBg = getRealBg;
})(window.WDS || (window.WDS = {}));

// 调用示例
// console.log(WDS.getRealBg(document.getElementById("myText")));
```

## 4. 参考资料

- [Google Web Dev: 使用无障碍色彩和对比度](https://web.dev/learn/accessibility/color-contrast?hl=zh-cn#using_color)
- [DOM 背景色递归查询逻辑探究](https://cloud.tencent.com/developer/article/1494511)
