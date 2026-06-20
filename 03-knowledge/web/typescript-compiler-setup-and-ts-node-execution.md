---
status: completed
filename: typescript-compiler-setup-and-ts-node-execution
title: "TypeScript 基础"
description: 本笔记是对微软开发的 JavaScript 超集语言 TypeScript (TS) 的快速入门总结。明确了 TS 引入静态类型系统以增强代码健壮性的核心定位。涵盖了全局安装流程，详细解析了编译器命令行 `tsc` 及其配置基石 `tsconfig.json` 的核心参数（如 --outFile, --noEmit, target 编译目标）。同时，推荐并演示了使用非官方生态工具 `ts-node` 直接在终端热运行 `.ts` 脚本而无需等待编译的实效方法，是前端工程化必备的基础查阅卡。
aliases: [TypeScript 基础, tsc 编译配置, ts-node 运行, tsconfig.json]
tags: [前端开发, TypeScript, JavaScript, 编译原理, 前端工程化]
date created: 星期一, 五月 19日 2025, 2:05:17 下午
date modified: 星期四, 六月 18日 2026, 13:15:00 晚上
---

<!-- toc -->

## 1. 语言定位与基础机制

**TypeScript (简称 TS)** 是微软开发的一种基于 JavaScript 的编程语言。

- **核心本质**：它是 JS 的 **严格超集**。完全向下兼容原生 JS 语法，并在此基础上引入了极其强大的 **静态类型系统**。
- **执行机制**：浏览器和 Node.js 原生无法直接运行 TS。开发阶段编写的 `.ts` 源码，必须经过编译器 (`tsc`) 降维转译为纯 `.js` 代码后，才能送入引擎执行。

*(安装依赖：`npm install -g typescript`)*

---

## 2. 编译器 (`tsc`) 实战与参数控制

直接在终端调用 `tsc` 编译器将源文件转换为 JavaScript：

### 2.1. 核心命令行参数

```bash
# 基础转换 (生成同名的 app1.js)
tsc app1.ts 

# 将多个输入文件合并打包为一个独立的 js 产物
tsc app1.ts app2.ts --outFile app.bundle.js 

# 指定输出的目录，隔离源码与产物
tsc app1.ts --outDir dist/ 

# 指定降级转译的目标 ECMAScript 语法版本 (默认极低以兼容上古浏览器，推荐 es6+)
tsc app1.ts --target es2015 

# 严格模式：一旦发生类型校验错误，直接中断并拒绝输出 js 文件
tsc app1.ts --noEmitOnError  

# 类型检查模式：只扫描代码爆出类型警告，彻底不生成任何 js 物理文件
tsc app1.ts --noEmit   
```

### 2.2. 工程化基石：`tsconfig.json`

在现代项目中，绝不会手动敲击冗长的 CLI 参数，而是通过根目录的 `tsconfig.json` 声明式控制编译策略。

```json
{
  "files": [
    "src/file1.ts", 
    "src/file2.ts"
  ],
  "compilerOptions": {
    "outDir": "./dist",
    "target": "ES6",
    "strict": true
  }
}
```

*在包含此文件的目录下，直接在终端输入 `tsc` 回车即可根据规则全量编译项目。*

---

## 3. 语法

### 3.1. 类型

```typescript
let foo:string
function toString(num:number):string {
    return String(num);
}
```

- 使用冒号: 类型的格式
- 类型声明不是必须的，会有类型推断。

---

## 4. 进阶利器：`ts-node` (跳过物理编译直接运行)

在开发 Node.js 后端脚本或进行算法测试时，频繁执行 `tsc -> node app.js` 非常繁琐。
**`ts-node`** 是一个广受欢迎的社区工具，它能在底层实时（JIT）转译并立刻执行 TS 代码，不在磁盘上生成冗余的 `.js` 垃圾。

```bash
# 全局安装
npm install -g ts-node 

# 一键运行 TS 脚本文件
ts-node script.ts 

# 直接启动带有 TS 语法支持的交互式终端 (REPL)
ts-node 
```

## 5. 参考资料

- [TypeScript 官方中英双语文档](https://www.typescriptlang.org/docs/)
- [官方在线 Playground (游乐场实时预览编译)](https://www.typescriptlang.org/play)
- [阮一峰 TypeScript 基础教程](https://wangdoc.com/typescript/)
