---
title: "Node包管理与规范"
filename: node-dependency-and-modules-guide
summary: 详解 Node.js 的包管理器（Npm、Yarn、Pnpm、Npx）配置与对比，涵盖全局路径重定向及硬链接复用机制。深入剖析 CommonJS 与 ES6 模块化规范的导入导出语法及编译识别规则，并提供了两种规范的混用解决方案。此外还记录了内存不足导致 Npm 被 Kill 的 Swap 应对措施与常用 Node 工具包推荐。
tags:
  - Node.js
  - 包管理器
  - CommonJS
  - ES6模块
  - 依赖冲突
aliases:
  - Node包管理与规范
  - CommonJS vs ES6
  - pnpm配置教程
status: completed
date created: 星期一, 五月 19日 2025, 2:05:18 下午
date modified: 星期二, 六月 16日 2026, 6:24:24 晚上
---

<!-- toc -->

## 1. 依赖管理

### 1.1. Npm

- 使用

```shell
npm install # 安装所有依赖
npm install <package-name> # 安装单个包
npm install <package-name> --save-dev # 安装为开发依赖 (npm i -D)
npm install <package-name> --save # 安装为生产依赖 (npm i -S)
npm update # 更新所有包
npm uninstall <package-name> # 卸载包

npm install --registry=https://registry.npmmirror.com # 安装时指定国内源
npm config set registry https://registry.npmmirror.com # 设置国内源
npm config get registry # 查看源配置
```

- 特点
  - `package.json`: 项目的元数据文件，记录了项目的名称、版本、描述、依赖等信息。
  - `package-lock.json`: 锁定依赖版本，确保不同环境下安装的依赖版本一致性。
  - 拥有庞大的生态系统和社区支持。

### 1.2. Yarn

- 使用

```shell
yarn add <package-name> # 添加包
yarn global add <package-name> # 全局添加包
yarn install # 安装所有依赖
yarn remove <package-name> # 移除包
yarn upgrade # 升级所有包
yarn outdated # 检查过时的包
yarn config set registry https://registry.npmmirror.com/ # 设置国内源
```

- 特点
  - `yarn.lock`: 锁定依赖版本，确保不同环境下安装的依赖版本一致性。
  - 相对 npm 优势
    - 更快 (引入并行下载)
    - 版本锁定更严格
    - 校验更严格
    - 输出更简洁
    - 离线支持更稳定

> 出现 certificate has expired 问题，可以尝试删除 `yarn.lock` 文件后重新安装。

### 1.3. Pnpm

也是一个包管理器，特点是速度快、节省磁盘空间。

- 安装

```shell
npm install -g pnpm # 全局安装 pnpm
```

- 配置

```
# 为了防止 pnpm 把全局包和你的 NVM Node 版本混在一起（导致你换了 Node 版本后，全局安装的工具就找不到了），建议显式指定全局安装和全局 bin 的路径：

# 1. 设置全局安装包的存放位置
pnpm config set global-dir "$HOME/.pnpm-global/store"

# 1. 设置全局可执行命令的存放位置
pnpm config set global-bin-dir "$HOME/.pnpm-global/bin"

# 2. 建议配置到bashrc
export PNPM_HOME="$HOME/.pnpm-global"
export PATH="$PNPM_HOME/bin:$PATH"

```

- 使用

```shell
pnpm install # 安装所有依赖
pnpm add <package-name> # 添加包
pnpm add -D <package-name> # 添加为开发依赖
pnpm add -S <package-name> # 添加为生产依赖
pnpm update # 更新所有包
pnpm remove <package-name> # 移除包
```

- 特点
  - **硬链接和符号链接**: 通过内容可寻址存储，实现依赖的复用，大大节省磁盘空间。
  - `pnpm-lock.yaml`: 锁定依赖版本，比 `package-lock.json` 和 `yarn.lock` 更严格，能更好地保证一致性。
  - **非扁平化的 `node_modules`**: 避免幽灵依赖和版本冲突。
  - 速度快，性能优异。

### 1.4. Npx

- 用于执行 `node_modules` 中可执行文件或者直接运行远程 npm 包。
- 解决的问题:
  - 无需全局安装包即可运行其可执行文件，避免全局污染。
  - 可以方便地运行一次性命令或测试不同版本的工具。
- 使用:

```shell
npx <package-name> [arguments] # 执行包中的命令
npx create-react-app my-app # 运行 create-react-app 包创建项目
```

## 2. 常见函数

- 路径函数

```javascript
var path = require("path")
path.resolve() //返回绝对路径
```

## 3. 常见全局变量

```javascript
__dirname  // 当前文件的路径
```

## 4. 模块知识

### 4.1. Commonjs 规范

- 导出

```node
exports = modules.exports = {}; // 导出分类实施
```

- 导入

```node
const data = require("fs")
import("fs").then(modele=>{})　// 动态导入
```

### 4.2. ES6 规范

- 导出

```node
export const a = "data" // 多数据导出 
export default a = "data"
```

> 注意 export 出现多次、而 export default 只能出现一次。 export 可以导出变量表达式，export default 不可以。

- 导入

```node
import {a as a_data} from "a" //从export导入数据并且重命名
import a from "a" //从export default导入数据
import("fs").then(modele=>{})　// 动态导入
```

> 异步导入其实就是动态创建 script 的方式

### 4.3. Node 编译环境

- 环境识别
  - 以 cjs、js 为后缀的会默认使用 commonjs 规范、以 mjs 为后缀的文件会默认使用 ES6 规范
- commonjs 环境导入 ES6 规范模块
  - 方式 1
    - 将文件后缀名修改为 mjs
  - 方式 2
    - 修改 pageckage.json 文件

    ```json
    {
        type:"module"
    }
    ```

  - 方式 3
    - 使用 babel 进行编译

- ES6 环境实导入 commonjs 规范模块

  ```node
    import { default as csv } from 'csvtojson';
  ```

## 5. 常见问题

### 5.1. 记录一次 npm 安装被 kill 的问题

- 问题原因是因为内存不够的问题
- 解决方式
  - 新增内存
  - 开启 swap

## 6. 常见的 node 包

- jsontocsv json 转化为 csv
- csvtojson csv 转化为 json
- lodash 工具库
- moment 处理时间库

## 7. 参考资料

- [pnpm 解析](https://zhuanlan.zhihu.com/p/576969574)
